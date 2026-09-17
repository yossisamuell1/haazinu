#!/usr/bin/env python3
"""Grow the catalogue from Apple Music: pull the track lists of male Jewish artists (iTunes Search API, no key),
match Hebrew track titles as phrases against the Hebrew Tanakh and siddur texts (downloaded to .work/), and add
each match as a song with that track as its preview. English/transliterated titles are matched against existing
catalogue titles by a loose transliteration skeleton and attached as extra recordings.

Usage: python3 scripts/mine_itunes.py [--dry] [--artists "Name,Name"]
Inputs: .work/text/<Book>.<ch>.json, .work/siddurtext/<ref>.json, data/songs.json, data/recording_blocklist.txt
"""
import json, re, sys, os, time, urllib.request, urllib.parse, unicodedata
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / ".work"
SONGS = ROOT / "data" / "songs.json"
DRY = "--dry" in sys.argv
BOOKS = ["Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","I Samuel","II Samuel","I Kings","II Kings","Isaiah","Jeremiah","Ezekiel","Hosea","Joel","Amos","Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah","Malachi","Psalms","Proverbs","Job","Song of Songs","Ruth","Lamentations","Ecclesiastes","Esther","Daniel","Ezra","Nehemiah","I Chronicles","II Chronicles"]
ARTISTS_IL = ["אברהם פריד","מאיר גרין","יונתן רזאל ואהרן רזאל","הרב שלמה קרליבך","אבי פיאמנטה","ידידים","פרחי ירושלים","מקהלת מלכות","מקהלת ידידים","שירה חדשה","רגש","נעימה","יוסי גרין","מונה רוזנבלום","אלי גרשטנהבר","בערי ובר","שמחה ליינר","מרדכי בן דוד ווברשטאק","אהרון רזאל","עמיחי","יאיר לוי","שולם לעמער","פנחס ביכלר","יעקב שוואקי","דוד ד'אור","עמית משולם","בן ציון שנקר","אריה קונצביץ","מנדי ורדיגר","ישראל אדלר","נחמן שלמה","דודי קאליש","ר' מיכאל שטרייכר","יוסי אזולאי","עוזיה צדוק","חיים דוד","אהרן לנדאו","מוטי ווייס","יוסף מוסקוביץ","ניגון","חסידי","ברסלב","קרליבך","פיוטים","בקשות","ישי ריבו","יונתן רזאל","אהרן רזאל","עמיר בניון","אביתר בנאי","אהוד בנאי","שולי רנד","חנן בן ארי","עקיבא","נפתלי קמפה","ישי לפידות","אודי דוידי","יוסף קרדונר","שלמה כץ","איתן כץ","אריאל זילבר","אברהם פריד","מרדכי בן דוד","יעקב שוואקי","בני פרידמן","מוטי שטיינמץ","שמואלי אונגר","ליפא שמלצר","גד אלבז","חיים ישראל","יצחק מאיר","אהרל'ה סאמט","שלמה קרליבך","מנחם הרמן","אביהו מדינה","יהורם גאון","עידן רייכל","ניגוני חב\"ד","יונתן שינפלד","אברהם טל","נריה","יובל טייב","דודו פישר","זושא","בן סנוף","אלי הרצליך","מוטי וייס","יואלי גרינפלד","אהרן רזאל ויונתן רזאל","עמירן דביר","דודי קאליש","שמעון בוסקילה","נתנאל ישראל","סימן טוב","ר' שלמה קרליבך"]
ARTISTS_US = ["Baruch Chait","Country Yossi","The Rabbis Sons","Journeys","Mendy Wald","Yitzchak Fuchs","Sheya Mendlowitz","MBD","Yisroel Lamm","Neginah","Israel Portnoy","Eitan Freilich","Yoni Z","Benny Amar","Zemiros Choir","Yeshiva Boys Choir","Kinderlach","Tzlil Vezemer","Avremi Roth","Yitzy Waldner","Yossi Green","Yaakov Yosef","Sruli Broncher","Chaim Blumenfeld","Shmuel Brazil","Regesh Choir","Nachas","Yedidim Choir","Malchus Choir","Shira Choir","Zemer Orchestra","Ari Boiangiu","Isaac Honig","Ben Zion Shenker","Yossele Rosenblatt","Moshe Koussevitzky","David Werdyger","Chazzan","Cantor","Modzitz","Bobov","Skulen","Vizhnitz","Belz","Ger Nigunim","Breslov","Carlebach Minyan","The Chevra","Ohr Chadash","Simply Tsfat","Aish","Maccabeats","Six13","Yeshiva University","Shlock Rock","Blue Fringe","Pey Dalid","Yonatan Shainfeld","Aryeh Kunstler","Eli Schwebel","Levy Falkowitz","Motty Ilowitz","Yisroel Adler","Zanvil Weinberger","Shmueli Ungar","Hershy Weinberger","Dovid Pearlman","Avrumi Berko","Yoely Klein","Yanky Briskman","Naftali Schnitzler","Hershy Rottenberg","Duvid Stern","Mendy Hershkowitz","Yossi Muller","Avremel Roth","Shlomo Carlebach","Mordechai Ben David","Avraham Fried","Yaakov Shwekey","Benny Friedman","Ishay Ribo","Yonatan Razel","Eitan Katz","Shlomo Katz","Yosef Karduner","Zusha","8th Day","Miami Boys Choir","Shalsheles","Lev Tahor","Dedi","Abie Rotenberg","Yehuda Green","Chaim Dovid","Baruch Levine","Simcha Leiner","Beri Weber","Mordechai Shapiro","Ari Goldwag","Yehuda Solomon","Diaspora Yeshiva Band","Yaakov Lemmer","Yisroel Werdyger","Uncle Moishy","Yeedle","Ohad Moskowitz","Avraham Rosenblum","Joey Newcomb","Nochi Krohn","Michoel Pruzansky","Lipa Schmeltzer","Reva L'Sheva","Moshav Band","Soulfarm","Piamenta","Shmueli Ungar","Motty Steinmetz","Yehuda!","Chaim Dovid Saracik","Nichoach","Chabad Nigunim","Yoel Sharabi","Yisroel Williger","Sruly Williger","Dovid Gabay","Yehuda Glantz","Kol Achai","Shwekey","Menachem Herman","Neginah Orchestra","London School of Jewish Song","Toronto Pirchei","Pirchei","Amudai Shaish","Tzlil V'Zemer","Yerachmiel Begun","Regesh","Suki & Ding","Naftali Kempeh","Shloime Daskal","Levy Falkowitz","Shloime Gertner","Meilech Kohn","Shulem Lemmer","Ari Hill","Eli Marcus","Gershon Veroba","Mendy Jerufi","Shmuel Perednik","Eli Beer","Mendy Worch"]
BLOCK = [l.strip().lower() for l in (ROOT / "data" / "recording_blocklist.txt").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
blocked = lambda *f: any(t in " ".join(x or "" for x in f).lower() for t in BLOCK)

# ---- Hebrew normalisation ----
NIKKUD = re.compile(r"[֑-ׇ]")
def hnorm(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = NIKKUD.sub("", s)
    s = s.replace("־", " ").replace("׀", " ").replace("{פ}", " ").replace("{ס}", " ")
    s = s.replace("יְיָ", "יהוה").replace("ה'", "יהוה").replace("ה׳", "יהוה").replace("השם", "יהוה").replace("יי", "יהוה")
    s = s.replace("אלוקים", "אלהים").replace("אלוקינו", "אלהינו").replace("אלוקי", "אלהי").replace("אלוקיך", "אלהיך").replace("קל ", "אל ")
    s = re.sub(r"[^א-ת ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()
def clean_title(t):
    t = re.sub(r"\((.*?)\)|\[(.*?)\]", " ", t)  # drop (Live), (feat. …)
    t = re.sub(r"(?i)\b(live|remix|acoustic|version|feat\.?|ft\.?|single|bonus track|instrumental|karaoke|cover|edit|radio|official|remastered|new)\b.*$", " ", t)
    t = re.split(r"[-–|/:]", t)[0]
    return t.strip()

# ---- corpus: verse index (normalised) ----
verses = []  # (ref, norm)
for b in BOOKS:
    for f in sorted((WORK / "text").glob(f"{b}.*.json"), key=lambda p: int(p.stem.rsplit(".", 1)[1])):
        c = int(f.stem.rsplit(".", 1)[1])
        try: txt = json.load(open(f))["versions"][0]["text"]
        except Exception: continue
        for i, v in enumerate(txt): verses.append((f"{b} {c}:{i+1}", " " + hnorm(v) + " "))
print("verses indexed:", len(verses), file=sys.stderr)
sid = []  # (ref, norm)
for f in (WORK / "siddurtext").glob("*.json"):
    try:
        d = json.load(open(f)); v = d["versions"][0]["text"]
        flat = v if isinstance(v, list) else [v]
        while any(isinstance(x, list) for x in flat): flat = [y for x in flat for y in (x if isinstance(x, list) else [x])]
        sid.append((d["ref"], " " + hnorm(" ".join(flat)) + " "))
    except Exception: pass
print("siddur passages indexed:", len(sid), file=sys.stderr)
BOOK_ORDER = {b: i for i, b in enumerate(BOOKS)}
def find_refs(phrase):
    """Verse refs for a title phrase. 3+ words: anywhere in a verse. 2 words: only as the opening of a verse
    (song titles are usually verse openings) and only if it opens at most 3 verses. Siddur: 3+ words only."""
    p = " " + phrase + " "
    words = phrase.split()
    if len(words) < 2 or len(phrase.replace(" ", "")) < 6: return [], []
    if len(words) >= 3: hits = [r for r, n in verses if p in n]
    else: hits = [r for r, n in verses if n.startswith(p)]; hits = hits if len(hits) <= 3 else []
    if hits:
        hits.sort(key=lambda r: (0 if r.startswith("Psalms") else 1, BOOK_ORDER[r.rsplit(" ", 1)[0]]))
        return hits[:3], []
    if len(words) >= 3:
        sh = [r for r, n in sid if p in n]
        return [], sh[:2]
    return [], []

# ---- transliteration skeleton for English titles ----
def skel(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z]", "", s)
    s = s.replace("ph", "f").replace("kh", "ch").replace("ck", "k").replace("q", "k").replace("tz", "ts").replace("tch", "ch").replace("sh", "s").replace("th", "t").replace("w", "v")
    s = re.sub(r"[aeiouy]+", "a", s)
    s = re.sub(r"(.)\1+", r"\1", s)
    return s

# ---- catalogue ----
data = json.load(open(SONGS, encoding="utf-8"))
songs = data["songs"]
by_he = {}
for s in songs:
    if s.get("title_he"): by_he.setdefault(hnorm(s["title_he"]), []).append(s)
by_skel = {}
for s in songs:
    k = skel(s["title"]);
    if len(k) >= 5: by_skel.setdefault(k, []).append(s)
    if s.get("words"): by_skel.setdefault(skel(s["words"]), [])

# ---- iTunes ----
def itunes_artist(name, country):
    url = f"https://itunes.apple.com/search?term={urllib.parse.quote(name)}&entity=song&attribute=artistTerm&limit=200&country={country}"
    for a in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=40)).get("results", [])
        except Exception: time.sleep(3)
    return []
artists = sys.argv[sys.argv.index("--artists") + 1].split(",") if "--artists" in sys.argv else None
tracks = {}
for country, names in (("il", ARTISTS_IL), ("us", ARTISTS_US)):
    for a in names:
        if artists and a not in artists: continue
        rs = itunes_artist(a, country)
        for r in rs:
            if not r.get("previewUrl") or r.get("kind") != "song": continue
            if a.lower() not in (r.get("artistName") or "").lower(): continue
            if blocked(r.get("trackName"), r.get("artistName"), r.get("collectionName")): continue
            tracks[r["trackId"]] = r
        print(f"{a:<28} {len(rs):4d} tracks  (total {len(tracks)})", file=sys.stderr)
        time.sleep(0.4)

added, attached, seen_new = 0, 0, {}
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")
def rec(r): return {"track": r["trackName"], "artist": r["artistName"], "album": r.get("collectionName", ""), "preview": r["previewUrl"], "url": r.get("trackViewUrl", ""), "art": (r.get("artworkUrl100") or "").replace("100x100", "300x300"), "ms": r.get("trackTimeMillis", 0)}
def attach(s, r):
    global attached
    s.setdefault("itunes", [])
    if any(x.get("preview") == r["previewUrl"] or (x.get("track") == r["trackName"] and x.get("artist") == r["artistName"]) for x in s["itunes"]): return
    if len(s["itunes"]) >= 6: return
    s["itunes"].append(rec(r)); attached += 1
for r in tracks.values():
    title = clean_title(r["trackName"])
    if re.search(r"[א-ת]", title):
        h = hnorm(title)
        if not h: continue
        if h in by_he: [attach(s, r) for s in by_he[h]]; continue
        if h in seen_new: attach(seen_new[h], r); continue
        trefs, srefs = find_refs(h)
        refs = trefs or srefs
        if not refs: continue
        # an existing song on the same ref with the same opening words?
        dup = next((s for s in songs if any(x in s["refs"] for x in refs) and hnorm(s.get("words", "")).startswith(h)), None)
        if dup: attach(dup, r); by_he[h] = [dup]; continue
        s = {"id": f"am-{slug(title) or str(r['trackId'])}", "title": title, "title_he": title, "performer": r["artistName"], "year": (r.get("releaseDate") or "")[:4] or None,
             "type": "verbatim" if trefs else "liturgical", "refs": refs, "words": title, "note": "Found on Apple Music; verse matched by phrase.", "youtube": None, "itunes": [rec(r)], "auto": True}
        if s["id"] in {x["id"] for x in songs}: s["id"] += f"-{r['trackId']}"
        songs.append(s); seen_new[h] = s; added += 1
    else:
        k = skel(title)
        if len(k) >= 5 and k in by_skel and by_skel[k]: [attach(s, r) for s in by_skel[k]]
data["meta"]["count"] = len(songs)
print(f"tracks scanned {len(tracks)}; new songs {added}; recordings attached {attached}; catalogue {len(songs)}", file=sys.stderr)
if not DRY: json.dump(data, open(SONGS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
else: json.dump([{"title": s["title"], "artist": s["performer"], "refs": s["refs"], "type": s["type"]} for s in songs if s.get("auto")], open(WORK / "mine_preview.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
