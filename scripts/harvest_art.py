#!/usr/bin/env python3
"""Harvest public-domain Tanakh artwork from Wikimedia Commons into .work/art/art_raw.json.

Walks a list of Bible-illustration categories, fetches each file's metadata once (cached), and reads a verse
reference out of the filename or the Commons description. Handles the formats these collections actually use:
  "Genesis cap 1 v 16"  "(Genesis 19 30)"  "Genesis 1:3"  "Gen. 1,3"  "1 Samuel 17 49"  "1. Mose 3,7"  "Psalm 23"
Only Tanakh books are accepted, so New Testament plates drop out on their own. Non-free licences and
nudity-suggesting titles are rejected here; every surviving image is then screened by scripts/screen_art.py.

Usage: python3 scripts/harvest_art.py [--cats "Category:A,Category:B"] [--refresh]
"""
import json, re, sys, time, urllib.request, urllib.parse, html
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / ".work/art"; ART.mkdir(parents=True, exist_ok=True)
CACHE = ART / "meta_cache.json"
OUT = ART / "art_raw.json"
UA = {"User-Agent": "Haazinu/1.0 (personal Torah app; verse-indexed artwork)"}
REFRESH = "--refresh" in sys.argv

CATS = [
    "Category:The Phillip Medhurst Picture Torah", "Category:The Phillip Medhurst Collection",
    "Category:Old Testament by James Tissot", "Category:Doré's English Bible",
    "Category:Die Bibel in Bildern by Julius Schnorr von Carolsfeld", "Category:Dalziels' Bible Gallery",
    "Category:Old Testament engravings in the Rijksmuseum Amsterdam", "Category:Old Testament woodcuts in the Rijksmuseum Amsterdam",
    "Category:Old Testament prints in the Metropolitan Museum of Art", "Category:Old Testament engravings in the Metropolitan Museum of Art",
    "Category:Bible Pictures with brief descriptions by Charles Foster", "Category:Holman Bible (1890 ed.)",
    "Category:The Bible and Its Story Taught by One Thousand Picture Lessons", "Category:The story of the Bible from Genesis to Revelation",
    "Category:Biblia ectypa (1695)", "Category:Bible de Mortier", "Category:Mortierbijbel",
    "Category:De schriftuurlyke geschiedenissen en gelykenissen van het Oude en Nieuwe Verbond",
    "Category:Prentbijbel met voorstellingen uit het Oude Testament, Deel 1", "Category:Prentbijbel met voorstellingen uit het Oude Testament, Deel 2",
    "Category:Religious themes by Ephraim Moshe Lilien", "Category:Illustrations by Ephraim Moses Lilien",
    "Category:Arthur Szyk", "Category:Maciejowski Bible", "Category:Bible primer, Old Testament, for use in the primary department of Sunday schools (1919)",
    "Category:The art Bible, comprising the Old and new Testaments - with numerous illustrations (1896)",
    "Category:Bowyer Bible", "Category:Old Testament illustrations", "Category:Bible illustrations",
    "Category:Kennicott Bible", "Category:Golden Haggadah", "Category:Sister Haggadah", "Category:Sarajevo Haggadah",
    "Category:Nuremberg Chronicle Old Testament", "Category:Liber Chronicarum, Old Testament",
    "Category:Old Testament paintings", "Category:Paintings of the Old Testament",
    "Category:Bible moralisée", "Category:Figures de la Bible", "Category:Icones Biblicae",
]
if "--cats" in sys.argv: CATS = sys.argv[sys.argv.index("--cats") + 1].split(",")

def api(params):
    body = urllib.parse.urlencode({**params, "format": "json"}).encode()
    for a in range(6):
        try:
            time.sleep(0.15)
            return json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php", data=body, headers=UA), timeout=90))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(8 * (a + 1)); continue
            if e.code in (414, 400): return {}
            raise
        except Exception: time.sleep(3)
    return {}

NT = re.compile(r"new testament|matthew|mark\b|luke|john\b|acts|romans|corinth|galat|ephes|philipp|coloss|thessal|timothy|titus|philemon|hebrews|james\b|peter\b|jude\b|revelation|apocalyp|jesus|christ|gospel|nativity|crucifix|apostle|virgin mary|madonna", re.I)
def members(cat, depth=0, seen=None):
    seen = seen if seen is not None else set()
    out = []; cont = {}
    while True:
        j = api({"action": "query", "list": "categorymembers", "cmtitle": cat, "cmlimit": "500", **cont})
        for m in j.get("query", {}).get("categorymembers", []):
            if m["ns"] == 6: out.append(m["title"])
            elif m["ns"] == 14 and depth < 2 and m["title"] not in seen and not NT.search(m["title"]):
                seen.add(m["title"]); out += members(m["title"], depth + 1, seen)
        if "continue" in j: cont = j["continue"]
        else: break
    return out

# ---------------- verse reference parsing ----------------
BOOK_ALIASES = {
    "Genesis": ["genesis", "gen", "gn", "1 mose", "1. mose", "i mose", "erste buch mose", "genese", "bereshit", "bereshith"],
    "Exodus": ["exodus", "exod", "exo", "ex", "2 mose", "2. mose", "ii mose", "shemot"],
    "Leviticus": ["leviticus", "levit", "lev", "lv", "3 mose", "3. mose", "iii mose", "vayikra"],
    "Numbers": ["numbers", "numeri", "num", "nm", "4 mose", "4. mose", "iv mose", "bamidbar"],
    "Deuteronomy": ["deuteronomy", "deuteronomium", "deut", "dtn", "dt", "5 mose", "5. mose", "v mose", "devarim"],
    "Joshua": ["joshua", "josua", "jozua", "josh", "jos"], "Judges": ["judges", "richter", "rechters", "judg", "jdg", "juges", "iudicum"],
    "Ruth": ["ruth", "rut"], "I Samuel": ["1 samuel", "1. samuel", "i samuel", "1 sam", "1sam", "1 sm", "erste samuel"],
    "II Samuel": ["2 samuel", "2. samuel", "ii samuel", "2 sam", "2sam", "2 sm"],
    "I Kings": ["1 kings", "1. kings", "i kings", "1 kön", "1 koningen", "1 kgs", "1 reg", "1 könige"],
    "II Kings": ["2 kings", "2. kings", "ii kings", "2 kön", "2 koningen", "2 kgs", "2 reg", "2 könige"],
    "I Chronicles": ["1 chronicles", "i chronicles", "1 chron", "1 chr"], "II Chronicles": ["2 chronicles", "ii chronicles", "2 chron", "2 chr"],
    "Ezra": ["ezra", "esra"], "Nehemiah": ["nehemiah", "nehemia", "neh"], "Esther": ["esther", "ester", "est"],
    "Job": ["job", "hiob", "iob"], "Psalms": ["psalms", "psalm", "psalmen", "psaume", "ps", "tehillim"],
    "Proverbs": ["proverbs", "sprüche", "spreuken", "prov", "proverbia", "mishlei"],
    "Ecclesiastes": ["ecclesiastes", "prediker", "kohelet", "qoheleth", "eccl"],
    "Song of Songs": ["song of songs", "song of solomon", "canticles", "hooglied", "hohelied", "shir hashirim", "cant"],
    "Isaiah": ["isaiah", "jesaja", "jesaia", "isaias", "isa", "yeshayahu"], "Jeremiah": ["jeremiah", "jeremia", "jeremias", "jer", "yirmiyahu"],
    "Lamentations": ["lamentations", "klagelieder", "klaagliederen", "eicha", "lam"], "Ezekiel": ["ezekiel", "hesekiel", "ezechiel", "ezek", "yechezkel"],
    "Daniel": ["daniel", "dan"], "Hosea": ["hosea", "hoshea", "osee"], "Joel": ["joel"], "Amos": ["amos"], "Obadiah": ["obadiah", "obadja", "abdias"],
    "Jonah": ["jonah", "jona", "jonas"], "Micah": ["micah", "micha", "michea"], "Nahum": ["nahum"], "Habakkuk": ["habakkuk", "habakuk"],
    "Zephaniah": ["zephaniah", "zephanja", "sophonias"], "Haggai": ["haggai", "hagai"], "Zechariah": ["zechariah", "sacharja", "zacharias", "zach"], "Malachi": ["malachi", "maleachi"],
}
ALIAS2BOOK = {a: b for b, al in BOOK_ALIASES.items() for a in al}
ALT = "|".join(sorted((re.escape(a) for a in ALIAS2BOOK), key=len, reverse=True))
# book  [cap] chap  [v|vv|,|:|.]  verse [-verse]
REF_RE = re.compile(rf"\b({ALT})\b[\s.]*(?:cap\.?|chapter|kap\.?|hoofdstuk)?[\s.]*(\d{{1,3}})\s*(?:vv?\.?|:|,|\s)\s*(\d{{1,3}})(?:\s*[-–]\s*(\d{{1,3}}))?", re.I)
CHAP_RE = re.compile(rf"\b({ALT})\b[\s.]*(?:cap\.?|chapter|kap\.?)?[\s.]*(\d{{1,3}})\b", re.I)
VERSES = json.load(open(ART / "verse_counts.json")) if (ART / "verse_counts.json").exists() else {}
def parse_ref(text, allow_chapter=False):
    if not text: return None
    t = html.unescape(re.sub(r"<[^>]+>", " ", text)).replace("’", "'")
    m = REF_RE.search(t)
    if m:
        book = ALIAS2BOOK[m.group(1).lower()]; c, v = int(m.group(2)), int(m.group(3)); v2 = m.group(4)
        if c < 1 or v < 1: return None
        if VERSES.get(book) and (c > len(VERSES[book]) or v > VERSES[book][c - 1]): return None
        return f"{book} {c}:{v}" + (f"-{v2}" if v2 and int(v2) > v else "")
    if allow_chapter:
        m = CHAP_RE.search(t)
        if m:
            book = ALIAS2BOOK[m.group(1).lower()]; c = int(m.group(2))
            if VERSES.get(book) and 1 <= c <= len(VERSES[book]): return f"{book} {c}:1"
    return None

SKIP = re.compile(r"\bnude|nudit|naked|naakt|nackt|\bnus\b|\bnue\b|bath(e|es|ing|s)?\b|baadt|\bbaden\b|bethsab|bathsheba|batseba|susanna|suzanne|zuzana|"
                  r"lot\b[^.]{0,20}\bdaughter|daughter[^.]{0,12}\blot\b|filles de lot|dochters van lot|drunk|dronken|ivresse|trunken|"
                  r"potiphar|putiphar|tamar|thamar|dinah|dina\b|adam and eve|adam en eva|adam und eva|adam et [\u00e9e]ve|\beve\b|\beva\b|paradise|paradijs|garden of eden|"
                  r"creation of (eve|woman)|harlot|prostitut|hoer\b|concubine|bijvrouw|\brape\b|verkracht|seduc|verleid|nakedness|shame of|uncover", re.I)
FREE = re.compile(r"public domain|^pd|cc0|cc[- ]by", re.I)

# ---------------- gather ----------------
files = {}
for cat in CATS:
    try: fs = members(cat)
    except Exception as e: print(f"!! {cat}: {e}", file=sys.stderr); continue
    for f in fs: files.setdefault(f, cat)
    print(f"{len(fs):6d}  {cat}", file=sys.stderr)
print(f"total distinct files: {len(files)}", file=sys.stderr)

cache = json.load(open(CACHE)) if CACHE.exists() and not REFRESH else {}
todo = [f for f in files if f not in cache and not f.lower().endswith((".pdf", ".djvu", ".ogv", ".webm", ".svg"))]
print(f"metadata to fetch: {len(todo)}", file=sys.stderr)
BATCH = 50
def fetch_batch(batch):
    j = api({"action": "query", "titles": "|".join(batch), "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": "500"})
    q = j.get("query", {}) if j else {}
    back = {n["to"]: n["from"] for n in q.get("normalized", [])}
    out = {}
    for p in q.get("pages", {}).values():
        title = back.get(p.get("title"), p.get("title"))
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        out[title] = {"thumb": ii.get("thumburl"), "image": ii.get("url"), "page": ii.get("descriptionurl"),
                      "desc": (em.get("ImageDescription", {}) or {}).get("value", "")[:1200],
                      "artist": (em.get("Artist", {}) or {}).get("value", "")[:200],
                      "date": (em.get("DateTimeOriginal", {}) or {}).get("value", "")[:60],
                      "lic": (em.get("LicenseShortName", {}) or {}).get("value", "")}
    for t in batch:
        if t not in out: out[t] = {}
    return out
batches = [todo[i:i + BATCH] for i in range(0, len(todo), BATCH)]
done = 0
with ThreadPoolExecutor(max_workers=4) as ex:
    for got in ex.map(fetch_batch, batches):
        cache.update(got); done += len(got)
        if done % 1000 < BATCH:
            json.dump(cache, open(CACHE, "w"), ensure_ascii=False); print(f"  meta {done}/{len(todo)}", file=sys.stderr)
json.dump(cache, open(CACHE, "w"), ensure_ascii=False)

# ---------------- build works ----------------
def clean_artist(a):
    a = html.unescape(re.sub(r"<[^>]+>", " ", a or "")); a = re.sub(r"\s+", " ", a).strip()
    a = re.sub(r"(?i)\b(unknown author|unknown|anonymous|see below|internet archive book images|creator:)\b", "", a).strip(" ,;")
    return a[:60]
MEDHURST = re.compile(r"(?i)^the phillip medhurst (?:picture torah|collection|picture bible)\s*[\d.]*\s*", re.I)
def split_medhurst(f):
    """'...Torah 1. The Almighty. Genesis cap 1 v 16. De Vos.jpg' -> (title, engraver)"""
    base = re.sub(r"\.\w{3,4}$", "", f.replace("File:", ""))
    if not MEDHURST.search(base): return None, None
    parts = [p.strip() for p in MEDHURST.sub("", base).split(".") if p.strip()]
    if len(parts) < 2: return None, None
    body = [p for p in parts if not CHAP_RE.search(p)]
    title = body[0] if body else parts[0]
    eng = body[-1] if len(body) > 1 else ""
    if eng.lower().startswith("after "): eng = eng[6:].strip()
    title = title.strip(" ,;-–")
    return title, (eng if 1 < len(eng) < 40 and not eng.lower().startswith(("cap", "v ")) else "")
def clean_title(t):
    t = re.sub(r"\.\w{3,4}$", "", t.replace("File:", ""))
    t = re.sub(r"(?i)^the phillip medhurst (picture torah|collection)\s*\d*\.?\s*", "", t)
    t = re.sub(r"(?i)\s*(RP-P-[\w.()-]+|MET \w+|\(IA [\w.-]+\)|btv\w+)\s*", " ", t)
    t = re.sub(r"(?i)\s*•\s*(invenit|pinxit|excudit|praesentat)[^•]*", " ", t)
    t = re.sub(r"(?i)\b(cap\.?|chapter)\s*\d+\s*vv?\.?\s*[\d-]+\.?", " ", t)
    t = re.sub(r"\([^)]*\d+[\s:,]\d+[^)]*\)", " ", t)
    t = re.sub(r"^[\d.\s]+", "", t); t = re.sub(r"\s+", " ", t).strip(" .,-–")
    return t[:90]
works, skipped = {}, {"nt": 0, "noref": 0, "modest": 0, "nonfree": 0, "nothumb": 0}
DORE = json.load(open(ART / "dore_map.json")) if (ART / "dore_map.json").exists() else {}
for f, cat in files.items():
    m = cache.get(f) or {}
    if not m.get("thumb"): skipped["nothumb"] += 1; continue
    if m.get("lic") and not FREE.search(m["lic"]): skipped["nonfree"] += 1; continue
    blob = f + " " + (m.get("desc") or "")
    if SKIP.search(blob): skipped["modest"] += 1; continue
    ref = parse_ref(f) or parse_ref(m.get("desc"), allow_chapter=False)
    if not ref:
        for frag, r in DORE.items():
            if frag.lower() in f.lower(): ref = r; break
    if not ref: ref = parse_ref(f, allow_chapter=True)
    if not ref:
        if NT.search(blob): skipped["nt"] += 1
        else: skipped["noref"] += 1
        continue
    mt, meng = split_medhurst(f)
    title = mt or clean_title(f) or ref
    artist = meng or clean_artist(m.get("artist"))
    if artist.lower().startswith("phillip medhurst") and meng: artist = meng
    key = (title.lower(), artist.lower(), ref)
    if key in works: continue
    works[key] = {"title": title, "artist": artist or "Unknown", "year": (lambda y: y if y and int(y) < 1960 else None)((re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", m.get("date") or "") or [None, None])[1] if re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", m.get("date") or "") else None),
                  "refs": [ref], "thumb": m["thumb"], "image": m["image"], "page": m["page"], "source": cat.replace("Category:", ""), "file": f}
items = list(works.values())
for n, w in enumerate(items): w["id"] = f"art-{n+1}"
json.dump({"meta": {"note": "Public-domain Tanakh artwork from Wikimedia Commons, keyed to the verse depicted.", "count": len(items)}, "works": items}, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
print(f"\nworks: {len(items)}  (skipped: {skipped})", file=sys.stderr)
import collections
print(collections.Counter(w["refs"][0].rsplit(" ", 1)[0] for w in items).most_common(20), file=sys.stderr)
print(collections.Counter(w["source"] for w in items).most_common(20), file=sys.stderr)
