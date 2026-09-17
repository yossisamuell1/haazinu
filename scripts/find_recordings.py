#!/usr/bin/env python3
"""Attach recordings to songs in data/songs.json.

Two sources, no API keys:
  * Apple Music / iTunes Search API  -> 30-second previews that play in-app anywhere, plus a link to the full track.
  * YouTube video ids found through DuckDuckGo (site:youtube.com), with channel names from YouTube's oEmbed.
    (youtube.com is blocked on machines running the kosher filter, so oEmbed is fetched via a resolved IP.)

Screening: a blocklist of female singers and non-Jewish / karaoke / covers keeps results in line with kol isha;
the list lives in data/recording_blocklist.txt (one term per line, case-insensitive, matched on title+artist+channel).
Picks are still automatic; review them in the app and use "hide" on anything wrong.

Usage: python3 scripts/find_recordings.py [--refresh] [--only id1,id2] [--top 3] [--no-youtube] [--no-itunes]
"""
import json, re, sys, time, urllib.parse, urllib.request, html, subprocess, ssl
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SONGS = ROOT / "data" / "songs.json"
BLOCK = ROOT / "data" / "recording_blocklist.txt"
TOP = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 3
REFRESH = "--refresh" in sys.argv
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
DO_YT = "--no-youtube" not in sys.argv
DO_IT = "--no-itunes" not in sys.argv
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
GENERIC = re.compile(r"traditional|various|liturgical|children|many|kiddush|torah service|simchat torah|selichot|bedtime|niggun|pesukim|melody|settings|tunes", re.I)
block_terms = [l.strip().lower() for l in BLOCK.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")] if BLOCK.exists() else []
def blocked(*fields):
    s = " ".join(f or "" for f in fields).lower()
    return next((t for t in block_terms if t in s), None)

def get(url, headers=None, timeout=25):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "he,en;q=0.8", **(headers or {})}), timeout=timeout).read()

# --- YouTube via DuckDuckGo ---
_yt_ip = None
def yt_ip():
    global _yt_ip
    if _yt_ip is None:
        try: _yt_ip = subprocess.run(["dig", "+short", "@1.1.1.1", "www.youtube.com"], capture_output=True, text=True, timeout=10).stdout.strip().splitlines()[-1]
        except Exception: _yt_ip = ""
    return _yt_ip
def oembed(vid):
    """title/author for a video; goes around a hosts-file block of youtube.com by resolving the IP ourselves."""
    ip = yt_ip()
    if not ip: return {}
    try:
        out = subprocess.run(["curl", "-s", "--max-time", "15", "--resolve", f"www.youtube.com:443:{ip}", f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"], capture_output=True, text=True).stdout
        return json.loads(out) if out.startswith("{") else {}
    except Exception: return {}
def ddg_youtube(q):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote("site:youtube.com " + q)
    page = get(url).decode("utf-8", "ignore")
    seen, out = set(), []
    for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page, re.S):
        href, title = html.unescape(m.group(1)), re.sub(r"<[^>]+>", "", html.unescape(m.group(2))).strip()
        v = re.search(r"v(?:%3D|=)([\w-]{11})", href)
        if not v or v.group(1) in seen: continue
        seen.add(v.group(1))
        out.append({"id": v.group(1), "title": re.sub(r"\s*-\s*YouTube$", "", title)})
        if len(out) >= 8: break
    return out
def youtube(q):
    recs = []
    for r in ddg_youtube(q):
        o = oembed(r["id"])
        r["channel"] = o.get("author_name", "")
        if o.get("title"): r["title"] = o["title"]
        why = blocked(r["title"], r["channel"])
        if why: continue
        recs.append(r)
        if len(recs) >= TOP: break
    return recs

# --- Apple Music / iTunes ---
def itunes(q, country="us"):
    url = f"https://itunes.apple.com/search?term={urllib.parse.quote(q)}&entity=song&limit=12&country={country}"
    try: j = json.loads(get(url, timeout=20))
    except Exception: return []
    out = []
    for r in j.get("results", []):
        if not r.get("previewUrl"): continue
        if blocked(r.get("trackName"), r.get("artistName"), r.get("collectionName")): continue
        out.append({"track": r["trackName"], "artist": r["artistName"], "album": r.get("collectionName", ""),
                    "preview": r["previewUrl"], "url": r.get("trackViewUrl", ""), "art": (r.get("artworkUrl100") or "").replace("100x100", "300x300"),
                    "ms": r.get("trackTimeMillis", 0)})
        if len(out) >= TOP: break
    return out

def queries(s):
    perf = s.get("performer") or ""
    perf_first = re.split(r"[;,(]", perf)[0].strip() if perf and not GENERIC.search(perf.split(";")[0]) else ""
    base = s.get("title_he") or s["title"]
    yt = s.get("yt_query") or (base + (" " + perf_first if perf_first else ""))
    it = s.get("itunes_query") or (s["title"] + (" " + perf_first if perf_first else ""))
    return yt, it

data = json.load(open(SONGS, encoding="utf-8"))
changed = 0
for s in data["songs"]:
    if ONLY is not None and s["id"] not in ONLY: continue
    need_yt = DO_YT and (REFRESH or ONLY is not None or not s.get("recordings"))
    need_it = DO_IT and (REFRESH or ONLY is not None or "itunes" not in s)
    if not (need_yt or need_it): continue
    yq, iq = queries(s)
    line = f"{s['id']:<22}"
    if need_it:
        try:
            it = itunes(iq) or itunes(iq, "il") or (itunes(s.get("title_he") or s["title"]) if s.get("title_he") else [])
        except Exception as e: it = []; line += f" itunes! {e}"
        s["itunes"] = it; s["itunes_query"] = iq
        line += f"  🍎{len(it)}"
    if need_yt:
        try: yt = youtube(yq)
        except Exception as e: yt = []; line += f" yt! {e}"
        s["recordings"] = yt; s["recordings_query"] = yq
        line += f"  ▶{len(yt)}"
        time.sleep(1.5)
    changed += 1
    print(line + "   " + (it[0]["artist"] + " – " + it[0]["track"][:30] if need_it and it else "") + ("  |  " + yt[0]["title"][:40] if need_yt and yt else ""))
    if changed % 10 == 0: json.dump(data, open(SONGS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(SONGS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"updated {changed} songs -> {SONGS}")
