#!/usr/bin/env python3
"""Screen data/art.json for nudity with NudeNet (offline image classifier) on top of the title keyword filter.
Downloads each thumbnail to .work/art/thumbs/, runs the detector, and removes any work with an exposed-body
detection above the threshold. Rejected works are listed in .work/art/rejected.json for review.
Usage: python3 scripts/screen_art.py [--threshold 0.25] [--in data/art.json]"""
import json, sys, os, urllib.request, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
INP = Path(sys.argv[sys.argv.index("--in") + 1]) if "--in" in sys.argv else ROOT / "data/art.json"
THR = float(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 0.25
TH = ROOT / ".work/art/thumbs"; TH.mkdir(parents=True, exist_ok=True)
from concurrent.futures import ThreadPoolExecutor
from nudenet import NudeDetector
det = NudeDetector()
EXPOSED = {"FEMALE_BREAST_EXPOSED", "FEMALE_GENITALIA_EXPOSED", "MALE_GENITALIA_EXPOSED", "BUTTOCKS_EXPOSED", "ANUS_EXPOSED", "MALE_BREAST_EXPOSED", "BELLY_EXPOSED"}
STRICT = {"FEMALE_BREAST_EXPOSED", "FEMALE_GENITALIA_EXPOSED", "MALE_GENITALIA_EXPOSED", "BUTTOCKS_EXPOSED", "ANUS_EXPOSED"}
d = json.load(open(INP)); works = d["works"]
def fetch(w):
    f = TH / (w["id"] + ".jpg")
    if f.exists() and f.stat().st_size > 1000: return
    for a in range(3):
        try:
            req = urllib.request.Request(w["thumb"], headers={"User-Agent": "Haazinu/1.0 (personal Torah app)"})
            f.write_bytes(urllib.request.urlopen(req, timeout=60).read()); return
        except Exception: time.sleep(1.5)
with ThreadPoolExecutor(max_workers=8) as ex:
    for n, _ in enumerate(ex.map(fetch, works)):
        if (n + 1) % 200 == 0: print(f"  fetched {n+1}/{len(works)}", file=sys.stderr)
keep, rejected = [], []
for i, w in enumerate(works):
    f = TH / (w["id"] + ".jpg")
    if not f.exists() or f.stat().st_size < 1000:
        for a in range(3):
            try:
                # Wikimedia rejects the default python-urllib agent
                req = urllib.request.Request(w["thumb"], headers={"User-Agent": "Haazinu/1.0 (personal Torah app)"})
                f.write_bytes(urllib.request.urlopen(req, timeout=60).read()); break
            except Exception: time.sleep(2)
    if not f.exists() or f.stat().st_size < 1000: rejected.append({**w, "why": "thumbnail unavailable"}); continue
    try: dets = det.detect(str(f))
    except Exception as e: rejected.append({**w, "why": f"detector error {e}"}); continue
    hits = [(x["class"], round(x["score"], 2)) for x in dets if x["class"] in EXPOSED and x["score"] >= THR]
    strict = [h for h in hits if h[0] in STRICT]
    # reject on any strict exposure, or on two or more softer exposures (belly / male chest)
    if strict or len(hits) >= 2: rejected.append({**w, "why": hits})
    else: keep.append(w)
    if (i + 1) % 100 == 0: print(f"  {i+1}/{len(works)} screened, {len(rejected)} rejected", file=sys.stderr)
d["works"] = keep; d["meta"]["count"] = len(keep); d["meta"]["screened"] = "NudeNet image screen + title keywords"
json.dump(d, open(INP, "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(rejected, open(ROOT / ".work/art/rejected.json", "w"), ensure_ascii=False, indent=0)
print(f"kept {len(keep)}, rejected {len(rejected)} -> {INP}")
for r in rejected[:40]: print("  ", r["artist"], "|", r["title"][:50], "|", r["why"])
