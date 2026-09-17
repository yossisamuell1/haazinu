#!/usr/bin/env python3
"""Build data/siddur.json from Sefaria's indexes for several nusachot.
Output: {"nusachot":[{"id","title","heTitle","leaves":[{"ref","title","he","path","hePath"}]}]}
Chabad = Sefaria's Weekday Siddur Chabad, plus the Shabbat / festival / life-cycle sections of Siddur Sefard
(Sefaria has no Chabad Shabbat siddur; Nusach Sefard is the closest available text)."""
import json, urllib.request
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "data" / "siddur.json"

def prim(n, lang):
    return next((t["text"] for t in n.get("titles", []) if t.get("lang") == lang and t.get("primary")), n.get("key", ""))

def leaves_of(title):
    idx = json.load(urllib.request.urlopen(f"https://www.sefaria.org/api/v2/index/{title.replace(' ', '_')}"))
    out = []
    def walk(n, path, hepath, depth=0):
        en, he = prim(n, "en"), prim(n, "he")
        p, hp = (path + [en], hepath + [he]) if depth else (path, hepath)
        if "nodes" in n:
            for c in n["nodes"]: walk(c, p, hp, depth + 1)
        else:
            out.append({"ref": f"{title}, " + ", ".join(p), "title": en, "he": he, "path": p, "hePath": hp})
    walk(idx["schema"], [], [])
    return idx["heTitle"], out

ash_he, ash = leaves_of("Siddur Ashkenaz")
sef_he, sef = leaves_of("Siddur Sefard")
chb_he, chb = leaves_of("Weekday Siddur Chabad")
# Chabad: weekday from the Chabad siddur; everything not weekday from Sefard
WEEKDAY_SEFARD = {"Upon Arising", "Weekday Shacharit", "Additional Prayers ", "Additional Prayers", "Weekday Mincha", "Weekday Maariv", "Various Blessings", "Birchat HaMazon", "Blessings"}
chabad = chb + [l for l in sef if l["path"][0] not in WEEKDAY_SEFARD]
nusachot = [
    {"id": "chabad", "title": "Siddur Chabad", "heTitle": "סידור חב״ד (נוסח האר״י)", "note": "Weekday text is Sefaria's Weekday Siddur Chabad; Shabbat and festival sections are from Siddur Sefard, the closest text Sefaria has.", "leaves": chabad},
    {"id": "sefard", "title": "Siddur Sefard", "heTitle": sef_he, "leaves": sef},
    {"id": "ashkenaz", "title": "Siddur Ashkenaz", "heTitle": ash_he, "leaves": ash},
]
OUT.write_text(json.dumps({"nusachot": nusachot}, ensure_ascii=False, indent=0))
for n in nusachot: print(n["id"], len(n["leaves"]), "leaves")
