#!/usr/bin/env python3
# Generiert die statischen Seiten der Bücherei Münzbach
import json, os
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = str(ROOT)
REPO = str(ROOT)
team = json.load(open(f'{REPO}/content/team.json'))
articles = json.load(open(f'{REPO}/content/articles.json'))
sponsors = json.load(open(f'{REPO}/content/sponsors.json'))

import hashlib
def ver(rel): return hashlib.md5(open(f'{OUT}/{rel}','rb').read()).hexdigest()[:8]
CSSV = ver('assets/css/style.css'); JSV = ver('assets/js/main.js')
EMAIL = 'buecherei.muenzbach@gmail.com'
TEL = '+43 680 3269469'; TELH = '+436803269469'
ADR = 'Markt 1, 4323 Münzbach'
CAT = 'https://www.biblioweb.at/muenzbach'
INSTA = 'https://www.instagram.com/buecherei.muenzbach/'
ROUTE = 'https://www.google.com/maps/search/?api=1&amp;query=Markt+1+4323+M%C3%BCnzbach'
OSM = 'https://www.openstreetmap.org/export/embed.html?bbox=14.6995%2C48.2425%2C14.7155%2C48.2500&amp;layer=mapnik&amp;marker=48.2464%2C14.7075'
HOURS = [('Dienstag', '18:00 – 19:00'), ('Donnerstag', '16:00 – 17:30'), ('Samstag', '08:30 – 10:00'), ('Sonntag', '09:00 – 11:00')]

EXT = '<svg class="ext" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>'
SR_NEW = '<span class="skip-sr" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)"> (öffnet in neuem Tab)</span>'
SEARCH = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
DL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>'
IG = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
I_DOOR = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1b6f7b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 21V4h11v17M16 7h3v14M3 21h18"/><circle cx="13" cy="13" r=".8" fill="#1b6f7b"/></svg>'
I_CAR = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1b6f7b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 16l1.5-5h11L19 16M4 16h16v3H4zM7 19v1.5M17 19v1.5"/></svg>'
I_ACC = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1b6f7b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="4.5" r="1.8"/><path d="M12 7v6h5l2 6M12 10H8"/><path d="M9.5 13.5a4.5 4.5 0 1 0 5 5"/></svg>'
I_CAL = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#1b6f7b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>'

def ext(href, label, cls='btn', extra=''):
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener"{extra}>{label}{EXT}{SR_NEW}</a>'

def pic(path, alt, cls='', sizes='(max-width: 860px) 100vw, 50vw', w=1600, h=1200, eager=False):
    base = path[:-4]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{path}" srcset="{base}-800.jpg 800w, {path} {w}w" sizes="{sizes}" alt="{alt}" '
            f'width="{w}" height="{h}" {load} decoding="async"{" class=" + chr(34) + cls + chr(34) if cls else ""}>')

IMG = {
 'neu': ('/images/buecherei/neuheitenregal.jpg', 'Helles Bücherregal mit Neuerscheinungen, davor ein Bücherwagen mit Bilderbüchern', 1600, 1200),
 'schild': ('/images/buecherei/schild-reich-der-buecher.jpg', 'Von Kindern gestaltetes Schild „Reich der Bücher“ mit bunten Handabdrücken', 1600, 1407),
 'sach': ('/images/buecherei/regal-sachbuecher-kinder.jpg', 'Regal mit Sach- und Jugendbüchern, die Titel frontal aufgestellt', 1200, 1600),
 'raumhoch': ('/images/buecherei/raum-ueberblick-hochformat.jpg', 'Hohe Holzregale unter dem Gewölbe der Bücherei', 1200, 1600),
 'eingang': ('/images/buecherei/eingang-pfarrhof.jpg', 'Eingang zum Pfarrhof Münzbach mit Holztür und Steinstufen', 1600, 1200),
 'theke': ('/images/buecherei/ausleihtheke.jpg', 'Ausleihtheke mit Prospekten, dahinter die Bücherregale', 1200, 1600),
 'romane': ('/images/buecherei/regalgang-romane.jpg', 'Gang zwischen zwei Regalreihen mit Romanen und Krimis', 1200, 1600),
 'kinder': ('/images/buecherei/kinderregal-spiele-tonies.jpg', 'Kinderregal mit bunten Büchern, Spielen und Tonies', 1200, 1600),
 'ecke': ('/images/buecherei/buchtipp-ecke.jpg', 'Ecke mit Buchempfehlungen auf Holzkisten und einem rot gedeckten Tisch', 1600, 1200),
 'raum': ('/images/buecherei/raum-ueberblick.jpg', 'Innenraum der Bücherei mit Regalen und einem Trog voller Bilderbücher', 1600, 1200),
 'theke2': ('/images/buecherei/theke-und-regale.jpg', 'Arbeitsplatz an der Ausleihe mit Blick auf die Regale', 1200, 1600),
}
def P(k, cls='', sizes='(max-width: 860px) 100vw, 50vw', eager=False):
    p, a, w, h = IMG[k]; return pic(p, a, cls, sizes, w, h, eager)

NAV = [('index', 'Startseite', '/'), ('angebot', 'Angebot', '/angebot'), ('veranstaltungen', 'Veranstaltungen', '/veranstaltungen'),
       ('team', 'Team', '/team'), ('artikel', 'Artikel & Downloads', '/artikel'), ('kontakt', 'Kontakt', '/kontakt')]

def header(cur):
    links = '\n'.join(f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if k == cur else ""}>{t.replace("&", "&amp;")}</a>' for k, t, h in NAV)
    return f'''<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="site-header">
<div class="wrap">
<a class="brand" href="/" aria-label="Bücherei Münzbach – zur Startseite"><img src="/assets/img/logo-buecherei.png" alt="Bücherei Münzbach" width="252" height="186"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="hauptnavigation" aria-label="Menü öffnen"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<nav class="nav" id="hauptnavigation" aria-label="Hauptnavigation">
{links}
<a class="nav-cta" href="{CAT}" target="_blank" rel="noopener">{SEARCH}Online-Katalog{SR_NEW}</a>
</nav>
</div>
</header>'''

def hours_dl(cls='hours'):
    return f'<dl class="{cls}">' + ''.join(f'<dt>{d}</dt><dd>{t}</dd>' for d, t in HOURS) + '</dl>'

FOOTER = f'''<footer class="site-footer">
<div class="wrap">
<div class="cols">
<div class="stack">
<span class="name">Bücherei Münzbach</span>
<p class="soft">Öffentliche Bücherei der Pfarre Münzbach. Rund 4.400 Bücher, Spiele, Hörbücher und Tonies zum Ausleihen.</p>
<a href="{INSTA}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:10px;font-weight:700;text-decoration:none;min-height:44px">{IG}@buecherei.muenzbach{SR_NEW}</a>
</div>
<div>
<h2>Öffnungszeiten</h2>
{hours_dl('f-hours')}
<p class="soft" style="margin-top:10px">An Feiertagen geschlossen.</p>
</div>
<div class="stack" style="gap:6px">
<h2>Kontakt</h2>
<span>{ADR}</span>
<a href="mailto:{EMAIL}">{EMAIL}</a>
<span>Martina: <a href="tel:{TELH}">{TEL}</a><br><span class="soft">(WhatsApp bevorzugt)</span></span>
</div>
<div>
<h2>Links</h2>
<div class="links">
<a href="{CAT}" target="_blank" rel="noopener">Online-Katalog (Biblioweb) ↗{SR_NEW}</a>
<a href="https://www.dioezese-linz.at/pfarre/4240" target="_blank" rel="noopener">Pfarre Münzbach ↗{SR_NEW}</a>
<a href="/kontakt#anfahrt">Anfahrt &amp; Parken</a>
<a href="/kontakt">Medienwunsch senden</a>
</div>
</div>
</div>
<div class="bottom">
<span>© 2026 Öffentliche Bücherei der Pfarre Münzbach</span>
<nav aria-label="Rechtliches"><a href="/impressum">Impressum</a><a href="/datenschutz">Datenschutz</a></nav>
</div>
</div>
</footer>'''

def page(slug, title, desc, cur, body):
    t = 'Bücherei Münzbach' if slug == 'index' else f'{title} – Bücherei Münzbach'
    canon = 'https://www.buecherei-muenzbach.at' + ('/' if slug == 'index' else '/' + slug)
    ld = ''
    if slug == 'index':
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Library", "name": "Öffentliche Bücherei der Pfarre Münzbach",
            "url": "https://www.buecherei-muenzbach.at/", "email": EMAIL, "telephone": TELH,
            "address": {"@type": "PostalAddress", "streetAddress": "Markt 1", "postalCode": "4323", "addressLocality": "Münzbach", "addressCountry": "AT"},
            "openingHoursSpecification": [
                {"@type": "OpeningHoursSpecification", "dayOfWeek": "Tuesday", "opens": "18:00", "closes": "19:00"},
                {"@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "16:00", "closes": "17:30"},
                {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:30", "closes": "10:00"},
                {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "09:00", "closes": "11:00"}],
            "sameAs": [INSTA, CAT]}, ensure_ascii=False) + '</script>\n'
    html = f'''<!doctype html>
<html lang="de-AT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://www.buecherei-muenzbach.at/images/buecherei/neuheitenregal.jpg">
<meta property="og:locale" content="de_AT">
<meta name="theme-color" content="#1b6f7b">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/nunito-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={CSSV}">
{ld}</head>
<body>
{header(cur)}
<main id="inhalt">
{body}
</main>
{FOOTER}
<script src="/assets/js/main.js?v={JSV}" defer></script>
</body>
</html>
'''
    open(f'{OUT}/{slug}.html', 'w', encoding='utf-8').write(html)

# ---------- Bausteine ----------
def visit():
    return f'''<section class="visit" id="zeiten" aria-labelledby="h-besuch">
<h2 id="h-besuch">Dein Besuch in der Bücherei</h2>
<div class="grid g3">
<div class="card pad"><h3 class="card-title">Öffnungszeiten</h3>{hours_dl()}<p class="note"><strong>An Feiertagen ist die Bücherei geschlossen.</strong></p></div>
<div class="card pad"><h3 class="card-title">So findest du uns</h3>
<p style="font-size:19px;font-weight:700;line-height:1.5">{ADR}</p>
<p class="info">{I_DOOR}<span><strong>Eingang:</strong> direkt im Pfarrheim</span></p>
<p class="info">{I_CAR}<span><strong>Parken:</strong> am Marktplatz oder am Kirchenparkplatz</span></p>
<p class="info">{I_ACC}<span><strong>Barrierefreiheit:</strong> Der Eingang ist leider nur über Stufen erreichbar.</span></p>
{ext(ROUTE, "Route planen", "btn2 btn-sm", ' style="align-self:flex-start;margin-top:auto"')}
</div>
<div class="card pad"><h3 class="card-title">Schließtage</h3>
<ul class="facts closed">
<li><strong>[TT.MM.]</strong>[Anlass, z. B. Allerheiligen]</li>
<li><strong>[TT.MM.] – [TT.MM.]</strong>[z. B. Weihnachtspause]</li>
<li><strong>[TT.MM.] – [TT.MM.]</strong>[z. B. Sommerpause]</li>
</ul>
<p class="note"><strong>An Feiertagen ist die Bücherei geschlossen.</strong></p>
</div>
</div>
</section>'''

def form(prefix, full=False):
    chips = ''
    if full:
        chips = '''<fieldset class="chips"><legend class="legend">Worum geht es?</legend>
<label><input type="radio" name="anliegen" value="Medienwunsch" checked><span>Medienwunsch</span></label>
<label><input type="radio" name="anliegen" value="Frage"><span>Frage</span></label>
<label><input type="radio" name="anliegen" value="Ehrenamt"><span>Mitarbeiten</span></label>
<label><input type="radio" name="anliegen" value="Sonstiges"><span>Sonstiges</span></label>
</fieldset>'''
        row = f'''<div class="row2">
<div class="field"><label for="{prefix}-titel">Titel <small>(bei Medienwunsch)</small></label><input id="{prefix}-titel" name="titel" class="inp" type="text" placeholder="z. B. Titel des Buchs, Spiels oder Tonies"></div>
<div class="field"><label for="{prefix}-autor">Autor:in <small>(falls bekannt)</small></label><input id="{prefix}-autor" name="autor" class="inp" type="text"></div>
</div>'''
    else:
        row = f'''<div class="row2">
<div class="field"><label for="{prefix}-anliegen">Anliegen</label><select id="{prefix}-anliegen" name="anliegen" class="inp"><option>Medienwunsch</option><option>Frage</option><option>Sonstiges</option></select></div>
<div class="field"><label for="{prefix}-titel">Titel / Autor:in <small>(bei Medienwunsch)</small></label><input id="{prefix}-titel" name="titel" class="inp" type="text"></div>
</div>'''
    head = '<h2 style="font-size:clamp(28px,2.6vw,38px)">Nachricht &amp; Medienwunsch</h2>' if full else ''
    return f'''<form class="card" data-contact novalidate>
{head}{chips}
<div class="row2">
<div class="field"><label for="{prefix}-name">Name</label><input id="{prefix}-name" name="name" class="inp" type="text" autocomplete="name" placeholder="Vor- und Nachname" required></div>
<div class="field"><label for="{prefix}-mail">E-Mail</label><input id="{prefix}-mail" name="email" class="inp" type="email" autocomplete="email" placeholder="name@beispiel.at" required></div>
</div>
{row}
<div class="field"><label for="{prefix}-msg">Nachricht</label><textarea id="{prefix}-msg" name="nachricht" class="inp" rows="{5 if full else 4}"></textarea></div>
<div class="hp" aria-hidden="true"><label for="{prefix}-web">Website</label><input id="{prefix}-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<label class="consent"><input type="checkbox" name="zustimmung" value="ja" required><span>Ich bin einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage gespeichert werden. Mehr dazu in der <a href="/datenschutz">Datenschutzerklärung</a>.</span></label>
<button type="submit" class="btn" style="align-self:flex-start">Nachricht senden</button>
<p class="form-msg" role="status" tabindex="-1"></p>
</form>'''

def cta(title, text, href='/kontakt', label='Medienwunsch senden'):
    return f'<section class="cta"><div><h2>{title}</h2><p>{text}</p></div><a class="btn" href="{href}">{label}</a></section>'

def sponsors_block():
    items = '\n'.join(f'<li><img src="{s["logo"]}" alt="{s["name"]}" loading="lazy"></li>' for s in sponsors if s.get('logo'))
    return f'<section class="sponsors" aria-labelledby="h-unterst"><h2 class="eyebrow" id="h-unterst">Mit Unterstützung von</h2><ul class="logos">\n{items}\n</ul></section>'

def tm(m, size):
    src = m['image']; b = src[:-4]
    return f'<img src="{b}-400.jpg" srcset="{b}-400.jpg 400w, {src} 800w" sizes="{size}px" alt="Porträt von {m["name"]}" width="400" height="400" loading="lazy" decoding="async">'

MON={'Aug':'August','Mai':'Mai','Apr':'April','Dez':'Dezember','Sep':'September'}
EVENTS = [
 ('31', 'Aug', '2026', 'Für Kinder', 'Ferienaktion der Bücherei', 'Ein Nachmittag mit Spielen, Basteln und Vorlesen für Kinder – zum Abschluss der Sommerferien.', 'Pfarrblatt Sommer 2026'),
 ('22', 'Mai', '2026', 'Für Familien', 'Miteinanderfest mit Bücherwurm Willi', 'Gemeinsam mit Kindergarten und Krabbelstubengruppe: Abenteuer im Reich des Bücherwurms, im Pfarrgarten und in der Bücherei.', 'Pfarrblatt Sommer 2026'),
 ('24', 'Apr', '2026', 'Für Kinder', 'Lange Nacht der Bibliotheken', 'Lesetheater „Als der Mond die Sterne ordnen wollte“ nach Lena Raubaum – mit den Kindern einstudiert, Kulisse inklusive, Aufführung am Abend.', 'Pfarrblatt Sommer 2026'),
 ('13', 'Dez', '2025', 'Für Kinder & Familien', 'Lesezauber im Advent', 'Michael Hölzel aus Mauthausen las aus seinem Kinderbuch „Hexe Maxim und der Himmelszug“. Dazu wurden Engel aus alten Buchseiten gebastelt.', 'Rundblick März 2026'),
 ('20', 'Sep', '2025', 'Für alle', 'Büchereicafé mit Bücherflohmarkt', 'Bücher, Spiele und DVDs zum Schnäppchenpreis, dazu Kaffee und Kuchen. Mit dem Erlös wurden neue Medien angeschafft.', 'Rundblick November 2025'),
 ('01', 'Sep', '2025', 'Für Kinder von 6 bis 12', 'Bunte Ferienaktion', 'Spielen, Tanzen, Basteln und Vorlesen. Die Lesemännchen und Handabdrücke der Kinder schmücken seither die Bücherei.', 'Rundblick November 2025'),
]

# ---------- Kommende Termine (Platzhalter bis zur Pflege im Backoffice) ----------
UPCOMING = [
 ('Für Kinder', '[Vorlesestunde]', '[Wochentag], [Uhrzeit] · Bücherei Münzbach', 'Foto: Vorlesen in der Kinderecke'),
 ('Für Erwachsene', '[Lesung mit Autor:in]', '[Wochentag], [Uhrzeit] · [Ort]', 'Foto: Lesung'),
 ('Für die ganze Familie', '[Spielenachmittag]', '[Wochentag], [Uhrzeit] · Bücherei Münzbach', 'Foto: Spiele am Tisch'),
]
HOME_UP = [('[Vorlesestunde für Kinder]', '[Uhrzeit] · Bücherei Münzbach'), ('[Lesung / Buchausstellung]', '[Uhrzeit] · [Ort]'), ('[Spielenachmittag]', '[Uhrzeit] · Bücherei Münzbach')]
upcoming_home = '\n'.join(f'<a class="card ev" href="/veranstaltungen"><span class="date"><b>[TT]</b><small>[Monat]</small></span><span class="t"><strong>{t}</strong><span>{m}</span></span></a>' for t, m in HOME_UP)
upcoming_page = '\n'.join(f'''<article class="card up">
<span class="date date-lg"><b>[TT]</b><small>[Monat]</small></span>
<div class="ph">{ph}</div>
<div class="stack" style="gap:12px"><span class="tag">{tag}</span><h3>{t}</h3><span class="muted">{m}</span><p>[Kurzbeschreibung: Worum geht es, für wen ist es gedacht, braucht es eine Anmeldung?]</p></div>
</article>''' for tag, t, m, ph in UPCOMING)

# ---------- Startseite ----------
recent = '\n'.join(f'''<a class="card ev" href="/veranstaltungen#rueckblick"><span class="date" aria-hidden="true"><b>{d}</b><small>{m}</small></span><span class="t"><strong>{t}</strong><span>{int(d)}. {MON[m]} {y} · {tag}</span></span></a>'''
                   for d, m, y, tag, t, x, s in [(e[0], e[1], e[2], e[3], e[4], e[5], e[6]) for e in EVENTS[:3]] for m2 in [m])
home = f'''<div class="wrap">
<section class="hero" aria-labelledby="h-start">
<div class="stack">
<span class="eyebrow">Öffentliche Bücherei der Pfarre Münzbach</span>
<h1 id="h-start">Mehr Zeit für gute <span>Geschichten.</span></h1>
<p class="lead">Bücher, Spiele, Tonies und Hörbücher für Groß und Klein. Ausleihen, schmökern und sich beraten lassen – mitten in Münzbach.</p>
<div class="btns"><a class="btn" href="#zeiten">Öffnungszeiten ansehen</a>{ext(CAT, "Online-Katalog", "btn2")}</div>
</div>
<div class="hero-media">{P("neu", eager=True)}<div class="badge" aria-hidden="true">Für Groß &amp; Klein – jeder findet sein Buch</div></div>
</section>

{visit()}

<section class="section" aria-labelledby="h-fuerwen">
<div class="section-head"><div class="stack"><span class="eyebrow">Für wen</span><h2 id="h-fuerwen">Jeder findet sein Buch</h2></div><a class="more" href="/angebot">Ganzes Angebot ansehen →</a></div>
<div class="grid g3">
<a class="card aud" href="/angebot">{P("schild", sizes="(max-width: 860px) 100vw, 33vw")}<span class="body"><strong>Kinder</strong><span>Bilderbücher, Erstlesebücher und Tonies zum Mitnehmen.</span></span></a>
<a class="card aud c2" href="/angebot">{P("sach", sizes="(max-width: 860px) 100vw, 33vw")}<span class="body"><strong>Schulkinder &amp; Jugendliche</strong><span>Reihen, Comics, Fantasy, Sachbücher und Jugendromane.</span></span></a>
<a class="card aud c3" href="/angebot">{P("raumhoch", sizes="(max-width: 860px) 100vw, 33vw")}<span class="body"><strong>Erwachsene</strong><span>Romane, Bestseller, New Adult, Krimis, Thriller und Sachbücher – laufend ergänzt.</span></span></a>
</div>
<div class="card strip"><span class="ico">{SEARCH.replace('width="18" height="18"', 'width="32" height="32"').replace('currentColor', '#1b6f7b')}</span><span class="txt"><strong>Medienbestand online abfragen</strong><span>Im Online-Katalog siehst du, welche Bücher, Spiele und Tonies gerade verfügbar sind.</span></span>{ext(CAT, "Online-Katalog (Biblioweb)", "btn btn-sm")}</div>
</section>

<section class="section duo" aria-label="Buchtipp und Neuigkeiten">
<div class="card tip">
<span class="eyebrow">Buchtipp aus der Bücherei</span>
<div class="tip-inner">
<div class="cover" aria-hidden="true"><small>Kriminalroman</small><b>Donau so rot</b><small>Thomas Baum</small></div>
<div class="stack" style="gap:10px">
<h3>Donau so rot</h3>
<span class="meta">Thomas Baum · Kriminalroman</span>
<p>Ein Krimi eines Linzer Autors, der in der Region spielt. Gut für alle, die Spannung mit vertrauter Kulisse mögen.</p>
<span class="by">Empfohlen vom Bücherei-Team</span>
</div>
</div>
</div>
<div>
<div class="section-head" style="margin-bottom:20px"><div class="stack"><span class="eyebrow">Was ansteht</span><h2 style="font-size:clamp(28px,2.8vw,40px)">Veranstaltungen</h2></div><a class="more" href="/veranstaltungen">Alle Termine →</a></div>
<div class="ev-list">
{upcoming_home}
</div>
</div>
</section>

<section class="section" aria-labelledby="h-rundgang">
<div class="section-head"><div class="stack"><span class="eyebrow">Rundgang</span><h2 id="h-rundgang">Ein Blick in die Bücherei</h2><p class="lead">Vom Eingang über die Ausleihe bis zur Kinderecke: So sieht es bei uns aus.</p></div></div>
<div class="gallery">
{P("eingang", sizes="(max-width: 860px) 100vw, 50vw")}
{P("theke", sizes="(max-width: 860px) 50vw, 25vw")}
{P("romane", sizes="(max-width: 860px) 50vw, 25vw")}
{P("kinder", sizes="(max-width: 860px) 50vw, 25vw")}
{P("ecke", sizes="(max-width: 860px) 50vw, 25vw")}
</div>
</section>
</div>

<section class="quote" aria-label="Zitat">
<div class="wrap"><span class="eyebrow">Weniger Bildschirm, mehr Papier</span>
<blockquote>„Beim Lesen guter Bücher wächst die Seele empor.“</blockquote>
<cite>Voltaire</cite></div>
</section>

<div class="wrap">
<section class="section" aria-labelledby="h-team">
<div class="section-head"><div class="stack"><span class="eyebrow">Unser Team</span><h2 id="h-team">Die Geschichtenhüter:innen</h2><p class="lead">Elf Ehrenamtliche mit viel Freude am Lesen – und immer bereit für eine Empfehlung.</p></div><a class="more" href="/team">Das ganze Team →</a></div>
<div class="team-teaser">
{''.join(f'<div class="person">{tm(m, 220)}<strong>{m["name"]}</strong></div>' for m in team[:4])}
</div>
</section>

{cta("Ein Buch fehlt im Regal?", "Schick uns deinen Medienwunsch. Wir prüfen, ob wir es für die Bücherei besorgen können.", "#kontakt")}

{sponsors_block()}

<section class="contact" id="kontakt" aria-labelledby="h-kontakt">
<div class="stack">
<span class="eyebrow">Kontakt</span>
<h2 id="h-kontakt">Schreib uns</h2>
<p class="lead">Eine Frage, eine Anregung oder ein Medienwunsch – wir melden uns so bald wie möglich.</p>
<div class="contact-lines">
<span><strong>E-Mail:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></span>
<span><strong>Telefon (Martina):</strong> <a href="tel:{TELH}">{TEL}</a> (WhatsApp bevorzugt)</span>
<span><strong>Adresse:</strong> {ADR}</span>
</div>
<a class="more" href="/kontakt">Alle Kontaktdaten &amp; Anfahrt →</a>
</div>
{form("h")}
</section>
</div>'''
page('index', 'Startseite', 'Öffentliche Bücherei der Pfarre Münzbach: Bücher, Spiele, Tonies und Hörbücher für Groß und Klein. Öffnungszeiten, Angebot, Veranstaltungen und Online-Katalog.', 'index', home)

# ---------- Angebot ----------
def media(letter, color, t, x):
    return f'<div class="card pad media"><span class="dot" style="background:{color}" aria-hidden="true"><span style="font-family:var(--f-head);font-weight:800;font-size:28px;color:#fff">{letter}</span></span><strong>{t}</strong><span>{x}</span></div>'
angebot = f'''<section class="page-hero"><div class="wrap">
<div class="stack"><span class="eyebrow">Unser Angebot</span><h1>Bücher, Spiele &amp; Geschichten zum Hören</h1><p class="lead">Romane, Krimis, Kinderbücher, Sachbücher und mehr – laufend ergänzt. Kommen, stöbern, ausleihen.</p></div>
{P("raum", eager=True, sizes="(max-width: 860px) 100vw, 42vw")}
</div></section>
<div class="wrap">
<section class="section" aria-labelledby="h-medien">
<div class="section-head"><div class="stack"><span class="eyebrow">Medienarten</span><h2 id="h-medien">Was du bei uns ausleihen kannst</h2></div></div>
<div class="grid g4">
{media("B", "#1b6f7b", "Bücher", "Romane, Krimis, Thriller, New Adult, Sachbücher, Kinder- und Jugendbücher.")}
{media("S", "#3f6620", "Spiele", "Brett- und Kartenspiele für Familie, Freundeskreis und Spieleabende.")}
{media("T", "#8a6410", "Tonies", "Rund 40 Tonie-Figuren mit Hörspielen und Liedern für die Toniebox.")}
{media("H", "#2f7a90", "Hörbücher &amp; CDs", "Zum Zuhören unterwegs, beim Autofahren oder vor dem Einschlafen.")}
</div>
</section>
<section class="section" aria-labelledby="h-zielgr">
<div class="section-head"><div class="stack"><span class="eyebrow">Für wen</span><h2 id="h-zielgr">Für jedes Alter das Passende</h2></div></div>
<div class="grid g3">
<div class="card aud">{P("kinder", sizes="(max-width: 860px) 100vw, 33vw")}<span class="body"><strong>Kinder</strong><span>Bilderbücher, Erstlesebücher, Vorlesebücher und Tonies. Dazu Kinderspiele für zu Hause.</span></span></div>
<div class="card aud c2">{P("sach", sizes="(max-width: 860px) 100vw, 33vw")}<span class="body"><strong>Schulkinder &amp; Jugendliche</strong><span>Reihen, Comics, Fantasy und Jugendromane, außerdem Sachbücher für Schule und Freizeit.</span></span></div>
<div class="card aud c3">{P("romane", sizes="(max-width: 860px) 100vw, 33vw")}<span class="body"><strong>Erwachsene</strong><span>Romane, Bestseller, New Adult, Krimis und Thriller sowie Sachbücher zu Sport, Technik und Geschichte.</span></span></div>
</div>
</section>
<section class="card split" aria-labelledby="h-kat">
<div class="stack" style="gap:16px"><span class="eyebrow">Online-Katalog</span><h2 id="h-kat">Medienstand jederzeit abrufen</h2>
<p class="lead">Über Biblioweb siehst du den aktuellen Bestand der Bücherei Münzbach: welche Titel es gibt und ob sie gerade verfügbar sind – auch bequem am Handy.</p>
<div class="btns">{ext(CAT, "Online-Katalog (Biblioweb)")}</div></div>
{P("theke2", sizes="(max-width: 860px) 100vw, 40vw")}
</section>
{cta("Ein Buch fehlt im Regal?", "Schick uns deinen Medienwunsch – Titel und Autor:in genügen.")}
<div style="height:clamp(56px,7vw,96px)"></div>
</div>'''
page('angebot', 'Angebot', 'Bücher, Spiele, Tonies, Hörbücher und CDs zum Ausleihen in der Bücherei Münzbach – für Kinder, Jugendliche und Erwachsene. Mit Online-Katalog.', 'angebot', angebot)

# ---------- Veranstaltungen ----------
past = '\n'.join(f'''<article class="card past">
<div class="when"><span class="date" aria-hidden="true"><b>{d}</b><small>{m}</small></span><div class="stack" style="gap:2px"><span class="tag">{tag}</span><span class="muted" style="font-size:16px">{int(d)}. {MON[m]} {y}</span></div></div>
<h3>{t}</h3><p>{x}</p><span class="src">Quelle: {s}</span></article>''' for d, m, y, tag, t, x, s in EVENTS)
veran = f'''<section class="page-hero"><div class="wrap single"><div class="stack"><span class="eyebrow">Veranstaltungen</span><h1>Lesen, zuhören, mitmachen</h1><p class="lead">Lesungen, Vorlesetheater, Ferienaktionen und das Büchereicafé: In der Bücherei Münzbach ist das ganze Jahr über etwas los.</p></div></div></section>
<div class="wrap">
<section class="section" aria-labelledby="h-demn">
<div class="section-head"><div class="stack"><span class="eyebrow">Demnächst</span><h2 id="h-demn">Kommende Termine</h2></div></div>
<div class="up-list">
{upcoming_page}
</div>
</section>
<section class="section" id="rueckblick" aria-labelledby="h-rueck">
<div class="section-head"><div class="stack"><span class="eyebrow">Rückblick</span><h2 id="h-rueck">So war's</h2><p class="lead">Ein Auszug aus den vergangenen Veranstaltungen.</p></div></div>
<div class="grid g3">
{past}
</div>
</section>
{cta("Eine Idee für eine Veranstaltung?", "Lesung, Spielenachmittag oder Bastelaktion – wir freuen uns über Vorschläge.", "/kontakt", "Kontakt aufnehmen")}
<div style="height:clamp(56px,7vw,96px)"></div>
</div>'''
page('veranstaltungen', 'Veranstaltungen', 'Lesungen, Lange Nacht der Bibliotheken, Ferienaktion und Büchereicafé: Veranstaltungen der Bücherei Münzbach.', 'veranstaltungen', veran)

# ---------- Team ----------
members = '\n'.join(f'''<div class="card member">{tm(m, 190)}<strong>{m["name"]}</strong>{'<span class="role">Leitung</span>' if m.get("role") else ''}<span class="reads">Liest gerne: {m.get("reads") or "[Genre]"}</span></div>''' for m in team)
teamp = f'''<section class="page-hero"><div class="wrap single"><div class="stack"><span class="eyebrow">Unser Team</span><h1>Die Geschichtenhüter:innen</h1>
<p class="lead">Die Bücherei Münzbach gibt es seit 1890 – damals als einzelner Bücherschrank in der Pfarrkanzlei. 1994 wurden Pfarr- und Gemeindebücherei zusammengelegt. Heute betreuen elf Ehrenamtliche rund 4.400 Medien, die Ausleihe und die Veranstaltungen.</p></div></div></section>
<div class="wrap">
<section class="section" aria-labelledby="h-wer">
<div class="section-head"><h2 id="h-wer">Wer dich in der Bücherei berät</h2></div>
<div class="team-grid">
{members}
</div>
</section>
<section class="section" aria-labelledby="h-quali">
<div class="card split" style="margin-top:0;grid-template-columns:1fr">
<div class="stack" style="gap:14px"><span class="eyebrow">Ausgezeichnet</span><h2 id="h-quali">Qualitätsbestätigung des Büchereiverbands</h2>
<p class="lead">Im März 2025 hat der Büchereiverband Österreichs (BVÖ) der Bücherei Münzbach erstmals die Qualitätsbestätigung verliehen – gültig für fünf Jahre. Die Anforderungen dafür hat das Team gemeinsam erarbeitet und erfüllt.</p></div>
</div>
</section>
{cta("Ehrenamtlich mitarbeiten", "Du möchtest dich ehrenamtlich in der Bücherei engagieren? Dann melde dich gerne bei unseren Geschichtenhüter:innen.", "/kontakt", "Kontakt aufnehmen")}
<div style="height:clamp(56px,7vw,96px)"></div>
</div>'''
page('team', 'Team', 'Das ehrenamtliche Team der Bücherei Münzbach – die Geschichtenhüter:innen rund um Leiterin Martina Prinz.', 'team', teamp)

# ---------- Artikel ----------
def kb(f): return f'{round(os.path.getsize(OUT + f) / 1024)} KB'
thumbs = {'/downloads/pfarrblatt-2026-07.pdf': '/images/artikel-pfarrblatt-2026-07.jpg', '/downloads/rundblick-2026-03.pdf': '/images/artikel-rundblick-2026-03.jpg', '/downloads/pfarrblatt-2026-04.pdf': '/images/artikel-pfarrblatt-2026-04.jpg'}
feat = [a for a in articles if a['featured']]; rest = [a for a in articles if not a['featured']]
fc = '\n'.join(f'''<article class="card art">
<div class="thumb"><img src="{thumbs[a["file"]]}" alt="" width="640" height="905" loading="lazy"></div>
<div class="body"><span class="src">{a["medium"]} · {a["issue"]}</span><h3>{a["title"]}</h3><p>{a["teaser"]}</p>
<a class="btn btn-sm" style="align-self:flex-start" href="{a["file"]}" download>{DL}PDF herunterladen<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)"> ({a["medium"]} {a["issue"]}, {kb(a["file"])})</span></a></div>
</article>''' for a in feat)
rows = '\n'.join(f'''<div class="list-row"><span class="pdf" aria-hidden="true">PDF</span><span class="t"><strong>{a["title"]}</strong><span>{a["medium"]} · {a["issue"]} · {kb(a["file"])}</span></span><a class="btn2 btn-sm" href="{a["file"]}" download>Herunterladen<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">: {a["title"]}</span></a></div>''' for a in rest)
art = f'''<section class="page-hero"><div class="wrap single"><div class="stack"><span class="eyebrow">Artikel &amp; Downloads</span><h1>Zum Nachlesen und Mitnehmen</h1><p class="lead">Beiträge der Bücherei aus dem Pfarrblatt und dem Rundblick – alles als PDF zum Herunterladen.</p></div></div></section>
<div class="wrap">
<section class="section" aria-labelledby="h-art">
<div class="section-head"><div class="stack"><span class="eyebrow">Aktuell</span><h2 id="h-art">Aus Pfarrblatt &amp; Rundblick</h2></div></div>
<div class="grid g3">
{fc}
</div>
</section>
<section class="section" aria-labelledby="h-alt" style="padding-bottom:clamp(56px,7vw,96px)">
<h2 id="h-alt" style="font-size:clamp(24px,2.2vw,30px);margin-bottom:20px">Ältere Beiträge</h2>
<div class="card list">
{rows}
</div>
</section>
</div>'''
page('artikel', 'Artikel & Downloads', 'Beiträge der Bücherei Münzbach aus Pfarrblatt und Rundblick zum Nachlesen und als PDF zum Herunterladen.', 'artikel', art)

# ---------- Kontakt ----------
kont = f'''<section class="page-hero"><div class="wrap single"><div class="stack"><span class="eyebrow">Kontakt</span><h1>Schau vorbei oder schreib uns</h1><p class="lead">Fragen, Anregungen oder ein Buch, das dir im Regal fehlt – wir melden uns.</p></div></div></section>
<div class="wrap">
<div class="kontakt">
{form("k", True)}
<div class="side" id="anfahrt">
<div class="card pad"><h2 class="card-title">Öffnungszeiten</h2>{hours_dl()}<p class="muted" style="font-size:16px">An Feiertagen ist die Bücherei geschlossen.</p></div>
<div class="card pad"><h2 class="card-title">So findest du uns</h2>
<p>Öffentliche Bücherei der Pfarre Münzbach<br>{ADR}</p>
<p class="info">{I_DOOR}<span><strong>Eingang:</strong> direkt im Pfarrheim</span></p>
<p class="info">{I_CAR}<span><strong>Parken:</strong> am Marktplatz oder am Kirchenparkplatz</span></p>
<p class="info">{I_ACC}<span><strong>Barrierefreiheit:</strong> Der Eingang ist leider nur über Stufen erreichbar.</span></p>
<p style="padding-top:10px;border-top:1px solid var(--line)"><a href="mailto:{EMAIL}" style="color:inherit">{EMAIL}</a><br>Martina: <a href="tel:{TELH}" style="color:inherit">{TEL}</a> (WhatsApp bevorzugt)</p>
{ext(ROUTE, "Route planen", "btn2 btn-sm", ' style="align-self:flex-start"')}
</div>
<div class="map" data-map="{OSM}"><div><p>Die Karte wird von OpenStreetMap geladen. Dabei wird deine IP-Adresse an OpenStreetMap übertragen.</p><button type="button" class="btn2 btn-sm">Karte anzeigen</button></div></div>
<a class="card insta" href="{INSTA}" target="_blank" rel="noopener">{IG.replace('width="22" height="22"', 'width="30" height="30"').replace('currentColor"', '#1b6f7b"', 1)}<span><strong>@buecherei.muenzbach</strong><small>Neuheiten und Termine auf Instagram</small></span>{SR_NEW}</a>
</div>
</div>
</div>'''
page('kontakt', 'Kontakt', 'Kontakt zur Bücherei Münzbach: Öffnungszeiten, Anfahrt, E-Mail und Formular für Fragen und Medienwünsche.', 'kontakt', kont)

# ---------- Impressum ----------
imp = f'''<section class="page-hero"><div class="wrap single"><div class="stack"><h1>Impressum</h1></div></div></section>
<div class="wrap"><div class="prose">
<h2 style="margin-top:0">Medieninhaber und Herausgeber</h2>
<p>Öffentliche Bücherei der Pfarre Münzbach<br>Rechtsträger: Römisch-katholische Pfarre Münzbach<br>{ADR}<br>Österreich</p>
<p>E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a><br>Telefon: <a href="tel:{TELH}">{TEL}</a></p>
<h2>Leitung der Bücherei</h2>
<p>Martina Prinz</p>
<h2>Grundlegende Richtung</h2>
<p>Information über das Angebot, die Öffnungszeiten und die Veranstaltungen der Öffentlichen Bücherei der Pfarre Münzbach.</p>
<h2>Fotos</h2>
<p>Bücherei Münzbach. Logos der Unterstützer: jeweilige Unternehmen und Vereine.</p>
<h2>Umsetzung</h2>
<p>Social Agency, Perg – <a href="https://www.social-agency.at" target="_blank" rel="noopener">social-agency.at</a></p>
<h2>Haftung für Links</h2>
<p>Für die Inhalte verlinkter externer Seiten sind ausschließlich deren Betreiber verantwortlich.</p>
</div></div>'''
page('impressum', 'Impressum', 'Impressum der Website der Öffentlichen Bücherei der Pfarre Münzbach.', '', imp)

# ---------- Datenschutz ----------
ds = f'''<section class="page-hero"><div class="wrap single"><div class="stack"><h1>Datenschutzerklärung</h1></div></div></section>
<div class="wrap"><div class="prose">
<h2 style="margin-top:0">Verantwortlich</h2>
<p>Öffentliche Bücherei der Pfarre Münzbach, {ADR}, E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>Grundsatz</h2>
<p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Werbewerkzeuge und lädt keine Schriften oder Inhalte von Drittanbietern, solange du nicht selbst aktiv wirst (etwa beim Laden der Karte).</p>
<h2>Hosting</h2>
<p>Die Website wird bei Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, USA, betrieben. Beim Aufruf verarbeitet Vercel technisch notwendige Daten wie IP-Adresse, Datum und Uhrzeit, aufgerufene Seite und Browsertyp, um die Website auszuliefern und vor Missbrauch zu schützen (Art. 6 Abs. 1 lit. f DSGVO). Mit Vercel besteht ein Auftragsverarbeitungsvertrag; die Übermittlung in die USA erfolgt auf Grundlage des EU-US Data Privacy Framework bzw. von Standardvertragsklauseln.</p>
<h2>Kontaktformular und E-Mail</h2>
<p>Wenn du uns über das Formular oder per E-Mail schreibst, verarbeiten wir die angegebenen Daten (Name, E-Mail-Adresse, Nachricht, gegebenenfalls Medienwunsch) ausschließlich zur Bearbeitung deiner Anfrage (Art. 6 Abs. 1 lit. a und b DSGVO). Die Nachricht wird über den Versanddienst Resend (Resend Inc., USA) an unser Postfach weitergeleitet. Wir löschen die Daten, sobald die Anfrage erledigt ist und keine gesetzlichen Aufbewahrungspflichten bestehen.</p>
<h2>Karte (OpenStreetMap)</h2>
<p>Auf der Kontaktseite kannst du eine Karte von OpenStreetMap laden. Erst nach deinem Klick auf „Karte anzeigen“ wird eine Verbindung zu den Servern der OpenStreetMap Foundation (St John’s Innovation Centre, Cowley Road, Cambridge, CB4 0WS, Vereinigtes Königreich) aufgebaut und deine IP-Adresse übertragen (Art. 6 Abs. 1 lit. a DSGVO).</p>
<h2>Externe Links</h2>
<p>Links zum Online-Katalog (Biblioweb), zu Instagram, Google Maps und zur Pfarre Münzbach führen auf Seiten anderer Anbieter. Für die Datenverarbeitung dort sind die jeweiligen Betreiber verantwortlich.</p>
<h2>Deine Rechte</h2>
<p>Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie das Recht, eine erteilte Einwilligung jederzeit zu widerrufen. Wende dich dazu an <a href="mailto:{EMAIL}">{EMAIL}</a>. Du kannst dich außerdem bei der Österreichischen Datenschutzbehörde (<a href="https://www.dsb.gv.at" target="_blank" rel="noopener">dsb.gv.at</a>) beschweren.</p>
<p class="muted">Stand: Oktober 2026</p>
</div></div>'''
page('datenschutz', 'Datenschutz', 'Datenschutzerklärung der Website der Öffentlichen Bücherei der Pfarre Münzbach.', '', ds)

# ---------- 404 ----------
nf = f'''<section class="page-hero"><div class="wrap single"><div class="stack"><span class="eyebrow">Seite nicht gefunden</span><h1>Diese Seite gibt es leider nicht.</h1><p class="lead">Vielleicht hilft dir einer dieser Wege weiter.</p><div class="btns"><a class="btn" href="/">Zur Startseite</a><a class="btn2" href="/kontakt">Kontakt</a></div></div></div></section>'''
page('404', 'Seite nicht gefunden', 'Diese Seite wurde nicht gefunden.', '', nf)
print('ok')
