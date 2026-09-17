#!/usr/bin/env python3
"""Attach YouTube recordings to songs in data/songs.json.

For every song without a "recordings" list, search YouTube (public results page, no API key)
for `yt_query` if present, else Hebrew title + performer, and store the top N results:
  {"id", "title", "channel", "length", "views"}
Nothing is downloaded or hosted; the app embeds the official YouTube player.

Usage: python3 scripts/find_youtube.py [--refresh] [--top 3] [--only id1,id2]
"""
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

SONGS = Path(__file__).resolve().parent.parent / "data" / "songs.json"
TOP = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 3
REFRESH = "--refresh" in sys.argv
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
GENERIC = re.compile(r"traditional|various|liturgical|children|many|kiddush|torah service|simchat torah|selichot|bedtime", re.I)
HDRS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
        "Accept-Language": "he-IL,he;q=0.9,en;q=0.8", "Cookie": "CONSENT=YES+1"}

def search(q):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)
    html = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=25).read().decode("utf-8", "ignore")
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m: return []
    out = []
    def walk(x):
        if isinstance(x, dict):
            if "videoRenderer" in x: yield x["videoRenderer"]
            for v in x.values(): yield from walk(v)
        elif isinstance(x, list):
            for v in x: yield from walk(v)
    for v in walk(json.loads(m.group(1))):
        try:
            out.append({"id": v["videoId"], "title": "".join(r["text"] for r in v["title"]["runs"]),
                        "channel": v.get("ownerText", {}).get("runs", [{}])[0].get("text", ""),
                        "length": v.get("lengthText", {}).get("simpleText", ""),
                        "views": v.get("viewCountText", {}).get("simpleText", "")})
        except (KeyError, IndexError): pass
        if len(out) >= 12: break
    # skip very long uploads (full concerts/albums) and anything under 40 s (shorts)
    def ok(r):
        parts = [int(p) for p in r["length"].split(":")] if r["length"] and r["length"].replace(":", "").isdigit() else None
        if not parts: return True
        secs = sum(p * 60 ** i for i, p in enumerate(reversed(parts)))
        return 40 <= secs <= 15 * 60
    BLOCK = re.compile(r"hillsong|worship|jesus|christ|ישוע|gospel|karaoke|קריוקי|ringtone|1 hour|שעה של", re.I)
    return [r for r in out if ok(r) and not BLOCK.search(r["title"] + " " + r["channel"])][:TOP]

def query_for(s):
    if s.get("yt_query"): return s["yt_query"]
    perf = s.get("performer") or ""
    q = s.get("title_he") or s["title"]
    if perf and not GENERIC.search(perf): q += " " + perf
    return q

data = json.load(open(SONGS, encoding="utf-8"))
changed = 0
for s in data["songs"]:
    if ONLY is not None and s["id"] not in ONLY: continue
    if s.get("recordings") and not REFRESH and ONLY is None: continue
    q = query_for(s)
    try:
        recs = search(q)
    except Exception as e:
        print(f"  ! {s['id']}: {e}"); continue
    s["recordings"] = recs
    s["recordings_query"] = q
    changed += 1
    print(f"{s['id']:<22} {q!r:<45} -> " + (" | ".join(f"{r['title'][:40]} ({r['channel'][:18]}, {r['length']})" for r in recs[:2]) or "nothing"))
    time.sleep(1.2)
json.dump(data, open(SONGS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"updated {changed} songs -> {SONGS}")
