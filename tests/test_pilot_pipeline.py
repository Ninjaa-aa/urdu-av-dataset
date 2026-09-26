"""Timing and exclusion invariants for automated corpus extraction."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('pipeline', Path(__file__).parents[1] / 'scripts/pilot_pipeline.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class TimingTests(unittest.TestCase):
    def test_cut_contains_word_on_original_frame_grid(self):
        for start, end in [(0, .05), (2.82, 3.22), (293.14, 293.30), (299.8, 300)]:
            a, b = p.cut_window(start, end)
            self.assertLessEqual(a, start)
            self.assertGreaterEqual(b, end)
            self.assertGreaterEqual(a, 0)
            self.assertLessEqual(b, 300)
            self.assertAlmostEqual(a*30, round(a*30))
            self.assertAlmostEqual(b*30, round(b*30))
            self.assertAlmostEqual((90+b)-(90+a), b-a)

    def test_missing_zero_and_overrun_cannot_pass(self):
        for word in [{}, {'start':293.14,'end':293.14,'score':1},
                     {'start':299.9,'end':300.1,'score':1},
                     {'start':float('nan'),'end':2,'score':1}]:
            self.assertIn('missing_or_invalid_alignment', p.alignment_reasons(word))

    def test_unknown_letter_or_missing_score_excluded(self):
        self.assertIn('alignment_score', p.alignment_reasons({'start':1,'end':1.4}))
        self.assertIn('unsupported_letters',p.alignment_reasons({'start':1,'end':1.4,'score':1,'unsupported_letters':['x']}))

    def test_sync_runs_never_bridge_rejection_cut_or_track(self):
        frames=[{'good':True,'shot':0,'track_id':0}, {'good':False},
                {'good':True,'shot':0,'track_id':0}, {'good':True,'shot':1,'track_id':0},
                {'good':True,'shot':1,'track_id':1}, {'good':True,'shot':1,'track_id':1}]
        self.assertEqual(p.runs(frames),[(0,1,(0,0)),(2,3,(0,0)),(3,4,(1,0)),(4,6,(1,1))])

    def test_crop_stays_in_frame_and_contains_motion(self):
        boxes=[[1,3,90,70],[40,20,101,95]]
        x,y,w,h=p.union_box(boxes,.2,w=120,h=100)
        self.assertTrue(all(v%2==0 for v in [x,y,w,h]))
        self.assertTrue(0<=x<x+w<=120 and 0<=y<y+h<=100)
        self.assertTrue(all(x<=a and y<=b and x+w>=c and y+h>=d for a,b,c,d in boxes))

    def test_lookup_does_not_replace_urdu_letters(self):
        self.assertEqual(p.lookup(' اردو، '),'اردو')
        self.assertNotEqual(p.lookup('ی'),p.lookup('ے'))

if __name__ == '__main__': unittest.main()
