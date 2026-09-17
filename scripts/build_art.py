#!/usr/bin/env python3
"""Build data/art.json: public-domain artworks keyed to verses, with thumbnails from Wikimedia Commons.
Sources: James Tissot's Old Testament series (Phillip Medhurst collection; verse refs are in the file titles) and
Gustave Doré's English Bible plates (mapped by title below). Immodest scenes and Apocrypha plates are skipped.
Usage: python3 scripts/build_art.py   (reads .work/art/commons_lists.json, calls the Commons API for thumbnails)"""
import json, re, time, urllib.request, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
LISTS = json.load(open(ROOT / ".work/art/commons_lists.json"))
OUT = ROOT / "data/art.json"
UA = {"User-Agent": "Haazinu/1.0 (personal Torah app)"}
def api(params):
    body = urllib.parse.urlencode({**params, "format": "json"}).encode()
    for a in range(6):
        try: time.sleep(0.7); return json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php", data=body, headers=UA), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(8 * (a + 1)); continue
            raise
    return {}
SKIP = re.compile(r"nus\b|nue\b|nudit|Adam et [ÉE]ve|\bEve\b|Ève|Bethsab|Bathsheba|Suzanne|Susanna|filles de Lot|Lot's daughters|ivresse|drunken|Putiphar|Potiphar|Thamar|Creation of Eve|Driven out of Eden|Dina\b|Dinah", re.I)
BOOKS = {"genesis": "Genesis", "exodus": "Exodus", "leviticus": "Leviticus", "numbers": "Numbers", "deuteronomy": "Deuteronomy", "joshua": "Joshua", "judges": "Judges", "ruth": "Ruth", "1 samuel": "I Samuel", "2 samuel": "II Samuel", "i samuel": "I Samuel", "ii samuel": "II Samuel", "1 kings": "I Kings", "2 kings": "II Kings", "i kings": "I Kings", "ii kings": "II Kings", "1 chronicles": "I Chronicles", "2 chronicles": "II Chronicles", "i chronicles": "I Chronicles", "ii chronicles": "II Chronicles", "isaiah": "Isaiah", "jeremiah": "Jeremiah", "lamentations": "Lamentations", "ezekiel": "Ezekiel", "daniel": "Daniel", "hosea": "Hosea", "joel": "Joel", "amos": "Amos", "obadiah": "Obadiah", "jonah": "Jonah", "micah": "Micah", "nahum": "Nahum", "habakkuk": "Habakkuk", "zephaniah": "Zephaniah", "haggai": "Haggai", "zechariah": "Zechariah", "malachi": "Malachi", "psalms": "Psalms", "proverbs": "Proverbs", "job": "Job", "song of songs": "Song of Songs", "ecclesiastes": "Ecclesiastes", "esther": "Esther", "ezra": "Ezra", "nehemiah": "Nehemiah"}
TISSOT_RE = re.compile(r"\(([1-2I]{0,2}\s?[A-Za-z ]+?) (\d+) (\d+)\)")
DORE = {  # title fragment -> ref (Doré's English Bible, Tanakh plates only)
 "Creation of Light": "Genesis 1:3", "Cain and Abel Offer": "Genesis 4:3-4", "Cain Slays Abel": "Genesis 4:8", "World Is Destroyed by Water": "Genesis 7:21", "The Great Flood": "Genesis 7:17", "Dove Is Sent Forth": "Genesis 8:8", "Noah Curses Ham": "Genesis 9:25", "Tower of Babel": "Genesis 11:4",
 "Abraham Goes to the Land": "Genesis 12:5", "Abraham and the Three Angels": "Genesis 18:2", "Lot Flees": "Genesis 19:24", "Abraham Sends Hagar": "Genesis 21:14", "Hagar and Ishmael in the Wilderness": "Genesis 21:16", "Testing of Abraham": "Genesis 22:10", "Burial of Sarah": "Genesis 23:19", "Eliezer and Rebekah": "Genesis 24:15", "Meeting of Isaac and Rebekah": "Genesis 24:64", "Isaac Blesses Jacob": "Genesis 27:27", "Jacob's Dream": "Genesis 28:12", "Jacob Tends Laban": "Genesis 29:10", "Jacob Prays for Protection": "Genesis 32:10", "Jacob Wrestles": "Genesis 32:25", "Jacob and Esau Meet": "Genesis 33:4", "Joseph Is Sold": "Genesis 37:28", "Joseph Interprets Pharaoh": "Genesis 41:25", "Joseph Reveals Himself": "Genesis 45:3", "Jacob Goes to Egypt": "Genesis 46:5",
 "Child Moses on the Nile": "Exodus 2:3", "Finding of Moses": "Exodus 2:5", "Moses and Aaron Appear": "Exodus 5:1", "Fifth Plague": "Exodus 9:6", "Ninth Plague": "Exodus 10:22", "Firstborn of the Egyptians": "Exodus 12:29", "Egyptians Ask Moses to Depart": "Exodus 12:33", "Egyptians Drown": "Exodus 14:28", "Giving of the Law": "Exodus 19:20", "Moses Comes Down": "Exodus 34:29", "Moses Strikes the Rock": "Exodus 17:6", "Moses Breaks the Tables": "Exodus 32:19",
 "Death of Korah": "Numbers 16:32", "Spies Return": "Numbers 13:26", "Bronze Serpent": "Numbers 21:9", "Angel Appears to Balaam": "Numbers 22:31",
 "Cross the Jordan": "Joshua 3:17", "Angel Appears to the Israelites": "Judges 2:1", "Walls of Jericho": "Joshua 6:20", "Joshua Spares Rahab": "Joshua 6:25", "Achan Is Stoned": "Joshua 7:25", "Joshua Burns the Town of Ai": "Joshua 8:28", "Army of the Amorites": "Joshua 10:11", "Sun to Stand Still": "Joshua 10:12",
 "Jael Kills Sisera": "Judges 4:21", "Deborah Praises Jael": "Judges 5:24", "Deborah's song": "Judges 5:1", "Lied der Debora": "Judges 5:1", "Gideon Chooses": "Judges 7:7", "Midianites Are Routed": "Judges 7:21", "Death of Gideon's Sons": "Judges 9:5", "Death of Abimelech": "Judges 9:53", "Jephthah's Daughter Comes": "Judges 11:34", "Mourn with Jephthah": "Judges 11:40", "Samson Slays a Lion": "Judges 14:6", "Ass' Jawbone": "Judges 15:15", "Gates of Gaza": "Judges 16:3", "Samson and Delilah": "Judges 16:19", "Death of Samson": "Judges 16:30", "Levite Finds": "Judges 19:27", "Levite Carries": "Judges 19:28", "Virgins of Jabesh": "Judges 21:12",
 "Naomi and Her Daughters": "Ruth 1:14", "Ruth and Boaz": "Ruth 2:8",
 "Ark Is Returned": "I Samuel 6:13", "Samuel Blesses Saul": "I Samuel 10:1", "Death of Agag": "I Samuel 15:33", "David Slays Goliath": "I Samuel 17:49", "Saul Attempts to Kill David": "I Samuel 19:10", "David Escapes through a Window": "I Samuel 19:12", "David and Jonathan": "I Samuel 20:41", "How He Spared His Life": "I Samuel 24:11", "Witch of Endor": "I Samuel 28:14", "Death of Saul": "I Samuel 31:4", "Recover the Bodies of Saul": "I Samuel 31:12",
 "Soldiers of Ish-bosheth": "II Samuel 2:16", "David Attacks the Ammonites": "II Samuel 12:29", "Death of Absalom": "II Samuel 18:14", "David Mourns": "II Samuel 19:1", "Rizpah": "II Samuel 21:10", "Abishai Saves": "II Samuel 21:17", "Plague of Jerusalem": "II Samuel 24:15",
 "Judgment of Solomon": "I Kings 3:25", "Cedars Are Cut Down": "I Kings 5:20", "Queen of Sheba": "I Kings 10:1", "Solomon in Old Age": "I Kings 11:4", "Disobedient Prophet": "I Kings 13:24", "Widow of Zarephath": "I Kings 17:22", "Prophets of Baal": "I Kings 18:40", "Elijah Is Nourished": "I Kings 19:5", "Slaughter the Syrians": "I Kings 20:20", "Death of Ahab": "I Kings 22:34",
 "Messengers of Ahaziah": "II Kings 1:10", "Chariot of Fire": "II Kings 2:11", "Destroyed by Bears": "II Kings 2:24", "Famine in Samaria": "II Kings 6:25", "Death of Jezebel": "II Kings 9:33", "Jezebel's Remains": "II Kings 9:35", "Death of Athaliah": "II Kings 11:16", "Slain by Lions": "II Kings 17:25", "Sennacherib": "II Kings 19:35", "Zedekiah's Sons": "II Kings 25:7", "Ammonite and Moabite": "II Chronicles 20:23",
 "Cyrus Restores": "Ezra 1:7", "Rebuilding of the Temple": "Ezra 3:10", "Artaxerxes Grants": "Ezra 7:13", "Ezra Kneels": "Ezra 9:5", "Nehemiah Views": "Nehemiah 2:13", "Ezra Reads the Law": "Nehemiah 8:3",
 "Vashti": "Esther 1:12", "Esther Before the King": "Esther 5:2", "Triumph of Mordecai": "Esther 6:11", "Esther Accuses Haman": "Esther 7:6", "Job Hears": "Job 1:14", "Job Speaks": "Job 2:11",
 "Prophet Isaiah": "Isaiah 1:1", "Destruction of Babylon": "Isaiah 13:19", "Leviathan": "Isaiah 27:1", "Baruch Writes": "Jeremiah 36:4", "Prophet Jeremiah": "Jeremiah 1:1", "Mourn over the Destruction": "Lamentations 1:1", "Prophet Ezekiel": "Ezekiel 1:1", "Daniel among the Exiles": "Daniel 1:6", "Furnace": "Daniel 3:25", "Writing on the Wall": "Daniel 5:25", "Lions' Den": "Daniel 6:17", "Four Beasts": "Daniel 7:3", "Prophet Amos": "Amos 1:1", "Spewed Forth": "Jonah 2:11", "Jonah Preaches": "Jonah 3:4", "Micah Exhorts": "Micah 6:8", "Four Chariots": "Zechariah 6:1",
 "Deluge": "Genesis 7:17", "Trial of Abraham": "Genesis 22:10", "Death of Abel": "Genesis 4:8",
}
works = {}
def add(file, title, artist, year, ref, source):
    if SKIP.search(title) or SKIP.search(file): return
    key = (title, artist, ref)
    if key in works: return
    works[key] = {"file": file, "title": title, "artist": artist, "year": year, "refs": [ref], "source": source}
for f in LISTS["Category:Old Testament by James Tissot"]:
    t = f.replace("File:", "")
    m = TISSOT_RE.search(t)
    if not m: continue
    book = BOOKS.get(m.group(1).strip().lower())
    if not book: continue
    title = re.sub(r"^[\d.\s]+", "", t.split(" (")[0]).strip()
    add(f, title, "James Tissot", "1896–1902", f"{book} {m.group(2)}:{m.group(3)}", "Tissot, The Old Testament (Jewish Museum, New York); Phillip Medhurst collection")
seen_dore = set()
for f in LISTS["Category:Doré's English Bible"]:
    t = f.replace("File:", "").rsplit(".", 1)[0]
    if "Bible gallery" in t or "Bible Gallery" in t: continue
    for frag, ref in DORE.items():
        if frag.lower() in t.lower():
            title = re.sub(r"^\d+[A-Z]?\.\s*", "", t).replace(" (89392244)", "").replace(" (89397429)", "")
            if (frag, ref) in seen_dore: break
            seen_dore.add((frag, ref)); add(f, title, "Gustave Doré", "1866", ref, "Doré's English Bible"); break
print("works:", len(works), "tissot:", sum(1 for w in works.values() if w["artist"] == "James Tissot"), "doré:", sum(1 for w in works.values() if w["artist"] == "Gustave Doré"))
# thumbnails
items = list(works.values())
for i in range(0, len(items), 20):
    batch = items[i:i + 20]
    j = api({"action": "query", "titles": "|".join(w["file"] for w in batch), "prop": "imageinfo", "iiprop": "url", "iiurlwidth": "480"})
    pages = j.get("query", {}).get("pages", {})
    norm = j.get("query", {}).get("normalized", [])
    back = {n["to"]: n["from"] for n in norm}
    got = {}
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        got[back.get(p.get("title"), p.get("title"))] = ii
    for w in batch:
        ii = got.get(w["file"], {})
        w["thumb"] = ii.get("thumburl"); w["image"] = ii.get("url"); w["page"] = ii.get("descriptionurl")
    pass
items = [w for w in items if w.get("thumb")]
for n, w in enumerate(items): w["id"] = f"art-{n+1}"; del w["file"]
json.dump({"meta": {"note": "Public-domain artworks keyed to verses. Images are served by Wikimedia Commons; refs are the verse the scene depicts.", "count": len(items)}, "works": items}, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
print("wrote", OUT, len(items))
