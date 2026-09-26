"""Optional real-media export regression; synthetic labels are never corpus outputs."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
import wave

from test_pilot_pipeline import p

SOURCE=Path(__file__).parents[1]/'data/raw/VD-RK-nY66k.mp4'

@unittest.skipUnless(SOURCE.exists() and importlib.util.find_spec('imageio_ffmpeg'), 'Local source and imageio-ffmpeg required')
class PairedExportTest(unittest.TestCase):
    def test_same_frame_interval_for_all_four_exports(self):
        import imageio_ffmpeg
        with tempfile.TemporaryDirectory(prefix='urdu-test-only-') as directory:
            root=Path(directory);(root/'raw').mkdir()
            (root/'raw/VD-RK-nY66k.mp4').symlink_to(SOURCE)
            out=root/'processed_0090_0390';out.mkdir()
            word=dict(word='test fixture only',lookup='test',occurrence_id='test_only',start=3.10,end=3.30,alignment_reasons=[],score=1)
            p.save(out/'alignment.json',{'words':[word]})
            frames=[dict(good=True,shot=0,track_id=0,face_box=[700,250,1000,600],mouth_box=[760,450,900,520]) for _ in range(9000)]
            p.save(out/'visual.json',{'frames':frames})
            p.save(out/'sync.json',{'windows':[dict(start=0,end=10,pass_gate=True)]})
            with contextlib.redirect_stdout(io.StringIO()):p.export_stage(root,out)
            item=p.read(out/'occurrences.json')[0]
            expected=item['cut_end']-item['cut_start']
            with wave.open(str(out/item['files']['audio'])) as wav:
                self.assertEqual(wav.getframerate(),16000)
                self.assertLessEqual(abs(wav.getnframes()/16000-expected),1/16000)
            for kind,size in [('av',(1920,1080)),('face',(256,256)),('mouth',(160,96))]:
                reader=imageio_ffmpeg.read_frames(str(out/item['files'][kind]))
                meta=next(reader);count=sum(1 for _ in reader)
                self.assertEqual(meta['size'],size)
                self.assertEqual(meta['fps'],30)
                self.assertEqual(count,round(expected*30))
            self.assertEqual(p.read(out/'dictionary.json')['test'],['test_only'])

if __name__=='__main__':unittest.main()
