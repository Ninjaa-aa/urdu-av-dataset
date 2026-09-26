"""Look up every passing occurrence of an Urdu written form."""
import argparse
import json
import sqlite3
from pathlib import Path
from pilot_pipeline import lookup

p=argparse.ArgumentParser()
p.add_argument('word')
p.add_argument('--database',type=Path,default=Path('outputs/processed_0090_0390/dictionary.sqlite'))
p.add_argument('--include-excluded',action='store_true')
a=p.parse_args()
with sqlite3.connect(a.database.resolve().as_uri()+'?mode=ro',uri=True) as db:
    sql='SELECT metadata FROM occurrences WHERE lookup = ?'
    if not a.include_excluded:sql+=" AND status = 'automatic_candidate_pass'"
    rows=[json.loads(r[0]) for r in db.execute(sql+' ORDER BY id',(lookup(a.word),))]
print(json.dumps(rows,ensure_ascii=False,indent=2))
