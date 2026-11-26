# Bücherei Münzbach – Website

Website der Öffentlichen Bücherei der Pfarre Münzbach. Umsetzung: Social Agency.

## Stand

Fertige statische Website, Hosting über Netlify. Kein Framework; der Netlify-Build kopiert nur die auszuliefernden Dateien nach `dist/`.

| Seite | Datei |
|---|---|
| Startseite | `index.html` |
| Angebot | `angebot.html` |
| Veranstaltungen | `veranstaltungen.html` |
| Team | `team.html` |
| Artikel & Downloads | `artikel.html` |
| Kontakt | `kontakt.html` |
| Impressum, Datenschutz, 404 | `impressum.html`, `datenschutz.html`, `404.html` |

## Struktur

- `assets/` – CSS, JavaScript, lokal eingebundene Schriften (Manrope, Nunito – keine Google-Fonts-Verbindung), Logo
- `images/` – Fotos (jeweils 1600 px und 800 px), Porträts (800 und 400 px), Unterstützer-Logos (PNG, transparent)
- `downloads/` – Beiträge aus Pfarrblatt und Rundblick als PDF
- Kontaktformular über **Netlify Forms** (Formulare `kontakt` und `kontakt-kurz`, Spam-Schutz über das versteckte Feld `website`)
- `netlify.toml` – Build, Weiterleitungen, Header
- `api/`, `vercel.json`, `.vercelignore` – alte Vercel-Variante, wird auf Netlify nicht verwendet
- `content/*.json` – Team, Beiträge, Unterstützer: Startdaten für das spätere Supabase-Backoffice
- `tools/generate.py` – erzeugt die HTML-Seiten aus den JSON-Daten (`python3 tools/generate.py`)
- `_archiv/wireframe/` – Klick-Prototyp, wird nicht ausgeliefert

## Go-live mit Netlify

1. Netlify → Add new site → Import an existing project → GitHub → Repo `buecherei_muenzbach` wählen. Build-Einstellungen kommen aus `netlify.toml` (nichts eintragen).
2. Forms aktivieren (Project configuration → Forms → Enable form detection), danach neu deployen. Unter Forms → Form notifications eine E-Mail-Benachrichtigung an `buecherei.muenzbach@gmail.com` anlegen.
3. Domain unter Domain management hinzufügen, DNS beim Domain-Anbieter auf Netlify umstellen (HTTPS stellt Netlify automatisch aus).
4. Falls die Domain nicht `buecherei-muenzbach.at` ist: Domain in `tools/generate.py` (canonical, og:image, Schema), `robots.txt` und `sitemap.xml` anpassen.

Klappt der Versand nicht, bietet das Formular automatisch an, die Nachricht per E-Mail-Programm zu schicken.

## Termine

Kommende Termine stehen in `UPCOMING` in `tools/generate.py`. Datum, Uhrzeit und Ort für Google (strukturierte Daten „Event“) stehen je Titel in `EVENT_LD`. Die Sitemap wird beim Generieren neu geschrieben; das Änderungsdatum einer Seite ändert sich nur, wenn sich ihr Inhalt ändert. Vergangene Termine dort entfernen und bei Bedarf in `EVENTS` (Rückblick) übernehmen; ist `UPCOMING` leer, zeigt die Startseite automatisch die letzten Veranstaltungen.

## Vor dem Go-live mit der Bücherei klären

- Kartenmarkierung prüfen (Adresse Markt 1 laut Urkunde bestätigt)
- Impressum: Rechtsträger (Pfarre Münzbach) und Leitung bestätigen
- Datenschutzerklärung von jemandem mit DSGVO-Erfahrung prüfen lassen

## Nächster Schritt

Supabase-Backoffice unter `/admin`, damit die Bücherei Team, Termine, Buchtipp, Downloads und Hinweise selbst pflegen kann. Die Daten in `content/` dienen als Startbestand.
