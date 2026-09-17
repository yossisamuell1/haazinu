/* Haazinu — the Tanakh and the Siddur through sound.
   Text: Sefaria API (live). Torah reading: Rabbi Michoel Slavin (Chabad.org) with computed verse timings in data/kriah.json.
   Songs: data/songs.json (+ localStorage additions); Apple Music previews and YouTube embeds. */

const SEFARIA = "https://www.sefaria.org/api";
const DATA_V = "202609171313";  // bump when data/*.json changes so browsers do not reuse an old cached copy
const TORAH = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"];
const BOOKS = [
  { en: "Genesis", he: "בראשית", ch: 50, sec: "Torah" }, { en: "Exodus", he: "שמות", ch: 40, sec: "Torah" }, { en: "Leviticus", he: "ויקרא", ch: 27, sec: "Torah" },
  { en: "Numbers", he: "במדבר", ch: 36, sec: "Torah" }, { en: "Deuteronomy", he: "דברים", ch: 34, sec: "Torah" },
  { en: "Joshua", he: "יהושע", ch: 24, sec: "Nevi'im" }, { en: "Judges", he: "שופטים", ch: 21, sec: "Nevi'im" }, { en: "I Samuel", he: "שמואל א", ch: 31, sec: "Nevi'im" },
  { en: "II Samuel", he: "שמואל ב", ch: 24, sec: "Nevi'im" }, { en: "I Kings", he: "מלכים א", ch: 22, sec: "Nevi'im" }, { en: "II Kings", he: "מלכים ב", ch: 25, sec: "Nevi'im" },
  { en: "Isaiah", he: "ישעיהו", ch: 66, sec: "Nevi'im" }, { en: "Jeremiah", he: "ירמיהו", ch: 52, sec: "Nevi'im" }, { en: "Ezekiel", he: "יחזקאל", ch: 48, sec: "Nevi'im" },
  { en: "Hosea", he: "הושע", ch: 14, sec: "Nevi'im" }, { en: "Joel", he: "יואל", ch: 4, sec: "Nevi'im" }, { en: "Amos", he: "עמוס", ch: 9, sec: "Nevi'im" },
  { en: "Obadiah", he: "עובדיה", ch: 1, sec: "Nevi'im" }, { en: "Jonah", he: "יונה", ch: 4, sec: "Nevi'im" }, { en: "Micah", he: "מיכה", ch: 7, sec: "Nevi'im" },
  { en: "Nahum", he: "נחום", ch: 3, sec: "Nevi'im" }, { en: "Habakkuk", he: "חבקוק", ch: 3, sec: "Nevi'im" }, { en: "Zephaniah", he: "צפניה", ch: 3, sec: "Nevi'im" },
  { en: "Haggai", he: "חגי", ch: 2, sec: "Nevi'im" }, { en: "Zechariah", he: "זכריה", ch: 14, sec: "Nevi'im" }, { en: "Malachi", he: "מלאכי", ch: 3, sec: "Nevi'im" },
  { en: "Psalms", he: "תהלים", ch: 150, sec: "Ketuvim" }, { en: "Proverbs", he: "משלי", ch: 31, sec: "Ketuvim" }, { en: "Job", he: "איוב", ch: 42, sec: "Ketuvim" },
  { en: "Song of Songs", he: "שיר השירים", ch: 8, sec: "Ketuvim" }, { en: "Ruth", he: "רות", ch: 4, sec: "Ketuvim" }, { en: "Lamentations", he: "איכה", ch: 5, sec: "Ketuvim" },
  { en: "Ecclesiastes", he: "קהלת", ch: 12, sec: "Ketuvim" }, { en: "Esther", he: "אסתר", ch: 10, sec: "Ketuvim" }, { en: "Daniel", he: "דניאל", ch: 12, sec: "Ketuvim" },
  { en: "Ezra", he: "עזרא", ch: 10, sec: "Ketuvim" }, { en: "Nehemiah", he: "נחמיה", ch: 13, sec: "Ketuvim" }, { en: "I Chronicles", he: "דברי הימים א", ch: 29, sec: "Ketuvim" },
  { en: "II Chronicles", he: "דברי הימים ב", ch: 36, sec: "Ketuvim" },
];
const ALIASES = {
  gen: "Genesis", bereshit: "Genesis", bereishit: "Genesis", breishis: "Genesis", bereishis: "Genesis", ex: "Exodus", exo: "Exodus", shemot: "Exodus", shmot: "Exodus", shemos: "Exodus",
  lev: "Leviticus", vayikra: "Leviticus", num: "Numbers", bamidbar: "Numbers", deut: "Deuteronomy", devarim: "Deuteronomy", dvarim: "Deuteronomy",
  ps: "Psalms", psalm: "Psalms", tehillim: "Psalms", tehilim: "Psalms", תהילים: "Psalms", mishlei: "Proverbs", prov: "Proverbs", iyov: "Job", shir: "Song of Songs", shirhashirim: "Song of Songs",
  kohelet: "Ecclesiastes", eicha: "Lamentations", yeshayahu: "Isaiah", isa: "Isaiah", yirmiyahu: "Jeremiah", jer: "Jeremiah", yechezkel: "Ezekiel", ezek: "Ezekiel", yehoshua: "Joshua", shoftim: "Judges",
  shmuel1: "I Samuel", shmuel2: "II Samuel", "1samuel": "I Samuel", "2samuel": "II Samuel", "1kings": "I Kings", "2kings": "II Kings", melachim1: "I Kings", melachim2: "II Kings",
  zech: "Zechariah", mal: "Malachi", hoshea: "Hosea", micha: "Micah", yona: "Jonah", "1chronicles": "I Chronicles", "2chronicles": "II Chronicles", ezra: "Ezra", nechemia: "Nehemiah", megilatesther: "Esther",
};
for (const b of BOOKS) { ALIASES[b.en.toLowerCase().replace(/[\s']/g, "")] = b.en; ALIASES[b.he.replace(/\s/g, "")] = b.en; }
// chabad.org pages for the readings we could not align (opens in a new tab)
const CHABAD_PAGES = { Vayikra: "https://www.chabad.org/multimedia/music_cdo/aid/1014656/jewish/Vayikra.htm", Haazinu: "https://www.chabad.org/multimedia/music_cdo/aid/1014846/jewish/Haazinu.htm", "Vezot Haberakhah": "https://www.chabad.org/multimedia/music_cdo/aid/1014849/jewish/VZos-HaBerachah.htm" };
const CHABAD_ALL = "https://www.chabad.org/multimedia/music_cdo/aid/982057/jewish/Torah-Reading-Recordings.htm";

const TROPE = {
  "֑": ["Etnachta", "אֶתְנַחְתָּא", "dis", 1], "֒": ["Segol", "סֶגוֹל", "dis", 2], "֓": ["Shalshelet", "שַׁלְשֶׁלֶת", "dis", 2],
  "֔": ["Zakef Katan", "זָקֵף קָטָן", "dis", 2], "֕": ["Zakef Gadol", "זָקֵף גָּדוֹל", "dis", 2], "֖": ["Tipcha", "טִפְחָא", "dis", 2],
  "֗": ["Revia", "רְבִיעִי", "dis", 2], "֘": ["Zarka", "זַרְקָא", "dis", 2], "֙": ["Pashta", "פַּשְׁטָא", "dis", 2], "֚": ["Yetiv", "יְתִיב", "dis", 2],
  "֛": ["Tevir", "תְּבִיר", "dis", 2], "֜": ["Geresh", "גֵּרֵשׁ", "dis", 2], "֝": ["Geresh Muqdam", "גֵּרֵשׁ מֻקְדָּם", "dis", 2],
  "֞": ["Gershayim", "גֵּרְשַׁיִם", "dis", 2], "֟": ["Karnei Farah", "קַרְנֵי פָרָה", "dis", 2], "֠": ["Telisha Gedola", "תְּלִישָא גְדוֹלָה", "dis", 2],
  "֡": ["Pazer", "פָּזֵר", "dis", 2], "֢": ["Atnach Hafuch", "אַתְנָח הָפוּךְ", "other", 0], "֣": ["Munach", "מוּנַח", "con", 0],
  "֤": ["Mahpach", "מַהְפַּךְ", "con", 0], "֥": ["Mercha", "מֵרְכָא", "con", 0], "֦": ["Mercha Kefula", "מֵרְכָא כְפוּלָה", "con", 0],
  "֧": ["Darga", "דַּרְגָּא", "con", 0], "֨": ["Kadma", "קַדְמָא", "con", 0], "֩": ["Telisha Ketana", "תְּלִישָא קְטַנָּה", "con", 0],
  "֪": ["Yerach Ben Yomo", "יֶרַח בֶּן יוֹמוֹ", "con", 0], "֫": ["Ole", "עוֹלֶה", "other", 0], "֬": ["Iluy", "עִלוּי", "other", 0],
  "֭": ["Dechi", "דְּחִי", "other", 0], "֮": ["Zinor", "צִנּוֹר", "other", 0], "׃": ["Sof Pasuk", "סוֹף פָּסוּק", "dis", 1],
};
const PASEQ = "׀", MAQAF = "־";

const $ = (s) => document.querySelector(s);
const diag = (m) => { if (/[?&]diag=1/.test(location.search)) fetch("/diag?" + encodeURIComponent(m)).catch(() => {}); };
const showError = (msg) => { diag("ERROR " + msg); const st = document.querySelector("#readerStatus"); if (!st) return; st.hidden = false; st.textContent = "Something broke: " + msg + " — reload with Cmd+Shift+R; if it persists, copy this line."; };
window.addEventListener("error", (e) => showError(e.message + (e.filename ? ` (${e.filename.split("/").pop()}:${e.lineno})` : "")));
window.addEventListener("unhandledrejection", (e) => showError(String(e.reason?.message || e.reason)));
const el = (tag, attrs = {}, ...kids) => {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") n.className = v;
    else if (k === "html") n.innerHTML = v;
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else if (v !== null && v !== undefined && v !== false) n.setAttribute(k, v === true ? "" : v);
  }
  for (const k of kids.flat()) if (k !== null && k !== undefined && k !== false) n.append(k.nodeType ? k : document.createTextNode(k));
  return n;
};
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
};

const state = { map: store.get("hz:map", "songs"), mode: "tanakh", book: "Genesis", chapter: 1, verse: 1, nusach: store.get("hz:nusach", "chabad"), leaf: 0, text: null, tab: "kriah", ytBlocked: false, week: null };
const data = { parshiot: [], kriah: null, songs: [], mine: [], hidden: store.get("hz:hidden", []), siddur: null, art: [] };
const bookInfo = (b) => BOOKS.find((x) => x.en === b);
const isTorah = () => state.mode === "tanakh" && TORAH.includes(state.book);
const nusach = () => data.siddur.nusachot.find((n) => n.id === state.nusach) || data.siddur.nusachot[0];
const leaf = () => nusach().leaves[state.leaf];

/* ---------------- data ---------------- */
async function loadData() {
  const j = (u) => fetch(`${u}?v=${DATA_V}`).then((r) => r.json());
  const [p, k, s, sd, art] = await Promise.all([j("data/parshiot.json"), j("data/kriah.json").catch(() => null), j("data/songs.json"), j("data/siddur.json"), j("data/art.json").catch(() => ({ works: [] }))]);
  data.parshiot = p; data.kriah = k; data.songs = s.songs; data.siddur = sd; data.art = art.works || [];
  data.mine = store.get("hz:mysongs", store.get("sht:mysongs", []));
  if (!data.siddur.nusachot.some((n) => n.id === state.nusach)) state.nusach = data.siddur.nusachot[0].id;
}
// Orthodox translations: Metsudah Chumash for the Torah, Koren Jerusalem Bible for the rest of Tanakh (Sefaria withholds the Kehot Chumash from its API); siddur keeps Sefaria's default English.
const EN_VERSION = (ref) => { const b = ref.replace(/ \d+.*$/, ""); if (TORAH.includes(b)) return "Metsudah Chumash, Metsudah Publications, 2009"; if (BOOKS.some((x) => x.en === b)) return "The Koren Jerusalem Bible"; return null; };
async function fetchText(ref) {
  const key = `hz:text2:${ref}`;
  const c = store.get(key, null); if (c) return c;
  const ver = EN_VERSION(ref);
  const url = `${SEFARIA}/v3/texts/${encodeURIComponent(ref)}?version=hebrew&version=${encodeURIComponent(ver ? "english|" + ver : "english")}&return_format=text_only`;
  let r = await fetch(url);
  if (!r.ok) throw new Error(`Sefaria ${r.status}`);
  let j = await r.json();
  if (ver && !j.versions.some((v) => v.language === "en")) { r = await fetch(`${SEFARIA}/v3/texts/${encodeURIComponent(ref)}?version=hebrew&version=english&return_format=text_only`); j = await r.json(); }
  const he = j.versions.find((v) => v.language === "he"), en = j.versions.find((v) => v.language === "en");
  const flat = (x) => (Array.isArray(x) ? x.flat(Infinity) : [x]);
  const out = { heRef: j.heRef, ref: j.ref, he: he ? flat(he.text) : [], en: en ? flat(en.text) : [], heVersion: he ? `${he.versionTitle} (${he.license})` : "", enVersion: en ? `${en.versionTitle} (${en.license})` : "" };
  store.set(key, out);
  return out;
}

/* ---------------- refs ---------------- */
const cmp = (a, b) => (a[0] - b[0]) || (a[1] - b[1]);
const BOOK_RE = new RegExp(`^(${BOOKS.map((b) => b.en).join("|")})\\s+(\\d+):(\\d+)(?:-(?:(\\d+):)?(\\d+))?$`);
function parseRange(ref) {
  const m = ref.match(BOOK_RE);
  if (!m) return null;
  const c1 = +m[2], v1 = +m[3];
  return { book: m[1], from: [c1, v1], to: [m[4] ? +m[4] : c1, m[5] ? +m[5] : v1] };
}
const stripMarks = (s) => s.replace(/[֑-ׇ]/g, "");
const normHe = (s) => stripMarks(s || "").replace(/[^א-ת]/g, "");
// siddur song refs are written against Siddur Ashkenaz; match passages across nusachot by Hebrew title
function siddurRefLeaf(r) {
  for (const n of data.siddur.nusachot) { const l = n.leaves.find((l) => r === l.ref || r.startsWith(l.ref + " ")); if (l) return { n, l, rest: r === l.ref ? "" : r.slice(l.ref.length + 1) }; }
  return null;
}
function refCovers(r, v) {
  if (state.mode === "tanakh") {
    const rng = parseRange(r);
    return !!rng && rng.book === state.book && cmp([state.chapter, v], rng.from) >= 0 && cmp([state.chapter, v], rng.to) <= 0;
  }
  const cur = leaf(); const hit = siddurRefLeaf(r);
  if (!hit) return false;
  const same = hit.l === cur || (normHe(hit.l.he) && normHe(hit.l.he) === normHe(cur.he));
  if (!same) return false;
  if (!hit.rest || hit.n !== nusach()) return true;
  const m = hit.rest.match(/^(\d+)(?:-(\d+))?$/);
  return !!m && v >= +m[1] && v <= +(m[2] || m[1]);
}
const currentRef = (v) => (state.mode === "tanakh" ? `${state.book} ${state.chapter}:${v}` : `${leaf().ref} ${v}`);
const currentHeRef = (v) => (state.mode === "tanakh" ? `${state.text.heRef}:${toHebNum(v)}` : `${state.text.heRef} ${toHebNum(v)}`);
const sefariaUrl = (ref) => `https://www.sefaria.org/${ref.replace(/ /g, "_").replace(/:/g, ".")}`;
const GEMATRIA = { א: 1, ב: 2, ג: 3, ד: 4, ה: 5, ו: 6, ז: 7, ח: 8, ט: 9, י: 10, כ: 20, ל: 30, מ: 40, נ: 50, ס: 60, ע: 70, פ: 80, צ: 90, ק: 100, ר: 200, ש: 300, ת: 400, ך: 20, ם: 40, ן: 50, ף: 80, ץ: 90 };
function hebNum(s) { s = s.replace(/[׳״'"]/g, ""); if (!s || ![...s].every((ch) => GEMATRIA[ch])) return null; return [...s].reduce((a, ch) => a + GEMATRIA[ch], 0); }
const num = (s) => (/^\d+$/.test(s) ? +s : hebNum(s));
function toHebNum(n) {
  const ones = ["", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"], tens = ["", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"], hund = ["", "ק", "ר", "ש", "ת"];
  let s = ""; let h = Math.floor(n / 100); n %= 100;
  while (h > 4) { s += "ת"; h -= 4; } s += hund[h];
  if (n === 15) s += "טו"; else if (n === 16) s += "טז"; else s += tens[Math.floor(n / 10)] + ones[n % 10];
  return s.length > 1 ? s.slice(0, -1) + "״" + s.slice(-1) : s + "׳";
}

/* ---------------- search / go to ---------------- */
const normQ = (s) => stripMarks(s).toLowerCase().replace(/[’'`"\s\-־.,:]/g, "").replace(/kh/g, "ch").replace(/q/g, "k").replace(/tz/g, "ts").replace(/ph/g, "f").replace(/w/g, "v").replace(/(.)\1+/g, "$1");
function searchAll(q, limit = 12) {
  q = q.trim(); if (!q) return [];
  const nq = normQ(q); const out = [];
  const push = (r) => { if (!out.some((x) => x.hash === r.hash)) out.push(r); };
  // exact ref / book chapter
  const m = q.replace(/[.,]/g, " ").replace(/\s+/g, " ").match(/^(.+?)\s+([^\s:]+)(?:[:\s]([^\s:]+))?$/);
  const bk = (s) => ALIASES[s.toLowerCase().replace(/[\s']/g, "")] || ALIASES[s.replace(/\s/g, "")];
  if (m && bk(m[1])) { const book = bk(m[1]); const c = num(m[2]), v = m[3] ? num(m[3]) : 1; if (c) push({ hash: `#${book}.${Math.min(Math.max(c, 1), bookInfo(book).ch)}.${v || 1}`, title: `${book} ${c}${v ? ":" + v : ""}`, he: bookInfo(book).he, kind: "ref" }); }
  if (bk(q)) { const book = bk(q); push({ hash: `#${book}.1.1`, title: book, he: bookInfo(book).he, kind: "book" }); }
  for (const p of data.parshiot) if (normQ(p.id).startsWith(nq) || normQ(p.he).startsWith(nq)) { const [c, v] = p.begin.split(":").map(Number); push({ hash: `#${p.book}.${c}.${v}`, title: `Parashat ${p.id}`, he: stripMarks(p.he), kind: "parasha" }); }
  for (const b of BOOKS) if (nq.length >= 2 && (normQ(b.en).includes(nq) || normQ(b.he).includes(nq))) push({ hash: `#${b.en}.1.1`, title: b.en, he: b.he, kind: b.sec });
  const n = nusach();
  n.leaves.forEach((l, i) => { if (nq.length >= 2 && (normQ(l.title).includes(nq) || normQ(l.he).includes(nq))) push({ hash: `#s/${n.id}/${encodeURIComponent(l.ref)}/1`, title: l.title, he: l.he, kind: l.path.slice(0, -1).join(" › ") }); });
  for (const s of allSongs()) if (nq.length >= 2 && (normQ(s.title).includes(nq) || normQ(s.title_he || "").includes(nq) || normQ(s.performer || "").includes(nq))) push({ hash: hashForRef(s.refs[0]), title: s.title, he: s.title_he || "", kind: `♪ ${s.refs[0]}` });
  return out.slice(0, limit);
}
function hashForRef(r) {
  const rng = parseRange(r); if (rng) return `#${rng.book}.${rng.from[0]}.${rng.from[1]}`;
  const hit = siddurRefLeaf(r); if (!hit) return "#";
  const cur = nusach(); const li = cur.leaves.findIndex((l) => l === hit.l || (normHe(l.he) && normHe(l.he) === normHe(hit.l.he)));
  const nid = li >= 0 ? cur.id : hit.n.id, idx = li >= 0 ? li : hit.n.leaves.indexOf(hit.l);
  const para = hit.rest.match(/^(\d+)/); return `#s/${nid}/${encodeURIComponent((li >= 0 ? cur : hit.n).leaves[idx].ref)}/${para ? para[1] : 1}`;
}

/* ---------------- tokenising ---------------- */
const _ta = document.createElement("textarea");
const decode = (s) => { _ta.innerHTML = s; return _ta.value; };
function tokenize(heVerse) {
  const clean = decode(heVerse.replace(/<[^>]+>/g, "")).replace(/\{[פס]\}/g, "").replace(/\([^)]*\)/g, "").replace(/[\[\]]/g, "").replace(/[\s  ]+/g, " ").trim();
  const words = [];
  for (const tok of clean.split(" ").filter(Boolean)) {
    if (tok === PASEQ) { if (words.length) words[words.length - 1] += " " + tok; continue; }
    const parts = tok.split(MAQAF);
    parts.forEach((p, i) => { if (p) words.push(i < parts.length - 1 ? p + MAQAF : p); });
  }
  return words.map((w) => w.replace(/ׇ/g, "ָ"));
}
function tropesIn(word) { const seen = new Set(); const out = []; for (const ch of word) if (TROPE[ch] && !seen.has(ch)) { seen.add(ch); out.push(TROPE[ch]); } return out; }
const phraseClass = (word) => { let lvl = 0; for (const t of tropesIn(word)) if (t[3] === 1) lvl = 1; else if (t[3] === 2 && lvl !== 1) lvl = 2; return lvl ? `d${lvl}` : ""; };
const tikkunText = (w) => stripMarks(w).replace(/[־]/g, "־");
function timingFor(book, c, v) {
  const t = data.kriah?.verses?.[book]?.[`${c}:${v}`];
  return t ? { parsha: t[0], url: data.kriah.files[t[0]].url, times: t[1] } : null;
}
const parshaOf = (book, c, v) => data.parshiot.find((p) => p.book === book && cmp([c, v], p.begin.split(":").map(Number)) >= 0 && cmp([c, v], p.end.split(":").map(Number)) <= 0);
const aliyahOf = (p, c, v) => p?.aliyot.find((a) => a.n !== "M" && cmp([c, v], a.begin.split(":").map(Number)) >= 0 && cmp([c, v], a.end.split(":").map(Number)) <= 0);

/* ---------------- songs ---------------- */
const allSongs = () => [...data.songs, ...data.mine.map((s) => ({ ...s, mine: true }))];
const songsOn = (v) => allSongs().filter((s) => s.refs.some((r) => refCovers(r, v)));
function segmentsWithSongs() {
  const map = new Map(); const n = state.text?.he.length || 0;
  for (const s of allSongs()) for (let v = 1; v <= n; v++) if (s.refs.some((r) => refCovers(r, v))) { if (!map.has(v)) map.set(v, []); map.get(v).push(s); }
  return map;
}
const ytId = (u) => { const m = (u || "").match(/(?:v=|youtu\.be\/|embed\/|shorts\/)([\w-]{11})/); return m ? m[1] : (/^[\w-]{11}$/.test(u || "") ? u : null); };
const chaptersWithSongs = (book) => { const s = new Set(); for (const x of allSongs()) for (const r of x.refs) { const g = parseRange(r); if (g && g.book === book) for (let c = g.from[0]; c <= g.to[0]; c++) s.add(c); } return s; };

/* ---------------- art ---------------- */
const artOn = (v) => state.mode === "tanakh" ? data.art.filter((w) => w.refs.some((r) => refCovers(r, v))) : [];
function segmentsWithArt() {
  const map = new Map(); if (state.mode !== "tanakh") return map;
  const n = state.text?.he.length || 0;
  for (const w of data.art) for (const r of w.refs) { const g = parseRange(r); if (!g || g.book !== state.book) continue; for (let v = 1; v <= n; v++) if (cmp([state.chapter, v], g.from) >= 0 && cmp([state.chapter, v], g.to) <= 0) { if (!map.has(v)) map.set(v, []); map.get(v).push(w); } }
  return map;
}
function artCard(w) {
  return el("button", { class: "artwork", type: "button", title: "View larger", onclick: () => openLightbox(w) },
    el("img", { src: w.thumb, alt: w.title, loading: "lazy" }),
    el("div", { class: "cap" }, el("b", {}, w.title), el("span", {}, `${w.artist}${w.year ? ", " + w.year : ""} · ${w.refs[0]}`)));
}
function openLightbox(w) {
  $("#lightboxImg").src = w.image || w.thumb; $("#lightboxTitle").textContent = w.title; $("#lightboxMeta").textContent = `${w.artist}${w.year ? ", " + w.year : ""} · ${w.refs.join(", ")}`; $("#lightboxLink").href = w.page || "#"; $("#lightbox").hidden = false;
}
function renderArt() {
  const v = state.verse;
  $("#artRefHe").textContent = currentHeRef(v); $("#artRefEn").textContent = currentRef(v);
  const list = $("#artList"); list.innerHTML = "";
  const works = artOn(v);
  if (!works.length) list.append(el("div", { class: "empty", style: "grid-column:1/-1" }, state.mode === "tanakh" ? "No artwork catalogued on this verse." : "Art is catalogued on Tanakh verses."));
  for (const w of works) list.append(artCard(w));
  const ca = $("#chapterArt"); ca.innerHTML = "";
  const map = segmentsWithArt();
  const others = [...map.entries()].filter(([vv]) => vv !== v).sort((a, b) => a[0] - b[0]);
  if (!others.length) ca.append(el("div", { class: "fine" }, "No other verses in this chapter have art yet."));
  for (const [vv, ws] of others) ca.append(el("a", { href: hashFor(vv), onclick: (e) => { e.preventDefault(); selectVerse(vv, { scroll: true }); } }, el("span", {}, el("b", {}, `${state.chapter}:${vv}`), ` ${[...new Set(ws.map((x) => x.title))].slice(0, 3).join(", ")}${ws.length > 3 ? "…" : ""}`), el("span", { class: "fine" }, ws[0].artist.split(" ").pop())));
}

/* ---------------- audio: Torah reading ---------------- */
const audio = $("#audio"), preview = $("#preview");
const player = {
  queue: [], idx: -1, cur: null, raf: 0, label: "",
  async playVerse(book, c, v) {
    const t = timingFor(book, c, v);
    if (!t) { this.stop(); setPlayerState("No recording for this verse"); return false; }
    stopPreview(); closeEmbeds();
    this.cur = { book, c, v, t };
    audio.playbackRate = +$("#rate").value;
    if (audio.src !== t.url) { audio.src = t.url; audio.load(); }
    const ready = audio.readyState >= 1 ? Promise.resolve() : new Promise((res) => { audio.addEventListener("loadedmetadata", res, { once: true }); audio.addEventListener("error", res, { once: true }); });
    audio.muted = true;  // stay silent until the seek lands (Safari needs play() inside the tap)
    const playing = audio.play();
    setPlayerState("Loading recording…");
    await ready;
    if (!this.cur || this.cur.v !== v) return false;
    audio.currentTime = t.times[0];
    await new Promise((res) => { audio.addEventListener("seeked", res, { once: true }); setTimeout(res, 1500); });
    audio.muted = false;
    try { await playing; } catch (err) { audio.muted = false; setPlayerState(err?.name === "NotAllowedError" ? "Tap play again" : "Could not load the recording"); return false; }
    setPlayerState(`${this.label || "Chanting"} ${book} ${c}:${v}`);
    markPlaying(v, true);
    cancelAnimationFrame(this.raf);
    const tick = () => {
      if (!this.cur) return;
      const { times } = this.cur.t; const now = audio.currentTime;
      const end = times[times.length - 1];
      let wi = -1;
      if (now >= times[0]) { wi = times.length - 2; for (let i = 0; i < times.length - 1; i++) if (now < times[i + 1]) { wi = i; break; } }
      highlightWord(v, wi);
      $("#progressBar").style.width = `${Math.min(100, Math.max(0, ((now - times[0]) / (end - times[0])) * 100))}%`;
      if (now >= end - 0.02 || audio.ended) { this.onVerseEnd(); return; }
      this.raf = requestAnimationFrame(tick);
    };
    this.raf = requestAnimationFrame(tick);
    return true;
  },
  onVerseEnd() {
    const c = this.cur; if (!c) return;
    if ($("#loopVerse").checked && this.queue.length === 0) { this.playVerse(c.book, c.c, c.v); return; }
    if (this.queue.length && this.idx < this.queue.length - 1) { this.idx++; const n = this.queue[this.idx]; this.goTo(n); this.playVerse(n.book, n.c, n.v); return; }
    if ($("#loopVerse").checked && this.queue.length) { this.idx = 0; const n = this.queue[0]; this.goTo(n); this.playVerse(n.book, n.c, n.v); return; }
    this.stop("Done");
  },
  goTo(n) { if (n.book !== state.book || n.c !== state.chapter) { location.hash = `#${n.book}.${n.c}.${n.v}`; } else selectVerse(n.v, { scroll: true, silentHash: true }); },
  playQueue(list, label = "Chanting") { if (!list.length) return; this.queue = list; this.idx = 0; this.label = label; const n = list[0]; this.goTo(n); this.playVerse(n.book, n.c, n.v); },
  stop(msg = "Ready") {
    cancelAnimationFrame(this.raf); audio.pause();
    if (this.cur) { markPlaying(this.cur.v, false); highlightWord(this.cur.v, -1); }
    this.cur = null; this.queue = []; this.idx = -1; this.label = "";
    $("#progressBar").style.width = "0"; setPlayerState(msg);
    document.querySelectorAll(".aliyot button.playing").forEach((b) => b.classList.remove("playing"));
  },
  async seekWord(book, c, v, i) {
    if (!this.cur || this.cur.c !== c || this.cur.v !== v || this.cur.book !== book) { const ok = await this.playVerse(book, c, v); if (!ok) return; }
    audio.currentTime = this.cur.t.times[i];
  },
};
audio.addEventListener("ended", () => player.cur && player.onVerseEnd());
audio.addEventListener("error", () => { if (player.cur) { player.stop("Could not load the recording"); } });
function setPlayerState(s) { $("#playerState").textContent = s; }
function markPlaying(v, on) { document.querySelectorAll(".verse.playing").forEach((n) => n.classList.remove("playing")); if (on) verseEl(v)?.classList.add("playing"); }
function highlightWord(v, i) {
  const ve = verseEl(v); if (!ve) return;
  ve.querySelectorAll(".w.now").forEach((n) => n.classList.remove("now"));
  document.querySelectorAll("#wordList li.now").forEach((n) => n.classList.remove("now"));
  if (i >= 0) { ve.querySelector(`.w[data-i="${i}"]`)?.classList.add("now"); if (v === state.verse) $(`#wordList li[data-i="${i}"]`)?.classList.add("now"); }
}
const verseEl = (v) => document.querySelector(`.verse[data-v="${v}"]`);
function closeEmbeds() { document.querySelectorAll(".embed").forEach((f) => f.remove()); document.querySelectorAll(".rec.playing").forEach((r) => r.classList.remove("playing")); }
function stopPreview() { preview.pause(); preview.removeAttribute("src"); document.querySelectorAll(".rec.playing").forEach((r) => r.classList.remove("playing")); }
// verses of an aliyah (may span chapters) as a queue
function aliyahQueue(p, a) {
  const [c1, v1] = a.begin.split(":").map(Number), [c2, v2] = a.end.split(":").map(Number);
  const out = [];
  for (let c = c1; c <= c2; c++) {
    const last = c === c2 ? v2 : verseCount(p.book, c);
    for (let v = c === c1 ? v1 : 1; v <= last; v++) if (timingFor(p.book, c, v)) out.push({ book: p.book, c, v });
  }
  return out;
}
function verseCount(book, c) { const vs = Object.keys(data.kriah?.verses?.[book] || {}).filter((k) => k.startsWith(c + ":")); return vs.length ? Math.max(...vs.map((k) => +k.split(":")[1])) : (state.book === book && state.chapter === c ? state.text.he.length : 0); }

/* ---------------- record yourself ---------------- */
const rec = { mr: null, chunks: [], url: null };
async function toggleRecord() {
  const btn = $("#recBtn");
  if (rec.mr && rec.mr.state === "recording") { rec.mr.stop(); return; }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    rec.chunks = []; rec.mr = new MediaRecorder(stream);
    rec.mr.ondataavailable = (e) => rec.chunks.push(e.data);
    rec.mr.onstop = () => { stream.getTracks().forEach((t) => t.stop()); if (rec.url) URL.revokeObjectURL(rec.url); rec.url = URL.createObjectURL(new Blob(rec.chunks, { type: rec.mr.mimeType })); btn.classList.remove("on"); btn.textContent = "● Record me"; $("#recPlay").hidden = false; $("#recState").textContent = `Your take of ${currentRef(state.verse)} (kept until you leave)`; };
    rec.mr.start(); btn.classList.add("on"); btn.textContent = "■ Stop"; $("#recState").textContent = "Recording…";
  } catch (e) { $("#recState").textContent = "Microphone not available"; }
}

/* ---------------- library (TOC) ---------------- */
function renderToc() {
  const wrap = $("#tocList"); wrap.innerHTML = "";
  const withSongs = new Map(BOOKS.map((b) => [b.en, chaptersWithSongs(b.en)]));
  // Torah by parasha
  wrap.append(el("h4", {}, "Torah · ", el("span", { class: "he-inline" }, "תורה")));
  for (const b of BOOKS.filter((b) => b.sec === "Torah")) {
    const det = el("details", { "data-book": b.en }, el("summary", {}, b.en, el("span", { class: "he-inline" }, b.he)));
    for (const p of data.parshiot.filter((p) => p.book === b.en)) {
      const [c, v] = p.begin.split(":").map(Number);
      det.append(el("a", { href: `#${b.en}.${c}.${v}`, "data-parsha": p.id }, p.id, el("span", { class: "he-inline" }, stripMarks(p.he))));
    }
    wrap.append(det);
  }
  for (const sec of ["Nevi'im", "Ketuvim"]) {
    wrap.append(el("h4", {}, sec + " · ", el("span", { class: "he-inline" }, sec === "Nevi'im" ? "נביאים" : "כתובים")));
    for (const b of BOOKS.filter((b) => b.sec === sec)) {
      const det = el("details", { "data-book": b.en }, el("summary", {}, el("span", {}, b.en, withSongs.get(b.en).size ? el("small", {}, `${withSongs.get(b.en).size} chapters with songs`) : null), el("span", { class: "he-inline" }, b.he)));
      const grid = el("div", { class: "chapgrid" });
      for (let c = 1; c <= b.ch; c++) grid.append(el("a", { href: `#${b.en}.${c}.1`, "data-chapter": `${b.en}.${c}`, class: withSongs.get(b.en).has(c) ? "has-song" : "" }, String(c)));
      det.append(grid); wrap.append(det);
    }
  }
  renderSiddurToc();
  renderRecent();
}
function renderSiddurToc() {
  const st = $("#siddurToc"); st.innerHTML = "";
  const n = nusach();
  const sel = el("select", { id: "nusachToc", onchange: (e) => setNusach(e.target.value) });
  for (const x of data.siddur.nusachot) sel.append(el("option", { value: x.id, selected: x.id === n.id }, `${x.title} · ${x.heTitle}`));
  st.append(el("div", { class: "nusach-row" }, "Nusach", sel));
  if (n.note) st.append(el("p", { class: "fine", style: "margin:0 1rem .5rem" }, n.note));
  const groups = new Map();
  n.leaves.forEach((l, i) => { const key = l.path.slice(0, 2).join(" / "); if (!groups.has(key)) groups.set(key, { he: l.hePath.slice(0, 2).join(" / "), items: [] }); groups.get(key).items.push([l, i]); });
  let lastTop = "";
  for (const [key, g] of groups) {
    const top = key.split(" / ")[0];
    if (top !== lastTop) { st.append(el("h4", {}, top)); lastTop = top; }
    const det = el("details", { "data-group": key }, el("summary", {}, key.split(" / ").slice(1).join(" / ") || key, el("span", { class: "he-inline" }, g.he.split(" / ").slice(1).join(" / "))));
    for (const [l, i] of g.items) {
      const sub = l.path.length > 3 ? l.path.slice(2, -1).join(" › ") + " › " : "";
      det.append(el("a", { href: `#s/${n.id}/${encodeURIComponent(l.ref)}/1`, "data-leaf": i }, el("span", {}, el("small", {}, sub), l.title), el("span", { class: "he-inline" }, l.he)));
    }
    st.append(det);
  }
  const ns = $("#nusachSelect"); ns.innerHTML = ""; for (const x of data.siddur.nusachot) ns.append(el("option", { value: x.id, selected: x.id === n.id }, x.title));
}
function setNusach(id) {
  if (id === state.nusach) return;
  const cur = state.mode === "siddur" ? leaf() : null;
  state.nusach = id; store.set("hz:nusach", id); renderSiddurToc();
  if (cur) { const n = nusach(); let li = n.leaves.findIndex((l) => normHe(l.he) && normHe(l.he) === normHe(cur.he)); if (li < 0) li = 0; location.hash = `#s/${n.id}/${encodeURIComponent(n.leaves[li].ref)}/1`; }
}
function renderRecent() {
  const r = store.get("hz:recent", []); const box = $("#recent"); box.innerHTML = ""; box.hidden = !r.length;
  if (!r.length) return;
  box.append(el("h4", {}, "Recent"));
  for (const x of r.slice(0, 6)) box.append(el("a", { href: x.hash }, x.title, el("span", { class: "he-inline" }, x.he || "")));
}
function pushRecent(hash, title, he) {
  const r = store.get("hz:recent", []).filter((x) => x.hash !== hash); r.unshift({ hash, title, he }); store.set("hz:recent", r.slice(0, 8)); renderRecent();
}
function setMode(mode) {
  state.mode = mode; document.body.dataset.mode = mode;
  document.querySelectorAll(".mode button").forEach((b) => b.classList.toggle("active", b.dataset.mode === mode));
  $("#tocList").hidden = mode !== "tanakh"; $("#siddurToc").hidden = mode !== "siddur";
}
function setLibrary(open) { document.body.classList.toggle("focus", !open); $("#menuBtn").setAttribute("aria-expanded", String(open)); }

/* ---------------- rendering ---------------- */
async function showPassage(target) {
  const status = $("#readerStatus"); status.hidden = false; status.textContent = "Loading from Sefaria…";
  $("#welcome").hidden = true; $("#chapterHead").hidden = false;
  player.stop(); closeEmbeds(); stopPreview();
  setMode(target.mode);
  let ref, verse = target.verse || 1;
  if (target.mode === "tanakh") { state.book = target.book; state.chapter = target.chapter; ref = `${state.book} ${state.chapter}`; }
  else { if (target.nusach && target.nusach !== state.nusach) { state.nusach = target.nusach; store.set("hz:nusach", target.nusach); renderSiddurToc(); } state.leaf = target.leaf; ref = leaf().ref; }
  try { state.text = await fetchText(ref); diag("text ok " + ref); }
  catch (e) { diag("text FAIL " + e.message); status.textContent = `Could not load ${ref}: ${e.message}. Check your connection.`; return; }
  status.hidden = true;
  const n = state.text.he.length;
  const ali = $("#aliyot"); ali.hidden = true; ali.innerHTML = "";
  if (state.mode === "tanakh") {
    const info = bookInfo(state.book), p = isTorah() ? parshaOf(state.book, state.chapter, 1) : null;
    $("#locBtn").textContent = `${state.book} ${state.chapter}`;
    $("#chapTitleHe").textContent = state.text.heRef || `${info.he} ${state.chapter}`;
    $("#chapTitleEn").textContent = `${state.book} ${state.chapter} · ${n} verses`;
    $("#chapterParsha").innerHTML = p ? `Parashat <b>${p.id}</b> <span class="he-inline">${p.he}</span>` : (isTorah() ? "" : `<b>${info.sec}</b>`);
    document.querySelectorAll("#tocList a").forEach((a) => a.classList.toggle("active", (!!p && a.dataset.parsha === p.id) || a.dataset.chapter === `${state.book}.${state.chapter}`));
    const det = document.querySelector(`#tocList details[data-book="${state.book}"]`); if (det) det.open = true;
    $("#prevChap").disabled = state.book === "Genesis" && state.chapter === 1;
    $("#nextChap").disabled = state.book === "II Chronicles" && state.chapter === info.ch;
    $("#playChapter").hidden = !isTorah();
    $("#playChapter").disabled = !data.kriah?.verses?.[state.book]?.[`${state.chapter}:1`];
    if (p) {
      ali.hidden = false; ali.append(el("span", { class: "lab" }, "Aliyot"));
      for (const a of p.aliyot) {
        const q = aliyahQueue(p, a);
        ali.append(el("button", { "data-aliyah": a.n, disabled: !q.length, title: `${p.book} ${a.begin}–${a.end}${q.length ? " · play" : " · no recording"}`, onclick: (e) => { const b = e.currentTarget; if (b.classList.contains("playing")) { player.stop(); return; } player.playQueue(q, `Aliyah ${a.n} ·`); document.querySelectorAll(".aliyot button.playing").forEach((x) => x.classList.remove("playing")); b.classList.add("playing"); } }, a.n === "M" ? "Maftir" : a.n));
      }
      if (!data.kriah?.files?.[p.id] && CHABAD_PAGES[p.id]) ali.append(el("a", { class: "chip", href: CHABAD_PAGES[p.id], target: "_blank", rel: "noopener" }, "Hear this parasha on Chabad.org ↗"));
    }
    pushRecent(`#${state.book}.${state.chapter}.1`, p ? `${p.id} · ${state.book} ${state.chapter}` : `${state.book} ${state.chapter}`, p ? stripMarks(p.he) : info.he);
  } else {
    const l = leaf(), nu = nusach();
    $("#locBtn").textContent = l.title;
    $("#chapTitleHe").textContent = l.he;
    $("#chapTitleEn").textContent = `${l.path.join(" › ")} · ${n} paragraph${n === 1 ? "" : "s"}`;
    $("#chapterParsha").innerHTML = `<b>${nu.title}</b> <span class="he-inline">${nu.heTitle}</span>`;
    document.querySelectorAll("#siddurToc a").forEach((a) => a.classList.toggle("active", +a.dataset.leaf === state.leaf));
    const det = document.querySelector(`#siddurToc details[data-group="${l.path.slice(0, 2).join(" / ")}"]`); if (det) det.open = true;
    $("#prevChap").disabled = state.leaf === 0;
    $("#nextChap").disabled = state.leaf === nu.leaves.length - 1;
    $("#playChapter").hidden = true;
    pushRecent(`#s/${nu.id}/${encodeURIComponent(l.ref)}/1`, l.title, l.he);
  }
  renderVerses();
  $("#reader").scrollTop = 0;
  selectVerse(Math.min(verse, n) || 1, { scroll: verse > 1 });
  if ($("#autoHide").checked) setLibrary(false);
}
function renderVerses() {
  const songMap = segmentsWithSongs(), artMap = segmentsWithArt();
  const list = $("#verses"); list.innerHTML = "";
  const tikkun = document.body.classList.contains("tikkun");
  state.text.he.forEach((heV, i) => {
    const v = i + 1;
    const heEl = el("div", { class: "txt-he", lang: "he" });
    if (state.mode === "tanakh") {
      const words = tokenize(heV);
      const t = isTorah() ? timingFor(state.book, state.chapter, v) : null;
      const aligned = t?.times && t.times.length - 1 === words.length;
      words.forEach((w, wi) => { heEl.append(el("span", { class: `w approx ${phraseClass(w)}`, "data-i": aligned ? wi : null }, tikkun ? tikkunText(w) : w)); heEl.append(" "); });
    } else { heEl.classList.add("prose"); heEl.innerHTML = tikkun ? stripMarks(heV) : heV; }
    const li = el("li", { class: "verse", "data-v": v, tabindex: 0, onclick: () => selectVerse(v), onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); selectVerse(v); } } },
      el("div", { class: "n" }, songMap.has(v) ? el("span", { class: "dot", title: `${songMap.get(v).length} song(s) here` }) : null, artMap.has(v) ? el("span", { class: "dot art", title: `${artMap.get(v).length} artwork(s) here` }) : null, String(v)),
      el("div", {}, heEl, el("div", { class: "txt-en", html: state.text.en[i] || "" })));
    list.append(li);
  });
}
function selectVerse(v, { scroll = false, silentHash = false } = {}) {
  state.verse = v;
  document.querySelectorAll(".verse.selected").forEach((n) => n.classList.remove("selected"));
  const ve = verseEl(v); if (ve) { ve.classList.add("selected"); if (scroll) ve.scrollIntoView?.({ block: "center", behavior: "smooth" }); }
  if (!silentHash) { const h = hashFor(v); if (location.hash !== h) history.replaceState(null, "", h); }
  document.querySelectorAll(".aliyot button").forEach((b) => { const p = parshaOf(state.book, state.chapter, v); const a = p && aliyahOf(p, state.chapter, v); b.classList.toggle("here", !!a && b.dataset.aliyah === a.n); });
  renderKriah(); renderSongs(); renderArt();
}
const hashFor = (v) => (state.mode === "tanakh" ? `#${state.book}.${state.chapter}.${v}` : `#s/${nusach().id}/${encodeURIComponent(leaf().ref)}/${v}`);

function renderKriah() {
  const v = state.verse;
  $("#tropRefHe").textContent = currentHeRef(v); $("#tropRefText").textContent = currentRef(v);
  $("#sefariaLink").href = sefariaUrl(state.mode === "tanakh" ? currentRef(v) : leaf().ref);
  const torahOnly = $("#tropTorah"), note = $("#tropSiddurNote");
  if (state.mode === "siddur") {
    torahOnly.hidden = true; note.hidden = false; note.innerHTML = "";
    note.append(el("p", {}, "The siddur is davened in nusach rather than chanted with trop. Recordings of this passage live in the ", el("a", { href: "#", onclick: (e) => { e.preventDefault(); setTab("songs"); } }, "Songs"), " tab."));
    const hits = searchAll(leaf().title, 4).filter((r) => r.kind === "ref" || r.kind === "parasha");
    return;
  }
  torahOnly.hidden = false; note.hidden = true;
  const { book, chapter: c } = state;
  const heV = state.text.he[v - 1] || "";
  const t = isTorah() ? timingFor(book, c, v) : null;
  const words = tokenize(heV);
  const notice = $("#tropNoAudio");
  const p = isTorah() ? parshaOf(book, c, v) : null, a = aliyahOf(p, c, v);
  if (!isTorah()) { notice.hidden = false; notice.textContent = "Recordings are available for the Torah. The trop of each word is shown below."; }
  else if (!t) { notice.hidden = false; notice.innerHTML = ""; notice.append("No recording is indexed for this verse. ", p && CHABAD_PAGES[p.id] ? el("a", { href: CHABAD_PAGES[p.id], target: "_blank", rel: "noopener" }, `Hear Parashat ${p.id} on Chabad.org ↗`) : el("a", { href: CHABAD_ALL, target: "_blank", rel: "noopener" }, "Chabad.org recordings ↗")); }
  else notice.hidden = true;
  $("#playVerse").disabled = !t; $("#playFromHere").disabled = !t;
  $(".player").hidden = !isTorah();
  const ul = $("#wordList"); ul.innerHTML = "";
  const aligned = t && t.times.length - 1 === words.length;
  words.forEach((w, i) => {
    const tr = tropesIn(w);
    ul.append(el("li", { "data-i": i, onclick: () => aligned && player.seekWord(book, c, v, i), title: aligned ? "Play from about this word" : "" },
      el("span", { class: "i" }, String(i + 1)),
      el("span", { class: "w", lang: "he" }, w),
      el("span", { class: "t" }, tr.length ? tr.map(([en, he, cls]) => el("span", { class: `trope ${cls}`, title: he }, en)) : el("span", { class: "trope other" }, "—"))));
  });
  const attr = $("#attribution"); attr.querySelector(".ctx")?.remove();
  if (t && p && a) attr.append(el("div", { class: "ctx" }, `Parashat ${p.id}, aliyah ${a.n} (${p.book} ${a.begin}–${a.end}) · verse timings computed from pauses, word highlight approximate · text ${state.text.heVersion}`));
}

function renderSongs() {
  const v = state.verse;
  $("#songRefHe").textContent = currentHeRef(v); $("#songRefEn").textContent = currentRef(v);
  $("#ytNote").hidden = !state.ytBlocked;
  const list = $("#songList"); list.innerHTML = "";
  const songs = songsOn(v);
  if (!songs.length) list.append(el("div", { class: "empty" }, state.mode === "tanakh" ? "No songs catalogued on this verse yet. Know one? Paste a link below." : "No recordings catalogued for this passage yet. Paste one below."));
  for (const s of songs) list.append(songCard(s));
  const cs = $("#chapterSongs"); cs.innerHTML = "";
  const map = segmentsWithSongs();
  const others = [...map.entries()].filter(([vv]) => vv !== v).sort((a, b) => a[0] - b[0]);
  $("#chapterSongsH").textContent = state.mode === "tanakh" ? "Elsewhere in this chapter" : "Elsewhere in this passage";
  if (!others.length) cs.append(el("div", { class: "fine" }, state.mode === "tanakh" ? "No other verses in this chapter have songs yet." : "Nothing else here yet."));
  for (const [vv, ss] of others) cs.append(el("a", { href: hashFor(vv), onclick: (e) => { e.preventDefault(); selectVerse(vv, { scroll: true }); } },
    el("span", {}, el("b", {}, state.mode === "tanakh" ? `${state.chapter}:${vv}` : `¶ ${vv}`), ` ${[...new Set(ss.map((x) => x.title))].join(", ")}`), el("span", { class: "he-inline" }, ss[0].title_he || "")));
}
function recRow(r) {
  const isYt = !!r.id;
  const row = el("button", { class: `rec ${isYt ? "yt" : "am"}`, type: "button", title: isYt ? "Play here (YouTube)" : "Play 30-second preview (Apple Music)" },
    el("img", { src: isYt ? `https://i.ytimg.com/vi/${r.id}/mqdefault.jpg` : r.art, alt: "", loading: "lazy" }),
    el("span", { class: "rec-meta" }, el("span", { class: "rec-title" }, isYt ? r.title : r.track), el("span", { class: "rec-sub" }, isYt ? r.channel : [r.artist, r.album].filter(Boolean).join(" · ")), el("span", { class: "rec-src" }, isYt ? "YouTube" : "Apple Music · preview")),
    el("span", { class: "rec-play" }, "▶"));
  row.onclick = () => {
    const open = row.classList.contains("playing");
    closeEmbeds(); stopPreview(); player.stop();
    if (open) return;
    row.classList.add("playing");
    if (isYt) row.after(el("iframe", { class: "embed", src: `https://www.youtube-nocookie.com/embed/${r.id}?autoplay=1&rel=0`, allow: "autoplay; encrypted-media; picture-in-picture", allowfullscreen: true, title: r.title }));
    else { preview.src = r.preview; preview.play().catch(() => {}); preview.onended = () => row.classList.remove("playing"); }
  };
  return row;
}
function songCard(s) {
  const q = encodeURIComponent(s.recordings_query || `${s.title_he || s.title} ${s.performer && !/traditional|various|liturgical|children|many|zemer|kiddush|nusach|niggun|pesukim/i.test(s.performer) ? s.performer.split(/[;,(]/)[0] : ""}`.trim());
  const card = el("div", { class: "song" },
    el("div", { class: "song-head" }, el("div", { class: "song-title" }, s.title, s.title_he ? el("span", { class: "he-inline" }, s.title_he) : null), el("span", { class: `badge ${s.mine ? "mine" : s.type}` }, s.mine ? "mine" : s.type)),
    el("div", { class: "song-meta" }, [s.performer, s.year].filter(Boolean).join(" · ")),
    s.words ? el("div", { class: "song-words", lang: "he" }, s.words) : null,
    s.note ? el("p", { class: "song-note" }, s.note) : null);
  const hidden = new Set(data.hidden);
  const recs = [];
  for (const r of s.itunes || []) if (!hidden.has(r.preview)) recs.push(r);
  const uid = ytId(s.youtube); if (uid && !state.ytBlocked) recs.push({ id: uid, title: "Your link", channel: "" });
  if (!state.ytBlocked) for (const r of s.recordings || []) if (r.id && !hidden.has(r.id) && !recs.some((x) => x.id === r.id)) recs.push(r);
  if (recs.length) {
    const wrap = el("div", { class: "recs" });
    for (const r of recs) {
      const row = recRow(r); wrap.append(row);
      wrap.append(el("div", { class: "rec-more" }, r.url ? el("a", { href: r.url, target: "_blank", rel: "noopener" }, "Full track on Apple Music ↗") : null,
        el("button", { class: "hide-rec", type: "button", title: "Hide this recording on this device", onclick: () => { data.hidden.push(r.id || r.preview); store.set("hz:hidden", data.hidden); renderSongs(); } }, "hide")));
    }
    card.append(wrap);
  }
  card.append(el("div", { class: "song-actions" },
    el("a", { class: "btn", target: "_blank", rel: "noopener", href: `https://music.apple.com/us/search?term=${q}` }, "Apple Music"),
    el("a", { class: "btn", target: "_blank", rel: "noopener", href: `https://www.youtube.com/results?search_query=${q}`, title: state.ytBlocked ? "YouTube is blocked on this device" : "" }, "YouTube"),
    s.mine ? el("button", { class: "btn quiet", onclick: () => { data.mine = data.mine.filter((x) => x.id !== s.id); saveMine(); refresh(); } }, "Remove") : null));
  return card;
}
function saveMine() { store.set("hz:mysongs", data.mine); }
function refresh() { showPassage(state.mode === "tanakh" ? { mode: "tanakh", book: state.book, chapter: state.chapter, verse: state.verse } : { mode: "siddur", leaf: state.leaf, verse: state.verse }); }

// one-field add: a YouTube / Apple Music link, or just a name
async function addSong(q) {
  q = q.trim(); if (!q) return;
  const ref = state.mode === "tanakh" ? currentRef(state.verse) : leaf().ref;
  const song = { id: `mine-${Date.now()}`, title: q, title_he: null, performer: null, year: null, type: "verbatim", refs: [ref], youtube: null, itunes: [], note: "", added: new Date().toISOString().slice(0, 10) };
  const hint = $("#addSongHint"); hint.textContent = "Looking up…";
  const yid = ytId(q);
  if (yid) {
    song.youtube = `https://www.youtube.com/watch?v=${yid}`; song.title = "YouTube recording";
    try { const j = await (await fetch(`https://noembed.com/embed?url=https://www.youtube.com/watch?v=${yid}`)).json(); if (j.title) { song.title = j.title; song.performer = j.author_name || null; } } catch {}
  } else if (/music\.apple\.com/.test(q)) {
    const m = q.match(/i=(\d+)/) || q.match(/\/(\d+)(?:\?|$)/);
    if (m) { try { const j = await (await fetch(`https://itunes.apple.com/lookup?id=${m[1]}`)).json(); const r = j.results?.find((x) => x.previewUrl) || j.results?.[0]; if (r) { song.title = r.trackName || r.collectionName; song.performer = r.artistName; if (r.previewUrl) song.itunes = [{ track: r.trackName, artist: r.artistName, album: r.collectionName, preview: r.previewUrl, url: r.trackViewUrl, art: (r.artworkUrl100 || "").replace("100x100", "300x300") }]; } } catch {} }
  } else {
    try { const j = await (await fetch(`https://itunes.apple.com/search?term=${encodeURIComponent(q)}&entity=song&limit=3`)).json(); song.itunes = (j.results || []).filter((r) => r.previewUrl).map((r) => ({ track: r.trackName, artist: r.artistName, album: r.collectionName, preview: r.previewUrl, url: r.trackViewUrl, art: (r.artworkUrl100 || "").replace("100x100", "300x300") })); if (song.itunes[0]) song.performer = song.itunes[0].artist; } catch {}
  }
  data.mine.push(song); saveMine(); hint.textContent = `Added "${song.title}" on ${ref}.`; renderSongs();
}

/* ---------------- song book ---------------- */
function openSongbook() {
  const sb = $("#songbook"); sb.hidden = false;
  const bookSel = $("#songbookBook");
  if (bookSel.options.length === 1) { for (const sec of ["Torah", "Nevi'im", "Ketuvim"]) { const og = el("optgroup", { label: sec }); for (const b of BOOKS.filter((b) => b.sec === sec)) og.append(el("option", { value: b.en }, b.en)); bookSel.append(og); } bookSel.append(el("option", { value: "Siddur" }, "Siddur")); }
  renderSongbook(); setTimeout(() => $("#songbookSearch").focus(), 30);
}
function renderSongbook() {
  const q = normQ($("#songbookSearch").value), type = $("#songbookType").value, book = $("#songbookBook").value;
  const list = $("#songbookList"); list.innerHTML = "";
  const rows = allSongs().filter((s) => (!type || s.type === type) && (!book || s.refs.some((r) => book === "Siddur" ? r.startsWith("Siddur") : r.startsWith(book + " "))) &&
    (!q || normQ(s.title).includes(q) || normQ(s.title_he || "").includes(q) || normQ(s.performer || "").includes(q) || normQ(s.refs.join(" ")).includes(q) || normQ(s.words || "").includes(q)))
    .sort((a, b) => a.title.localeCompare(b.title));
  $("#songbookCount").textContent = `${rows.length} of ${allSongs().length} songs`;
  for (const s of rows) {
    const r = s.refs[0].replace(/^Siddur (Ashkenaz|Sefard|Chabad), /, "");
    list.append(el("a", { class: "sb", href: hashForRef(s.refs[0]), onclick: () => { $("#songbook").hidden = true; setTab("songs"); } },
      el("span", {}, el("b", {}, s.title), s.title_he ? el("span", { class: "he-inline" }, s.title_he) : null, el("small", {}, [s.performer, s.type, (s.itunes?.length || s.recordings?.length) ? `${(s.itunes?.length || 0) + (s.recordings?.length || 0)} recordings` : ""].filter(Boolean).join(" · "))),
      el("span", { class: "ref" }, r)));
  }
}

/* ---------------- song map (heatmap of songs per chapter / passage) ---------------- */
function songCounts() {
  const tanakh = new Map();  // "Book" -> Map(chapter -> Set(song ids))
  const siddur = new Map();  // leaf index in current nusach -> Set(song ids)
  const n = nusach();
  for (const s of allSongs()) for (const r of s.refs) {
    const g = parseRange(r);
    if (g) { if (!tanakh.has(g.book)) tanakh.set(g.book, new Map()); const m = tanakh.get(g.book); for (let c = g.from[0]; c <= g.to[0]; c++) { if (!m.has(c)) m.set(c, new Set()); m.get(c).add(s.id); } continue; }
    const hit = siddurRefLeaf(r); if (!hit) continue;
    let li = n.leaves.indexOf(hit.l); if (li < 0) li = n.leaves.findIndex((l) => normHe(l.he) && normHe(l.he) === normHe(hit.l.he));
    if (li >= 0) { if (!siddur.has(li)) siddur.set(li, new Set()); siddur.get(li).add(s.id); }
  }
  return { tanakh, siddur };
}
const heat = (k) => (k >= 6 ? "h5" : k >= 4 ? "h4" : k >= 3 ? "h3" : k >= 2 ? "h2" : k >= 1 ? "h1" : "");
function artCounts() {
  const tanakh = new Map();
  for (const w of data.art) for (const r of w.refs) { const g = parseRange(r); if (!g) continue; if (!tanakh.has(g.book)) tanakh.set(g.book, new Map()); const m = tanakh.get(g.book); for (let c = g.from[0]; c <= g.to[0]; c++) { if (!m.has(c)) m.set(c, new Set()); m.get(c).add(w.id); } }
  return { tanakh, siddur: new Map() };
}
function renderSongMap() {
  const grid = $("#songmapGrid"); grid.innerHTML = "";
  const artMode = state.map === "art";
  document.body.classList.toggle("map-art", artMode);
  document.querySelectorAll(".map-toggle button").forEach((b) => b.classList.toggle("active", b.dataset.map === (artMode ? "art" : "songs")));
  const { tanakh, siddur } = artMode ? artCounts() : songCounts();
  const byId = new Map((artMode ? data.art : allSongs()).map((s) => [s.id, s]));
  const names = (set) => [...set].slice(0, 6).map((id) => byId.get(id)?.title).filter(Boolean).join(", ") + (set.size > 6 ? "…" : "");
  let total = 0;
  for (const sec of ["Torah", "Nevi'im", "Ketuvim"]) {
    grid.append(el("div", { class: "sm-sec" }, sec));
    for (const b of BOOKS.filter((b) => b.sec === sec)) {
      const m = tanakh.get(b.en) || new Map();
      const count = [...m.values()].reduce((a, x) => a + x.size, 0); total += count;
      const cells = el("div", { class: "sm-cells" });
      for (let c = 1; c <= b.ch; c++) { const k = m.get(c)?.size || 0; cells.append(el("a", { href: `#${b.en}.${c}.1`, class: heat(k), title: `${b.en} ${c}` + (k ? ` · ${k} ${artMode ? "work" : "song"}${k > 1 ? "s" : ""}: ${names(m.get(c))}` : ""), onclick: () => setTab(artMode ? "art" : "songs") })); }
      grid.append(el("div", { class: "sm-row" }, el("div", { class: "sm-name" }, el("span", {}, b.en), el("span", { class: "he-inline" }, b.he)), cells));
    }
  }
  const n = nusach();
  if (artMode) { $("#songmapCount").textContent = `${data.art.length} artworks · ${total} placements`; return; }
  grid.append(el("div", { class: "sm-sec" }, `Siddur · ${n.title}`));
  const groups = new Map();
  n.leaves.forEach((l, i) => { const key = l.path.slice(0, 2).join(" / "); if (!groups.has(key)) groups.set(key, []); groups.get(key).push(i); });
  for (const [key, idxs] of groups) {
    const cells = el("div", { class: "sm-cells" }); let count = 0;
    for (const i of idxs) { const k = siddur.get(i)?.size || 0; count += k; const l = n.leaves[i]; cells.append(el("a", { href: `#s/${n.id}/${encodeURIComponent(l.ref)}/1`, class: `wide ${heat(k)}`, title: l.title + (k ? ` · ${k}: ${names(siddur.get(i))}` : ""), onclick: () => setTab("songs") }, l.title.length > 22 ? l.title.slice(0, 20) + "…" : l.title)); }
    total += count;
    const [top, sub] = key.split(" / ");
    grid.append(el("div", { class: "sm-row" }, el("div", { class: "sm-name" }, el("span", {}, sub || top), el("span", { class: "he-inline" }, (n.leaves[idxs[0]].hePath[1] || n.leaves[idxs[0]].hePath[0] || ""))), cells));
  }
  $("#songmapCount").textContent = `${allSongs().length} songs · ${total} placements`;
}
/* ---------------- this week's parasha (Hebcal, diaspora) ---------------- */
async function loadWeek() {
  const cached = store.get("hz:week", null);
  const today = new Date().toISOString().slice(0, 10);
  let week = cached && cached.day === today ? cached : null;
  if (!week) {
    try {
      const d = new Date(); const j = await (await fetch(`https://www.hebcal.com/hebcal?v=1&cfg=json&s=on&i=off&year=${d.getFullYear()}&month=${d.getMonth() + 1}`)).json();
      const items = (j.items || []).filter((i) => i.category === "parashat" && i.date >= today);
      if (!items.length) { const d2 = new Date(d.getFullYear(), d.getMonth() + 1, 1); const j2 = await (await fetch(`https://www.hebcal.com/hebcal?v=1&cfg=json&s=on&i=off&year=${d2.getFullYear()}&month=${d2.getMonth() + 1}`)).json(); items.push(...(j2.items || []).filter((i) => i.category === "parashat")); }
      const it = items[0]; if (it) week = { day: today, date: it.date, title: it.title.replace(/^Parashat\s+/, ""), he: it.hebrew?.replace(/^פרשת\s+/, "") || "" };
    } catch {}
    if (week) store.set("hz:week", week);
  }
  if (!week) return;
  state.week = week.title.split("-")[0].trim();
  const p = data.parshiot.find((p) => normQ(p.id) === normQ(state.week)) || data.parshiot.find((p) => normQ(p.id).startsWith(normQ(state.week).slice(0, 5)));
  if (!p) return;
  const [c, v] = p.begin.split(":").map(Number); const href = `#${p.book}.${c}.${v}`;
  $("#welcomeWeek").href = href; $("#welcomeWeek").textContent = `This week: ${week.title}`;
  document.querySelectorAll("#tocList a[data-parsha]").forEach((a) => a.classList.toggle("week", a.dataset.parsha === p.id));
}
// is youtube.com reachable? (the kosher filter maps it to 127.0.0.1)
function detectYouTube() {
  return new Promise((res) => { const img = new Image(); const t = setTimeout(() => res(false), 4000); img.onload = () => { clearTimeout(t); res(true); }; img.onerror = () => { clearTimeout(t); res(false); }; img.src = "https://www.youtube.com/favicon.ico?" + Date.now(); });
}

/* ---------------- navigation ---------------- */
function parseHash() {
  const h = decodeURIComponent(location.hash.slice(1));
  let m = h.match(/^s\/(chabad|sefard|ashkenaz)\/(.+?)(?:\/(\d+))?$/);
  if (m) { const n = data.siddur.nusachot.find((x) => x.id === m[1]); const li = n.leaves.findIndex((l) => l.ref === m[2]); if (li >= 0) return { mode: "siddur", nusach: n.id, leaf: li, verse: +m[3] || 1 }; return null; }
  m = h.match(/^s\/(.+?)(?:\/(\d+))?$/);  // legacy: Ashkenaz refs
  if (m) { for (const n of data.siddur.nusachot) { const li = n.leaves.findIndex((l) => l.ref === m[1]); if (li >= 0) return { mode: "siddur", nusach: n.id, leaf: li, verse: +m[2] || 1 }; } return null; }
  m = h.match(/^(.+?)[. ](\d+)(?:[.:](\d+))?$/);
  if (!m) return null;
  const book = ALIASES[m[1].toLowerCase().replace(/[\s'_]/g, "")]; if (!book) return null;
  return { mode: "tanakh", book, chapter: Math.min(+m[2], bookInfo(book).ch) || 1, verse: +m[3] || 1 };
}
function go(t) {
  const same = state.text && t.mode === state.mode && (t.mode === "tanakh" ? t.book === state.book && t.chapter === state.chapter : t.leaf === state.leaf && (!t.nusach || t.nusach === state.nusach));
  if (same) selectVerse(t.verse, { scroll: true }); else showPassage(t);
}
function step(delta) {
  if (state.mode === "siddur") { const n = nusach(); const i = state.leaf + delta; if (i >= 0 && i < n.leaves.length) location.hash = `#s/${n.id}/${encodeURIComponent(n.leaves[i].ref)}/1`; return; }
  let bi = BOOKS.findIndex((b) => b.en === state.book), c = state.chapter + delta;
  if (c < 1) { if (bi === 0) return; bi--; c = BOOKS[bi].ch; }
  else if (c > BOOKS[bi].ch) { if (bi === BOOKS.length - 1) return; bi++; c = 1; }
  location.hash = `#${BOOKS[bi].en}.${c}.1`;
}
function setTab(name) {
  state.tab = name;
  document.querySelectorAll(".tab").forEach((x) => { const on = x.dataset.tab === name; x.classList.toggle("active", on); x.setAttribute("aria-selected", on); });
  document.querySelectorAll(".tabpane").forEach((p) => p.hidden = p.id !== `tab-${name}`);
}

function wire() {
  $("#prevChap").onclick = () => step(-1);
  $("#nextChap").onclick = () => step(1);
  $("#menuBtn").onclick = () => setLibrary(document.body.classList.contains("focus"));
  $("#locBtn").onclick = () => setLibrary(true);
  $("#brandLink").onclick = (e) => { e.preventDefault(); showWelcome(); };
  document.querySelectorAll(".mode button").forEach((b) => b.onclick = () => { setMode(b.dataset.mode); });
  // go-to with live hints
  const input = $("#gotoInput"), hints = $("#gotoHints"); let hi = -1;
  const showHints = () => { const rs = searchAll(input.value); hints.innerHTML = ""; hi = -1; hints.hidden = !rs.length; for (const r of rs) hints.append(el("a", { href: r.hash, onclick: () => { hints.hidden = true; input.value = ""; } }, el("span", {}, r.title, " ", el("small", {}, r.kind)), el("span", { class: "he-inline" }, r.he))); };
  input.oninput = showHints; input.onfocus = showHints;
  input.onkeydown = (e) => { const as = [...hints.querySelectorAll("a")]; if (e.key === "ArrowDown") { hi = Math.min(as.length - 1, hi + 1); as.forEach((a, i) => a.classList.toggle("active", i === hi)); e.preventDefault(); } if (e.key === "ArrowUp") { hi = Math.max(0, hi - 1); as.forEach((a, i) => a.classList.toggle("active", i === hi)); e.preventDefault(); } if (e.key === "Escape") { hints.hidden = true; input.blur(); } };
  document.addEventListener("click", (e) => { if (!e.target.closest(".goto")) hints.hidden = true; });
  $("#gotoForm").onsubmit = (e) => { e.preventDefault(); const rs = searchAll(input.value); const r = rs[hi >= 0 ? hi : 0]; if (!r) { input.setCustomValidity("Try: Genesis 1:1, תהלים כג, a parasha, a prayer, or a song"); input.reportValidity(); return; } input.setCustomValidity(""); input.value = ""; hints.hidden = true; location.hash = r.hash; };
  input.oninput = (e) => { e.target.setCustomValidity(""); showHints(); };
  // settings
  $("#showEn").onchange = (e) => { document.body.classList.toggle("hide-en", !e.target.checked); store.set("hz:en", e.target.checked); };
  $("#showSongDots").onchange = (e) => document.body.classList.toggle("hide-dots", !e.target.checked);
  $("#tikkun").onchange = (e) => { document.body.classList.toggle("tikkun", e.target.checked); store.set("hz:tikkun", e.target.checked); if (state.text) { renderVerses(); selectVerse(state.verse, { silentHash: true }); } };
  $("#phraseColors").onchange = (e) => { document.body.classList.toggle("phrase", e.target.checked); store.set("hz:phrase", e.target.checked); };
  $("#autoHide").onchange = (e) => store.set("hz:autohide", e.target.checked);
  $("#nusachSelect").onchange = (e) => setNusach(e.target.value);
  document.querySelectorAll(".tab").forEach((t) => t.onclick = () => setTab(t.dataset.tab));
  const chapterQueue = () => state.text.he.map((_, i) => ({ book: state.book, c: state.chapter, v: i + 1 })).filter((x) => timingFor(x.book, x.c, x.v));
  $("#playVerse").onclick = () => { player.queue = []; player.playVerse(state.book, state.chapter, state.verse); };
  $("#playFromHere").onclick = () => player.playQueue(chapterQueue().filter((x) => x.v >= state.verse));
  $("#playChapter").onclick = () => player.playQueue(chapterQueue());
  $("#stopBtn").onclick = () => player.stop();
  $("#rate").onchange = (e) => { audio.playbackRate = +e.target.value; };
  $("#recBtn").onclick = toggleRecord;
  $("#recPlay").onclick = () => { if (rec.url) { player.stop(); stopPreview(); preview.src = rec.url; preview.play(); } };
  $("#addSongForm").onsubmit = (e) => { e.preventDefault(); const f = e.target.elements.q; addSong(f.value); f.value = ""; };
  $("#exportSongs").onclick = () => { const blob = new Blob([JSON.stringify({ songs: data.mine }, null, 2)], { type: "application/json" }); const a = el("a", { href: URL.createObjectURL(blob), download: "my-songs.json" }); document.body.append(a); a.click(); a.remove(); };
  $("#songbookBtn").onclick = openSongbook; $("#welcomeSongbook").onclick = openSongbook;
  const ex = $("#exploreInput"), exh = $("#exploreHints"); let ei = -1;
  const exHints = () => { const rs = searchAll(ex.value); exh.innerHTML = ""; ei = -1; exh.hidden = !rs.length; for (const r of rs) exh.append(el("a", { href: r.hash, onclick: () => { exh.hidden = true; ex.value = ""; } }, el("span", {}, r.title, " ", el("small", {}, r.kind)), el("span", { class: "he-inline" }, r.he))); };
  ex.oninput = exHints; ex.onfocus = exHints;
  ex.onkeydown = (e) => { const as = [...exh.querySelectorAll("a")]; if (e.key === "ArrowDown") { ei = Math.min(as.length - 1, ei + 1); as.forEach((a, i) => a.classList.toggle("active", i === ei)); e.preventDefault(); } if (e.key === "ArrowUp") { ei = Math.max(0, ei - 1); as.forEach((a, i) => a.classList.toggle("active", i === ei)); e.preventDefault(); } if (e.key === "Enter") { e.preventDefault(); const r = searchAll(ex.value)[ei >= 0 ? ei : 0]; if (r) { ex.value = ""; exh.hidden = true; location.hash = r.hash; } } if (e.key === "Escape") { exh.hidden = true; ex.blur(); } };
  $("#exploreLibrary").onclick = () => setLibrary(true);
  document.querySelectorAll(".map-toggle button").forEach((b) => b.onclick = () => { state.map = b.dataset.map; store.set("hz:map", state.map); renderSongMap(); });
  $("#lightboxClose").onclick = () => { $("#lightbox").hidden = true; };
  $("#lightbox").onclick = (e) => { if (e.target === e.currentTarget) e.currentTarget.hidden = true; };
  $("#exploreSiddur").onclick = (e) => { e.preventDefault(); const n = nusach(); location.hash = `#s/${n.id}/${encodeURIComponent(n.leaves[0].ref)}/1`; };
  $("#songbookClose").onclick = () => { $("#songbook").hidden = true; };
  $("#songbook").onclick = (e) => { if (e.target === e.currentTarget) e.currentTarget.hidden = true; };
  $("#songbookSearch").oninput = renderSongbook; $("#songbookType").onchange = renderSongbook; $("#songbookBook").onchange = renderSongbook;
  window.addEventListener("hashchange", () => { const r = parseHash(); if (r) go(r); });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { $("#songbook").hidden = true; $("#lightbox").hidden = true; return; }
    if (e.target.matches("input,select,textarea") || e.metaKey || e.ctrlKey) return;
    if (e.key === "/") { e.preventDefault(); $("#gotoInput").focus(); return; }
    if (e.key === "s") { openSongbook(); return; }
    if (e.key === "m") { setLibrary(document.body.classList.contains("focus")); return; }
    if (e.key === "t") { $("#tikkun").click(); return; }
    if (!state.text) return;
    if (e.key === "j" || e.key === "ArrowDown") { e.preventDefault(); if (state.verse < state.text.he.length) selectVerse(state.verse + 1, { scroll: true }); }
    if (e.key === "k" || e.key === "ArrowUp") { e.preventDefault(); if (state.verse > 1) selectVerse(state.verse - 1, { scroll: true }); }
    if (e.key === " " && isTorah()) { e.preventDefault(); player.cur ? player.stop() : $("#playVerse").click(); }
    if (e.key === "]") step(1); if (e.key === "[") step(-1);
  });
  // restore settings
  const en = store.get("hz:en", true); $("#showEn").checked = en; document.body.classList.toggle("hide-en", !en);
  const tk = store.get("hz:tikkun", false); $("#tikkun").checked = tk; document.body.classList.toggle("tikkun", tk);
  const ph = store.get("hz:phrase", false); $("#phraseColors").checked = ph; document.body.classList.toggle("phrase", ph);
  $("#autoHide").checked = store.get("hz:autohide", true);
}
function showWelcome() {
  history.replaceState(null, "", location.pathname);
  $("#welcome").hidden = false; $("#chapterHead").hidden = true; $("#verses").innerHTML = ""; state.text = null; $("#locBtn").textContent = "Haazinu";
  setLibrary(false); renderSongMap();
  setTimeout(() => $("#exploreInput").focus(), 50);
}
async function evictServiceWorker() {
  // A service worker from an earlier build can swallow every fetch in Safari; drop it and start clean once.
  if (!("serviceWorker" in navigator)) return false;
  try {
    const rs = await Promise.race([navigator.serviceWorker.getRegistrations(), new Promise((r) => setTimeout(() => r([]), 1500))]);
    if (!rs.length) return false;
    await Promise.all(rs.map((r) => r.unregister()));
    try { const ks = await caches.keys(); await Promise.all(ks.map((k) => caches.delete(k))); } catch {}
    if (navigator.serviceWorker.controller && !sessionStorage.getItem("hz:swReloaded")) { sessionStorage.setItem("hz:swReloaded", "1"); location.reload(); return true; }
  } catch {}
  return false;
}
(async function main() {
  $("#readerStatus").hidden = false; $("#readerStatus").textContent = "Loading…";
  diag("main start"); if (await evictServiceWorker()) return; diag("sw ok");
  const timer = setTimeout(() => { $("#readerStatus").textContent = "Still loading the data files… if this stays, reload with Cmd+Shift+R (an old cached worker may be in the way)."; }, 6000);
  await loadData();
  clearTimeout(timer); diag("data ok " + data.parshiot.length + " " + data.songs.length + " " + (data.kriah ? "kriah" : "nokriah") + " " + data.siddur.nusachot.length);
  renderToc(); diag("toc ok"); wire(); diag("wire ok");
  detectYouTube().then((ok) => { state.ytBlocked = !ok; if (state.text) renderSongs(); });
  loadWeek();
  const r = parseHash();
  diag("hash " + JSON.stringify(r)); if (r) showPassage(r).then(() => diag("passage ok " + document.querySelectorAll(".verse").length)); else { $("#readerStatus").hidden = true; showWelcome(); }
})();
