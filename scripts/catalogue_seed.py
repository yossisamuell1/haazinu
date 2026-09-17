#!/usr/bin/env python3
"""Merge the built-in song catalogue (below) into data/songs.json, keeping existing entries and their recordings.
Performers listed are male singers/composers or traditional; recordings are screened separately in find_recordings.py."""
import json
from pathlib import Path
SONGS = Path(__file__).resolve().parent.parent / "data" / "songs.json"
# id | title | Hebrew title | performer | type | refs (;-separated) | opening words | note
RAW = r"""
# ---------- Torah ----------
yehi-or|Yehi Or|יהי אור|Children's song|children|Genesis 1:3|וַיֹּאמֶר אֱלֹהִים יְהִי אוֹר|Creation song for young children; several tunes.
vayehi-erev|Vayehi Erev Vayehi Voker|ויהי ערב ויהי בקר|Children's song|children|Genesis 1:5|וַיְהִי עֶרֶב וַיְהִי בֹקֶר|Days-of-creation refrain.
vayechulu|Vayechulu|ויכולו|Traditional (Kiddush)|liturgical|Genesis 2:1-3|וַיְכֻלּוּ הַשָּׁמַיִם וְהָאָרֶץ|Opening of Friday night Kiddush; many nusach tunes and choral settings.
lech-lecha|Lech Lecha|לך לך|Debbie Friedman melody, sung by many; also Ishay Ribo|adapted|Genesis 12:1|לֶךְ לְךָ מֵאַרְצְךָ|Prefer male recordings.
vaavarcha|Va'avarcha Mevarachecha|ואברכה מברכיך|Traditional|verbatim|Genesis 12:3|וַאֲבָרְכָה מְבָרְכֶיךָ|
uforatzta|Ufaratzta|ופרצת|Chabad niggun (Lubavitch)|verbatim|Genesis 28:14|וּפָרַצְתָּ יָמָּה וָקֵדְמָה|The signature Chabad niggun of the Rebbe's early years; sung at every farbrengen.
vehinei-sulam|Vehinei Sulam|והנה סולם|Traditional|verbatim|Genesis 28:12|וְהִנֵּה סֻלָּם מֻצָּב אַרְצָה|
vehinei-hashem|Vehinei Hashem Nitzav Alav|והנה ה' נצב עליו|Chabad 12 Pesukim|children|Genesis 28:13|וְהִנֵּה ה' נִצָּב עָלָיו|One of the Twelve Pesukim (with the Tanya's explanation).
ma-nora|Ma Nora HaMakom Hazeh|מה נורא המקום הזה|Traditional|verbatim|Genesis 28:17|מַה נּוֹרָא הַמָּקוֹם הַזֶּה|
im-yihyeh|Im Yihyeh Elokim Imadi|אם יהיה אלקים עמדי|Traditional|verbatim|Genesis 28:20-22|אִם יִהְיֶה אֱלֹהִים עִמָּדִי|Jacob's vow.
katonti|Katonti|קטנתי|Yonatan Razel|verbatim|Genesis 32:11|קָטֹנְתִּי מִכֹּל הַחֲסָדִים|2012.
ki-sarita|Ki Sarita|כי שרית|Traditional|verbatim|Genesis 32:29|כִּי שָׂרִיתָ עִם אֱלֹהִים|
hamalach|HaMalach HaGoel|המלאך הגואל|Traditional; Avraham Fried, Yosef Karduner|verbatim|Genesis 48:16|הַמַּלְאָךְ הַגֹּאֵל אֹתִי|Blessing of the children; bedtime Shema.
yesimcha|Yesimcha Elokim|ישימך אלקים|Traditional|liturgical|Genesis 48:20|יְשִׂמְךָ אֱלֹהִים כְּאֶפְרַיִם וְכִמְנַשֶּׁה|Friday night blessing of sons.
lo-yasur|Lo Yasur Shevet|לא יסור שבט|Traditional|verbatim|Genesis 49:10|לֹא יָסוּר שֵׁבֶט מִיהוּדָה|
vayomer-hashem-hineni|Hineni|הנני|Traditional|adapted|Exodus 3:4|וַיֹּאמֶר הִנֵּנִי|
ehyeh|Ehyeh Asher Ehyeh|אהיה אשר אהיה|Traditional|verbatim|Exodus 3:14|אֶהְיֶה אֲשֶׁר אֶהְיֶה|
ashira|Ashira LaHashem|אשירה לה'|Traditional; Shlomo Carlebach|verbatim|Exodus 15:1|אָשִׁירָה לַה' כִּי גָאֹה גָּאָה|Shirat HaYam opening.
ozi|Ozi VeZimrat Kah|עזי וזמרת י-ה|Shlomo Carlebach; Yosef Karduner|verbatim|Exodus 15:2|עָזִּי וְזִמְרָת יָ-הּ|
zeh-keili|Zeh Keili|זה א-לי|Traditional|verbatim|Exodus 15:2|זֶה אֵ-לִי וְאַנְוֵהוּ|
hashem-ish|Hashem Ish Milchama|ה' איש מלחמה|Traditional|verbatim|Exodus 15:3|ה' אִישׁ מִלְחָמָה|
yemincha|Yemincha Hashem|ימינך ה'|Traditional|verbatim|Exodus 15:6|יְמִינְךָ ה' נֶאְדָּרִי בַּכֹּחַ|
mi-chamocha|Mi Chamocha|מי כמוכה|Traditional; many settings|verbatim|Exodus 15:11|מִי כָמֹכָה בָּאֵלִם ה'|Sung daily in Shacharit and Maariv.
nachita|Nachita VeChasdecha|נחית בחסדך|Traditional|verbatim|Exodus 15:13|נָחִיתָ בְחַסְדְּךָ|
ad-yaavor|Ad Yaavor Amecha|עד יעבור עמך|Traditional|verbatim|Exodus 15:16|עַד יַעֲבֹר עַמְּךָ ה'|
hashem-yimloch|Hashem Yimloch|ה' ימלוך|Traditional; Shlomo Carlebach|verbatim|Exodus 15:18|ה' יִמְלֹךְ לְעֹלָם וָעֶד|
ani-hashem-rofecha|Ani Hashem Rofecha|אני ה' רופאך|Traditional|verbatim|Exodus 15:26|כִּי אֲנִי ה' רֹפְאֶךָ|
anochi|Anochi Hashem|אנכי ה'|Traditional|verbatim|Exodus 20:2|אָנֹכִי ה' אֱלֹהֶיךָ|
zachor|Zachor Et Yom HaShabbat|זכור את יום השבת|Traditional|verbatim|Exodus 20:8|זָכוֹר אֶת יוֹם הַשַּׁבָּת לְקַדְּשׁוֹ|
naaseh|Na'aseh VeNishma|נעשה ונשמע|Traditional; Miami Boys Choir|verbatim|Exodus 24:7|נַעֲשֶׂה וְנִשְׁמָע|
veasu-li|Ve'asu Li Mikdash|ועשו לי מקדש|Avraham Fried (Veshachanti); Shlomo Carlebach|verbatim|Exodus 25:8|וְעָשׂוּ לִי מִקְדָּשׁ וְשָׁכַנְתִּי בְּתוֹכָם|
veshamru|Veshamru|ושמרו|Traditional; many settings|verbatim|Exodus 31:16-17|וְשָׁמְרוּ בְנֵי יִשְׂרָאֵל אֶת הַשַּׁבָּת|Friday night and Shabbat morning.
yud-gimmel-middot|Hashem Hashem Kel Rachum|ה' ה' א-ל רחום|Traditional (Selichot)|liturgical|Exodus 34:6-7|ה' ה' אֵ-ל רַחוּם וְחַנּוּן|The Thirteen Attributes.
vayikra-el-moshe|Vayikra El Moshe|ויקרא אל משה|Children's song|children|Leviticus 1:1|וַיִּקְרָא אֶל מֹשֶׁה|Traditional start of a child's learning.
kedoshim|Kedoshim Tihyu|קדושים תהיו|Traditional|verbatim|Leviticus 19:2|קְדֹשִׁים תִּהְיוּ|
veahavta-lereacha|Ve'ahavta LeRe'acha|ואהבת לרעך|Chabad 12 Pesukim; Shlomo Carlebach|verbatim|Leviticus 19:18|וְאָהַבְתָּ לְרֵעֲךָ כָּמוֹךָ|One of the Twelve Pesukim.
ukratem-dror|Ukratem Dror|וקראתם דרור|Traditional|verbatim|Leviticus 25:10|וּקְרָאתֶם דְּרוֹר בָּאָרֶץ|
venatati-shalom|Venatati Shalom|ונתתי שלום|Traditional|verbatim|Leviticus 26:6|וְנָתַתִּי שָׁלוֹם בָּאָרֶץ|
yevarechecha|Yevarechecha|יברכך|Traditional; many settings|verbatim|Numbers 6:24-26|יְבָרֶכְךָ ה' וְיִשְׁמְרֶךָ|Birkat Kohanim; Friday night blessing.
vayehi-binsoa|Vayehi Binsoa|ויהי בנסוע|Traditional (Torah service)|verbatim|Numbers 10:35|וַיְהִי בִּנְסֹעַ הָאָרֹן|Opening the ark.
uvnucho|Uvnucho Yomar|ובנחה יאמר|Traditional (Torah service)|verbatim|Numbers 10:36|וּבְנֻחֹה יֹאמַר שׁוּבָה ה'|Returning the Torah.
ma-tovu|Ma Tovu|מה טובו|Traditional; many settings|verbatim|Numbers 24:5|מַה טֹּבוּ אֹהָלֶיךָ יַעֲקֹב|Entering the synagogue.
shema|Shema Yisrael|שמע ישראל|Traditional; Chabad 12 Pesukim|verbatim|Deuteronomy 6:4|שְׁמַע יִשְׂרָאֵל ה' אֱלֹהֵינוּ ה' אֶחָד|
veahavta|Ve'ahavta|ואהבת|Traditional; Shlomo Carlebach|verbatim|Deuteronomy 6:5-9|וְאָהַבְתָּ אֵת ה' אֱלֹהֶיךָ|
veshinantam|Veshinantam Levanecha|ושננתם לבניך|Chabad 12 Pesukim|children|Deuteronomy 6:7|וְשִׁנַּנְתָּם לְבָנֶיךָ|One of the Twelve Pesukim.
vehaya-im-shamoa|Vehaya Im Shamoa|והיה אם שמוע|Traditional|verbatim|Deuteronomy 11:13-21|וְהָיָה אִם שָׁמֹעַ תִּשְׁמְעוּ|Second paragraph of Shema.
ki-hashem-elokecha|Ki Hashem Elokecha Mit'halech|כי ה' אלקיך מתהלך|Traditional|verbatim|Deuteronomy 23:15|כִּי ה' אֱלֹהֶיךָ מִתְהַלֵּךְ בְּקֶרֶב מַחֲנֶךָ|
lo-bashamayim|Lo BaShamayim Hi|לא בשמים היא|Traditional|verbatim|Deuteronomy 30:12|לֹא בַשָּׁמַיִם הִוא|
ki-karov|Ki Karov Elecha|כי קרוב אליך|Chabad 12 Pesukim|children|Deuteronomy 30:14|כִּי קָרוֹב אֵלֶיךָ הַדָּבָר מְאֹד|One of the Twelve Pesukim.
uvacharta|Uvacharta BaChayim|ובחרת בחיים|Traditional|verbatim|Deuteronomy 30:19|וּבָחַרְתָּ בַּחַיִּים|
chizku|Chizku Ve'imtzu|חזקו ואמצו|Traditional|verbatim|Deuteronomy 31:6|חִזְקוּ וְאִמְצוּ אַל תִּירְאוּ|
haazinu|Ha'azinu HaShamayim|האזינו השמים|Traditional|verbatim|Deuteronomy 32:1-2|הַאֲזִינוּ הַשָּׁמַיִם וַאֲדַבֵּרָה|Opening of the Song of Moses.
hatzur-tamim|HaTzur Tamim Po'olo|הצור תמים פעלו|Traditional (Tzidduk HaDin)|verbatim|Deuteronomy 32:4|הַצּוּר תָּמִים פָּעֳלוֹ|
ki-chelek|Ki Chelek Hashem Amo|כי חלק ה' עמו|Traditional|verbatim|Deuteronomy 32:9|כִּי חֵלֶק ה' עַמּוֹ|
yimtzaehu|Yimtza'ehu Be'eretz Midbar|ימצאהו בארץ מדבר|Traditional|verbatim|Deuteronomy 32:10|יִמְצָאֵהוּ בְּאֶרֶץ מִדְבָּר|
kenesher|KeNesher Ya'ir Kino|כנשר יעיר קנו|Traditional|verbatim|Deuteronomy 32:11|כְּנֶשֶׁר יָעִיר קִנּוֹ|
hashem-badad|Hashem Badad Yanchenu|ה' בדד ינחנו|Traditional|verbatim|Deuteronomy 32:12|ה' בָּדָד יַנְחֶנּוּ|
reu-ata|Re'u Ata Ki Ani Ani Hu|ראו עתה כי אני אני הוא|Traditional|verbatim|Deuteronomy 32:39|רְאוּ עַתָּה כִּי אֲנִי אֲנִי הוּא|
harninu|Harninu Goyim Amo|הרנינו גוים עמו|Traditional|verbatim|Deuteronomy 32:43|הַרְנִינוּ גוֹיִם עַמּוֹ|
torah-tziva|Torah Tziva|תורה צוה|Chabad 12 Pesukim; traditional|verbatim|Deuteronomy 33:4|תּוֹרָה צִוָּה לָנוּ מֹשֶׁה|First of the Twelve Pesukim; a child's first verse.
vayehi-bishurun|Vayehi Bishurun Melech|ויהי בישורון מלך|Traditional|verbatim|Deuteronomy 33:5|וַיְהִי בִישֻׁרוּן מֶלֶךְ|
ashrecha-yisrael|Ashrecha Yisrael|אשריך ישראל|Traditional|verbatim|Deuteronomy 33:29|אַשְׁרֶיךָ יִשְׂרָאֵל מִי כָמוֹךָ|
vezot-hatorah|Vezot HaTorah|וזאת התורה|Traditional (Hagbah)|liturgical|Deuteronomy 4:44|וְזֹאת הַתּוֹרָה אֲשֶׁר שָׂם מֹשֶׁה|
veatem-hadveikim|Ve'atem HaDveikim|ואתם הדבקים|Traditional (Torah service)|verbatim|Deuteronomy 4:4|וְאַתֶּם הַדְּבֵקִים בַּה' אֱלֹהֵיכֶם|
ve-ata-yisrael|Ve'ata Yisrael Mah Hashem|ועתה ישראל מה ה'|Traditional|verbatim|Deuteronomy 10:12|וְעַתָּה יִשְׂרָאֵל מָה ה' אֱלֹהֶיךָ שֹׁאֵל|
# ---------- Nevi'im ----------
chazak-veematz|Chazak Ve'ematz|חזק ואמץ|Traditional|verbatim|Joshua 1:9|חֲזַק וֶאֱמָץ אַל תַּעֲרֹץ|
lo-yamush|Lo Yamush|לא ימוש|Traditional|verbatim|Joshua 1:8|לֹא יָמוּשׁ סֵפֶר הַתּוֹרָה הַזֶּה מִפִּיךָ|
ein-kadosh|Ein Kadosh KaHashem|אין קדוש כה'|Traditional|verbatim|I Samuel 2:2|אֵין קָדוֹשׁ כַּה'|
ki-mitzion|Ki MiTzion|כי מציון|Traditional (Torah service); many settings|verbatim|Isaiah 2:3|כִּי מִצִּיּוֹן תֵּצֵא תוֹרָה|
lo-yisa-goy|Lo Yisa Goy|לא ישא גוי|Shlomo Carlebach|verbatim|Isaiah 2:4|לֹא יִשָּׂא גוֹי אֶל גּוֹי חֶרֶב|
kadosh-kadosh|Kadosh Kadosh Kadosh|קדוש קדוש קדוש|Traditional (Kedushah)|liturgical|Isaiah 6:3|קָדוֹשׁ קָדוֹשׁ קָדוֹשׁ ה' צְבָאוֹת|
hinei-el|Hinei El Yeshuati|הנה א-ל ישועתי|Traditional (Havdalah)|verbatim|Isaiah 12:2|הִנֵּה אֵ-ל יְשׁוּעָתִי אֶבְטָח|
ushavtem-mayim|Ushavtem Mayim|ושאבתם מים|Traditional (Emanuel Amiran melody)|verbatim|Isaiah 12:3|וּשְׁאַבְתֶּם מַיִם בְּשָׂשׂוֹן|
uvau-haovdim|Uva'u HaOvdim|ובאו האובדים|Chabad niggun; Shlomo Carlebach|verbatim|Isaiah 27:13|וּבָאוּ הָאֹבְדִים בְּאֶרֶץ אַשּׁוּר|
nachamu|Nachamu Nachamu Ami|נחמו נחמו עמי|Traditional; Shlomo Carlebach|verbatim|Isaiah 40:1|נַחֲמוּ נַחֲמוּ עַמִּי|
vekovei|VeKovei Hashem|וקוי ה'|Traditional|verbatim|Isaiah 40:31|וְקוֹיֵ ה' יַחֲלִיפוּ כֹחַ|
al-tira|Al Tira|אל תירא|Traditional|verbatim|Isaiah 41:10|אַל תִּירָא כִּי עִמְּךָ אָנִי|
ki-vesimcha|Ki VeSimcha Tetze'u|כי בשמחה תצאו|Chabad niggun; traditional|verbatim|Isaiah 55:12|כִּי בְשִׂמְחָה תֵצֵאוּ|
ki-veiti|Ki Veiti Beit Tefila|כי ביתי בית תפלה|Traditional|verbatim|Isaiah 56:7|כִּי בֵיתִי בֵּית תְּפִלָּה|
kumi-ori|Kumi Ori|קומי אורי|Traditional|verbatim|Isaiah 60:1|קוּמִי אוֹרִי כִּי בָא אוֹרֵךְ|
sos-asis|Sos Asis|שוש אשיש|Traditional (wedding)|verbatim|Isaiah 61:10|שׂוֹשׂ אָשִׂישׂ בַּה'|
od-yishama|Od Yishama|עוד ישמע|Traditional (wedding); Shlomo Carlebach|verbatim|Jeremiah 33:10-11|עוֹד יִשָּׁמַע בְּעָרֵי יְהוּדָה|
kol-sason|Kol Sason VeKol Simcha|קול ששון וקול שמחה|Traditional (wedding)|verbatim|Jeremiah 33:11|קוֹל שָׂשׂוֹן וְקוֹל שִׂמְחָה|
haben-yakir|HaBen Yakir Li Efraim|הבן יקיר לי אפרים|Traditional; Avraham Fried|verbatim|Jeremiah 31:19|הֲבֵן יַקִּיר לִי אֶפְרַיִם|
veshavu-vanim|VeShavu Vanim|ושבו בנים|Traditional|verbatim|Jeremiah 31:16|וְשָׁבוּ בָנִים לִגְבוּלָם|
yeish-tikva|Yeish Tikva|יש תקוה|Traditional|verbatim|Jeremiah 31:16|וְיֵשׁ תִּקְוָה לְאַחֲרִיתֵךְ|
vezarakti|Vezarakti Aleichem|וזרקתי עליכם|Traditional|verbatim|Ezekiel 36:25|וְזָרַקְתִּי עֲלֵיכֶם מַיִם טְהוֹרִים|
veerastich|Ve'erastich Li|וארשתיך לי|Traditional (tefillin)|verbatim|Hosea 2:21-22|וְאֵרַשְׂתִּיךְ לִי לְעוֹלָם|
higid-lecha|Higid Lecha Adam|הגיד לך אדם|Traditional|verbatim|Micah 6:8|הִגִּיד לְךָ אָדָם מַה טּוֹב|
mi-kel-kamocha|Mi Kel Kamocha|מי א-ל כמוך|Traditional (Tashlich)|verbatim|Micah 7:18-20|מִי אֵ-ל כָּמוֹךָ|
lo-vechayil|Lo VeChayil|לא בחיל|Traditional|verbatim|Zechariah 4:6|לֹא בְחַיִל וְלֹא בְכֹחַ כִּי אִם בְּרוּחִי|
vehaya-hashem|Vehaya Hashem LeMelech|והיה ה' למלך|Traditional (Aleinu); many settings|verbatim|Zechariah 14:9|וְהָיָה ה' לְמֶלֶךְ עַל כָּל הָאָרֶץ|
hinei-anochi|Hinei Anochi Sholeach|הנה אנכי שולח|Traditional|verbatim|Malachi 3:23|הִנֵּה אָנֹכִי שֹׁלֵחַ לָכֶם אֵת אֵלִיָּה|
# ---------- Tehillim ----------
ashrei-haish|Ashrei HaIsh|אשרי האיש|Traditional|verbatim|Psalms 1:1-3|אַשְׁרֵי הָאִישׁ|
lama-ragshu|Lama Ragshu|למה רגשו|Traditional|verbatim|Psalms 2:1|לָמָּה רָגְשׁוּ גוֹיִם|
hashem-adoneinu|Hashem Adoneinu|ה' אדנינו|Traditional; Miami Boys Choir|verbatim|Psalms 8:2|ה' אֲדֹנֵינוּ מָה אַדִּיר שִׁמְךָ|
hashamayim-mesaprim|HaShamayim Mesaprim|השמים מספרים|Traditional|verbatim|Psalms 19:2|הַשָּׁמַיִם מְסַפְּרִים כְּבוֹד אֵ-ל|
yaancha|Ya'ancha Hashem|יענך ה'|Traditional|verbatim|Psalms 20:2|יַעַנְךָ ה' בְּיוֹם צָרָה|
eleh-varechev|Eleh VaRechev|אלה ברכב|Traditional; Miami Boys Choir|verbatim|Psalms 20:8|אֵלֶּה בָרֶכֶב וְאֵלֶּה בַסּוּסִים|
mizmor-ledavid-23|Mizmor LeDavid (Hashem Ro'i)|מזמור לדוד ה' רועי|Traditional; Ben Zion Shenker, many|verbatim|Psalms 23:1-6|ה' רֹעִי לֹא אֶחְסָר|Seudah Shlishit staple.
gam-ki-elech|Gam Ki Elech|גם כי אלך|Traditional|verbatim|Psalms 23:4|גַּם כִּי אֵלֵךְ בְּגֵיא צַלְמָוֶת|
seu-shearim|Se'u She'arim|שאו שערים|Traditional|verbatim|Psalms 24:7-10|שְׂאוּ שְׁעָרִים רָאשֵׁיכֶם|
hashem-ori|Hashem Ori VeYish'i|ה' אורי וישעי|Traditional (Elul)|verbatim|Psalms 27:1|ה' אוֹרִי וְיִשְׁעִי|
achat-shaalti|Achat Sha'alti|אחת שאלתי|Shlomo Carlebach; Yaakov Shwekey; many|verbatim|Psalms 27:4|אַחַת שָׁאַלְתִּי מֵאֵת ה'|
lulei-heemanti|Lulei He'emanti|לולא האמנתי|Traditional|verbatim|Psalms 27:13|לוּלֵא הֶאֱמַנְתִּי|
kaveh-el-hashem|Kaveh El Hashem|קוה אל ה'|Traditional|verbatim|Psalms 27:14|קַוֵּה אֶל ה' חֲזַק|
hoshia-et-amecha|Hoshia Et Amecha|הושיעה את עמך|Chabad niggun (Alter Rebbe's Hoshia); traditional|verbatim|Psalms 28:9|הוֹשִׁיעָה אֶת עַמֶּךָ|Sung by Chabad on Simchat Torah.
havu-lashem|Havu LaHashem|הבו לה'|Traditional (Kabbalat Shabbat)|verbatim|Psalms 29:1-2|הָבוּ לַה' בְּנֵי אֵלִים|
hashem-oz|Hashem Oz Le'amo Yiten|ה' עוז לעמו יתן|Traditional; Shlomo Carlebach|verbatim|Psalms 29:11|ה' עֹז לְעַמּוֹ יִתֵּן|
ranenu-tzadikim|Ranenu Tzadikim|רננו צדיקים|Traditional|verbatim|Psalms 33:1|רַנְּנוּ צַדִּיקִים בַּה'|
yehi-chasdecha|Yehi Chasdecha|יהי חסדך|Traditional|verbatim|Psalms 33:22|יְהִי חַסְדְּךָ ה' עָלֵינוּ|
mi-haish|Mi HaIsh|מי האיש|Baruch Chait; Miami Boys Choir|verbatim|Psalms 34:13-15|מִי הָאִישׁ הֶחָפֵץ חַיִּים|
sur-mera|Sur MeRa|סור מרע|Traditional|verbatim|Psalms 34:15|סוּר מֵרָע וַעֲשֵׂה טוֹב|
ma-yakar|Ma Yakar Chasdecha|מה יקר חסדך|Traditional|verbatim|Psalms 36:8|מַה יָּקָר חַסְדְּךָ אֱלֹהִים|
naar-hayiti|Na'ar Hayiti|נער הייתי|Traditional (bentching)|verbatim|Psalms 37:25|נַעַר הָיִיתִי גַּם זָקַנְתִּי|
lev-tahor|Lev Tahor|לב טהור|Traditional; Shlomo Carlebach|verbatim|Psalms 51:12|לֵב טָהוֹר בְּרָא לִי אֱלֹהִים|
padah-beshalom|Padah BeShalom|פדה בשלום|Chabad niggun|verbatim|Psalms 55:19|פָּדָה בְשָׁלוֹם נַפְשִׁי|Sung by Chabad on Yud-Tes Kislev, the Alter Rebbe's release.
tzama-lecha|Tzama Lecha Nafshi|צמאה לך נפשי|Chabad niggun (Alter Rebbe); Avraham Fried|verbatim|Psalms 63:2|צָמְאָה לְךָ נַפְשִׁי|One of the Alter Rebbe's ten niggunim; sung at Kabbalat Shabbat in Chabad.
elokim-yechaneinu|Elokim Yechaneinu|אלקים יחננו|Traditional (Psalm 67)|verbatim|Psalms 67:2|אֱלֹהִים יְחָנֵּנוּ וִיבָרְכֵנוּ|
yismechu-hashamayim|Yismechu HaShamayim|ישמחו השמים|Traditional|verbatim|Psalms 96:11|יִשְׂמְחוּ הַשָּׁמַיִם וְתָגֵל הָאָרֶץ|
or-zarua|Or Zarua LaTzadik|אור זרוע לצדיק|Traditional|verbatim|Psalms 97:11|אוֹר זָרֻעַ לַצַּדִּיק|
ivdu|Ivdu Et Hashem BeSimcha|עבדו את ה' בשמחה|Traditional; Shlomo Carlebach|verbatim|Psalms 100:2|עִבְדוּ אֶת ה' בְּשִׂמְחָה|
ki-tov-hashem|Ki Tov Hashem|כי טוב ה'|Traditional|verbatim|Psalms 100:5|כִּי טוֹב ה' לְעוֹלָם חַסְדּוֹ|
barchi-nafshi|Barchi Nafshi|ברכי נפשי|Traditional|verbatim|Psalms 104:1|בָּרְכִי נַפְשִׁי אֶת ה'|
ma-rabu|Ma Rabu Ma'asecha|מה רבו מעשיך|Traditional|verbatim|Psalms 104:24|מָה רַבּוּ מַעֲשֶׂיךָ ה'|
ashira-lashem-bechayai|Ashira LaHashem BeChayai|אשירה לה' בחיי|Traditional; Shlomo Carlebach|verbatim|Psalms 104:33|אָשִׁירָה לַה' בְּחַיָּי|
hodu-lashem-107|Hodu LaHashem Ki Tov|הודו לה' כי טוב|Traditional|verbatim|Psalms 118:1-4|הוֹדוּ לַה' כִּי טוֹב|Hallel.
min-hametzar|Min HaMetzar|מן המצר|Traditional; Shlomo Carlebach; Yosef Karduner|verbatim|Psalms 118:5|מִן הַמֵּצַר קָרָאתִי יָּ-הּ|Hallel.
hashem-li|Hashem Li Lo Ira|ה' לי לא אירא|Traditional|verbatim|Psalms 118:6|ה' לִי לֹא אִירָא|
tov-lachasot|Tov Lachasot|טוב לחסות|Traditional|verbatim|Psalms 118:8-9|טוֹב לַחֲסוֹת בַּה'|
kol-rina|Kol Rina VeYeshua|קול רנה וישועה|Chabad niggun; traditional|verbatim|Psalms 118:15-16|קוֹל רִנָּה וִישׁוּעָה|
lo-amut|Lo Amut Ki Echyeh|לא אמות כי אחיה|Traditional|verbatim|Psalms 118:17|לֹא אָמוּת כִּי אֶחְיֶה|
pitchu-li|Pitchu Li|פתחו לי|Traditional; Shlomo Carlebach|verbatim|Psalms 118:19-20|פִּתְחוּ לִי שַׁעֲרֵי צֶדֶק|Hallel.
odecha|Odecha Ki Anitani|אודך כי עניתני|Traditional|verbatim|Psalms 118:21|אוֹדְךָ כִּי עֲנִיתָנִי|
even-maasu|Even Ma'asu HaBonim|אבן מאסו הבונים|Traditional|verbatim|Psalms 118:22|אֶבֶן מָאֲסוּ הַבּוֹנִים|
zeh-hayom|Zeh HaYom|זה היום|Traditional; Shlomo Carlebach|verbatim|Psalms 118:24|זֶה הַיּוֹם עָשָׂה ה'|Hallel.
ana-hashem-hoshia|Ana Hashem Hoshia Na|אנא ה' הושיעה נא|Traditional (Hallel)|verbatim|Psalms 118:25|אָנָּא ה' הוֹשִׁיעָה נָּא|
baruch-haba|Baruch HaBa|ברוך הבא|Traditional (Hallel, wedding)|verbatim|Psalms 118:26|בָּרוּךְ הַבָּא בְּשֵׁם ה'|
keili-ata|Keili Ata|א-לי אתה|Chabad niggun (Alter Rebbe)|verbatim|Psalms 118:28|אֵ-לִי אַתָּה וְאוֹדֶךָּ|One of the Alter Rebbe's ten niggunim; sung at Hallel and Simchat Torah in Chabad.
tov-li|Tov Li Torat Picha|טוב לי תורת פיך|Traditional|verbatim|Psalms 119:72|טוֹב לִי תוֹרַת פִּיךָ|
lulei-toratecha|Lulei Toratecha|לולי תורתך|Traditional; Shlomo Carlebach|verbatim|Psalms 119:92|לוּלֵי תוֹרָתְךָ שַׁעֲשֻׁעָי|
shir-lamaalot-121|Esa Einai (Shir LaMa'alot)|אשא עיני|Shlomo Carlebach; Yosef Karduner; Shlomo Katz; many|verbatim|Psalms 121:1-8|אֶשָּׂא עֵינַי אֶל הֶהָרִים|
hinei-lo-yanum|Hinei Lo Yanum|הנה לא ינום|Traditional|verbatim|Psalms 121:4|הִנֵּה לֹא יָנוּם וְלֹא יִישָׁן|
samachti|Samachti Be'omrim Li|שמחתי באומרים לי|Traditional|verbatim|Psalms 122:1|שָׂמַחְתִּי בְּאֹמְרִים לִי|
shaalu-shlom|Sha'alu Shlom Yerushalayim|שאלו שלום ירושלים|Traditional; Shlomo Carlebach|verbatim|Psalms 122:6-9|שַׁאֲלוּ שְׁלוֹם יְרוּשָׁלִָם|
lemaan-achai|Lema'an Achai|למען אחי|Traditional; Shlomo Carlebach|verbatim|Psalms 122:8|לְמַעַן אַחַי וְרֵעָי|
shir-hamaalot-126|Shir HaMa'alot (Beshuv Hashem)|שיר המעלות|Traditional (bentching); dozens of tunes|verbatim|Psalms 126:1-6|שִׁיר הַמַּעֲלוֹת בְּשׁוּב ה'|Sung before Birkat HaMazon on Shabbat.
hazorim|HaZor'im BeDim'a|הזורעים בדמעה|Traditional|verbatim|Psalms 126:5-6|הַזֹּרְעִים בְּדִמְעָה בְּרִנָּה יִקְצֹרוּ|
im-hashem-lo|Im Hashem Lo Yivneh|אם ה' לא יבנה|Traditional|verbatim|Psalms 127:1|אִם ה' לֹא יִבְנֶה בַיִת|
eshet-chayil-ps|Ashrei Kol Yerei Hashem|אשרי כל ירא ה'|Traditional|verbatim|Psalms 128:1-6|אַשְׁרֵי כָּל יְרֵא ה'|
mimaamakim|MiMa'amakim|ממעמקים|Traditional; Idan Raichel (adapted)|adapted|Psalms 130:1|מִמַּעֲמַקִּים קְרָאתִיךָ ה'|
hinei-ma-tov|Hinei Ma Tov|הנה מה טוב|Traditional; countless settings|verbatim|Psalms 133:1|הִנֵּה מַה טּוֹב וּמַה נָּעִים|
al-naharot|Al Naharot Bavel|על נהרות בבל|Traditional|verbatim|Psalms 137:1|עַל נַהֲרוֹת בָּבֶל|
im-eshkachech|Im Eshkachech|אם אשכחך|Traditional (wedding); Shlomo Carlebach|verbatim|Psalms 137:5-6|אִם אֶשְׁכָּחֵךְ יְרוּשָׁלִָם|
ashrei-yoshvei|Ashrei Yoshvei Veitecha|אשרי יושבי ביתך|Traditional|liturgical|Psalms 84:5;Psalms 145:1-21|אַשְׁרֵי יוֹשְׁבֵי בֵיתֶךָ|Said three times daily.
poteach|Pote'ach Et Yadecha|פותח את ידך|Traditional|verbatim|Psalms 145:16|פּוֹתֵחַ אֶת יָדֶךָ|
somech|Somech Hashem|סומך ה'|Traditional|verbatim|Psalms 145:14|סוֹמֵךְ ה' לְכָל הַנֹּפְלִים|
boneh-yerushalayim|Boneh Yerushalayim|בונה ירושלים|Traditional|verbatim|Psalms 147:2-3|בּוֹנֵה יְרוּשָׁלִַם ה'|
harofeh|HaRofeh Lishvurei Lev|הרופא לשבורי לב|Traditional|verbatim|Psalms 147:3|הָרוֹפֵא לִשְׁבוּרֵי לֵב|
halelu-kel|Halelu Kel BeKodsho|הללו א-ל בקדשו|Traditional|verbatim|Psalms 150:1-6|הַלְלוּ אֵ-ל בְּקָדְשׁוֹ|
kol-haneshama|Kol HaNeshama|כל הנשמה|Traditional; Shlomo Carlebach|verbatim|Psalms 150:6|כֹּל הַנְּשָׁמָה תְּהַלֵּל יָ-הּ|
mizmor-shir-92|Mizmor Shir LeYom HaShabbat|מזמור שיר ליום השבת|Traditional (Kabbalat Shabbat)|verbatim|Psalms 92:1-2|מִזְמוֹר שִׁיר לְיוֹם הַשַּׁבָּת|
tov-lehodot|Tov LeHodot|טוב להודות|Traditional; Miami Boys Choir|verbatim|Psalms 92:2|טוֹב לְהֹדוֹת לַה'|
tzadik-katamar|Tzadik KaTamar|צדיק כתמר|Traditional; Shlomo Carlebach|verbatim|Psalms 92:13|צַדִּיק כַּתָּמָר יִפְרָח|
hashem-malach-geut|Hashem Malach Ge'ut Lavesh|ה' מלך גאות לבש|Traditional (Kabbalat Shabbat)|verbatim|Psalms 93:1|ה' מָלָךְ גֵּאוּת לָבֵשׁ|
ki-lo-yitosh|Ki Lo Yitosh|כי לא יטוש|Traditional; Shlomo Carlebach|verbatim|Psalms 94:14|כִּי לֹא יִטֹּשׁ ה' עַמּוֹ|
lechu-neranena|Lechu Neranena|לכו נרננה|Traditional (Kabbalat Shabbat)|verbatim|Psalms 95:1|לְכוּ נְרַנְּנָה לַה'|
yoshev-beseter|Yoshev BeSeter|יושב בסתר|Traditional|verbatim|Psalms 91:1|יֹשֵׁב בְּסֵתֶר עֶלְיוֹן|
ki-malachav|Ki Mal'achav|כי מלאכיו|Traditional; Shlomo Carlebach|verbatim|Psalms 91:11|כִּי מַלְאָכָיו יְצַוֶּה לָּךְ|
ma-ashiv|Ma Ashiv|מה אשיב|Traditional (Hallel)|verbatim|Psalms 116:12|מָה אָשִׁיב לַה'|
etalech|Etalech Lifnei Hashem|אתהלך לפני ה'|Traditional|verbatim|Psalms 116:9|אֶתְהַלֵּךְ לִפְנֵי ה'|
betzeit-yisrael|BeTzeit Yisrael|בצאת ישראל|Traditional (Hallel)|verbatim|Psalms 114:1|בְּצֵאת יִשְׂרָאֵל מִמִּצְרָיִם|
ki-leolam-chasdo|Ki Le'olam Chasdo|כי לעולם חסדו|Traditional (Hallel HaGadol)|verbatim|Psalms 136:1-26|הוֹדוּ לַה' כִּי טוֹב כִּי לְעוֹלָם חַסְדּוֹ|
ashrei-haam|Ashrei HaAm|אשרי העם|Traditional|verbatim|Psalms 144:15|אַשְׁרֵי הָעָם שֶׁכָּכָה לּוֹ|
hodu-ps-100|Mizmor LeToda|מזמור לתודה|Traditional|verbatim|Psalms 100:1-5|מִזְמוֹר לְתוֹדָה|
gal-einai|Gal Einai|גל עיני|Traditional|verbatim|Psalms 119:18|גַּל עֵינַי וְאַבִּיטָה|
ana-bechoach-ps|Rachem Al Tzion|רחם על ציון|Traditional|verbatim|Psalms 102:14|אַתָּה תָקוּם תְּרַחֵם צִיּוֹן|
# ---------- Ketuvim ----------
etz-chaim|Etz Chaim Hi|עץ חיים היא|Traditional (Torah service); many settings|verbatim|Proverbs 3:18;Proverbs 3:17|עֵץ חַיִּים הִיא לַמַּחֲזִיקִים בָּהּ|
deracheha|Deracheha Darchei Noam|דרכיה דרכי נועם|Traditional|verbatim|Proverbs 3:17|דְּרָכֶיהָ דַרְכֵי נֹעַם|
ki-ner|Ki Ner Mitzvah|כי נר מצוה|Traditional|verbatim|Proverbs 6:23|כִּי נֵר מִצְוָה וְתוֹרָה אוֹר|
eshet-chayil|Eshet Chayil|אשת חיל|Traditional (Friday night)|verbatim|Proverbs 31:10-31|אֵשֶׁת חַיִל מִי יִמְצָא|
bechol-derachecha|BeChol Derachecha|בכל דרכיך|Traditional|verbatim|Proverbs 3:6|בְּכָל דְּרָכֶיךָ דָעֵהוּ|
ki-lekach-tov|Ki Lekach Tov|כי לקח טוב|Traditional (Torah service)|verbatim|Proverbs 4:2|כִּי לֶקַח טוֹב נָתַתִּי לָכֶם|
sof-davar|Sof Davar|סוף דבר|Traditional|verbatim|Ecclesiastes 12:13|סוֹף דָּבָר הַכֹּל נִשְׁמָע|
dodi-li|Dodi Li|דודי לי|Traditional (wedding)|verbatim|Song of Songs 2:16|דּוֹדִי לִי וַאֲנִי לוֹ|
kol-dodi|Kol Dodi|קול דודי|Traditional|verbatim|Song of Songs 2:8|קוֹל דּוֹדִי הִנֵּה זֶה בָּא|
ani-ledodi|Ani LeDodi|אני לדודי|Traditional (wedding, Elul)|verbatim|Song of Songs 6:3|אֲנִי לְדוֹדִי וְדוֹדִי לִי|
simeni-kachotam|Simeni KaChotam|שימני כחותם|Traditional|verbatim|Song of Songs 8:6|שִׂימֵנִי כַחוֹתָם עַל לִבֶּךָ|
hashiveinu|Hashiveinu|השיבנו|Traditional (Torah service)|verbatim|Lamentations 5:21|הֲשִׁיבֵנוּ ה' אֵלֶיךָ וְנָשׁוּבָה|
ki-el-asher|Ki El Asher Telchi|כי אל אשר תלכי|Traditional|verbatim|Ruth 1:16|כִּי אֶל אֲשֶׁר תֵּלְכִי אֵלֵךְ|
layehudim|LaYehudim Hayta Ora|ליהודים היתה אורה|Traditional (Havdalah, Purim)|verbatim|Esther 8:16|לַיְּהוּדִים הָיְתָה אוֹרָה וְשִׂמְחָה|
lecha-hashem|Lecha Hashem HaGedula|לך ה' הגדולה|Traditional (Torah service)|verbatim|I Chronicles 29:11|לְךָ ה' הַגְּדֻלָּה וְהַגְּבוּרָה|
chedvat-hashem|Chedvat Hashem Hi Ma'uzchem|חדות ה' היא מעוזכם|Traditional|verbatim|Nehemiah 8:10|כִּי חֶדְוַת ה' הִיא מָעֻזְּכֶם|
"""
songs = []
for line in RAW.strip().splitlines():
    line = line.strip()
    if not line or line.startswith("#"): continue
    sid, title, he, perf, typ, refs, words, note = [x.strip() for x in line.split("|")]
    songs.append({"id": sid, "title": title, "title_he": he, "performer": perf or None, "year": None, "type": typ,
                  "refs": [r.strip() for r in refs.split(";") if r.strip()], "words": words, "note": note, "youtube": None})
data = json.load(open(SONGS, encoding="utf-8"))
have = {s["id"] for s in data["songs"]}
added = 0
for s in songs:
    if s["id"] in have: continue
    data["songs"].append(s); added += 1
data["meta"]["count"] = len(data["songs"])
json.dump(data, open(SONGS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"added {added}; catalogue now {len(data['songs'])} songs")
