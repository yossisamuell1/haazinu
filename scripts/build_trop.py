#!/usr/bin/env python3
"""Build data/trop.json: word-level chant timings for every Torah verse.

Sources (all CC-BY-SA, PocketTorah / not-a-box media lab):
  https://github.com/rneiss/PocketTorah
    data/aliyah.json            aliyah verse ranges per parsha
    data/torah/labels/*.txt     comma-separated word start times per aliyah MP3
    data/torah/json/*.json      Tanach.us word tokenisation (for word counts)
    data/audio/*.mp3            the recordings (streamed from raw.githubusercontent.com)
"""
import json, os, re, sys, urllib.request, urllib.parse
from pathlib import Path

RAW = "https://raw.githubusercontent.com/rneiss/PocketTorah/master/"
HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"
OUT = HERE.parent / "data" / "trop.json"
BOOKS = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]

def fetch(rel, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    url = RAW + urllib.parse.quote(rel)
    print("  fetch", rel)
    urllib.request.urlretrieve(url, dest)
    return dest

def load_json(p):
    return json.load(open(p, encoding="utf-8-sig"))

# --- inputs -----------------------------------------------------------
aliyah = load_json(fetch("data/aliyah.json", CACHE / "aliyah.json"))["parshiot"]["parsha"]
label_paths = [l.strip() for l in open(CACHE / "labels.txt") if l.strip()]
audio_files = load_json(CACHE / "audio_files.json")
def norm(s):
    return re.sub(r"[^a-z0-9-]", "", s.lower())
audio_by_key = {norm(a[:-4]): a for a in audio_files}

# word counts per verse, per book, from PocketTorah's Tanach.us JSON
words = {}
for b in BOOKS:
    d = load_json(fetch(f"data/torah/json/{b}.json", CACHE / "json" / f"{b}.json"))
    chapters = d["Tanach"]["tanach"]["book"]["c"]
    words[b] = []
    for c in chapters:
        if not isinstance(c, dict) or "v" not in c:
            continue
        vs = c["v"] if isinstance(c["v"], list) else [c["v"]]
        counts = []
        for v in vs:
            w = v.get("w", [])
            counts.append(len(w) if isinstance(w, list) else 1)
        words[b].append(counts)

# which book each parsha is in, from its "_verse" field ("Genesis 1:1 - 6:8")
def parsha_book(p):
    return p["_verse"].split(" ")[0] if not p["_verse"].startswith("I") else p["_verse"].rsplit(" ", 3)[0]

def parse_cv(s):
    c, v = s.split(":")
    return int(c), int(v)

def verses_between(book, begin, end):
    (c1, v1), (c2, v2) = parse_cv(begin), parse_cv(end)
    out = []
    c, v = c1, v1
    while (c, v) <= (c2, v2):
        out.append((c, v))
        if v < len(words[book][c - 1]):
            v += 1
        else:
            c, v = c + 1, 1
    return out

# --- build ------------------------------------------------------------
files = {}          # fileId -> url
verses = {b: {} for b in BOOKS}   # book -> "c:v" -> [fileId, [t0..tn]]
missing_labels, mismatches = [], []

for p in aliyah:
    pid = p["_id"]
    book = parsha_book(p)
    if book not in BOOKS:
        continue
    for al in p["fullkriyah"]["aliyah"]:
        n = al["_num"]
        if n == "M":
            continue
        key = norm(f"{pid}-{n}")
        audio = audio_by_key.get(key)
        if not audio:
            missing_labels.append(f"{pid}-{n} (no audio)")
            continue
        file_id = audio[:-4]
        files[file_id] = RAW + "data/audio/" + audio
        vlist = verses_between(book, al["_begin"], al["_end"])
        # label file may be "Achrei Mot-1.txt" style; find it case/space-insensitively
        lp = next((l for l in label_paths if norm(os.path.basename(l)[:-4]) == key), None)
        if not lp:
            missing_labels.append(f"{pid}-{n}")
            for c, v in vlist:
                verses[book][f"{c}:{v}"] = [file_id, None]
            continue
        raw = open(fetch(lp, CACHE / "labels" / os.path.basename(lp)), encoding="utf-8-sig").read()
        times = [round(float(x), 3) for x in raw.replace("\n", ",").split(",") if x.strip()]
        expected = sum(words[book][c - 1][v - 1] for c, v in vlist)
        if len(times) != expected:
            mismatches.append(f"{pid}-{n}: {len(times)} labels vs {expected} words")
        i = 0
        for c, v in vlist:
            n_w = words[book][c - 1][v - 1]
            seg = times[i:i + n_w + 1]
            if len(seg) == n_w + 1:
                verses[book][f"{c}:{v}"] = [file_id, seg]
            elif len(seg) == n_w:  # last verse of the file: no following word, end = null (audio end)
                verses[book][f"{c}:{v}"] = [file_id, seg + [None]]
            else:
                verses[book][f"{c}:{v}"] = [file_id, None]
            i += n_w

meta = {
    "source": "PocketTorah",
    "reader": "Ashkenazi cantillation, Binder/Avery style",
    "license": "CC-BY-SA 3.0",
    "attribution": "Audio recordings of the weekly Torah portions used in PocketTorah, released under CC-BY-SA by not-a-box media lab. https://github.com/rneiss/PocketTorah",
    "format": "verses[book]['c:v'] = [fileId, [wordStart0, ..., wordStartN-1, verseEnd]] ; null end = play to end of file",
}
OUT.parent.mkdir(exist_ok=True)
json.dump({"meta": meta, "files": files, "verses": verses}, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))

parshiot = []
for p in aliyah:
    b = parsha_book(p)
    if b not in BOOKS: continue
    rng = p["_verse"].split(" ", 1)[1] if not b.startswith("I") else p["_verse"]
    begin, end = [x.strip() for x in rng.split("-")]
    parshiot.append({"id": p["_id"], "he": p["_hebrew"], "book": b, "begin": begin, "end": end,
                     "aliyot": [{"n": a["_num"], "begin": a["_begin"], "end": a["_end"]} for a in p["fullkriyah"]["aliyah"]]})
json.dump(parshiot, open(OUT.parent / "parshiot.json", "w"), ensure_ascii=False, indent=0)
total = sum(len(v) for v in verses.values())
timed = sum(1 for b in verses.values() for x in b.values() if x[1])
print(f"wrote {OUT} ({OUT.stat().st_size//1024} KB): {total} verses, {timed} with word timings, {len(files)} audio files")
if missing_labels: print("no label file:", ", ".join(missing_labels))
if mismatches: print("count mismatches:", *mismatches, sep="\n  ")
