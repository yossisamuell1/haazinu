#!/usr/bin/env python3
"""Second seed batch: more Tehillim, Tanakh, Chabad niggunim and siddur/zemirot/Haggadah songs, plus extra
refs on existing siddur songs so they show in Chabad and Sefard nusachot (their passages are named differently)."""
import json
from pathlib import Path
SONGS = Path(__file__).resolve().parent.parent / "data" / "songs.json"
S = "Siddur Sefard, "; C = "Weekday Siddur Chabad, "; A = "Siddur Ashkenaz, "
RAW = f"""
# ---------- Chabad niggunim and Shabbat table ----------
hu-elokeinu|Hu Elokeinu|הוא אלקינו|Chabad niggun (Musaf Kedushah)|liturgical|{S}Shabbat Morning Services, Amidah;{A}Shabbat, Musaf LeShabbat, Amidah|הוּא אֱלֹהֵינוּ הוּא אָבִינוּ|Sung in the Shabbat Musaf Kedushah in Chabad.
ata-vechartanu|Ata Vechartanu|אתה בחרתנו|Chabad niggun (Festival Amidah)|liturgical|{S}Holidays, Maariv, Shacharit & Mincha Amidah|אַתָּה בְחַרְתָּנוּ מִכָּל הָעַמִּים|Festival Amidah; classic Chabad melody.
ashreinu|Ashreinu Ma Tov Chelkeinu|אשרינו מה טוב חלקנו|Chabad niggun; traditional|liturgical|{C}Shacharit, Morning Prayer;{S}Lag BaOmer Songs, Ashreinu Ma Tov|אַשְׁרֵינוּ מַה טּוֹב חֶלְקֵנוּ|Morning prayers before Shema.
haaderet|Ha'aderet Veha'emunah|האדרת והאמונה|Chabad niggun (the Alter Rebbe's Napoleon-era tune is different); traditional|liturgical|{S}Shabbat Morning Services, Pesukei D'Zimrah|הָאַדֶּרֶת וְהָאֱמוּנָה לְחַי עוֹלָמִים|Shabbat Pesukei DeZimra; famous marching Chabad melody.
azamer-bishvachin|Azamer Bishvachin|אזמר בשבחין|Chabad (Arizal's Friday night hymn); traditional|liturgical|{S}Shabbat Evening Meal, Zemirot;{S}Shabbat Evening Meal, Atkinu Seudata|אֲזַמֵּר בִּשְׁבָחִין|Arizal's Aramaic hymn for the Friday night meal.
askinu-seudata|Askinu Seudata|אתקינו סעודתא|Traditional (Arizal)|liturgical|{S}Shabbat Evening Meal, Atkinu Seudata;{A}Shabbat, Third Meal, Atkinu|אַתְקִינוּ סְעוּדָתָא|
asader-lisudata|Asader Lis'udata|אסדר לסעודתא|Traditional (Arizal)|liturgical|{S}Shabbat Day Meal, Zemirot|אֲסַדֵּר לִסְעוּדָתָא|Shabbat day meal hymn.
bnei-heichala|Bnei Heichala|בני היכלא|Traditional (Arizal); Chabad|liturgical|{S}Third Meal, Zemirot;{A}Shabbat, Third Meal, Atkinu|בְּנֵי הֵיכָלָא דִּכְסִיפִין|Seudah shlishit hymn.
kah-echsof|Kah Echsof|קה אכסוף|Karlin (Rabbi Aharon of Karlin)|liturgical|{S}Third Meal, Zemirot|קָהּ אֶכְסוֹף נֹעַם שַׁבָּת|Sung at the Friday night and third meals.
kel-mistater|Kel Mistater|א-ל מסתתר|Traditional (seudah shlishit)|liturgical|{S}Third Meal, Zemirot|אֵ-ל מִסְתַּתֵּר בְּשַׁפְרִיר חֶבְיוֹן|
shimru-shabtotai|Shimru Shabtotai|שמרו שבתותי|Traditional|liturgical|{A}Shabbat, Daytime Meal, Zemirot for Second Meal, Shimru Shabtotai;{S}Shabbat Day Meal, Zemirot|שִׁמְרוּ שַׁבְּתוֹתַי|
baruch-hashem-yom|Baruch Hashem Yom Yom|ברוך ה' יום יום|Traditional|liturgical|{S}Shabbat Day Meal, Zemirot|בָּרוּךְ ה' יוֹם יוֹם|
hamavdil|HaMavdil|המבדיל|Traditional (Motza'ei Shabbat); many settings|liturgical|{S}Motzaei Shabbat , Hamavdil;{A}Shabbat, Havdalah|הַמַּבְדִּיל בֵּין קֹדֶשׁ לְחֹל|
eliyahu-hanavi|Eliyahu HaNavi|אליהו הנביא|Traditional (Motza'ei Shabbat, Seder)|liturgical|{S}Motzaei Shabbat , Melava Malka Zemirot;{S}Pesach Haggadah, Barech|אֵלִיָּהוּ הַנָּבִיא אֵלִיָּהוּ הַתִּשְׁבִּי|
shavua-tov|Shavua Tov (A Gute Voch)|שבוע טוב|Traditional|liturgical|{S}Motzaei Shabbat , Melava Malka Zemirot|שָׁבוּעַ טוֹב|
david-melech|David Melech Yisrael|דוד מלך ישראל|Traditional (Kiddush Levanah)|liturgical|{C}Kiddush Levanah;{S}Kiddush Levanah|דָּוִד מֶלֶךְ יִשְׂרָאֵל חַי וְקַיָּם|
siman-tov|Siman Tov UMazal Tov|סימן טוב ומזל טוב|Traditional (Kiddush Levanah, celebrations)|liturgical|{C}Kiddush Levanah;{S}Kiddush Levanah|סִימָן טוֹב וּמַזָּל טוֹב|
yismechu|Yismechu BeMalchutcha|ישמחו במלכותך|Traditional; many settings|liturgical|{S}Shabbat Morning Services, Amidah;{A}Shabbat, Musaf LeShabbat, Amidah|יִשְׂמְחוּ בְמַלְכוּתְךָ שׁוֹמְרֵי שַׁבָּת|Shabbat Musaf.
vetaher-libeinu|Vetaher Libeinu|וטהר לבנו|Traditional; Shlomo Carlebach|liturgical|{S}Holidays, Maariv, Shacharit & Mincha Amidah;{S}Shabbat Morning Services, Amidah|וְטַהֵר לִבֵּנוּ לְעָבְדְּךָ בֶּאֱמֶת|
shochen-ad|Shochen Ad|שוכן עד|Traditional (Shabbat Shacharit)|liturgical|{S}Shabbat Morning Services, Pesukei D'Zimrah;{A}Shabbat, Shacharit, Pesukei Dezimra, Nishmat Kol Chai|שׁוֹכֵן עַד מָרוֹם וְקָדוֹשׁ שְׁמוֹ|
hakol-yoducha|HaKol Yoducha|הכל יודוך|Traditional (Shabbat Shacharit)|liturgical|{S}Shabbat Morning Services, Shema & Blessings;{A}Shabbat, Shacharit, Blessings of the Shema, First Blessing before Shema|הַכֹּל יוֹדוּךָ וְהַכֹּל יְשַׁבְּחוּךָ|
baruch-sheamar|Baruch She'amar|ברוך שאמר|Traditional|liturgical|{C}Shacharit, Pesukei Dezimra;{A}Weekday, Shacharit, Pesukei Dezimra, Baruch She'amar|בָּרוּךְ שֶׁאָמַר וְהָיָה הָעוֹלָם|
hodu-lashem-kiru|Hodu LaHashem Kir'u Vishmo|הודו לה' קראו בשמו|Traditional|verbatim|I Chronicles 16:8-36;{C}Shacharit, Hodu;{S}Weekday Shacharit, Hodu|הוֹדוּ לַה' קִרְאוּ בִשְׁמוֹ|Opens Pesukei DeZimra in Nusach Ari.
hashem-melech-malach|Hashem Melech, Hashem Malach|ה' מלך ה' מלך|Traditional; many settings|liturgical|{C}Shacharit, Hodu;{S}Weekday Shacharit, Hodu;{S}Shabbat Morning Services, Pesukei D'Zimrah|ה' מֶלֶךְ ה' מָלָךְ ה' יִמְלֹךְ|
yishtabach|Yishtabach|ישתבח|Traditional|liturgical|{C}Shacharit, Pesukei Dezimra;{A}Weekday, Shacharit, Pesukei Dezimra, Yishtabach|יִשְׁתַּבַּח שִׁמְךָ לָעַד|
ahavat-olam|Ahavat Olam|אהבת עולם|Traditional; Shlomo Carlebach|liturgical|{C}Maariv;{A}Weekday, Maariv, Blessings of the Shema, Second Blessing before Shema|אַהֲבַת עוֹלָם בֵּית יִשְׂרָאֵל|
vehaer-eineinu|Vehaer Eineinu|והאר עינינו|Traditional; Shlomo Carlebach|liturgical|{C}Shacharit, Blessings of the Shema;{A}Weekday, Shacharit, Blessings of the Shema, Second Blessing before Shema|וְהָאֵר עֵינֵינוּ בְּתוֹרָתֶךָ|
modim|Modim Anachnu Lach|מודים אנחנו לך|Traditional|liturgical|{C}Shacharit, The Amidah;{A}Weekday, Shacharit, Amidah, Thanksgiving|מוֹדִים אֲנַחְנוּ לָךְ|
elokai-netzor|Elokai Netzor|אלקי נצור|Traditional|liturgical|{C}Shacharit, The Amidah;{A}Weekday, Shacharit, Amidah, Concluding Passage|אֱלֹהַי נְצֹר לְשׁוֹנִי מֵרָע|
kedusha|Kedushah (Nekadesh / Na'aritzcha)|קדושה|Traditional; many settings|liturgical|{C}Shacharit, The Amidah;{S}Shabbat Morning Services, Amidah|נַעֲרִיצְךָ וְנַקְדִּישְׁךָ|
uva-letzion|Uva LeTzion|ובא לציון|Traditional|verbatim|Isaiah 59:20-21;{C}Shacharit, Ashrei Uva LeZion|וּבָא לְצִיּוֹן גּוֹאֵל|
al-tira-mipachad|Al Tira MiPachad Pitom|אל תירא מפחד פתאום|Traditional (end of Aleinu)|verbatim|Proverbs 3:25;Isaiah 8:10;{C}Shacharit, Aleinu|אַל תִּירָא מִפַּחַד פִּתְאֹם|
ach-tzadikim|Ach Tzadikim|אך צדיקים|Traditional|verbatim|Psalms 140:14;{C}Shacharit, Aleinu|אַךְ צַדִּיקִים יוֹדוּ לִשְׁמֶךָ|
elokai-neshama|Elokai Neshama|אלקי נשמה|Traditional|liturgical|{C}Shacharit, Morning Blessings;{A}Weekday, Shacharit, Morning Blessings, Elokai Neshama|אֱלֹהַי נְשָׁמָה שֶׁנָּתַתָּ בִּי|
bidecha-afkid|Bidecha Afkid Ruchi|בידך אפקיד רוחי|Traditional (bedtime)|verbatim|Psalms 31:6;{C}Bedtime Shema|בְּיָדְךָ אַפְקִיד רוּחִי|Closing line of Adon Olam.
acheinu|Acheinu Kol Beit Yisrael|אחינו כל בית ישראל|Traditional; Abie Rotenberg|liturgical|{C}Shacharit, Torah Reading;{S}Weekday Shacharit, Torah Reading|אַחֵינוּ כָּל בֵּית יִשְׂרָאֵל|Said after Monday and Thursday Torah reading.
vayevarech-david|Vayevarech David|ויברך דוד|Traditional|verbatim|I Chronicles 29:10-13;{C}Shacharit, Pesukei Dezimra|וַיְבָרֶךְ דָּוִיד אֶת ה'|
uvnei-yerushalayim|Uvnei Yerushalayim|ובנה ירושלים|Traditional (bentching)|liturgical|{C}Blessings, Birkat HaMazon;{A}Berachot, Birkat HaMazon|וּבְנֵה יְרוּשָׁלַיִם עִיר הַקֹּדֶשׁ|
harachaman|HaRachaman|הרחמן|Traditional (bentching)|liturgical|{C}Blessings, Birkat HaMazon;{A}Berachot, Birkat HaMazon|הָרַחֲמָן הוּא יִמְלוֹךְ עָלֵינוּ|
samach-tesamach|Samach Tesamach|שמח תשמח|Traditional (wedding)|liturgical|{C}Blessings, Sheva Berakhot;{S}Various Blessings, Sheva Berachot|שַׂמַּח תְּשַׂמַּח רֵעִים הָאֲהוּבִים|
mi-adir|Mi Adir|מי אדיר|Traditional (chuppah)|liturgical|{C}Blessings, Sheva Berakhot;{S}Various Blessings, Marriage Blessings|מִי אַדִּיר עַל הַכֹּל|
mi-bon-siach|Mi Bon Siach|מי בן שיח|Traditional (chuppah)|liturgical|{C}Blessings, Sheva Berakhot;{S}Various Blessings, Marriage Blessings|מִי בָן שִׂיחַ שׁוֹשַׁן חוֹחִים|
kol-yisrael-chelek|Kol Yisrael Yesh Lahem Chelek|כל ישראל יש להם חלק|Chabad 12 Pesukim (Mishnah Sanhedrin)|children|{S}Shabbat Mincha, Pirkei Avot|כָּל יִשְׂרָאֵל יֵשׁ לָהֶם חֵלֶק לָעוֹלָם הַבָּא|Said before each chapter of Pirkei Avot; one of the Twelve Pesukim.
al-shlosha|Al Shlosha Devarim|על שלשה דברים|Traditional (Avot 1:2); Chaim Zippel|liturgical|{S}Shabbat Mincha, Pirkei Avot|עַל שְׁלֹשָׁה דְבָרִים הָעוֹלָם עוֹמֵד|
im-ein-ani|Im Ein Ani Li|אם אין אני לי|Traditional (Avot 1:14)|liturgical|{S}Shabbat Mincha, Pirkei Avot|אִם אֵין אֲנִי לִי מִי לִי|
# ---------- Haggadah ----------
kadesh-urchatz|Kadesh Urchatz|קדש ורחץ|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Kadesh|קַדֵּשׁ וּרְחַץ כַּרְפַּס יַחַץ|
ma-nishtana|Ma Nishtana|מה נשתנה|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Maggid|מַה נִּשְׁתַּנָּה הַלַּיְלָה הַזֶּה|
avadim-hayinu|Avadim Hayinu|עבדים היינו|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Maggid|עֲבָדִים הָיִינוּ לְפַרְעֹה בְּמִצְרָיִם|
vehi-sheamda|Vehi She'amda|והיא שעמדה|Yonatan Razel; traditional|liturgical|{S}Pesach Haggadah, Maggid|וְהִיא שֶׁעָמְדָה לַאֲבוֹתֵינוּ וְלָנוּ|Yonatan Razel's setting (2008) became the standard.
dayenu|Dayenu|דיינו|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Maggid|כַּמָּה מַעֲלוֹת טוֹבוֹת לַמָּקוֹם עָלֵינוּ|
bechol-dor|Bechol Dor VaDor|בכל דור ודור|Chabad 12 Pesukim; traditional|liturgical|{S}Pesach Haggadah, Maggid|בְּכָל דּוֹר וָדוֹר חַיָּב אָדָם לִרְאוֹת אֶת עַצְמוֹ|One of the Twelve Pesukim.
baruch-hamakom|Baruch HaMakom|ברוך המקום|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Maggid|בָּרוּךְ הַמָּקוֹם בָּרוּךְ הוּא|
adir-hu|Adir Hu|אדיר הוא|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Nirtzah|אַדִּיר הוּא יִבְנֶה בֵּיתוֹ בְּקָרוֹב|
echad-mi-yodea|Echad Mi Yodea|אחד מי יודע|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Nirtzah|אֶחָד מִי יוֹדֵעַ|
chad-gadya|Chad Gadya|חד גדיא|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Nirtzah|חַד גַּדְיָא חַד גַּדְיָא|
karev-yom|Karev Yom|קרב יום|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Nirtzah|קָרֵב יוֹם אֲשֶׁר הוּא לֹא יוֹם וְלֹא לַיְלָה|
ki-lo-naeh|Ki Lo Na'eh|כי לו נאה|Traditional (Seder)|liturgical|{S}Pesach Haggadah, Nirtzah|כִּי לוֹ נָאֶה כִּי לוֹ יָאֶה|
leshana-habaa|LeShana HaBa'a BiYerushalayim|לשנה הבאה בירושלים|Traditional|liturgical|{S}Pesach Haggadah, Nirtzah|לְשָׁנָה הַבָּאָה בִּירוּשָׁלָיִם|
# ---------- Festivals ----------
sisu-vesimchu|Sisu VeSimchu|שישו ושמחו|Traditional (Hakafot)|liturgical|{S}Simchat Torah, Hakafot|שִׂישׂוּ וְשִׂמְחוּ בְּשִׂמְחַת תּוֹרָה|
moshe-emet|Moshe Emet VeTorato Emet|משה אמת ותורתו אמת|Traditional (Hakafot); Chabad|liturgical|{S}Simchat Torah, Hakafot|מֹשֶׁה אֱמֶת וְתוֹרָתוֹ אֱמֶת|Chabad's Hakafot staple.
hanerot-halalu|HaNerot Halalu|הנרות הללו|Traditional (Chanukah)|liturgical|{S}Chanukah, Menorah Lighting;{C}Chanukah|הַנֵּרוֹת הַלָּלוּ אָנוּ מַדְלִיקִין|
al-hanisim|Al HaNisim|על הנסים|Traditional (Chanukah, Purim)|liturgical|{C}Chanukah;{C}Purim|עַל הַנִּסִּים וְעַל הַפֻּרְקָן|
shoshanat-yaakov|Shoshanat Yaakov|שושנת יעקב|Traditional (Purim)|liturgical|{S}Purim, Megillah Reading;{C}Purim|שׁוֹשַׁנַּת יַעֲקֹב צָהֲלָה וְשָׂמֵחָה|
bar-yochai|Bar Yochai|בר יוחאי|Traditional (Rabbi Shimon Lavi); Lag BaOmer|liturgical|{S}Lag BaOmer Songs, Bar Yochai|בַּר יוֹחַאי נִמְשַׁחְתָּ אַשְׁרֶיךָ|
amar-rabbi-akiva|Amar Rabbi Akiva|אמר רבי עקיבא|Traditional (Lag BaOmer)|liturgical|{S}Lag BaOmer Songs, Amar Rabbi Akiva|אָמַר רַבִּי עֲקִיבָא אַשְׁרֵיכֶם יִשְׂרָאֵל|
vaamartem|Va'amartem Ko LeChai|ואמרתם כה לחי|Traditional (Lag BaOmer)|liturgical|{S}Lag BaOmer Songs, Va'amartem Ko Lechai|וַאֲמַרְתֶּם כֹּה לֶחָי|
shema-koleinu|Shema Koleinu|שמע קולנו|Traditional (Selichot); many settings|liturgical|{S}Fast Days, Selichot for BaHaB;{A}Festivals, Selichot, BaHaB|שְׁמַע קוֹלֵנוּ ה' אֱלֹהֵינוּ|
kel-melech-yoshev|Kel Melech Yoshev|א-ל מלך יושב|Traditional (Selichot)|liturgical|{S}Fast Days, Selichot for BaHaB;{A}Festivals, Selichot, BaHaB|אֵ-ל מֶלֶךְ יוֹשֵׁב עַל כִּסֵּא רַחֲמִים|
adon-haselichot|Adon HaSelichot|אדון הסליחות|Traditional (Selichot)|liturgical|{S}Fast Days, Selichot for BaHaB|אֲדוֹן הַסְּלִיחוֹת בּוֹחֵן לְבָבוֹת|
machnisei-rachamim|Machnisei Rachamim|מכניסי רחמים|Traditional (Selichot)|liturgical|{S}Fast Days, Selichot for BaHaB|מַכְנִיסֵי רַחֲמִים הַכְנִיסוּ רַחֲמֵינוּ|
# ---------- more Tehillim ----------
shiviti|Shiviti Hashem|שויתי ה'|Traditional|verbatim|Psalms 16:8|שִׁוִּיתִי ה' לְנֶגְדִּי תָמִיד|
torat-hashem-temima|Torat Hashem Temima|תורת ה' תמימה|Traditional|verbatim|Psalms 19:8|תּוֹרַת ה' תְּמִימָה מְשִׁיבַת נָפֶשׁ|
yihyu-leratzon|Yihyu LeRatzon|יהיו לרצון|Traditional|verbatim|Psalms 19:15|יִהְיוּ לְרָצוֹן אִמְרֵי פִי|
aromimcha|Aromimcha Hashem|ארוממך ה'|Traditional (Psalm 30)|verbatim|Psalms 30:2|אֲרוֹמִמְךָ ה' כִּי דִלִּיתָנִי|
taamu-uru|Ta'amu Ur'u|טעמו וראו|Traditional|verbatim|Psalms 34:9|טַעֲמוּ וּרְאוּ כִּי טוֹב ה'|
keayal-taarog|Ke'ayal Ta'arog|כאיל תערוג|Traditional|verbatim|Psalms 42:2|כְּאַיָּל תַּעֲרֹג עַל אֲפִיקֵי מָיִם|
hashem-tzevakot-imanu|Hashem Tzevakot Imanu|ה' צבאות עמנו|Traditional|verbatim|Psalms 46:8|ה' צְבָאוֹת עִמָּנוּ|
kol-haamim|Kol HaAmim Tik'u Chaf|כל העמים תקעו כף|Traditional (Rosh Hashanah)|verbatim|Psalms 47:2|כָּל הָעַמִּים תִּקְעוּ כָף|
gadol-hashem|Gadol Hashem UMehulal|גדול ה' ומהולל|Traditional|verbatim|Psalms 48:2|גָּדוֹל ה' וּמְהֻלָּל מְאֹד|
ura-chvodi|Ura Chvodi|עורה כבודי|Traditional|verbatim|Psalms 57:9|עוּרָה כְבוֹדִי עוּרָה הַנֵּבֶל וְכִנּוֹר|
vaani-tefilati|Va'ani Tefilati|ואני תפלתי|Traditional (Shabbat Mincha)|verbatim|Psalms 69:14|וַאֲנִי תְפִלָּתִי לְךָ ה'|
al-tashlicheni|Al Tashlicheni|אל תשליכני|Traditional|verbatim|Psalms 71:9|אַל תַּשְׁלִיכֵנִי לְעֵת זִקְנָה|
tiku-bachodesh|Tik'u BaChodesh Shofar|תקעו בחדש שופר|Traditional (Rosh Hashanah)|verbatim|Psalms 81:4|תִּקְעוּ בַחֹדֶשׁ שׁוֹפָר|
ma-yedidot|Ma Yedidot Mishkenotecha|מה ידידות משכנותיך|Traditional|verbatim|Psalms 84:2|מַה יְּדִידוֹת מִשְׁכְּנוֹתֶיךָ|
chesed-veemet|Chesed Ve'emet Nifgashu|חסד ואמת נפגשו|Traditional|verbatim|Psalms 85:11|חֶסֶד וֶאֱמֶת נִפְגָּשׁוּ|
ashrei-haam-yodei|Ashrei HaAm Yod'ei Terua|אשרי העם יודעי תרועה|Traditional (Rosh Hashanah)|verbatim|Psalms 89:16|אַשְׁרֵי הָעָם יוֹדְעֵי תְרוּעָה|
vihi-noam|Vihi Noam|ויהי נועם|Traditional (Motza'ei Shabbat)|verbatim|Psalms 90:17|וִיהִי נֹעַם ה' אֱלֹהֵינוּ עָלֵינוּ|
shiru-lashem|Shiru LaHashem Shir Chadash|שירו לה' שיר חדש|Traditional; many settings|verbatim|Psalms 96:1;Psalms 98:1;Psalms 149:1|שִׁירוּ לַה' שִׁיר חָדָשׁ|
romemu|Romemu|רוממו|Traditional|verbatim|Psalms 99:5;Psalms 99:9|רוֹמְמוּ ה' אֱלֹהֵינוּ|
kerachem-av|KeRachem Av|כרחם אב|Traditional|verbatim|Psalms 103:13|כְּרַחֵם אָב עַל בָּנִים|
yehi-chevod|Yehi Chevod|יהי כבוד|Traditional (Pesukei DeZimra)|verbatim|Psalms 104:31;{C}Shacharit, Pesukei Dezimra|יְהִי כְבוֹד ה' לְעוֹלָם|
yodu-lashem-chasdo|Yodu LaHashem Chasdo|יודו לה' חסדו|Traditional|verbatim|Psalms 107:8|יוֹדוּ לַה' חַסְדּוֹ|
reishit-chochma|Reishit Chochma|ראשית חכמה|Traditional (morning)|verbatim|Psalms 111:10|רֵאשִׁית חָכְמָה יִרְאַת ה'|
ashrei-ish|Ashrei Ish Yarei Et Hashem|אשרי איש ירא את ה'|Traditional|verbatim|Psalms 112:1|אַשְׁרֵי אִישׁ יָרֵא אֶת ה'|
halelu-avdei|Halleluyah Hallelu Avdei Hashem|הללויה הללו עבדי ה'|Traditional (Hallel)|verbatim|Psalms 113:1;{C}Hallel|הַלְלוּיָהּ הַלְלוּ עַבְדֵי ה'|
mekimi|Mekimi Me'afar Dal|מקימי מעפר דל|Traditional (Hallel)|verbatim|Psalms 113:7-9|מְקִימִי מֵעָפָר דָּל|
lo-lanu|Lo Lanu|לא לנו|Traditional (Hallel)|verbatim|Psalms 115:1|לֹא לָנוּ ה' לֹא לָנוּ|
ana-hashem-ki-ani|Ana Hashem Ki Ani Avdecha|אנה ה' כי אני עבדך|Traditional (Hallel); many settings|verbatim|Psalms 116:16|אָנָּה ה' כִּי אֲנִי עַבְדֶּךָ|
halelu-et-hashem|Halelu Et Hashem Kol Goyim|הללו את ה' כל גוים|Traditional (Hallel)|verbatim|Psalms 117:1-2|הַלְלוּ אֶת ה' כָּל גּוֹיִם|
ashrei-temimei|Ashrei Temimei Darech|אשרי תמימי דרך|Traditional|verbatim|Psalms 119:1|אַשְׁרֵי תְמִימֵי דָרֶךְ|
elecha-nasati|Elecha Nasati|אליך נשאתי|Traditional|verbatim|Psalms 123:1|אֵלֶיךָ נָשָׂאתִי אֶת עֵינַי|
lulei-hashem|Lulei Hashem SheHaya Lanu|לולי ה' שהיה לנו|Traditional|verbatim|Psalms 124:1-2|לוּלֵי ה' שֶׁהָיָה לָנוּ|
habotchim|HaBotchim BaHashem|הבוטחים בה'|Traditional|verbatim|Psalms 125:1|הַבֹּטְחִים בַּה' כְּהַר צִיּוֹן|
hashem-lo-gavah|Hashem Lo Gavah Libi|ה' לא גבה לבי|Traditional|verbatim|Psalms 131:1-3|ה' לֹא גָבַהּ לִבִּי|
hinei-barchu|Hinei Barchu Et Hashem|הנה ברכו את ה'|Traditional|verbatim|Psalms 134:1-3|הִנֵּה בָּרְכוּ אֶת ה'|
hashem-chakartani|Hashem Chakartani|ה' חקרתני|Traditional|verbatim|Psalms 139:1|ה' חֲקַרְתַּנִי וַתֵּדָע|
haleli-nafshi|Halleli Nafshi|הללי נפשי|Traditional|verbatim|Psalms 146:1-2|הַלְלִי נַפְשִׁי אֶת ה'|
halelu-min-hashamayim|Hallelu Et Hashem Min HaShamayim|הללו את ה' מן השמים|Traditional|verbatim|Psalms 148:1|הַלְלוּ אֶת ה' מִן הַשָּׁמַיִם|
# ---------- more Torah ----------
od-kol-yemei|Od Kol Yemei HaAretz|עוד כל ימי הארץ|Traditional|verbatim|Genesis 8:22|עֹד כָּל יְמֵי הָאָרֶץ|
habet-na|Habet Na HaShamayma|הבט נא השמימה|Traditional|verbatim|Genesis 15:5|הַבֶּט נָא הַשָּׁמַיְמָה|
hineni-akedah|Hineni (Akedah)|הנני|Traditional|verbatim|Genesis 22:1|וַיֹּאמֶר הִנֵּנִי|
hakol-kol-yaakov|HaKol Kol Yaakov|הקול קול יעקב|Traditional|verbatim|Genesis 27:22|הַקֹּל קוֹל יַעֲקֹב|
vehinei-anochi-imach|Vehinei Anochi Imach|והנה אנכי עמך|Traditional; Shlomo Carlebach|verbatim|Genesis 28:15|וְהִנֵּה אָנֹכִי עִמָּךְ|
ani-yosef|Ani Yosef|אני יוסף|Traditional|verbatim|Genesis 45:3|אֲנִי יוֹסֵף הַעוֹד אָבִי חָי|
anochi-ered|Anochi Ered Imcha|אנכי ארד עמך|Traditional|verbatim|Genesis 46:4|אָנֹכִי אֵרֵד עִמְּךָ מִצְרַיְמָה|
lishuatcha|Lishuatcha Kiviti|לישועתך קויתי|Traditional|verbatim|Genesis 49:18|לִישׁוּעָתְךָ קִוִּיתִי ה'|
vehotzeti|Vehotzeti (Four Expressions of Redemption)|והוצאתי|Traditional|verbatim|Exodus 6:6-7|וְהוֹצֵאתִי אֶתְכֶם|
hashem-yilachem|Hashem Yilachem Lachem|ה' ילחם לכם|Traditional|verbatim|Exodus 14:14|ה' יִלָּחֵם לָכֶם וְאַתֶּם תַּחֲרִשׁוּן|
mamlechet-kohanim|Mamlechet Kohanim|ממלכת כהנים|Traditional|verbatim|Exodus 19:5-6|וְאַתֶּם תִּהְיוּ לִי מַמְלֶכֶת כֹּהֲנִים|
hinei-anochi-malach|Hinei Anochi Shole'ach Mal'ach|הנה אנכי שולח מלאך|Traditional|verbatim|Exodus 23:20|הִנֵּה אָנֹכִי שֹׁלֵחַ מַלְאָךְ לְפָנֶיךָ|
venikdashti|Venikdashti|ונקדשתי|Traditional|verbatim|Leviticus 22:32|וְנִקְדַּשְׁתִּי בְּתוֹךְ בְּנֵי יִשְׂרָאֵל|
kel-na|Kel Na Refa Na La|א-ל נא רפא נא לה|Traditional|verbatim|Numbers 12:13|אֵ-ל נָא רְפָא נָא לָהּ|
salachti|Salachti Kidvarecha|סלחתי כדברך|Traditional (Yom Kippur)|verbatim|Numbers 14:20|סָלַחְתִּי כִּדְבָרֶךָ|
ali-beer|Ali Be'er|עלי באר|Traditional|verbatim|Numbers 21:17|עֲלִי בְאֵר עֱנוּ לָהּ|
hen-am|Hen Am Levadad Yishkon|הן עם לבדד ישכון|Traditional|verbatim|Numbers 23:9|הֶן עָם לְבָדָד יִשְׁכֹּן|
banim-atem|Banim Atem|בנים אתם|Traditional; Shlomo Carlebach|verbatim|Deuteronomy 14:1|בָּנִים אַתֶּם לַה' אֱלֹהֵיכֶם|
baruch-ata-bevoecha|Baruch Ata Bevo'echa|ברוך אתה בבואך|Traditional|verbatim|Deuteronomy 28:6|בָּרוּךְ אַתָּה בְּבֹאֶךָ|
eretz-asher|Eretz Asher Hashem Elokecha Doresh Ota|ארץ אשר ה' אלקיך דורש אותה|Traditional|verbatim|Deuteronomy 11:12|אֶרֶץ אֲשֶׁר ה' אֱלֹהֶיךָ דֹּרֵשׁ אֹתָהּ|
# ---------- more Nevi'im / Ketuvim ----------
ki-malah|Ki Mal'ah HaAretz De'ah|כי מלאה הארץ דעה|Traditional|verbatim|Isaiah 11:9|כִּי מָלְאָה הָאָרֶץ דֵּעָה אֶת ה'|
bila-hamavet|Bila HaMavet LaNetzach|בלע המות לנצח|Traditional|verbatim|Isaiah 25:8|בִּלַּע הַמָּוֶת לָנֶצַח|
bitchu-bashem|Bitchu BaHashem|בטחו בה'|Traditional|verbatim|Isaiah 26:4|בִּטְחוּ בַה' עֲדֵי עַד|
ufduyei|Ufduyei Hashem Yeshuvun|ופדויי ה' ישובון|Traditional|verbatim|Isaiah 35:10;Isaiah 51:11|וּפְדוּיֵי ה' יְשֻׁבוּן|
al-tira-ki-gealticha|Al Tira Ki Ge'alticha|אל תירא כי גאלתיך|Traditional|verbatim|Isaiah 43:1-2|אַל תִּירָא כִּי גְאַלְתִּיךָ|
ma-navu|Ma Navu|מה נאוו|Traditional; Shlomo Carlebach|verbatim|Isaiah 52:7|מַה נָּאווּ עַל הֶהָרִים|
ki-heharim|Ki HeHarim Yamushu|כי ההרים ימושו|Traditional|verbatim|Isaiah 54:10|כִּי הֶהָרִים יָמוּשׁוּ|
hoy-kol-tzamei|Hoy Kol Tzamei|הוי כל צמא|Traditional|verbatim|Isaiah 55:1|הוֹי כָּל צָמֵא לְכוּ לַמַּיִם|
umesos-chatan|UMesos Chatan|ומשוש חתן|Traditional (wedding)|verbatim|Isaiah 62:5|וּמְשׂוֹשׂ חָתָן עַל כַּלָּה|
sisu-et-yerushalayim|Sisu Et Yerushalayim|שישו את ירושלים|Traditional; Akiva Nof (adapted)|verbatim|Isaiah 66:10|שִׂישׂוּ אֶת יְרוּשָׁלִַם|
zacharti-lach|Zacharti Lach|זכרתי לך|Traditional|verbatim|Jeremiah 2:2|זָכַרְתִּי לָךְ חֶסֶד נְעוּרַיִךְ|
baruch-hagever|Baruch HaGever|ברוך הגבר|Traditional|verbatim|Jeremiah 17:7|בָּרוּךְ הַגֶּבֶר אֲשֶׁר יִבְטַח בַּה'|
merachok|MeRachok Hashem Nir'ah Li|מרחוק ה' נראה לי|Traditional|verbatim|Jeremiah 31:2|מֵרָחוֹק ה' נִרְאָה לִי|
shuva-yisrael|Shuva Yisrael|שובה ישראל|Traditional (Shabbat Shuva)|verbatim|Hosea 14:2|שׁוּבָה יִשְׂרָאֵל עַד ה' אֱלֹהֶיךָ|
roni-vesimchi|Roni VeSimchi Bat Tzion|רני ושמחי בת ציון|Traditional|verbatim|Zechariah 2:14|רָנִּי וְשִׂמְחִי בַּת צִיּוֹן|
tzom-harevii|Tzom HaRevi'i|צום הרביעי|Traditional|verbatim|Zechariah 8:19|צוֹם הָרְבִיעִי וְצוֹם הַחֲמִישִׁי|
gili-meod|Gili Me'od Bat Tzion|גילי מאד בת ציון|Traditional|verbatim|Zechariah 9:9|גִּילִי מְאֹד בַּת צִיּוֹן|
az-nidberu|Az Nidberu|אז נדברו|Traditional|verbatim|Malachi 3:16|אָז נִדְבְּרוּ יִרְאֵי ה'|
mi-keamcha|Mi Ke'amcha Yisrael|מי כעמך ישראל|Traditional|verbatim|II Samuel 7:23;I Chronicles 17:21|וּמִי כְעַמְּךָ כְּיִשְׂרָאֵל|
hashem-imachem|Hashem Imachem|ה' עמכם|Traditional|verbatim|Ruth 2:4|ה' עִמָּכֶם|
yishakeni|Yishakeni|ישקני|Traditional|verbatim|Song of Songs 1:2|יִשָּׁקֵנִי מִנְּשִׁיקוֹת פִּיהוּ|
hinei-hastav-avar|Ki Hinei HaStav Avar|כי הנה הסתו עבר|Traditional|verbatim|Song of Songs 2:11-12|כִּי הִנֵּה הַסְּתָו עָבָר|
ani-yesheina|Ani Yesheina VeLibi Er|אני ישנה ולבי ער|Traditional|verbatim|Song of Songs 5:2|אֲנִי יְשֵׁנָה וְלִבִּי עֵר|
mayim-rabim|Mayim Rabim|מים רבים|Traditional; Shlomo Carlebach|verbatim|Song of Songs 8:7|מַיִם רַבִּים לֹא יוּכְלוּ לְכַבּוֹת אֶת הָאַהֲבָה|
lakol-zman|LaKol Zman|לכל זמן|Traditional|verbatim|Ecclesiastes 3:1|לַכֹּל זְמָן וְעֵת לְכָל חֵפֶץ|
chanoch-lanaar|Chanoch LaNa'ar|חנוך לנער|Traditional|verbatim|Proverbs 22:6|חֲנֹךְ לַנַּעַר עַל פִּי דַרְכּוֹ|
kamayim-hapanim|KaMayim HaPanim|כמים הפנים|Traditional|verbatim|Proverbs 27:19|כַּמַּיִם הַפָּנִים לַפָּנִים|
chasdei-hashem|Chasdei Hashem Ki Lo Tamnu|חסדי ה' כי לא תמנו|Traditional|verbatim|Lamentations 3:22-23|חַסְדֵי ה' כִּי לֹא תָמְנוּ|
"""
# extra refs so the older Ashkenaz-catalogued siddur songs appear in Chabad / Sefard
ALIAS = {
    "Preparatory Prayers, Modeh Ani": [C + "Shacharit, Upon Arising"],
    "Preparatory Prayers, Adon Olam": [C + "Shacharit, Morning Blessings", C + "Bedtime Shema"],
    "Preparatory Prayers, Yigdal": [C + "Shacharit, Morning Blessings"],
    "Pesukei Dezimra, Ashrei": [C + "Shacharit, Pesukei Dezimra", C + "Mincha, Ashrei"],
    "Second Blessing after Shema": [C + "Maariv"],
    "Maariv, Amidah, Peace": [C + "Maariv"],
    "Shacharit, Amidah, Peace": [C + "Shacharit, The Amidah"],
    "Post Amidah, Avinu Malkenu": [C + "Shacharit, Tachnun"],
    "Tachanun, Shomer Yisrael": [C + "Shacharit, Tachnun"],
    "Concluding Prayers, Alenu": [C + "Shacharit, Aleinu"],
    "Musaf LeShabbat, Ein Keloheinu": [S + "Shabbat Morning Services, Amidah"],
    "Musaf LeShabbat, Shir HaKavod": [S + "Shabbat Morning Services, Amidah"],
    "Kaddish, Mourner's Kaddish": [C + "Shacharit, Mourner's Kaddish"],
    "Kabbalat Shabbat, Yedid Nefesh": [S + "Shabbat Eve Maariv, Shabbat Eve Maariv", S + "Third Meal, Zemirot"],
    "Kabbalat Shabbat, Ana Bekoach": [S + "Shabbat Eve Maariv, Shabbat Eve Maariv", C + "Sefirat HaOmer"],
    "Kabbalat Shabbat, Lekha Dodi": [S + "Shabbat Eve Maariv, Shabbat Eve Maariv"],
    "Kabbalat Shabbat, Psalm 92": [S + "Shabbat Eve Maariv, Shabbat Eve Maariv"],
    "Shabbat Evening, Shalom Aleichem": [S + "Shabbat Evening Meal, Shalom Aleichem"],
    "Shabbat Evening, Eshet Chayil": [S + "Shabbat Evening Meal, Eishet Chayil"],
    "Shabbat Evening, Kiddush": [S + "Shabbat Evening Meal, Shabbat Eve Kiddush"],
    "Zemirot for Shabbat Evening": [S + "Shabbat Evening Meal, Zemirot"],
    "Zemirot for Second Meal": [S + "Shabbat Day Meal, Zemirot"],
    "Hallel, Psalm 118": [C + "Hallel", S + "Rosh Chodesh, Hallel", S + "Pesach Haggadah, Hallel"],
    "Chanukah Candles, Maoz Tzur": [S + "Chanukah, Menorah Lighting", C + "Chanukah"],
    "Shabbat, Havdalah": [S + "Motzaei Shabbat , Havdala"],
    "Berachot, Birkat HaMazon": [C + "Blessings, Birkat HaMazon"],
    "Berachot, Tefillat HaDerech": [C + "Blessings, The Travelers' Prayer"],
    "Nishmat Kol Chai": [S + "Shabbat Morning Services, Pesukei D'Zimrah"],
    "First Blessing before Shema": [S + "Shabbat Morning Services, Shema & Blessings"],
}
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
aliased = 0
for s in data["songs"]:
    for r in list(s["refs"]):
        if not r.startswith("Siddur Ashkenaz"): continue
        for key, extra in ALIAS.items():
            if key in r:
                for e in extra:
                    if e not in s["refs"]: s["refs"].append(e); aliased += 1
data["meta"]["count"] = len(data["songs"])
json.dump(data, open(SONGS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"added {added}; aliased {aliased} refs; catalogue now {len(data['songs'])} songs")
