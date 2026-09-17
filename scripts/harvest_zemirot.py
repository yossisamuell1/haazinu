#!/usr/bin/env python3
"""Add songs from the Zemirot Database (zemirotdatabase.org), which lists zemirot, piyutim and table songs
with the scriptural source of each. Only factual metadata is taken: title, Hebrew opening words, and the
source verses, which are converted to Sefaria refs and merged into data/songs.json. Translations, user
recordings and commentary are not copied.

Usage: python3 scripts/harvest_zemirot.py [--dry] [--limit N]
"""
import json, re, sys, time, html, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SONGS = ROOT / "data/songs.json"
CACHE = ROOT / ".work/zemirot.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
DRY = "--dry" in sys.argv
LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
BOOKS = {"genesis":"Genesis","exodus":"Exodus","leviticus":"Leviticus","numbers":"Numbers","deuteronomy":"Deuteronomy","joshua":"Joshua","judges":"Judges","ruth":"Ruth",
 "i samuel":"I Samuel","ii samuel":"II Samuel","1 samuel":"I Samuel","2 samuel":"II Samuel","samuel i":"I Samuel","samuel ii":"II Samuel",
 "i kings":"I Kings","ii kings":"II Kings","1 kings":"I Kings","2 kings":"II Kings","kings i":"I Kings","kings ii":"II Kings",
 "i chronicles":"I Chronicles","ii chronicles":"II Chronicles","1 chronicles":"I Chronicles","2 chronicles":"II Chronicles","chronicles i":"I Chronicles","chronicles ii":"II Chronicles",
 "isaiah":"Isaiah","jeremiah":"Jeremiah","ezekiel":"Ezekiel","hosea":"Hosea","joel":"Joel","amos":"Amos","obadiah":"Obadiah","jonah":"Jonah","micah":"Micah","nahum":"Nahum",
 "habakkuk":"Habakkuk","zephaniah":"Zephaniah","haggai":"Haggai","zechariah":"Zechariah","malachi":"Malachi","psalm":"Psalms","psalms":"Psalms","tehillim":"Psalms",
 "proverbs":"Proverbs","job":"Job","song of songs":"Song of Songs","song of solomon":"Song of Songs","canticles":"Song of Songs","ruth":"Ruth","lamentations":"Lamentations",
 "ecclesiastes":"Ecclesiastes","esther":"Esther","daniel":"Daniel","ezra":"Ezra","nehemiah":"Nehemiah"}
ALT = "|".join(sorted((re.escape(b) for b in BOOKS), key=len, reverse=True))
REF_RE = re.compile(rf"\b({ALT})\.?\s*(\d{{1,3}})[:.,](\d{{1,3}})(?:\s*[-–]\s*(\d{{1,3}}))?", re.I)
def _strip_zw(t): return "".join(ch for ch in t if not (0x200b <= ord(ch) <= 0x200f or 0x202a <= ord(ch) <= 0x202e or ord(ch) == 0xfeff))
def clean(s): return re.sub(r"\s+", " ", _strip_zw(html.unescape(re.sub(r"<[^>]+>", " ", s or "")))).strip()
def get(u, t=40):
    for a in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read().decode("utf-8", "ignore")
        except Exception: time.sleep(2)
    return ""
index = get("https://www.zemirotdatabase.org/song_index.php")
entries = re.findall(r"view_song\.php\?id=(\d+)[^>]*>(.*?)</a>", index, re.S)
print(f"index: {len(entries)} songs", file=sys.stderr)
cache = json.load(open(CACHE)) if CACHE.exists() else {}
todo = [(i, t) for i, t in entries if i not in cache][:LIMIT]
def fetch(pair):
    sid, raw = pair
    page = get(f"https://www.zemirotdatabase.org/view_song.php?id={sid}")
    if not page: return sid, None
    he = clean((re.search(r"<div id='hebrew'[^>]*>(.*?)</div>", page, re.S) or [None, ""])[1])
    tr = clean((re.search(r"<div id='transliteration'[^>]*>(.*?)</div>", page, re.S) or [None, ""])[1])
    tl = (re.search(r"<div id='translation'[^>]*>(.*?)</div>", page, re.S) or [None, ""])[1]
    refs, seen = [], set()
    for m in REF_RE.finditer(clean(tl)):
        book = BOOKS[m.group(1).lower()]; c, v = m.group(2), m.group(3); v2 = m.group(4)
        r = f"{book} {c}:{v}" + (f"-{v2}" if v2 and int(v2) > int(v) else "")
        if r not in seen: seen.add(r); refs.append(r)
    cat = clean((re.search(r"Categor(?:y|ies):?\s*</h4>(.*?)</div>", page, re.S) or [None, ""])[1])[:80]
    title_full = clean(raw)
    return sid, {"title_full": title_full, "he_line": he[:160], "translit": tr[:160], "refs": refs[:4], "cat": cat}
if todo:
    with ThreadPoolExecutor(max_workers=5) as ex:
        for n, (sid, d) in enumerate(ex.map(fetch, todo)):
            if d: cache[sid] = d
            if (n + 1) % 100 == 0:
                json.dump(cache, open(CACHE, "w"), ensure_ascii=False); print(f"  {n+1}/{len(todo)}", file=sys.stderr)
    json.dump(cache, open(CACHE, "w"), ensure_ascii=False)
print(f"fetched: {len(cache)}", file=sys.stderr)
# ---- fallback: match the Hebrew opening line against the Tanakh text ----
NIK = re.compile(r"[֑-ׇ]")
def tanakh_key(t):
    t = NIK.sub("", _strip_zw(t or "")).replace("־", " ").replace("׀", " ")
    t = t.replace("יְיָ", "יהוה").replace("ה'", "יהוה").replace("ה\u05f3", "יהוה").replace("יי", "יהוה")
    t = t.replace("אלוקים", "אלהים").replace("אלוקינו", "אלהינו").replace("אלוקי", "אלהי")
    return re.sub(r"\s+", " ", re.sub(r"[^א-ת ]+", " ", t)).strip()
TEXT = ROOT / ".work/text"
verses = []
if TEXT.exists():
    for f in TEXT.glob("*.json"):
        book, ch = f.stem.rsplit(".", 1)
        try: txt = json.load(open(f))["versions"][0]["text"]
        except Exception: continue
        for i, v in enumerate(txt): verses.append((f"{book} {ch}:{i+1}", " " + tanakh_key(v) + " "))
    print(f"verse index: {len(verses)}", file=sys.stderr)
SID = ROOT / ".work/siddurtext"
sidx = []
if SID.exists():
    for f in SID.glob("*.json"):
        try:
            d = json.load(open(f)); t = d["versions"][0]["text"]
        except Exception: continue
        flat = t if isinstance(t, list) else [t]
        while any(isinstance(x, list) for x in flat): flat = [y for x in flat for y in (x if isinstance(x, list) else [x])]
        sidx.append((d["ref"], " " + tanakh_key(" ".join(str(x) for x in flat)) + " "))
    print(f"siddur index: {len(sidx)}", file=sys.stderr)
def match_line(line):
    k = tanakh_key(line); w = k.split()
    for n in (7, 6, 5, 4):
        if len(w) < n: continue
        p = " " + " ".join(w[:n]) + " "
        hits = [r for r, t in verses if p in t]
        if 1 <= len(hits) <= 3:
            hits.sort(key=lambda r: (0 if r.startswith("Psalms") else 1, r))
            return hits[:2]
    for n in (7, 6, 5):
        if len(w) < n: continue
        p = " " + " ".join(w[:n]) + " "
        hits = [r for r, t in sidx if p in t]
        if 1 <= len(hits) <= 4: return hits[:2]
    return []

# ---- merge ----
data = json.load(open(SONGS, encoding="utf-8")); songs = data["songs"]
norm = lambda s: re.sub(r"[^a-z]", "", (s or "").lower())
hnorm = lambda s: re.sub(r"[^א-ת]", "", s or "")
have_t = {norm(s["title"]) for s in songs}
have_h = {hnorm(s.get("title_he")) for s in songs if s.get("title_he")}
added = enriched = 0
matched = 0
for sid, d in cache.items():
    if not d: continue
    if not d["refs"] and verses and d.get("he_line"):
        d["refs"] = match_line(d["he_line"])
        if d["refs"]: matched += 1
    if not d["refs"]: continue
    tf = d["title_full"]
    en = clean(re.sub(r"[֐-׿\"'׳״\s]+$", "", tf)).strip()
    he = " ".join(re.findall(r"[֐-׿\"'׳״()\-]+", tf))[:60].strip()
    if not en: en = he
    key, hkey = norm(en), hnorm(he)
    ex = next((s for s in songs if norm(s["title"]) == key or (hkey and hnorm(s.get("title_he")) == hkey)), None)
    if ex:
        new = [r for r in d["refs"] if r not in ex["refs"]]
        if new: ex["refs"] += new; enriched += 1
        continue
    songs.append({"id": "zd-" + re.sub(r"[^a-z0-9]+", "-", en.lower()).strip("-")[:40] + "-" + sid,
                  "title": en[:70], "title_he": he or None, "performer": "Traditional", "year": None,
                  "type": "liturgical", "refs": d["refs"], "words": d["he_line"] or None,
                  "note": "Zemirot Database" + (f" · {d['cat']}" if d["cat"] else ""), "youtube": None})
    added += 1
data["meta"]["count"] = len(songs)
print(f"added {added}; enriched {enriched}; refs found by text match {matched}; catalogue {len(songs)}", file=sys.stderr)
if not DRY: json.dump(data, open(SONGS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
