#!/usr/bin/env python3
"""Cheap skin-area heuristic for painted nudity, used alongside the NudeNet and CLIP screens.
Counts pixels in a skin-tone range inside the image's central region and reports the fraction; a large
connected expanse of skin in a figurative painting is the signal that the photo-trained detector misses.
Usage: python3 scripts/skin_screen.py <thumbs dir> <art json>  -> prints id,fraction sorted high to low"""
import json, sys
from pathlib import Path
from PIL import Image
def skin_fraction(p):
    try: im = Image.open(p).convert("RGB")
    except Exception: return None
    im.thumbnail((160, 160))
    w, h = im.size
    px = im.load(); skin = tot = 0
    for y in range(int(h * .08), int(h * .95)):
        for x in range(int(w * .08), int(w * .92)):
            r, g, b = px[x, y]; tot += 1
            mx, mn = max(r, g, b), min(r, g, b)
            if r > 92 and g > 40 and b > 20 and mx - mn > 12 and abs(r - g) > 12 and r > g > b and r < 250 and g < 225: skin += 1
    return skin / tot if tot else 0
if __name__ == "__main__":
    TH, J = Path(sys.argv[1]), json.load(open(sys.argv[2]))
    out = []
    for w in J["works"]:
        f = TH / (w["id"] + ".jpg")
        if f.exists(): out.append((skin_fraction(f) or 0, w["id"], w["title"][:40], w["artist"][:20]))
    out.sort(reverse=True)
    for frac, i, t, a in out: print(f"{frac:.3f} {i} {t} | {a}")
