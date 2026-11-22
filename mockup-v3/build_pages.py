"""Build the mockup's pages from shared parts and real data.

Writes archive.html, authors.html, team.html, about.html and refreshes the shared
header, footer and indexing block inside index.html and article.html.

Run:  python build_pages.py
Data: data/archive.json (journal archive, pages 1-2), data/team.json (editorial board)
"""
import html
import json
import pathlib
import re

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"

E = html.escape


def uz(s):
    """Uzbek Latin typography: oʻ gʻ with U+02BB, tutuq belgisi with U+02BC."""
    s = re.sub(r"([oOgG])[‘’'`ʻ]", lambda m: m.group(1) + "ʻ", s)
    s = re.sub(r"(?<=[A-Za-zʻ])[’'`](?=[A-Za-z])", "ʼ", s)
    return s


NAV = [
    ("index.html", "Joriy son"),
    ("archive.html", "Arxiv"),
    ("authors.html", "Mualliflarga"),
    ("team.html", "Tahririyat"),
    ("about.html", "Jurnal haqida"),
]

INDEXING = [
    ("google-scholar.png", "Google Scholar", "https://scholar.google.com/citations?user=J0U89FQAAAAJ"),
    ("sjif.png", "Scientific Journal Impact Factor", "http://sjifactor.com/passport.php?id=22543"),
    ("index-copernicus.png", "Index Copernicus International", "https://journals.indexcopernicus.com/search/journal/issue?issueId=all&journalId=125703"),
    ("drji.png", "DRJI", "http://olddrji.lbp.world/JournalVolumeDetails.aspx?jid=2181-3035"),
    ("cyberleninka.png", "CyberLeninka", "https://cyberleninka.ru/journal/n/talqin-va-tadqiqotlar-ilmiy-uslubiy-jurnali"),
    ("zenodo.png", "Zenodo", "https://zenodo.org/communities/talqin-2181-3035"),
]

ICON_SEARCH = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
ICON_MENU = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'


def header(active):
    nav = "\n      ".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for href, label in NAV)
    return f'''<div class="util">
  <div class="wrap">
    <div class="l mono"><span>ISSN 2181-3035</span><span>Guvohnoma № 1540</span><span>Oyiga bir marta</span></div>
    <div class="r">
      <nav class="langs" aria-label="Til"><a href="#" aria-current="true">Oʻzbekcha</a><a href="#">Русский</a><a href="#">English</a></nav>
      <span class="auth"><a href="#">Kirish</a> · <a href="#">Roʻyxatdan oʻtish</a></span>
    </div>
  </div>
</div>

<header class="head">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="../svg/tvt-logo-horizontal-navy.svg" alt="Talqin va tadqiqotlar — ilmiy-uslubiy jurnal"></a>
    <nav id="nav" aria-label="Asosiy menyu">
      {nav}
    </nav>
    <div class="act">
      <label class="search" for="q">{ICON_SEARCH}<input id="q" type="search" placeholder="Maqola, muallif, kalit soʻz"></label>
      <a class="btn btn-primary" href="authors.html#yuborish">Maqola yuborish</a>
      <button class="menu-btn" aria-label="Menyu" aria-controls="nav" onclick="document.getElementById('nav').classList.toggle('open')">{ICON_MENU}</button>
    </div>
  </div>
</header>'''


FOOTER = '''<footer class="foot">
  <div class="wrap">
    <div class="top">
      <div>
        <img src="../svg/tvt-logo-horizontal-ivory.svg" alt="Talqin va tadqiqotlar">
        <p>Ilmiy-uslubiy jurnal. ISSN 2181-3035. Axborot va ommaviy kommunikatsiyalar agentligining 1540-son guvohnomasi.</p>
      </div>
      <div><h4>Nashrlar</h4><ul><li><a href="index.html">Joriy son</a></li><li><a href="archive.html">Arxiv</a></li><li><a href="archive.html#konferensiya">Konferensiya toʻplamlari</a></li></ul></div>
      <div><h4>Mualliflarga</h4><ul><li><a href="authors.html">Talablar</a></li><li><a href="authors.html#yuborish">Maqola yuborish</a></li><li><a href="#">Roʻyxatdan oʻtish</a></li></ul></div>
      <div><h4>Jurnal</h4><ul><li><a href="about.html">Jurnal haqida</a></li><li><a href="team.html">Tahririyat</a></li><li><a href="about.html#maxfiylik">Maxfiylik siyosati</a></li></ul></div>
    </div>
    <div class="bot"><span>© 2026 Talqin va tadqiqotlar</span><span>Fotosuratlar: Wikimedia Commons, CC BY-SA · Open Journal Systems</span></div>
  </div>
</footer>'''


def logos(cls="idx-logos"):
    items = "".join(
        f'<li><a href="{E(url)}" title="{E(name)}"><img src="img/indexing/{img}" alt="{E(name)}" loading="lazy"></a></li>'
        for img, name, url in INDEXING)
    return f'<ul class="{cls}">{items}</ul>'


def page(filename, title, active, body):
    doc = f'''<!doctype html>
<html lang="uz-Latn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<link rel="icon" href="../favicon.ico" sizes="any">
<link rel="icon" href="../svg/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>

{header(active)}

{body}

{FOOTER}

</body>
</html>
'''
    (HERE / filename).write_text(doc, encoding="utf-8")
    print("wrote", filename)


def page_head(crumb, h1, lede):
    return f'''<div class="wrap page-head">
    <nav class="crumbs" aria-label="Sahifa yoʻli"><a href="index.html">Bosh sahifa</a><span>/</span><span>{crumb}</span></nav>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>'''


# ---------------------------------------------------------------- archive
def issue_meta(item):
    t = item["title"].strip()
    kind = "konferensiya" if "konferensiya" in t.lower() else "son"
    date = re.search(r"(\d{2})[.,](\d{2})[.,](\d{4})", t)
    year = None
    if date:
        year = date.group(3)
    else:
        y = re.search(r"\((\d{4})\)", item["series"] + " " + t) or re.search(r"^(\d{4})$", item["series"])
        year = y.group(1) if y else None
    # tidy title: matching quotes, no trailing date when shown separately
    t = re.sub(r'^[“"]?Talqin va tadqiqotlar["”]', "“Talqin va tadqiqotlar”", t)
    t = t.replace('“Talqin va tadqiqotlar"', "“Talqin va tadqiqotlar”")
    t = re.sub(r"[,/]\s*\d{2}[.,]\d{2}[.,]\d{4}$", "", t).strip()
    if t.startswith("Том 1"):
        n = re.search(r"№\s*(\d+)", t)
        t = f"Jurnalning {n.group(1)}-soni" if n else t
    t = t.replace("Том 1 ", "").replace("Том", "Tom")
    # short display titles: the kind label above already says what it is
    low = t.lower()
    if kind == "konferensiya":
        if "magistrant" in low:
            t = "Magistrantlar talqinida: ilmiy-amaliy konferensiya"
        elif "yosh tadqiqotchilar" in low:
            n = re.search(r"(\d+)-sonli", t)
            t = f"Yosh tadqiqotchilar talqinida: {n.group(1)}-onlayn konferensiya" if n else "Yosh tadqiqotchilar talqinida"
        else:
            n = re.search(r"№\s*(\d+)", t)
            t = f"Respublika ilmiy konferensiyasi № {n.group(1)}" if n else "Respublika ilmiy konferensiyasi"
    else:
        pair = re.search(r"(\d+)\((\d+)\)\s*-\s*(\d+)\((\d+)\)", t)
        one = re.search(r"(\d+)\((\d+)\)", t)
        plain = re.search(r"(\d+)-so", t)
        if pair:
            t = f"№ {pair.group(1)} ({pair.group(2)}) – {pair.group(3)} ({pair.group(4)})"
        elif one:
            t = f"№ {one.group(1)} ({one.group(2)})"
        elif plain:
            t = f"№ {plain.group(1)}"
    when =f"{date.group(1)}.{date.group(2)}.{date.group(3)}" if date else (year or "")
    series = item["series"].replace("Том", "Tom")
    return {"kind": kind, "year": year or "", "title": uz(t), "when": when, "series": series,
            "cover": item["cover"], "id": item["id"]}


def build_archive():
    items = [issue_meta(x) for x in json.loads((DATA / "archive.json").read_text(encoding="utf-8"))]
    def sort_key(i):
        d = re.match(r"(\d{2})\.(\d{2})\.(\d{4})", i["when"])
        return (i["year"] or "0000", (d.group(2) + d.group(1)) if d else "0000")
    items.sort(key=sort_key, reverse=True)
    years = []
    for i in items:
        y = i["year"] or "Yil koʻrsatilmagan"
        if not years or years[-1][0] != y:
            years.append((y, []))
        years[-1][1].append(i)
    n_son = sum(1 for i in items if i["kind"] == "son")
    n_konf = len(items) - n_son
    groups = []
    for y, its in years:
        cards = []
        for i in its:
            cov = (f'<img src="https://talqinvatadqiqotlar.uz/public/journals/1/cover_issue_{i["cover"]}_ru_RU.jpg" alt="" loading="lazy">'
                   if i["cover"] else '<span class="nocover">Muqova yoʻq</span>')
            label = "Konferensiya toʻplami" if i["kind"] == "konferensiya" else "Jurnal soni"
            cards.append(f'''<li class="issue" data-kind="{i["kind"]}" data-text="{E(i["title"].lower())}">
          <a href="#"><span class="cov">{cov}</span>
          <span class="kind">{label}</span>
          <b>{E(i["title"])}</b>
          <span class="mono">{E(i["when"] or i["series"])}</span></a></li>''')
        groups.append(f'''<section class="year" data-year="{E(y)}">
      <h2>{E(y)}</h2>
      <ul class="issues">
        {"".join(cards)}
      </ul>
    </section>''')
    body = f'''<main>
  {page_head("Arxiv", "Arxiv", "Jurnal sonlari va “Ilm-fan muammolari tadqiqotchilar talqinida” respublika ilmiy konferensiyalari toʻplamlari. Jami 152 ta nashr.")}
  <div class="wrap">
    <div class="toolbar" role="group" aria-label="Saralash">
      <div class="seg">
        <button type="button" class="on" data-filter="all" aria-pressed="true">Barchasi <span class="mono">{len(items)}</span></button>
        <button type="button" data-filter="son" aria-pressed="false">Jurnal sonlari <span class="mono">{n_son}</span></button>
        <button type="button" data-filter="konferensiya" aria-pressed="false" id="konferensiya">Konferensiya toʻplamlari <span class="mono">{n_konf}</span></button>
      </div>
      <label class="search wide" for="aq">{ICON_SEARCH}<input id="aq" type="search" placeholder="Nashr nomi yoki sana"></label>
    </div>
    {"".join(groups)}
    <p class="empty" hidden>Hech narsa topilmadi. Boshqa soʻz bilan qidirib koʻring.</p>
    <p class="note">Maketda arxivning birinchi ikki sahifasidagi 50 ta nashr koʻrsatilgan. Saytda roʻyxat yillar boʻyicha avtomatik shakllanadi.</p>
  </div>
</main>
<script>
(() => {{
  const btns = [...document.querySelectorAll('.seg button')];
  const q = document.getElementById('aq');
  let kind = 'all';
  function apply() {{
    const s = q.value.trim().toLowerCase();
    let shown = 0;
    document.querySelectorAll('.year').forEach(sec => {{
      let n = 0;
      sec.querySelectorAll('.issue').forEach(li => {{
        const ok = (kind === 'all' || li.dataset.kind === kind) && (!s || li.dataset.text.includes(s) || li.textContent.toLowerCase().includes(s));
        li.hidden = !ok; if (ok) n++;
      }});
      sec.hidden = n === 0; shown += n;
    }});
    document.querySelector('.empty').hidden = shown > 0;
  }}
  btns.forEach(b => b.addEventListener('click', () => {{
    kind = b.dataset.filter;
    btns.forEach(x => {{ x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', String(x === b)); }});
    apply();
  }}));
  q.addEventListener('input', apply);
  if (location.hash === '#konferensiya') document.getElementById('konferensiya').click();
}})();
</script>'''
    page("archive.html", "Arxiv — Talqin va tadqiqotlar", "archive.html", body)


# ---------------------------------------------------------------- authors
RULES = [
    "Maqolalar oʻzbek, rus yoki ingliz tilida yozilgan boʻlishi kerak.",
    "Maqola qaysi tilda yozilishidan qatʼi nazar, unda ingliz tilida sarlavha, qisqa annotatsiya va kalit soʻzlar boʻlishi shart. Maqola jurnal yoʻnalishiga oid dolzarb mavzuda, tugallangan ilmiy fikrga asoslangan, taklif va tavsiyalar bilan taqdim etiladi.",
    "Maqola Microsoft Word formatida, Times New Roman 14 shriftida, satrlar orasi 1,15 intervalda terilgan holda elektron shaklda topshiriladi.",
    "Maqolaning umumiy hajmi (rasm, jadval va diagrammalar bilan) kamida 5 sahifa boʻlishi kerak.",
    "Muallifning familiyasi, ismi-sharifi, ish joyi, lavozimi, manzili va elektron pochtasi koʻrsatiladi.",
    "Rasm, jadval, diagramma va chizmalar aniq tasvirlanadi, qisqartmalarning toʻliq izohi beriladi. Formulalar maxsus kompyuter dasturlarida kiritiladi.",
    "Foydalanilgan adabiyotlar maqola oxirida matndagi ketma-ketlik boʻyicha umumiy roʻyxatda beriladi. Kitoblar uchun muallif, toʻliq nom, shahar va nashr yili; maqolalar uchun muallif, maqola nomi, jurnal nomi, yili, soni va sahifalari koʻrsatiladi.",
    "Tahririyatga taqdim etilgan maqolalar taqrizga beriladi. Zarur boʻlsa, maqola savol va eʼtirozlar bilan muallifga qayta ishlash uchun qaytariladi.",
    "Ijobiy taqriz olgan maqola qabul qilingan hisoblanadi. Tahririyat matnni qisqartirish va tahririy oʻzgartirishlar kiritish huquqiga ega.",
]
CHECKLIST = [
    "Maqola ilgari nashr etilmagan va boshqa jurnalga yuborilmagan.",
    "Fayl Microsoft Word, OpenOffice yoki RTF formatida.",
    "Havolalar uchun toʻliq internet manzillar (URL) koʻrsatilgan.",
    "Rasm, grafik va jadvallar matnning tegishli joylarida joylashgan.",
    "Matn ushbu sahifadagi talablarga mos keladi.",
]


def build_authors():
    rules = "".join(f"<li>{E(r)}</li>" for r in RULES)
    check = "".join(f"<li>{E(c)}</li>" for c in CHECKLIST)
    body = f'''<main>
  {page_head("Mualliflarga", "Mualliflarga", "Maqolani tayyorlash, yuborish va nashr etish tartibi. Talablarga javob bermaydigan maqolalar koʻrib chiqilmaydi.")}
  <div class="wrap two-col">
    <div class="prose-page">
      <dl class="facts-grid">
        <div><dt>Maqola qabuli</dt><dd>Har oyning 25-sanasigacha</dd></div>
        <div><dt>Nashr sanasi</dt><dd>Har oyning 30-sanasi, fevraldan tashqari</dd></div>
        <div><dt>Bazalarda koʻrinadi</dt><dd>Nashrdan keyin 7 ish kuni ichida</dd></div>
        <div><dt>Nashr toʻlovi</dt><dd>150 000 soʻm, maqola qabul qilingandan soʻng</dd></div>
      </dl>

      <section id="rasmiylashtirish">
        <h2>Rasmiylashtirish</h2>
        <table class="spec">
          <tbody>
            <tr><th scope="row">Fayl</th><td>Microsoft Word (.docx)</td></tr>
            <tr><th scope="row">Shrift</th><td>Times New Roman, 14 pt</td></tr>
            <tr><th scope="row">Satrlar orasi</th><td>1,15</td></tr>
            <tr><th scope="row">Hajm</th><td>Kamida 5 sahifa, rasm va jadvallar bilan</td></tr>
            <tr><th scope="row">Ingliz tilida</th><td>Sarlavha, annotatsiya, kalit soʻzlar</td></tr>
            <tr><th scope="row">Tillar</th><td>Oʻzbek, rus, ingliz</td></tr>
          </tbody>
        </table>
      </section>

      <section id="talablar">
        <h2>Maqolaga qoʻyiladigan talablar</h2>
        <ol class="rules">{rules}</ol>
      </section>

      <section id="yuborish">
        <h2>Maqolani yuborish</h2>
        <ol class="steps">
          <li><b>Roʻyxatdan oʻting</b><span>Saytda muallif sifatida hisob yarating yoki kiring.</span></li>
          <li><b>Maqolani yuklang</b><span>Shaxsiy kabinetda “Yangi maqola” tugmasini bosing va faylni biriktiring.</span></li>
          <li><b>Taqrizni kuting</b><span>Tahrir hayʼati maqolani koʻrib chiqadi va natijani kabinetga yuboradi.</span></li>
          <li><b>Toʻlov va nashr</b><span>Qabul qilingan maqola toʻlovdan soʻng navbatdagi sonda chiqadi.</span></li>
        </ol>
        <h3>Yuborishdan oldin tekshiring</h3>
        <ul class="check">{check}</ul>
      </section>
    </div>
    <aside class="side-rail">
      <a class="btn btn-primary wide-btn" href="#">Maqola yuborish</a>
      <p class="note">Yuborish uchun saytga kiring yoki roʻyxatdan oʻting.</p>
      <div>
        <h3>Ushbu sahifada</h3>
        <ul class="toc-links"><li><a href="#rasmiylashtirish">Rasmiylashtirish</a></li><li><a href="#talablar">Talablar</a></li><li><a href="#yuborish">Yuborish tartibi</a></li></ul>
      </div>
      <div>
        <h3>Maqolalar uchun javobgarlik</h3>
        <p class="note">Maqolada keltirilgan maʼlumotlar uchun mualliflar masʼul.</p>
      </div>
    </aside>
  </div>
</main>'''
    page("authors.html", "Mualliflarga — Talqin va tadqiqotlar", "authors.html", body)


# ---------------------------------------------------------------- team
def build_team():
    members = json.loads((DATA / "team.json").read_text(encoding="utf-8"))
    cards = []
    for m in members:
        name = uz(m["name"])
        info = uz(m["info"]).replace("O`zbekiston", "Oʻzbekiston")
        initials = "".join(w[0] for w in name.split()[:2])
        cards.append(f'''<li data-text="{E((name + " " + info).lower())}"><span class="ini" aria-hidden="true">{E(initials)}</span>
          <div><b>{E(name)}</b><span>{E(info)}</span></div></li>''')
    body = f'''<main>
  {page_head("Tahririyat", "Tahririyat", "Jurnal tahririyati va tahrir kengashi: Oʻzbekiston oliy taʼlim muassasalari va ilmiy institutlarining olimlari.")}
  <div class="wrap">
    <div class="chiefs">
      <div><span class="label">Bosh muharrir</span><b>I. I. Abdumannonov</b></div>
      <div><span class="label">Masʼul muharrir</span><b>O. S. Isroilov</b></div>
    </div>
    <div class="toolbar">
      <h2>Tahrir kengashi <span class="mono">{len(members)}</span></h2>
      <label class="search wide" for="tq">{ICON_SEARCH}<input id="tq" type="search" placeholder="Ism, oliygoh yoki fan"></label>
    </div>
    <ul class="board">
      {"".join(cards)}
    </ul>
    <p class="empty" hidden>Hech kim topilmadi.</p>
  </div>
</main>
<script>
(() => {{
  const q = document.getElementById('tq');
  const items = [...document.querySelectorAll('.board li')];
  q.addEventListener('input', () => {{
    const s = q.value.trim().toLowerCase(); let n = 0;
    items.forEach(li => {{ const ok = !s || li.dataset.text.includes(s); li.hidden = !ok; if (ok) n++; }});
    document.querySelector('.empty').hidden = n > 0;
  }});
}})();
</script>'''
    page("team.html", "Tahririyat — Talqin va tadqiqotlar", "team.html", body)


# ---------------------------------------------------------------- about
AREAS = [("01.00.00", "Fizika-matematika"), ("02.00.00", "Kimyo"), ("03.00.00", "Biologiya"),
         ("04.00.00", "Geologiya va mineralogiya"), ("05.00.00", "Texnika"), ("06.00.00", "Qishloq xoʻjaligi"),
         ("07.00.00", "Tarix"), ("08.00.00", "Iqtisodiyot"), ("09.00.00", "Falsafa"), ("10.00.00", "Filologiya"),
         ("11.00.00", "Geografiya"), ("12.00.00", "Yuridik fanlar"), ("13.00.00", "Pedagogika"),
         ("14.00.00", "Tibbiyot"), ("15.00.00", "Farmatsevtika"), ("16.00.00", "Veterinariya"),
         ("17.00.00", "Sanʼatshunoslik"), ("18.00.00", "Arxitektura"), ("19.00.00", "Psixologiya"),
         ("22.00.00", "Sotsiologiya")]


def build_about():
    areas = "".join(f'<li><span class="mono">{c}</span><span>{n}</span></li>' for c, n in AREAS)
    body = f'''<main>
  {page_head("Jurnal haqida", "Jurnal haqida", "“Talqin va tadqiqotlar” — “Ilm-fan va ilmiy faoliyat toʻgʻrisida”gi Qonun hamda ilm-fan va taʼlimni rivojlantirishga oid Prezident qarorlari ijrosini taʼminlash maqsadida taʼsis etilgan ilmiy-uslubiy jurnal.")}
  <div class="wrap two-col">
    <div class="prose-page">
      <section>
        <h2>Asosiy maʼlumotlar</h2>
        <table class="spec">
          <tbody>
            <tr><th scope="row">ISSN</th><td class="mono">2181-3035</td></tr>
            <tr><th scope="row">Roʻyxatdan oʻtgan</th><td>Oʻzbekiston Respublikasi Prezidenti Administratsiyasi huzuridagi Axborot va ommaviy kommunikatsiyalarni rivojlantirish agentligi, guvohnoma № 1540</td></tr>
            <tr><th scope="row">Nashr shakli</th><td>Elektron</td></tr>
            <tr><th scope="row">Davriylik</th><td>Har oy, 30-sanasida (fevraldan tashqari)</td></tr>
            <tr><th scope="row">Rasmiy tillar</th><td>Oʻzbek, rus, ingliz</td></tr>
            <tr><th scope="row">Maqola qabuli</th><td>Har oyning 25-sanasigacha</td></tr>
            <tr><th scope="row">Sayt</th><td class="mono">talqinvatadqiqotlar.uz</td></tr>
          </tbody>
        </table>
      </section>

      <section>
        <h2>Ilmiy yoʻnalishlar</h2>
        <p class="sub">Oliy attestatsiya komissiyasi ixtisosliklari shifrlari boʻyicha.</p>
        <ul class="areas compact">{areas}</ul>
      </section>

      <section>
        <h2>Indekslanadi</h2>
        <p class="sub">Qabul qilingan maqolalar nashrdan keyin 7 ish kuni ichida quyidagi bazalarda koʻrinadi.</p>
        {logos("idx-logos big")}
      </section>

      <section id="maxfiylik">
        <h2>Maxfiylik siyosati</h2>
        <p>Jurnal saytiga kiritilgan ism va elektron pochta manzillari faqat jurnal belgilagan maqsadlarda foydalaniladi. Ular boshqa maqsadlarda ishlatilmaydi va uchinchi shaxslarga berilmaydi.</p>
      </section>
    </div>
    <aside class="side-rail">
      <figure class="side-photo">
        <img src="../photos/shahizinda-tiles.jpg" width="960" height="640" alt="Shohi Zinda majmuasidagi maqbara devorining moviy koshin bezagi" loading="lazy">
        <figcaption>Shohi Zinda majmuasi, Samarqand. Foto: <a class="lnk" href="https://commons.wikimedia.org/wiki/File:Samarkand_Shah-i-Zinda_Khodja-Akhmad_Mausoleum_detail_4.JPG">Wikimedia Commons</a>, CC BY-SA 3.0</figcaption>
      </figure>
      <div>
        <h3>Tezkor havolalar</h3>
        <ul class="toc-links"><li><a href="team.html">Tahririyat</a></li><li><a href="authors.html">Mualliflarga</a></li><li><a href="archive.html">Arxiv</a></li></ul>
      </div>
    </aside>
  </div>
</main>'''
    page("about.html", "Jurnal haqida — Talqin va tadqiqotlar", "about.html", body)


# ---------------------------------------------------------------- refresh index.html / article.html
def refresh(filename, active):
    p = HERE / filename
    s = p.read_text(encoding="utf-8")
    s = re.sub(r'<div class="util">.*?</header>', lambda m: header(active), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="foot">.*?</footer>', lambda m: FOOTER, s, count=1, flags=re.S)
    s = re.sub(r'<ul class="idx">.*?</ul>|<ul class="idx-logos">.*?</ul>', lambda m: logos(), s, count=1, flags=re.S)
    s = s.replace('<a class="btn btn-quiet" href="#">Talablar</a>', '<a class="btn btn-quiet" href="authors.html">Talablar</a>')
    s = s.replace('<a class="btn btn-primary" href="#">Maqola yuborish</a><a class="btn btn-quiet" href="authors.html">Talablar</a>',
                  '<a class="btn btn-primary" href="authors.html#yuborish">Maqola yuborish</a><a class="btn btn-quiet" href="authors.html">Talablar</a>')
    s = s.replace('<a class="btn btn-quiet" href="#">Barcha sonlar</a>', '<a class="btn btn-quiet" href="archive.html">Barcha sonlar</a>')
    s = s.replace('<a class="lnk" href="#">Barcha 152 son va toʻplam</a>', '<a class="lnk" href="archive.html">Barcha 152 son va toʻplam</a>')
    s = s.replace('<a class="all" href="#">', '<a class="all" href="archive.html">')
    s = s.replace('<a class="lnk" href="#">Tahririyat</a><a class="lnk" href="#">Nashr etikasi</a><a class="lnk" href="#">Maxfiylik siyosati</a>',
                  '<a class="lnk" href="team.html">Tahririyat</a><a class="lnk" href="authors.html">Mualliflarga</a><a class="lnk" href="about.html#maxfiylik">Maxfiylik siyosati</a>')
    s = s.replace('<a href="#">Arxiv</a><span>/</span>', '<a href="archive.html">Arxiv</a><span>/</span>')
    p.write_text(s, encoding="utf-8")
    print("refreshed", filename)


if __name__ == "__main__":
    build_archive()
    build_authors()
    build_team()
    build_about()
    refresh("index.html", "index.html")
    refresh("article.html", "index.html")
