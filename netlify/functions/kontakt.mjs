// Netlify Function: Kontaktformular → E-Mail an die Bücherei (Versand über Resend)
// Erreichbar unter /api/kontakt (Weiterleitung in netlify.toml).
// Umgebungsvariablen in Netlify (Site configuration → Environment variables):
//   RESEND_API_KEY      – API-Schlüssel von resend.com
//   KONTAKT_EMPFAENGER  – z. B. buecherei.muenzbach@gmail.com
//   KONTAKT_ABSENDER    – verifizierte Absenderadresse, z. B. "Website Bücherei Münzbach <website@buecherei-muenzbach.at>"

const clean = (v, max) => String(v || '').replace(/\r/g, '').trim().slice(0, max);
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const json = (status, data, headers = {}) =>
  new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json', ...headers } });

export default async (req) => {
  if (req.method !== 'POST') return json(405, { error: 'Methode nicht erlaubt' }, { Allow: 'POST' });

  let body = {};
  try { body = (await req.json()) || {}; } catch (e) { body = {}; }

  // Spam-Schutz: verstecktes Feld muss leer bleiben
  if (body.website) return json(200, { ok: true });

  const name = clean(body.name, 120);
  const email = clean(body.email, 160);
  const anliegen = clean(body.anliegen, 40) || 'Anfrage';
  const titel = clean(body.titel, 200);
  const autor = clean(body.autor, 160);
  const nachricht = clean(body.nachricht, 5000);
  const zustimmung = body.zustimmung === 'ja';

  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || (!nachricht && !titel) || !zustimmung) {
    return json(400, { error: 'Bitte alle Pflichtfelder ausfüllen.' });
  }

  const key = process.env.RESEND_API_KEY;
  const to = process.env.KONTAKT_EMPFAENGER || 'buecherei.muenzbach@gmail.com';
  const from = process.env.KONTAKT_ABSENDER;
  if (!key || !from) return json(503, { error: 'Versand noch nicht eingerichtet.' });

  const zeilen = [
    ['Anliegen', anliegen], ['Name', name], ['E-Mail', email],
    ['Titel', titel], ['Autor:in', autor],
  ].filter(([, v]) => v);
  const text = zeilen.map(([k, v]) => `${k}: ${v}`).join('\n') + '\n\n' + nachricht;
  const html = '<table style="font-family:sans-serif;font-size:15px">' +
    zeilen.map(([k, v]) => `<tr><td style="padding:2px 12px 2px 0;color:#666">${k}</td><td><b>${esc(v)}</b></td></tr>`).join('') +
    '</table><p style="font-family:sans-serif;font-size:15px;white-space:pre-wrap">' + esc(nachricht) + '</p>';

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from, to: [to], reply_to: email, subject: `${anliegen} über die Website – ${name}`, text, html }),
    });
    if (!r.ok) throw new Error(await r.text());
    return json(200, { ok: true });
  } catch (e) {
    console.error('Kontakt-Versand fehlgeschlagen', e);
    return json(502, { error: 'Versand fehlgeschlagen.' });
  }
};
