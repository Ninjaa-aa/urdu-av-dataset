"""Five-minute Urdu pilot: alignment, frame checks, SyncNet, paired exports.
Automatic measurements use provisional thresholds; they are not human ground truth.
"""
from pathlib import Path
import argparse, collections, hashlib, json, math, subprocess, sys, unicodedata

CONFIG = dict(min_word_seconds=0.04, max_word_seconds=2.0, min_alignment_score=0.1,
              min_mouth_pixels=28, min_face_height=100, max_yaw_degrees=40,
              min_mouth_laplacian=15, max_landmark_jump=0.3,
              sync_confidence=3.0, max_sync_offset_frames=2, context_seconds=0.12, face_detection_score=0.9)

def read(p): return json.loads(Path(p).read_text())
def save(p, v): Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=2, allow_nan=False)+'\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lookup(text):
    return ''.join(c for c in unicodedata.normalize('NFC', text).strip() if not unicodedata.category(c).startswith('P'))
def cut_window(start, end, duration=300, fps=30, context=.12):
    return max(0, math.floor((start-context)*fps))/fps, min(duration, math.ceil((end+context)*fps)/fps)
def alignment_reasons(w):
    a,b=w.get('start'),w.get('end'); reasons=[]
    if a is None or b is None or not all(math.isfinite(x) for x in [a,b]) or not 0<=a<b<=300:
        return ['missing_or_invalid_alignment']
    if not CONFIG['min_word_seconds']<=b-a<=CONFIG['max_word_seconds']: reasons.append('word_duration')
    if w.get('score',0)<CONFIG['min_alignment_score']: reasons.append('alignment_score')
    if w.get('unsupported_letters'): reasons.append('unsupported_letters')
    return reasons

def download(url, path):
    import urllib.request
    path=Path(path)
    if not path.exists():
        temp=path.with_suffix(path.suffix+'.part'); urllib.request.urlretrieve(url,temp);temp.replace(path)
    return path

def align_stage(root,out):
    import numpy as np, torch, whisperx, nltk
    from huggingface_hub import snapshot_download
    from scipy.io import wavfile
    torch.set_num_threads(2)
    nltk.download('punkt_tab',quiet=True)
    model_id='kingabzpro/wav2vec2-large-xls-r-300m-Urdu'
    model_path=snapshot_download(model_id,allow_patterns=['*.json','*.safetensors','pytorch_model.bin'])
    model,meta=whisperx.load_align_model('ur','cpu',model_name=model_path)
    sr,wav=wavfile.read(root/'pilot_0090_0390/audio_16k.wav');assert sr==16000 and len(wav)==4800000
    audio=wav.astype(np.float32)/32768
    raw=read(root/'pilot_0090_0390/transcript_raw.json')
    segments=[];words=[]; failures=[]
    for i,s in enumerate(raw['segments']):
        # Keep accepted text unchanged; expand the acoustic search window slightly.
        lo=max(0,s['start']-.15);hi=min(300,s['end']+.15)
        result=whisperx.align([dict(start=lo,end=hi,text=s['text'])],model,meta,audio,'cpu',return_char_alignments=True)
        segments.append(dict(parent_segment_id=s['id'],result=result))
        got=result['word_segments']
        expected=s['text'].split()
        if [w['word'] for w in got]!=expected:
            failures.append(dict(segment_id=s['id'],reason='token_sequence_mismatch',expected=expected,observed=[w['word'] for w in got]))
            got=[dict(word=w) for w in expected]
        for j,w0 in enumerate(got):
            w=dict(w0);w.update(occurrence_id=f"VD-RK-nY66k_0090_a{i:03d}_{j:03d}",parent_segment_id=s['id'],word_index=j)
            w['unsupported_letters']=[c for c in w['word'] if unicodedata.category(c)[0] in 'LN' and c.lower() not in meta['dictionary']]
            w['alignment_reasons']=alignment_reasons(w)
            w['lookup']=lookup(w['word']);words.append(w)
        print(f'ALIGN {i+1}/{len(raw["segments"])} words={len(got)}',flush=True)
    # Conflicting alignments at adjacent segment margins cannot both be exported.
    for before,after in zip(words,words[1:]):
        if before.get('end') is not None and after.get('start') is not None and before['end']>after['start']+.02:
            before['alignment_reasons'].append('overlapping_neighbor');after['alignment_reasons'].append('overlapping_neighbor')
    save(out/'alignment.json',dict(model_id=model_id,revision=Path(model_path).name,method='whisperx_word_ctc',words=words,segments=segments,failures=failures))
    print('ALIGN COMPLETE',len(words),sum(not w['alignment_reasons'] for w in words),flush=True)

def box(points,w,h,pad=.15):
    import numpy as np
    p=np.array(points);lo=p.min(axis=0);hi=p.max(axis=0);delta=(hi-lo)*pad
    return [max(0,int((lo[0]-delta[0])*w)),max(0,int((lo[1]-delta[1])*h)),min(w,int(math.ceil((hi[0]+delta[0])*w))),min(h,int(math.ceil((hi[1]+delta[1])*h)))]
def iou(a,b):
    inter=max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
    return inter/max(1,(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-inter)

def visual_stage(root,out):
    import cv2,numpy as np,mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    assets=out/'assets';assets.mkdir(exist_ok=True)
    task=download('https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task',assets/'face_landmarker.task')
    detector=vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=python.BaseOptions(model_asset_path=str(task)),running_mode=vision.RunningMode.IMAGE,num_faces=1,output_facial_transformation_matrixes=True))
    yunet_path=download('https://media.githubusercontent.com/media/opencv/opencv_zoo/f12e12798e8314f7c074a6656816c048dcc95b7a/models/face_detection_yunet/face_detection_yunet_2023mar.onnx',assets/'face_detection_yunet_2023mar.onnx')
    cv2.setNumThreads(2)
    yunet=cv2.FaceDetectorYN.create(str(yunet_path),'',(960,540),CONFIG['face_detection_score'],.3,5000)
    cap=cv2.VideoCapture(str(root/'raw/VD-RK-nY66k.mp4'))
    assert abs(cap.get(cv2.CAP_PROP_FPS)-30)<.001
    cap.set(cv2.CAP_PROP_POS_FRAMES,2700)
    cuts=[round((x-90)*30) for x in read(root/'pilot_0090_0390/scene_candidates.json')['source_seconds']]
    frames=[]; track=-1;prev=None;shot=0
    lips=[61,146,91,181,84,17,314,405,321,375,291,409,270,269,267,0,37,39,40,185,13,14]
    for f in range(9000):
        ok,image=cap.read()
        if not ok: raise RuntimeError(f'Video ended at frame {f}')
        if f in cuts: shot+=1;prev=None
        h,w=image.shape[:2]
        small=cv2.resize(image,(960,540))
        _,detections=yunet.detect(small)
        count=0 if detections is None else len(detections)
        rec=dict(frame=f,source_frame=f+2700,time=f/30,shot=shot,face_count=count,good=False)
        res=None
        if count==1:
            fx,fy,fw,fh=detections[0,:4]*2
            cx=fx+fw/2;cy=fy+fh/2;side=max(fw,fh)*2
            ox=max(0,int(cx-side/2));oy=max(0,int(cy-side/2));ex=min(w,int(cx+side/2));ey=min(h,int(cy+side/2))
            roi=image[oy:ey,ox:ex]
            rec.update(detector_score=float(detections[0,14]),landmark_input_xyxy=[ox,oy,ex,ey])
            res=detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)))
        if res is not None and len(res.face_landmarks)==1:
            lm=res.face_landmarks[0]; pts=[((p.x*(ex-ox)+ox)/w,(p.y*(ey-oy)+oy)/h) for p in lm]
            face=box(pts,w,h,0);mouth=box([pts[k] for k in lips],w,h,.35)
            if prev is None or iou(prev,face)<.3:track+=1
            R=np.array(res.facial_transformation_matrixes[0])[:3,:3]
            yaw=math.degrees(math.atan2(-R[2,0],math.hypot(R[0,0],R[1,0])))
            width=float(np.linalg.norm((np.array(pts[61])-np.array(pts[291]))*[w,h]))
            x1,y1,x2,y2=mouth;roi=image[y1:y2,x1:x2]
            blur=float(cv2.Laplacian(cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY),cv2.CV_64F).var()) if roi.size else 0
            jump=0 if prev is None else 1-iou(prev,face)
            reasons=[]
            if width<CONFIG['min_mouth_pixels'] or face[3]-face[1]<CONFIG['min_face_height']:reasons.append('small_face_or_mouth')
            if abs(yaw)>CONFIG['max_yaw_degrees']:reasons.append('head_pose')
            if blur<CONFIG['min_mouth_laplacian']:reasons.append('blur')
            if jump>CONFIG['max_landmark_jump']:reasons.append('landmark_jump')
            if any(not 0<=pts[k][0]<=1 or not 0<=pts[k][1]<=1 for k in lips):reasons.append('mouth_outside_frame')
            rec.update(face_box=face,mouth_box=mouth,mouth_width=width,yaw=yaw,blur=blur,track_id=track,reasons=reasons,good=not reasons)
            prev=face
        else:rec['reasons']=['face_count' if count!=1 else 'landmarks_missing'];prev=None
        frames.append(rec)
        if f%900==0:print('VISUAL',f,'/9000',flush=True)
    cap.release();detector.close()
    save(out/'visual.json',dict(frame_rate=30,model_sha256=sha(task),detector_sha256=sha(yunet_path),detector='YuNet 2023mar at OpenCV Zoo f12e12798e8314f7c074a6656816c048dcc95b7a; score >= 0.9; MediaPipe on 2x face crop',frames=frames,limitations='landmark, pose and blur proxies; not a dedicated mouth-occlusion classifier; track IDs are local continuity IDs'))
    print('VISUAL COMPLETE',sum(f['good'] for f in frames),'/9000',flush=True)

def runs(frames):
    result=[];start=None;key=None
    for i,f in enumerate(frames+[{'good':False}]):
        newkey=(f.get('shot'),f.get('track_id')) if f['good'] else None
        if start is not None and newkey!=key:
            result.append((start,i,key));start=None
        if f['good'] and start is None:start=i;key=newkey
    return result

def sync_stage(root,out):
    import cv2,numpy as np,torch,python_speech_features
    from scipy.io import wavfile
    from scipy.signal import medfilt
    torch.set_num_threads(2)
    assets=out/'assets';assets.mkdir(exist_ok=True)
    # Official implementation, recorded by content hash alongside the checkpoint.
    modelpy=download('https://raw.githubusercontent.com/joonson/syncnet_python/1fbfc081bda41f27aab51c0fbaa0e5e337126cf3/SyncNetModel.py',assets/'SyncNetModel.py')
    weights=download('https://www.robots.ox.ac.uk/~vgg/software/lipsync/data/syncnet_v2.model',assets/'syncnet_v2.model')
    sys.path.insert(0,str(assets));from SyncNetModel import S
    model=S();model.load_state_dict(torch.load(weights,map_location='cpu',weights_only=True));model.eval()
    frames=read(out/'visual.json')['frames']; _,wav=wavfile.read(root/'pilot_0090_0390/audio_16k.wav')
    cap=cv2.VideoCapture(str(root/'raw/VD-RK-nY66k.mp4'));results=[]
    eligible=[r for r in runs(frames) if r[1]-r[0]>=90]
    for n,(a,b,key) in enumerate(eligible):
        # Divide continuous suitable views into >=3-second windows, never across a cut.
        edges=list(range(a,b,180))
        if len(edges)>1 and b-edges[-1]<90:edges.pop()
        edges.append(b)
        for begin,end in zip(edges,edges[1:]):
            start=begin/30;duration=(end-begin)/30
            nf=int(math.floor(duration*25));indices=begin+np.floor(np.arange(nf)*30/25+.5).astype(int)
            boxes=np.array([frames[int(i)]['face_box'] for i in indices],dtype=float)
            smooth=np.stack([medfilt(boxes[:,j],13) for j in range(4)],axis=1)
            crops=[]
            cap.set(cv2.CAP_PROP_POS_FRAMES,2700+begin);cursor=begin-1;im=None
            for idx,bb in zip(indices,smooth):
                while cursor<idx:
                    ok,im=cap.read();cursor+=1
                    if not ok:raise RuntimeError('Missing sync frame')
                x=(bb[0]+bb[2])/2;y=(bb[1]+bb[3])/2;s=max(bb[2]-bb[0],bb[3]-bb[1])/2
                pad=int(s*1.8)+2;im2=np.pad(im,((pad,pad),(pad,pad),(0,0)),constant_values=110)
                crop=im2[int(y+pad-s):int(y+pad+s*1.8),int(x+pad-s*1.4):int(x+pad+s*1.4)]
                crops.append(cv2.resize(crop,(224,224)))
            video=torch.from_numpy(np.array(crops).transpose(3,0,1,2)[None].astype(np.float32))
            audio=wav[round(start*16000):round((start+nf/25)*16000)]
            mfcc=python_speech_features.mfcc(audio,16000).T
            sound=torch.from_numpy(mfcc[None,None].astype(np.float32));vf=[];af=[]
            last=min(nf-5,(mfcc.shape[1]-20)//4+1)
            with torch.inference_mode():
                for j in range(0,last,16):
                    vv=torch.cat([video[:,:,k:k+5] for k in range(j,min(last,j+16))])
                    aa=torch.cat([sound[:,:,:,k*4:k*4+20] for k in range(j,min(last,j+16))])
                    vf.append(model.forward_lip(vv));af.append(model.forward_aud(aa))
            vf=torch.cat(vf);af=torch.cat(af);shift=10
            # Exclude edge padding from the offset comparison.
            center=vf[shift:-shift]
            curve=torch.stack([torch.nn.functional.pairwise_distance(center,af[shift+d:len(af)-shift+d]).mean() for d in range(-shift,shift+1)])
            best=int(curve.argmin());offset=shift-best;confidence=float(curve.median()-curve[best])
            passed=confidence>=CONFIG['sync_confidence'] and abs(offset)<=CONFIG['max_sync_offset_frames']
            rec=dict(start=start,end=end/30,shot=key[0],track_id=key[1],offset_frames_25fps=offset,confidence=confidence,distance_curve=curve.tolist(),pass_gate=passed,method='SyncNet face/audio correspondence proxy')
            results.append(rec);save(out/'sync.partial.json',results)
            print(f'SYNC track {n+1}/{len(eligible)} {start:.2f}-{end/30:.2f} offset={offset} confidence={confidence:.2f} pass={passed}',flush=True)
    cap.release()
    save(out/'sync.json',dict(windows=results,model_sha256=sha(weights),implementation_sha256=sha(modelpy),method_notes='Official SyncNet network; MediaPipe crops with official crop geometry; nearest source frames sampled at 25 fps, no time warp; mean distance excludes shift-padding edges. Provisional thresholds; no independent identity verification.'))

def union_box(boxes,pad,w=1920,h=1080):
    x1=min(b[0] for b in boxes);y1=min(b[1] for b in boxes);x2=max(b[2] for b in boxes);y2=max(b[3] for b in boxes)
    dx=(x2-x1)*pad;dy=(y2-y1)*pad
    x=max(0,int(x1-dx)//2*2);y=max(0,int(y1-dy)//2*2)
    right=min(w,math.ceil((x2+dx)/2)*2);bottom=min(h,math.ceil((y2+dy)/2)*2)
    return [x,y,right-x,bottom-y]

def export_stage(root,out):
    import imageio_ffmpeg,sqlite3,zipfile
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    alignment=read(out/'alignment.json');frames=read(out/'visual.json')['frames'];windows=read(out/'sync.json')['windows']
    clips=out/'clips';clips.mkdir(exist_ok=True);entries=[]
    for k,w in enumerate(alignment['words']):
        reasons=list(w['alignment_reasons']);r=dict(w);r['previous_word']=alignment['words'][k-1]['word'] if k else None;r['next_word']=alignment['words'][k+1]['word'] if k+1<len(alignment['words']) else None
        if not reasons:
            a,b=cut_window(w['start'],w['end']);first=round(a*30);last=round(b*30);fs=frames[first:last]
            if not fs or not all(f['good'] for f in fs):reasons.append('visual_quality')
            if len({(f['shot'],f.get('track_id')) for f in fs})!=1:reasons.append('shot_or_track_change')
            matching=[i for i,s in enumerate(windows) if s['pass_gate'] and s['start']<=a+1e-6 and s['end']>=b-1e-6]
            if not matching:reasons.append('sync_unconfirmed_or_failed')
            r.update(cut_start=a,cut_end=b,source_start=90+a,source_end=90+b,lexical_offset_start=w['start']-a,lexical_offset_end=w['end']-a)
            if not reasons:
                face=union_box([f['face_box'] for f in fs],.2);mouth=union_box([f['mouth_box'] for f in fs],.05)
                stem=clips/w['occurrence_id'];outputs={x:str(stem.name)+'_'+x+'.mp4' for x in ['av','face','mouth']};outputs['audio']=stem.name+'_audio.wav'
                fc=f'[0:v]split=3[v0][v1][v2];[v1]crop={face[2]}:{face[3]}:{face[0]}:{face[1]},scale=256:256:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=256:256:(ow-iw)/2:(oh-ih)/2[vf];[v2]crop={mouth[2]}:{mouth[3]}:{mouth[0]}:{mouth[1]},scale=160:96:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=160:96:(ow-iw)/2:(oh-ih)/2[vm]'
                cmd=[ffmpeg,'-y','-v','error','-ss',str(90+a),'-t',str(b-a),'-i',str(root/'raw/VD-RK-nY66k.mp4'),'-filter_complex',fc]
                for label,tag in [('v0','av'),('vf','face'),('vm','mouth')]:
                    cmd+=['-map',f'[{label}]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-c:a','aac','-b:a','128k','-movflags','+faststart',str(clips/outputs[tag])]
                cmd+=['-map','0:a:0','-ac','1','-ar','16000','-c:a','pcm_s16le',str(clips/outputs['audio'])]
                subprocess.run(cmd,check=True)
                r.update(files={t:'clips/'+name for t,name in outputs.items()},face_crop_xywh=face,mouth_crop_xywh=mouth,crop_resize='aspect-preserving scale and centered black padding',face_output_size=[256,256],mouth_output_size=[160,96],track_id=fs[0]['track_id'],shot=fs[0]['shot'],sync_window=matching[0],status='automatic_candidate_pass',phonemes=None)
        r['rejection_reasons']=reasons
        if reasons:r['status']='excluded'
        entries.append(r)
        if k%50==0:print('EXPORT',k,'/',len(alignment['words']),'passing',sum(x['status']=='automatic_candidate_pass' for x in entries),flush=True)
    save(out/'occurrences.json',entries)
    dictionary={}
    for r in entries:
        if r['status']=='automatic_candidate_pass':dictionary.setdefault(r['lookup'],[]).append(r['occurrence_id'])
    save(out/'dictionary.json',dictionary)
    db=sqlite3.connect(out/'dictionary.sqlite');db.execute('CREATE TABLE IF NOT EXISTS occurrences (id TEXT PRIMARY KEY, word TEXT, lookup TEXT, status TEXT, metadata TEXT)');db.execute('DELETE FROM occurrences')
    db.executemany('INSERT INTO occurrences VALUES (?,?,?,?,?)',[(r['occurrence_id'],r['word'],r['lookup'],r['status'],json.dumps(r,ensure_ascii=False)) for r in entries]);db.execute('CREATE INDEX IF NOT EXISTS word_lookup ON occurrences(lookup,status)');db.commit();db.close()
    kept=[r for r in entries if r['status']=='automatic_candidate_pass'];intervals=sorted((r['cut_start'],r['cut_end']) for r in kept);merged=[]
    for a,b in intervals:
        if merged and a<=merged[-1][1]:merged[-1][1]=max(b,merged[-1][1])
        else:merged.append([a,b])
    report=dict(input_seconds=300,aligned_entries=len(entries),alignment_pass=sum(not r['alignment_reasons'] for r in entries),visual_good_frames=sum(f['good'] for f in frames),total_frames=len(frames),sync_windows=len(windows),sync_windows_pass=sum(w['pass_gate'] for w in windows),exported_occurrences=len(kept),vocabulary=len(dictionary),retained_unique_seconds=sum(b-a for a,b in merged),exported_seconds_with_repetition=sum(r['cut_end']-r['cut_start'] for r in kept),exclusion_reasons=dict(collections.Counter(x for r in entries for x in r['rejection_reasons'])),thresholds=CONFIG,status='automatically filtered pilot candidates; no measured human-reference accuracy',scope='Word corpus only. Phonemes, canonical generation, composition and dubbing not run.')
    save(out/'report.json',report);print(json.dumps(report,indent=2),flush=True)
    with zipfile.ZipFile(root/'urdu_pilot_processed.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob('*'):
            if p.is_file() and 'assets' not in p.relative_to(out).parts and '.partial.' not in p.name:z.write(p,p.relative_to(out))
    print('BUNDLE',root/'urdu_pilot_processed.zip',flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['align','visual','sync','export']);p.add_argument('--root',type=Path,default=Path('/content/urdu-av-pilot'));args=p.parse_args()
    out=args.root/'processed_0090_0390';out.mkdir(exist_ok=True)
    save(out/'config.json',CONFIG)
    globals()[args.stage+'_stage'](args.root,out)
if __name__=='__main__': main()
