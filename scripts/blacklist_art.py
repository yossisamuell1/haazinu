#!/usr/bin/env python3
"""Remove artworks on verse ranges traditionally depicted nude, whatever the classifiers said."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BLACK = [("Genesis",2,25,25),("Genesis",3,1,24),("Genesis",9,20,27),("Genesis",19,30,38),("Genesis",38,1,30),("Genesis",39,1,23),
         ("II Samuel",11,1,27),("II Samuel",13,1,22),("Judges",16,4,22),("Judges",19,1,30),("Ezekiel",16,1,63),("Ezekiel",23,1,49),("Esther",2,1,20)]
def hit(ref):
    m = re.match(r"^(.+) (\d+):(\d+)(?:-(\d+))?$", ref)
    if not m: return False
    b, c, v1 = m.group(1), int(m.group(2)), int(m.group(3)); v2 = int(m.group(4) or v1)
    return any(b == bb and c == cc and not (v2 < a or v1 > z) for bb, cc, a, z in BLACK)
d = json.load(open(ROOT / "data/art.json")); works = d["works"]
keep = [w for w in works if not any(hit(r) for r in w["refs"])]
drop = [w for w in works if any(hit(r) for r in w["refs"])]
p = ROOT / ".work/art/rejected.json"
prev = json.load(open(p)) if p.exists() else []
json.dump(prev + [{**w, "why": "scene blacklist"} for w in drop], open(p, "w"), ensure_ascii=False, indent=0)
d["works"] = keep; d["meta"]["count"] = len(keep)
d["meta"]["screened"] = "CLIP zero-shot (>=0.15 rejected) + NudeNet + title keywords + scene blacklist"
json.dump(d, open(ROOT / "data/art.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(f"blacklist removed {len(drop)}; kept {len(keep)}")
