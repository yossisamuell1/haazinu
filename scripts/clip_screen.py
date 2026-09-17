#!/usr/bin/env python3
"""Screen artwork for nudity with CLIP zero-shot classification.

NudeNet is trained on photographs and misses painted nudity (it scores a Rubens nude at zero), so this is the
primary modesty screen for an art corpus. Each image is scored against two prompt sets, one describing nude or
partially nude figures and one describing clothed figures, landscapes and text; a work is rejected when the
nude side wins by more than --threshold of the probability mass.

Usage: python3 scripts/clip_screen.py --json data/art.json --thumbs .work/art/thumbs [--threshold 0.35] [--apply]
Without --apply it only writes .work/art/clip_scores.json for review.
"""
import json, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
import torch, open_clip
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
JSON = Path(sys.argv[sys.argv.index("--json") + 1]) if "--json" in sys.argv else ROOT / "data/art.json"
TH = Path(sys.argv[sys.argv.index("--thumbs") + 1]) if "--thumbs" in sys.argv else ROOT / ".work/art/thumbs"
THRESH = float(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 0.35
APPLY = "--apply" in sys.argv
NUDE = [
    "a painting of a nude woman", "a painting of a naked woman with bare breasts",
    "an engraving of a nude figure", "a drawing of a naked man", "a nude body in classical art",
    "a woman bathing naked", "a painting of bare breasts", "a naked figure with exposed buttocks",
    "an undressed person in a painting", "a topless woman in a painting",
]
CLEAN = [
    "a painting of people wearing robes and clothes", "an engraving of clothed biblical figures",
    "a landscape painting with no people", "a page of printed text", "a drawing of men in long robes",
    "a painting of a crowd of dressed people", "an illustration of clothed men and women",
    "a portrait of a person wearing a coat", "an ornamental border or decorative pattern",
    "a picture of animals or buildings",
]
device = "cpu"
model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k", device=device)
tok = open_clip.get_tokenizer("ViT-B-32")
with torch.no_grad():
    tf = model.encode_text(tok(NUDE + CLEAN).to(device))
    tf /= tf.norm(dim=-1, keepdim=True)
def score(paths):
    ims = []
    for p in paths:
        try: ims.append(preprocess(Image.open(p).convert("RGB")))
        except Exception: ims.append(torch.zeros(3, 224, 224))
    with torch.no_grad():
        f = model.encode_image(torch.stack(ims).to(device)); f /= f.norm(dim=-1, keepdim=True)
        probs = (100.0 * f @ tf.T).softmax(dim=-1)
    return probs[:, :len(NUDE)].sum(dim=-1).tolist()
if __name__ == "__main__":
    if "--test" in sys.argv:
        for p in sys.argv[sys.argv.index("--test") + 1].split(","):
            print(f"{score([p])[0]:.3f}  {p}")
        sys.exit()
    d = json.load(open(JSON)); works = d["works"]
    have = [w for w in works if (TH / (w["id"] + ".jpg")).exists()]
    scores = {}
    for i in range(0, len(have), 32):
        b = have[i:i + 32]
        for w, s in zip(b, score([TH / (w["id"] + ".jpg") for w in b])): scores[w["id"]] = round(s, 4)
        if (i + 32) % 320 < 32: print(f"  {min(i+32,len(have))}/{len(have)}", file=sys.stderr)
    json.dump(scores, open(ROOT / ".work/art/clip_scores.json", "w"))
    flagged = [w for w in works if scores.get(w["id"], 0) >= THRESH]
    print(f"scored {len(scores)}; flagged {len(flagged)} at >= {THRESH}")
    for w in sorted(flagged, key=lambda w: -scores[w["id"]])[:30]: print(f"  {scores[w['id']]:.2f} {w['title'][:45]} | {w['artist'][:20]} | {w['refs'][0]}")
    if APPLY:
        keep = [w for w in works if scores.get(w["id"], 1) < THRESH]
        prev = json.load(open(ROOT / ".work/art/rejected.json")) if (ROOT / ".work/art/rejected.json").exists() else []
        json.dump(prev + [{**w, "why": f"clip {scores.get(w['id'])}"} for w in flagged], open(ROOT / ".work/art/rejected.json", "w"), ensure_ascii=False, indent=0)
        d["works"] = keep; d["meta"]["count"] = len(keep); d["meta"]["screened"] = "CLIP zero-shot + NudeNet + title keywords"
        json.dump(d, open(JSON, "w"), ensure_ascii=False, separators=(",", ":"))
        print(f"applied: kept {len(keep)}")
