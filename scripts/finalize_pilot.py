"""Verify exported files, record provenance, and make an offline word browser."""
from pathlib import Path
import argparse, hashlib, html, json, subprocess, sys, wave, zipfile
from datetime import datetime, timezone
from importlib.metadata import version, PackageNotFoundError


def read(path): return json.loads(path.read_text())
def save(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def finalize(root, pipeline):
    import imageio_ffmpeg
    import numpy as np
    from scipy.io import wavfile
    from scipy.signal import correlate, resample_poly
    out=root/'processed_0090_0390'
    entries=read(out/'occurrences.json')
    kept=[r for r in entries if r['status']=='automatic_candidate_pass']
    sr,reference=wavfile.read(root/'pilot_0090_0390/audio_16k.wav')
    assert sr==16000
    checks=[]
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    for i,r in enumerate(kept):
        expected=r['cut_end']-r['cut_start'];expected_frames=round(expected*30)
        streams=[]
        for kind,relative in r['files'].items():
            path=out/relative
            assert path.is_file() and path.stat().st_size>0
            if kind=='audio':
                with wave.open(str(path)) as w:
                    assert w.getframerate()==16000 and w.getnchannels()==1
                    duration=w.getnframes()/16000
                assert abs(duration-expected)<=1/16000+1e-6, (path,duration,expected)
                _,sample=wavfile.read(path)
                # Independent timing check against the authoritative processing WAV.
                center=round(r['cut_start']*16000);lo=max(0,center-1600)
                region=reference[lo:min(len(reference),center+len(sample)+1600)].astype(float)
                # Cuts on the 30 fps grid can fall between 16 kHz samples.
                # Compare on a 48 kHz analysis grid without modifying saved media.
                region=resample_poly(region,3,1);y=resample_poly(sample.astype(float),3,1)
                y-=y.mean();region-=region.mean()
                cross=correlate(region,y,mode='valid',method='fft')
                at=int(np.argmax(cross));match=region[at:at+len(y)];match=match-match.mean()
                similarity=float(np.dot(match,y)/(np.linalg.norm(match)*np.linalg.norm(y)+1e-12))
                lag=(lo+at/3-center)/16000
                assert abs(lag)<=.002 and similarity>.98, (r['occurrence_id'],lag,similarity)
                streams.append(dict(kind=kind,duration=duration,reference_lag_seconds=lag,reference_correlation=similarity,comparison_sample_rate=48000,sha256=sha(path)))
            else:
                probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(path)],text=True))
                video=[s for s in probe['streams'] if s['codec_type']=='video'][0]
                audio=[s for s in probe['streams'] if s['codec_type']=='audio'][0]
                assert int(video['nb_read_frames'])==expected_frames,(path,video['nb_read_frames'],expected_frames)
                assert abs(float(video['duration'])-expected)<1e-5
                assert abs(float(audio['duration'])-expected)<.04
                assert abs(float(video.get('start_time',0))-float(audio.get('start_time',0)))<.04
                # Decode both streams completely, not just container headers.
                subprocess.run([ffmpeg,'-v','error','-i',str(path),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
                streams.append(dict(kind=kind,video_frames=int(video['nb_read_frames']),video_duration=float(video['duration']),audio_duration=float(audio['duration']),width=video['width'],height=video['height'],sha256=sha(path)))
        checks.append(dict(occurrence_id=r['occurrence_id'],files=streams,status='passed'))
        if i%25==0:print('VERIFY',i,'/',len(kept),flush=True)
    save(out/'export_verification.json',dict(verified_occurrences=len(checks),file_count=sum(len(c['files']) for c in checks),checks=checks,scope='File decodability, frame counts, duration, stream starts and WAV source-time correlation on a 48 kHz comparison grid (saved WAVs remain 16 kHz). Not a perceptual lip-sync or word-boundary accuracy measurement.'))
    versions={}
    for name in ['torch','torchaudio','transformers','whisperx','numpy','scipy','mediapipe','opencv-python','opencv-contrib-python','python_speech_features','imageio-ffmpeg','huggingface_hub']:
        try:versions[name]=version(name)
        except PackageNotFoundError:pass
    manifest=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),source_id='VD-RK-nY66k',source_url='https://www.youtube.com/watch?v=VD-RK-nY66k',source_interval=[90,390],language='ur',transcript_selection='Unchanged ASR text accepted by user on 2026-09-27; acceptance does not validate timing',source_sha256=sha(root/'raw/VD-RK-nY66k.mp4'),transcript_sha256=sha(root/'pilot_0090_0390/transcript_raw.json'),pipeline_sha256=sha(pipeline),python=sys.version,packages=versions,speaker_label='Presenter attributed in source title to Dr. Arfa Zehra; no biometric identity verification',time_mapping='Source time = pilot time + 90 seconds; no temporal warp',rights='Dataset redistribution permission not established',threshold_status='Provisional and not calibrated against an independent labeled set')
    save(out/'run_manifest.json',manifest)
    (out/'pilot_pipeline.py').write_bytes(pipeline.read_bytes())
    (out/'finalize_pilot.py').write_bytes(Path(__file__).read_bytes())
    # Embed metadata so the browser works from disk without fetch/CORS requirements.
    payload=json.dumps(kept,ensure_ascii=False).replace('<','\\u003c')
    page='''<!doctype html><meta charset="utf-8"><title>Urdu pilot word dictionary</title>
<style>body{font:17px system-ui;max-width:1100px;margin:30px auto;padding:0 20px;background:#f7f8fc;color:#20283a}input{font:inherit;padding:12px;width:85%}article{background:white;padding:18px;margin:14px 0;border:1px solid #dde2ec;border-radius:9px}video{width:32%;max-height:240px;background:#111}small{display:block}a{margin-right:15px}h2{font-size:26px}</style>
<h1>Urdu pilot word dictionary</h1><p>Automatically filtered candidates from source 01:30–06:30. Search Urdu text or an occurrence ID. Repeated words remain separate. Clips include 120 ms of context, rounded to source video frames.</p>
<p>Scores and boundaries are model estimates. No phoneme labels, measured accuracy, or identity transfer. Frame checks and SyncNet use provisional thresholds.</p>
<input id="q" placeholder="Search, e.g. اردو" aria-label="Search Urdu word"><p id="count"></p><main id="results"></main>
<script>const rows=PAYLOAD;const q=document.getElementById('q');const area=document.getElementById('results');
function show(){const term=q.value.trim();const matches=rows.filter(r=>!term||r.word.includes(term)||r.occurrence_id.includes(term));document.getElementById('count').textContent=matches.length+' matches; showing first 30';area.replaceChildren();for(const r of matches.slice(0,30)){const a=document.createElement('article');const h=document.createElement('h2');h.textContent=r.word;h.dir='rtl';a.append(h);const p=document.createElement('p');p.textContent=r.occurrence_id+' | source '+r.source_start.toFixed(3)+'–'+r.source_end.toFixed(3)+' s | word inside clip '+r.lexical_offset_start.toFixed(3)+'–'+r.lexical_offset_end.toFixed(3)+' s';a.append(p);for(const kind of ['av','face','mouth']){const v=document.createElement('video');v.controls=true;v.preload='none';v.src=r.files[kind];v.title=kind;a.append(v);}const links=document.createElement('p');for(const [kind,path]of Object.entries(r.files)){const l=document.createElement('a');l.href=path;l.textContent=kind;links.append(l);}a.append(links);area.append(a);}}
q.addEventListener('input',show);show();</script>'''.replace('PAYLOAD',payload)
    (out/'dictionary.html').write_text(page)
    (out/'README.txt').write_text('Open dictionary.html next to clips/ in a regular browser. dictionary.json maps written forms to all passing occurrences; occurrences.json and dictionary.sqlite retain excluded entries and reasons. run_manifest.json contains source and model-run provenance. report.json contains automatic counts. export_verification.json contains file integrity/timing checks. Model estimates are not independent annotation ground truth. No media time stretching, waveform averaging or pixel averaging was applied.\n')
    bundle=root/'urdu_pilot_processed.zip'
    with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob('*'):
            if p.is_file() and 'assets' not in p.relative_to(out).parts and '.partial.' not in p.name:z.write(p,p.relative_to(out))
    print('VERIFIED',len(checks),'occurrences;',bundle,'bytes',bundle.stat().st_size,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path('/content/urdu-av-pilot'));p.add_argument('--pipeline',type=Path,default=Path('/content/pilot_pipeline.py'));a=p.parse_args();finalize(a.root,a.pipeline)
