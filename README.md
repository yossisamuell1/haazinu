# Haazinu · הַאֲזִינוּ

The Tanakh and the Siddur through sound. Pick any verse: the **Kriah** tab plays it read by Rabbi Michoel Slavin (ba'al korei of 770, Chabad trop) with the verse highlighted, and the **Songs** tab lists the songs written on that verse and plays them. The Siddur opens in Chabad nusach.

Static web app, no build step, no backend. Text comes live from the Sefaria API; verse timings and the song catalogue are precomputed JSON.

## Run

**Live:** https://yossisamuell1.github.io/haazinu/ — served from GitHub Pages off `main`. Push to `main` and the site rebuilds in about a minute; nothing else to deploy.

Locally:

```sh
cd ~/haazinu
python3 scripts/serve.py
open http://localhost:8787/
```

Any static server works (`file://` does not, the app fetches JSON). `.work/` (source audio) and `scripts/.cache/` are gitignored: hundreds of MB, all regenerable.

## What is where

| Path | Purpose |
|---|---|
| `index.html`, `styles.css`, `app.js` | The app. Vanilla JS module, no dependencies. |
| `sw.js`, `manifest.webmanifest`, `icon.svg` | Offline shell and install metadata. |
| `data/kriah.json` | Verse and word timings for Rabbi Slavin's per-parasha readings (50 of 54 parshiot). Word times are interpolated, so word highlight is approximate. |
| `data/parshiot.json` | The 54 parshiyot with aliyah ranges. |
| `data/art.json` | 1,625 public-domain artworks keyed to verses. Built by `harvest_art.py` (Commons), `harvest_museums.py` (Met/Chicago/Cleveland) and `harvest_archives.py` (National Gallery/Smithsonian/Yale/Wellcome); screened by `clip_screen.py` and `screen_art.py`. |
| `data/scenes.json` | 200 biblical scene titles mapped to the verse depicted, in English, Dutch, German and French. Museum records carry no chapter and verse, so this is what keys them to the text. |
| `data/songs.json` | Song catalogue (465 songs on Torah, Nevi'im, Ketuvim and siddur passages) with Apple Music previews and screened YouTube ids. |
| `data/recording_blocklist.txt` | Terms that exclude a recording (female vocalists for kol isha, worship, karaoke). |
| `data/siddur.json` | Three nusachot from Sefaria: Chabad (weekday from Weekday Siddur Chabad, Shabbat and festivals from Siddur Sefard), Sefard, Ashkenaz. |
| `data/trop.json` | Legacy PocketTorah timings, no longer used (the reader is a woman). |
| `scripts/align_slavin.py` | Builds `kriah.json`: downloads nothing itself; reads `.work/slavin/<id>.mp3` and `.work/text/`, finds pauses with a relative energy envelope, aligns them to verses by dynamic programming. `--only Noach,Bo` to redo some. |
| `scripts/catalogue_seed.py` | The built-in song list. Edit the table and re-run to add songs. |
| `scripts/mine_itunes.py` | Grows the catalogue from Apple Music: pulls male artists' track lists, matches Hebrew titles as phrases against the Tanakh and siddur texts in `.work/`, adds matches as songs with the track as preview. `--dry` writes `.work/mine_preview.json` for review. |
| `scripts/catalogue_seed2.py` | Second hand-written batch plus nusach alias refs for the Ashkenaz-catalogued siddur songs. |
| `scripts/find_recordings.py` | Attaches recordings: Apple Music via the open iTunes Search API, YouTube via DuckDuckGo. `--only id`, `--refresh`. |
| `scripts/build_siddur.py` | Rebuilds `siddur.json` from Sefaria's indexes. |

## Audio and where it comes from

- **Torah reading**: Rabbi Michoel Slavin, published by Chabad.org as "Torah Reading Recordings", streamed from torahcdn.net (torahdownloads.org's mirror). Nothing is re-hosted. Chabad.org says the recordings are for educational use.
- Missing on the mirror: **Vayikra, Haazinu, Vezot Haberachah**. The app links to their Chabad.org pages. To align them, download the MP3 from Chabad.org into `.work/slavin/` named `<anything>.mp3`, add a line `<name-without-.mp3> <Parasha>` to `.work/slavin_ids.txt`, and run `python3 scripts/align_slavin.py --only Haazinu`.
- **Songs**: Apple Music previews (30 s) play in-app everywhere and link to the full track. YouTube embeds are used only where youtube.com is reachable; the app detects the kosher-filter block and hides them.

## Adding songs

In the app, Songs tab, paste a YouTube or Apple Music link, or type a name, and press Add. Title and performer are looked up. "Export mine" downloads your additions to merge into `data/songs.json` (or add a row to `scripts/catalogue_seed.py`). Recordings picked automatically can be hidden per device with "hide".

## Art

Each Tanakh verse can carry artworks (Art tab, red mark in the margin, "Art map" on the landing page). 1,527 works drawn from 20 public-domain collections on Wikimedia Commons.

`scripts/harvest_art.py` walks a list of categories and reads a verse reference out of each file's name or Commons description, handling the formats these collections use (`Genesis cap 1 v 16`, `(Genesis 19 30)`, `Genesis 1:3`, `1. Mose 3,7`). Only Tanakh book names are accepted, so New Testament plates drop out on their own. Re-run it after adding a category to `CATS`; file metadata is cached in `.work/art/meta_cache.json`, so only the category walk repeats.

Three harvesters feed it:

- `harvest_art.py` walks Wikimedia Commons categories and reads the verse out of filenames and descriptions.
- `harvest_museums.py` queries the Met, the Art Institute of Chicago and the Cleveland Museum.
- `harvest_archives.py` queries National Gallery of Art open data, the Smithsonian, Yale and Wellcome.

Museum and archive titles have no verse, so they are matched against `data/scenes.json`. Those patterns need word boundaries and context: bare words caused real false matches ("cattle" pulled in cattle paintings, "endor" matched "vendor", "nebo" matched "Assinneboine"). Re-run the match-and-filter pass after editing the table.

Biggest sources: Phillip Medhurst Picture Torah (467), Tissot's Old Testament (228), National Gallery of Art (196), Art Institute of Chicago (127), Rijksmuseum engravings (127), Bowyer Bible (106), Doré's English Bible (86).

The Metropolitan Museum begins returning 403 after a few thousand object fetches. `harvest_museums.py` caches fetched objects in `.work/art/met_objects.json` and takes `--no-met`, so a later run resumes instead of refetching.

### Modesty screening

Four layers, in order, all before anything reaches the app:

1. **Title and description keywords** reject Bathsheba, Susanna, Lot's daughters, Potiphar's wife, drunkenness and Eden nakedness in English, German, Dutch and French.
2. **CLIP zero-shot** (`scripts/clip_screen.py`) scores every thumbnail against nude and clothed prompt sets; anything at or above 0.15 is rejected. This is the layer that works on paintings.
3. **NudeNet** (`scripts/screen_art.py`) as a second opinion. It is trained on photographs and misses painted nudity on its own, so it is never used alone.
4. **Scene blacklist** removes verse ranges traditionally painted nude (Genesis 3, Genesis 9:20-27, Genesis 19:30-38, Genesis 38-39, II Samuel 11 and 13, Judges 16:4-22, Judges 19, Ezekiel 16 and 23, Esther 2) whatever the classifier said.

Rejected works are kept in `.work/art/rejected.json` with the reason, including scene mismatches. Of about 2,370 harvested, some 750 were removed.

## Keys

`j`/`k` verses · `[`/`]` chapters · `space` chant · `m` library · `s` song book · `/` search · `t` tikkun view

## After editing data files

Browsers cache `data/*.json`; bump `DATA_V` at the top of `app.js` after regenerating any of them (and the `?v=` tags in `index.html` after editing `app.js` or `styles.css`). `scripts/serve.py` sends no-cache headers so plain reloads pick up edits. `diag.html`, or the app opened with `?diag=1`, reports each startup step to the server log when something will not load.

## Known limits

- Verse timings are computed from pauses, not hand-checked. A verse can start a second early or late; word highlight drifts inside long verses.
- Sefaria has no Chabad Shabbat siddur, so those sections are Nusach Sefard.
- Siddur song refs were catalogued against Siddur Ashkenaz and matched to other nusachot by Hebrew title; paragraph numbers do not transfer across nusachot.
