#!/usr/bin/env python3
"""Build data/kriah.json: verse-level (and interpolated word-level) timings for Rabbi Michoel Slavin's
per-parsha Torah readings (Chabad.org, streamed from torahcdn.net via torahdownloads.org).

Method: ffmpeg silencedetect finds pauses in each parsha MP3; a dynamic-programming alignment picks one pause
per verse boundary so that verse durations stay proportional to verse length in letters. Word times inside a
verse are interpolated by letter count. Timings are approximate (typically within a second) and are flagged so.

Inputs:  .work/slavin_ids.txt  (torahdownloads id + parsha name), .work/slavin/<id>.mp3, .work/text/<Book>.<ch>.json
Output:  data/kriah.json = {"meta":..., "files":{parsha:{"url","id","reader"}}, "verses":{Book:{"c:v":[parsha,[t0,t1,...tN]]}}}
Usage:   python3 scripts/align_slavin.py [--only Bereshit,Noach] [--frac 0.22] [--min 0.18]
"""
import json, re, subprocess, sys, os, math
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / ".work"
OUT = ROOT / "data" / "kriah.json"
PAUSE_FRAC = float(sys.argv[sys.argv.index("--frac") + 1]) if "--frac" in sys.argv else 0.25
PAUSE_MIN = float(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 0.2
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FF = "ffmpeg"

parshiot = json.load(open(ROOT / "data" / "parshiot.json"))
ids = dict(line.split(" ", 1)[::-1] for line in (WORK / "slavin_ids.txt").read_text().strip().splitlines())  # name -> id
norm = lambda x: re.sub(r"[^a-z]", "", x.lower())
ids = {norm(k): v.strip() for k, v in ids.items()}
_txt = {}
def chapter(book, c):
    k = (book, c)
    if k not in _txt:
        d = json.load(open(WORK / "text" / f"{book}.{c}.json"))
        _txt[k] = d["versions"][0]["text"]
    return _txt[k]
LET = re.compile(r"[א-ת]")
def clean(v):
    v = re.sub(r"<[^>]+>", "", v).replace("{פ}", "").replace("{ס}", "")
    v = re.sub(r"\([^)]*\)", "", v)
    return v
def words_of(v):
    toks = []
    for tok in clean(v).split():
        if tok == "׀": continue
        toks += [p for p in tok.split("־") if p]
    return toks
def verse_list(p):
    """All (book, c, v, text) in reading order for a parsha."""
    out = []
    (c1, v1), (c2, v2) = [tuple(map(int, x.split(":"))) for x in (p["begin"], p["end"])]
    c = c1
    while c <= c2:
        txt = chapter(p["book"], c)
        vs = range(v1 if c == c1 else 1, (v2 if c == c2 else len(txt)) + 1)
        for v in vs: out.append((p["book"], c, v, txt[v - 1]))
        c += 1
    return out

def silences(mp3, frac=None):
    """Pauses from a relative energy envelope (robust to room noise): 20 ms RMS frames, a pause is a run of
    frames below PAUSE_FRAC x the 60th-percentile RMS lasting >= PAUSE_MIN s. Returns [(start,end)], total."""
    import struct, array
    r = subprocess.run([FF, "-nostats", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True)
    a = array.array("h"); a.frombytes(r.stdout[: len(r.stdout) // 2 * 2])
    sr, fl = 8000, 160  # 20 ms
    n = len(a) // fl
    rms = [0.0] * n
    for i in range(n):
        seg = a[i * fl:(i + 1) * fl]
        rms[i] = math.sqrt(sum(x * x for x in seg) / fl)
    # smooth over 3 frames
    sm = [(rms[max(0, i - 1)] + rms[i] + rms[min(n - 1, i + 1)]) / 3 for i in range(n)]
    ref = sorted(sm)[int(n * 0.6)]
    thr = ref * (frac or PAUSE_FRAC)
    sil = []; i = 0
    while i < n:
        if sm[i] < thr:
            j = i
            while j < n and sm[j] < thr: j += 1
            if (j - i) * fl / sr >= PAUSE_MIN: sil.append((i * fl / sr, j * fl / sr))
            i = j
        else: i += 1
    return sil, n * fl / sr

def align(verses, sil, total):
    """Choose boundaries: verse i ends inside silence b_i, monotone; minimise sum over verses of
    |actual - expected|/expected where expected duration ∝ letters. Candidates = pause midpoints."""
    n = len(verses)
    letters = [max(1, len(LET.findall(clean(v[3])))) for v in verses]
    # speech starts after the first long silence if the file opens with silence; end at last speech
    first = sil[0][1] if sil and sil[0][0] < 0.5 else 0.0
    for st, en in sil:
        if en < 25 and en - st >= 1.5: first = en
        if st > 25: break
    last = sil[-1][0] if sil and total - sil[-1][1] < 1.0 else total
    cands = [((s + e) / 2, e - s) for s, e in sil if (s + e) / 2 > first + 0.3 and (s + e) / 2 < last - 0.3]
    cands.append((last, 1.0))
    m = len(cands)
    rate = (last - first) / sum(letters)  # seconds per letter
    INF = float("inf")
    # dp[i][j] = best cost with verse i (0-based) ending at candidate j
    dp = [[INF] * m for _ in range(n)]
    bp = [[-1] * m for _ in range(n)]
    def cost(i, t0, t1, gap):
        exp = letters[i] * rate
        d = abs((t1 - t0) - exp) / exp
        return d * d - 0.15 * min(gap, 1.5)  # reward longer pauses (sof pasuk pauses are longer)
    for j in range(m):
        dp[0][j] = cost(0, first, cands[j][0], cands[j][1])
    for i in range(1, n):
        best_prev = []  # running best over j' < j
        bj, bv = -1, INF
        for j in range(m):
            if j > 0 and dp[i - 1][j - 1] < bv: bj, bv = j - 1, dp[i - 1][j - 1]
            # allow skipping many candidates: check a window of previous j' (full scan is O(m^2) per verse; use running min over all j'<j)
            # running min ignores the pairwise cost dependency, so do a bounded exact scan:
            best = INF; arg = -1
            lo = max(0, j - 400)
            for jp in range(lo, j):
                if dp[i - 1][jp] == INF: continue
                c = dp[i - 1][jp] + cost(i, cands[jp][0], cands[j][0], cands[j][1])
                if c < best: best, arg = c, jp
            dp[i][j], bp[i][j] = best, arg
    # last verse must end at the final candidate
    j = m - 1
    if dp[n - 1][j] == INF:  # fall back: best reachable
        j = min(range(m), key=lambda k: dp[n - 1][k])
        print("  ! could not reach the end of the file; alignment truncated")
    ends = [0] * n
    for i in range(n - 1, -1, -1):
        ends[i] = cands[j][0]; j = bp[i][j]
        if j < 0 and i > 0: break
    starts = [first] + ends[:-1]
    return starts, ends

out = {"meta": {"reader": "Rabbi Michoel Slavin", "source": "Chabad.org Torah Reading Recordings, streamed from torahcdn.net (torahdownloads.org)", "method": "silence-detect + proportional DP alignment; word times interpolated by letters", "approximate": True}, "files": {}, "verses": {}}
if OUT.exists() and ONLY:
    out = json.load(open(OUT))
for p in parshiot:
    name = p["id"]
    if ONLY and name not in ONLY: continue
    sid = ids.get(norm(name))
    mp3 = WORK / "slavin" / f"{sid}.mp3" if sid else None
    if not sid or not mp3.exists() or mp3.stat().st_size < 100000:
        print(f"{name:<14} no audio"); continue
    verses = verse_list(p)
    sil, total = silences(mp3)
    frac = PAUSE_FRAC
    while len(sil) < 3 * len(verses) and frac < 0.75:  # noisier files need a higher relative threshold
        frac += 0.1; sil, total = silences(mp3, frac)
    starts, ends = align(verses, sil, total)
    out["files"][name] = {"url": f"https://torahcdn.net/tdn/{sid}.mp3", "id": sid, "duration": round(total, 2)}
    for (book, c, v, txt), s, e in zip(verses, starts, ends):
        ws = words_of(txt)
        L = [max(1, len(LET.findall(w))) for w in ws]
        tot = sum(L); t = s; times = []
        for l in L:
            times.append(round(t, 3)); t += (e - s) * l / tot
        times.append(round(e, 3))
        out["verses"].setdefault(book, {})[f"{c}:{v}"] = [name, times]
    print(f"{name:<14} {len(verses):4d} verses  {len(sil):4d} pauses  {total/60:5.1f} min  avg {(ends[-1]-starts[0])/len(verses):4.1f}s/verse")
OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print("wrote", OUT, sum(len(v) for v in out["verses"].values()), "verses")
