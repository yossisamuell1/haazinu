#!/usr/bin/env python3
"""Harvest verse-keyed Tanakh artwork from open museum APIs (no keys needed):
  * The Metropolitan Museum of Art   * Art Institute of Chicago   * Cleveland Museum of Art
Museum records carry no chapter and verse, so titles are matched against data/scenes.json, a table of
biblical scene titles to the verse depicted. Only public-domain / CC0 records with images are kept.
Output: .work/art/museum_raw.json (screen it with clip_screen.py before installing).
Usage: python3 scripts/harvest_museums.py [--limit-met 20]
"""
import json, re, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / ".work/art"; ART.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Haazinu/1.0 (personal Torah app)"}
MET_PER_SCENE = int(sys.argv[sys.argv.index("--limit-met") + 1]) if "--limit-met" in sys.argv else 20
SCENES = [(re.compile(p, re.I), r) for p, r in json.load(open(ROOT / "data/scenes.json"))["scenes"]]
SKIP = re.compile(r"\bnude|naked|nudit|bath(e|es|ing)?\b|bathsheba|susanna|lot and his daughter|daughters of lot|drunken|potiphar|tamar|delilah cut|adam and eve|\beve\b|paradise|venus|bacchus|diana|nymph", re.I)
def match_scene(title):
    if not title or SKIP.search(title): return None
    for rx, ref in SCENES:
        if rx.search(title): return ref
    return None
def get(u, t=45):
    for a in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t))
        except Exception: time.sleep(1.5 * (a + 1))
    return None
def query_of(pattern):
    q = pattern.split("|")[0]
    return re.sub(r"[\\^$.*+?()\[\]{}]|\(\?i\)|\\b|s\?|\(|\)", " ", q).replace("?", " ").strip()
MET_CACHE = ART / "met_objects.json"
met_cache = json.load(open(MET_CACHE)) if MET_CACHE.exists() else {}
works = {}
def add(w):
    key = (w["title"].lower()[:60], (w["artist"] or "").lower()[:30], w["refs"][0])
    works.setdefault(key, w)

# ---------- Art Institute of Chicago (100 records per request) ----------
FIELDS = "id,title,artist_title,date_display,image_id,is_public_domain,classification_title"
aic_seen = set()
def aic(q, pages=3):
    for page in range(1, pages + 1):
        j = get(f"https://api.artic.edu/api/v1/artworks/search?q={urllib.parse.quote(q)}&limit=100&page={page}&fields={FIELDS}")
        if not j or not j.get("data"): return
        base = j.get("config", {}).get("iiif_url", "https://www.artic.edu/iiif/2")
        for d in j["data"]:
            if d["id"] in aic_seen or not d.get("image_id") or not d.get("is_public_domain"): continue
            aic_seen.add(d["id"])
            ref = match_scene(d.get("title"))
            if not ref: continue
            add({"title": (d["title"] or "")[:90], "artist": (d.get("artist_title") or "Unknown")[:60],
                 "year": (re.search(r"\b(1[0-9]{3}|[1-9][0-9]{2})\b", d.get("date_display") or "") or [None]) and (re.search(r"\b(1[0-9]{3}|[1-9][0-9]{2})\b", d.get("date_display") or "").group(0) if re.search(r"\b(1[0-9]{3}|[1-9][0-9]{2})\b", d.get("date_display") or "") else None),
                 "refs": [ref], "thumb": f"{base}/{d['image_id']}/full/500,/0/default.jpg", "image": f"{base}/{d['image_id']}/full/1200,/0/default.jpg",
                 "page": f"https://www.artic.edu/artworks/{d['id']}", "source": "Art Institute of Chicago"})
# ---------- Cleveland (up to 1000 per request) ----------
def cma(q, limit=500):
    j = get(f"https://openaccess-api.clevelandart.org/api/artworks/?q={urllib.parse.quote(q)}&has_image=1&cc0=1&limit={limit}")
    if not j: return
    for d in j.get("data", []):
        ref = match_scene(d.get("title"))
        if not ref: continue
        im = d.get("images") or {}
        thumb = (im.get("web") or {}).get("url") or (im.get("print") or {}).get("url")
        if not thumb: continue
        cr = (d.get("creators") or [{}])[0].get("description", "")
        add({"title": (d.get("title") or "")[:90], "artist": re.sub(r"\s*\(.*", "", cr)[:60] or "Unknown",
             "year": str(d.get("creation_date_earliest") or "")[:4] or None, "refs": [ref],
             "thumb": thumb, "image": (im.get("print") or {}).get("url") or thumb,
             "page": d.get("url") or "", "source": "Cleveland Museum of Art"})
# ---------- Met (object fetch per id) ----------
met_ids = {}
def met_search(q, cap):
    j = get("https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q=" + urllib.parse.quote(q))
    for i in ((j or {}).get("objectIDs") or [])[:cap]: met_ids.setdefault(i, q)
def met_obj(i):
    key = str(i)
    if key in met_cache:
        o = met_cache[key]
    else:
        o = get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}", t=30)
        # keep only the fields we need, so the cache stays small
        met_cache[key] = {k: (o or {}).get(k) for k in ("title", "artistDisplayName", "objectBeginDate", "isPublicDomain", "primaryImageSmall", "primaryImage", "objectURL")} if o else {}
        o = met_cache[key]
    if not o or not o.get("isPublicDomain") or not o.get("primaryImageSmall"): return
    ref = match_scene(o.get("title"))
    if not ref: return
    add({"title": (o.get("title") or "")[:90], "artist": (o.get("artistDisplayName") or "Unknown")[:60],
         "year": (str(o.get("objectBeginDate")) if o.get("objectBeginDate") and o["objectBeginDate"] > 0 else None),
         "refs": [ref], "thumb": o["primaryImageSmall"], "image": o.get("primaryImage") or o["primaryImageSmall"],
         "page": o.get("objectURL", ""), "source": "The Metropolitan Museum of Art"})
def save_partial():
    items = list(works.values())
    for k, w in enumerate(items): w["id"] = f"mus-{k+1}"
    json.dump({"meta": {"note": "Tanakh artwork from open museum APIs", "count": len(items)}, "works": items}, open(ART / "museum_raw.json", "w"), ensure_ascii=False, separators=(",", ":"))
    try: json.dump(met_cache, open(MET_CACHE, "w"))
    except Exception: pass
BROAD = ["Old Testament", "Bible", "biblical", "Moses", "Abraham", "David", "Solomon", "Elijah", "Joseph Egypt",
         "Jacob", "Samson", "Daniel", "Jonah", "Esther", "Ruth", "Noah", "Isaac", "Joshua", "prophet", "Israelites"]
scene_qs = [query_of(p.pattern) for p, _ in SCENES]
print(f"scenes: {len(SCENES)}", file=sys.stderr)
for q in BROAD + scene_qs:
    aic(q, pages=3 if q in BROAD else 1)
print(f"after AIC: {len(works)}", file=sys.stderr)
for q in BROAD + scene_qs:
    cma(q, limit=300)
print(f"after Cleveland: {len(works)}", file=sys.stderr)
save_partial()
if "--no-met" in sys.argv:
    print("skipping Met (rate limited)", file=sys.stderr)
    ids = []
else:
    for q in BROAD: met_search(q, 400)
    for q in scene_qs: met_search(q, MET_PER_SCENE)
    print(f"Met objects to fetch: {len(met_ids)}", file=sys.stderr)
    ids = list(met_ids)
with ThreadPoolExecutor(max_workers=12) as ex:
    for n, _ in enumerate(ex.map(met_obj, ids)):
        if (n + 1) % 250 == 0:
            save_partial(); print(f"  met {n+1}/{len(ids)} (works {len(works)})", file=sys.stderr)
items = list(works.values())
for n, w in enumerate(items): w["id"] = f"mus-{n+1}"
json.dump({"meta": {"note": "Tanakh artwork from open museum APIs, keyed to verses via data/scenes.json", "count": len(items)}, "works": items}, open(ART / "museum_raw.json", "w"), ensure_ascii=False, separators=(",", ":"))
import collections
print(f"\nworks: {len(items)}", file=sys.stderr)
print(collections.Counter(w["source"] for w in items).most_common(), file=sys.stderr)
print(collections.Counter(w["refs"][0].rsplit(" ", 1)[0] for w in items).most_common(12), file=sys.stderr)
