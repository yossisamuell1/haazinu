#!/usr/bin/env python3
"""Merge every harvested art source into data/art.json, de-duplicating and re-numbering ids.
Sources: .work/art/art_raw.json (Wikimedia Commons), museum_raw.json (Met/AIC/Cleveland),
archive_raw.json (NGA/Smithsonian/Yale/Wellcome), plus whatever is already installed.
Screen the result with scripts/clip_screen.py before serving it.
Usage: python3 scripts/merge_art.py
"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / ".work/art"
out, seen = [], set()
def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())[:50]
sources = [ROOT / "data/art.json", ART / "museum_raw.json", ART / "archive_raw.json"]
for p in sources:
    if not p.exists(): continue
    d = json.load(open(p))
    n = 0
    for w in d.get("works", []):
        if not w.get("thumb") or not w.get("refs"): continue
        key = (norm(w["title"]), norm(w.get("artist")), w["refs"][0])
        if key in seen: continue
        seen.add(key); w.pop("file", None); out.append(w); n += 1
    print(f"{p.name}: +{n} (total {len(out)})")
for i, w in enumerate(out): w["id"] = f"art-{i+1}"
json.dump({"meta": {"note": "Public-domain Tanakh artwork keyed to the verse depicted, from Wikimedia Commons and open museum, library and archive APIs.", "count": len(out), "screened": "pending"}, "works": out}, open(ROOT / "data/art.json", "w"), ensure_ascii=False, separators=(",", ":"))
import collections
print(f"\nmerged {len(out)} works")
print(collections.Counter(w.get("source", "?")[:38] for w in out).most_common(12))
