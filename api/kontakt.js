// Vercel Serverless Function: Kontaktformular → E-Mail an die Bücherei (Versand über Resend)
// Benötigte Umgebungsvariablen in Vercel:
//   RESEND_API_KEY      – API-Schlüssel von resend.com
//   KONTAKT_EMPFAENGER  – z. B. buecherei.muenzbach@gmail.com
//   KONTAKT_ABSENDER    – verifizierte Absenderadresse, z. B. "Website Bücherei Münzbach <website@buecherei-muenzbach.at>"

const clean = (v, max) => String(v || '').replace(/\r/g, '').trim().slice(0, max);
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Methode nicht erlaubt' });
  }
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  body = body || {};

  // Spam-Schutz: verstecktes Feld muss leer bleiben
  if (body.website) return res.status(200).json({ ok: true });

  const name = clean(body.name, 120);
  const email = clean(body.email, 160);
  const anliegen = clean(body.anliegen, 40) || 'Anfrage';
  const titel = clean(body.titel, 200);
  const autor = clean(body.autor, 160);
  const nachricht = clean(body.nachricht, 5000);
  const zustimmung = body.zustimmung === 'ja';

  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || (!nachricht && !titel) || !zustimmung) {
    return res.status(400).json({ error: 'Bitte alle Pflichtfelder ausfüllen.' });
  }

  const key = process.env.RESEND_API_KEY;
  const to = process.env.KONTAKT_EMPFAENGER || 'buecherei.muenzbach@gmail.com';
  const from = process.env.KONTAKT_ABSENDER;
  if (!key || !from) return res.status(503).json({ error: 'Versand noch nicht eingerichtet.' });

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
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('Kontakt-Versand fehlgeschlagen', e);
    return res.status(502).json({ error: 'Versand fehlgeschlagen.' });
  }
};
