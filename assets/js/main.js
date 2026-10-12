(function () {
  // Mobile-Menü
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('hauptnavigation');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  }

  // Karte erst nach Klick laden (keine Daten an Dritte ohne Zustimmung)
  document.querySelectorAll('[data-map]').forEach(function (box) {
    var b = box.querySelector('button');
    if (!b) return;
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = box.getAttribute('data-map');
      f.title = 'Karte: Standort der Bücherei Münzbach';
      f.loading = 'lazy';
      box.innerHTML = '';
      box.classList.add('loaded');
      box.appendChild(f);
    });
  });

  // Kontaktformulare
  document.querySelectorAll('form[data-contact]').forEach(function (form) {
    var msg = form.querySelector('.form-msg');
    var submit = form.querySelector('button[type="submit"]');
    function show(type, html) { msg.className = 'form-msg ' + type; msg.innerHTML = html; msg.focus(); }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = String(v); });
      submit.disabled = true;
      fetch('/api/kontakt', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            show('ok', 'Danke! Deine Nachricht ist angekommen. Wir melden uns so bald wie möglich.');
          } else { throw new Error(res.j.error || 'Fehler'); }
        })
        .catch(function () {
          var body = 'Name: ' + (data.name || '') + '\nE-Mail: ' + (data.email || '') + '\nAnliegen: ' + (data.anliegen || '') +
            (data.titel ? '\nTitel: ' + data.titel : '') + (data.autor ? '\nAutor:in: ' + data.autor : '') + '\n\n' + (data.nachricht || '');
          var href = 'mailto:buecherei.muenzbach@gmail.com?subject=' + encodeURIComponent((data.anliegen || 'Anfrage') + ' über die Website') + '&body=' + encodeURIComponent(body);
          show('err', 'Die Nachricht konnte gerade nicht gesendet werden. <a href="' + href + '">Stattdessen per E-Mail schicken</a> oder bitte später noch einmal versuchen.');
        })
        .then(function () { submit.disabled = false; });
    });
  });
})();
