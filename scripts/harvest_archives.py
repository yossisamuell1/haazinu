#!/usr/bin/env python3
"""Harvest verse-keyed Tanakh artwork from open library and archive APIs that need no key:
  * National Gallery of Art open data (CSV dumps, CC0)
  * Smithsonian Open Access      * Yale LUX (Yale collections)      * Wellcome Collection
Titles carry no chapter and verse, so they are matched against data/scenes.json.
Output: .work/art/archive_raw.json  (screen with clip_screen.py before installing)
Usage: python3 scripts/harvest_archives.py [--only nga,si,yale,wellcome]
"""
import csv, json, re, sys, time, urllib.request, urllib.parse
from pathlib import Path
csv.field_size_limit(10 ** 8)
ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / ".work/art"
UA = {"User-Agent": "Haazinu/1.0 (personal Torah app)"}
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else {"nga", "si", "yale", "wellcome"}
SCENES = [(re.compile(p, re.I), r) for p, r in json.load(open(ROOT / "data/scenes.json"))["scenes"]]
SKIP = re.compile(r"\bnude|naked|nudit|bath(e|es|ing)?\b|bathsheba|susanna|lot and his daughter|daughters of lot|drunken|potiphar|tamar|delilah|adam and eve|\beve\b|paradise|venus|bacchus|diana|nymph|odalisque", re.I)
def match_scene(t):
    if not t or SKIP.search(t): return None
    for rx, ref in SCENES:
        if rx.search(t): return ref
    return None
def get(u, t=45, hdr=None):
    for a in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={**UA, **(hdr or {})}), timeout=t))
        except Exception: time.sleep(2 * (a + 1))
    return None
works = {}
def add(w):
    if not w.get("thumb"): return
    works.setdefault((w["title"].lower()[:60], (w["artist"] or "").lower()[:30], w["refs"][0]), w)

# ---------------- National Gallery of Art ----------------
if "nga" in ONLY and (ART / "nga/objects.csv").exists():
    imgs = {}
    with open(ART / "nga/published_images.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            oid = r.get("depictstmsobjectid")
            if oid and r.get("iiifthumburl") and oid not in imgs: imgs[oid] = (r["iiifthumburl"], r.get("iiifurl", ""))
    n = 0
    with open(ART / "nga/objects.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ref = match_scene(r.get("title"))
            if not ref: continue
            im = imgs.get(r["objectid"])
            if not im: continue
            add({"title": (r["title"] or "")[:90], "artist": (r.get("attribution") or "Unknown")[:60],
                 "year": (r.get("beginyear") or None), "refs": [ref],
                 "thumb": im[0] + "/full/!500,500/0/default.jpg" if not im[0].endswith(".jpg") else im[0],
                 "image": (im[1] or im[0]) + "/full/!1200,1200/0/default.jpg" if not (im[1] or im[0]).endswith(".jpg") else (im[1] or im[0]),
                 "page": f"https://www.nga.gov/collection/art-object-page.{r['objectid']}.html", "source": "National Gallery of Art"})
            n += 1
    print(f"NGA: {n} matched", file=sys.stderr)

# ---------------- Smithsonian Open Access ----------------
if "si" in ONLY:
    key = "DEMO_KEY"; n = 0
    for q in ["Old Testament", "bible", "Moses", "Abraham", "David Goliath", "prophet"]:
        for start in (0, 100, 200):
            j = get(f"https://api.si.edu/openaccess/api/v1.0/search?api_key={key}&q={urllib.parse.quote(q)}&rows=100&start={start}")
            rows = ((j or {}).get("response") or {}).get("rows") or []
            if not rows: break
            for d in rows:
                t = d.get("title", "")
                ref = match_scene(t)
                if not ref: continue
                c = d.get("content", {}) or {}
                media = (((c.get("descriptiveNonRepeating") or {}).get("online_media") or {}).get("media") or [])
                thumb = next((m.get("thumbnail") for m in media if m.get("thumbnail")), None)
                if not thumb: continue
                usage = (((c.get("descriptiveNonRepeating") or {}).get("online_media") or {}).get("media") or [{}])[0].get("usage", {}).get("access", "")
                if usage and usage != "CC0": continue
                fs = (c.get("freetext") or {})
                artist = next((x.get("content", "") for x in (fs.get("name") or []) if x.get("content")), "Unknown")
                date = next((x.get("content", "") for x in (fs.get("date") or []) if x.get("content")), "")
                add({"title": t[:90], "artist": str(artist)[:60], "year": (re.search(r"\b1[0-9]{3}\b", date) or [None]) and (re.search(r"\b1[0-9]{3}\b", date).group(0) if re.search(r"\b1[0-9]{3}\b", date) else None),
                     "refs": [ref], "thumb": thumb, "image": next((m.get("content") for m in media if m.get("content")), thumb),
                     "page": ((c.get("descriptiveNonRepeating") or {}).get("record_link") or ""), "source": "Smithsonian"})
                n += 1
            time.sleep(1.2)
    print(f"Smithsonian: {n} matched", file=sys.stderr)

# ---------------- Wellcome Collection ----------------
if "wellcome" in ONLY:
    n = 0
    for q in ["Old Testament", "bible illustration", "Moses", "Abraham", "David", "prophet", "biblical"]:
        for page in (1, 2, 3):
            j = get(f"https://api.wellcomecollection.org/catalogue/v2/works?query={urllib.parse.quote(q)}&pageSize=100&page={page}&include=items,production&items.locations.licenseId=pdm,cc-0,cc-by")
            res = (j or {}).get("results") or []
            if not res: break
            for d in res:
                ref = match_scene(d.get("title"))
                if not ref: continue
                iid = None
                for it in d.get("items", []):
                    for loc in it.get("locations", []):
                        u = loc.get("url", "")
                        m = re.search(r"/iiif/([^/]+)/", u)
                        if m: iid = m.group(1); break
                    if iid: break
                if not iid: continue
                add({"title": (d.get("title") or "")[:90], "artist": ", ".join(c["label"] for c in (d.get("contributors") or [])[:1]) or "Unknown",
                     "year": ((d.get("production") or [{}])[0].get("dates") or [{}])[0].get("label", "")[:4] or None,
                     "refs": [ref], "thumb": f"https://iiif.wellcomecollection.org/image/{iid}/full/500,/0/default.jpg",
                     "image": f"https://iiif.wellcomecollection.org/image/{iid}/full/1200,/0/default.jpg",
                     "page": f"https://wellcomecollection.org/works/{d['id']}", "source": "Wellcome Collection"})
                n += 1
            time.sleep(0.6)
    print(f"Wellcome: {n} matched", file=sys.stderr)

# ---------------- Yale LUX ----------------
if "yale" in ONLY:
    n = 0
    for q in ["Old Testament", "bible", "Moses", "Abraham", "David", "prophet"]:
        for page in (1, 2):
            j = get("https://lux.collections.yale.edu/api/search/item?q=" + urllib.parse.quote(json.dumps({"text": q})) + f"&page={page}&pageLength=100")
            items = (j or {}).get("orderedItems") or []
            if not items: break
            for it in items[:100]:
                d = get(it["id"], t=25)
                if not d: continue
                t = (d.get("_label") or "")
                ref = match_scene(t)
                if not ref: continue
                thumb = None
                for rep in d.get("representation", []):
                    for acc in rep.get("digitally_shown_by", []) or []:
                        for ap in acc.get("access_point", []) or []:
                            if ap.get("id", "").endswith((".jpg", "default.jpg")) or "iiif" in ap.get("id", ""): thumb = ap["id"]; break
                if not thumb: continue
                add({"title": t[:90], "artist": "Unknown", "year": None, "refs": [ref], "thumb": thumb, "image": thumb,
                     "page": d.get("id", ""), "source": "Yale collections"})
                n += 1
            time.sleep(0.5)
    print(f"Yale: {n} matched", file=sys.stderr)

items = list(works.values())
for n, w in enumerate(items): w["id"] = f"arc-{n+1}"
json.dump({"meta": {"note": "Tanakh artwork from open library and archive APIs, keyed to verses via data/scenes.json", "count": len(items)}, "works": items}, open(ART / "archive_raw.json", "w"), ensure_ascii=False, separators=(",", ":"))
import collections
print(f"\nworks: {len(items)}", file=sys.stderr)
print(collections.Counter(w["source"] for w in items).most_common(), file=sys.stderr)
