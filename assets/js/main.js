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
  // Foto-Slider bei den Veranstaltungen
  document.querySelectorAll('[data-slider]').forEach(function (sl) {
    var track = sl.querySelector('.sl-track');
    var dots = sl.querySelectorAll('.sl-dots span');
    var n = track.children.length;
    function idx() { return Math.round(track.scrollLeft / track.clientWidth); }
    function go(i) { i = (i + n) % n; track.scrollTo({ left: i * track.clientWidth, behavior: 'smooth' }); }
    var p = sl.querySelector('.prev'), nx = sl.querySelector('.next');
    if (p) p.addEventListener('click', function () { go(idx() - 1); });
    if (nx) nx.addEventListener('click', function () { go(idx() + 1); });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(idx() + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx() - 1); }
    });
    track.addEventListener('scroll', function () {
      var i = idx();
      dots.forEach(function (d, k) { d.classList.toggle('on', k === i); });
    }, { passive: true });
    // Klick oder Enter öffnet die Fotos groß
    var imgs = Array.prototype.slice.call(track.querySelectorAll('img'));
    imgs.forEach(function (im, k) { im.addEventListener('click', function () { lightbox(imgs, k, track); }); });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); lightbox(imgs, idx(), track); }
    });
  });

  // Großansicht der Fotos
  var lb, lbImg, lbCap, lbCount, lbList = [], lbI = 0, lbBack = null;
  function lbShow(i) {
    lbI = (i + lbList.length) % lbList.length;
    var im = lbList[lbI];
    lbImg.src = im.getAttribute('data-full') || im.currentSrc || im.src;
    lbImg.alt = im.alt;
    lbCap.textContent = im.alt;
    lbCount.textContent = (lbI + 1) + ' / ' + lbList.length;
    lb.classList.toggle('single', lbList.length < 2);
  }
  function lightbox(list, i, back) {
    if (!lb) {
      lb = document.createElement('dialog');
      lb.className = 'lb';
      lb.setAttribute('aria-label', 'Fotos in Großansicht');
      lb.innerHTML = '<button type="button" class="lb-close" aria-label="Schließen">×</button>'
        + '<button type="button" class="lb-nav prev" aria-label="Vorheriges Foto">‹</button>'
        + '<figure><img alt=""><figcaption><span class="lb-count"></span> <span class="lb-cap"></span></figcaption></figure>'
        + '<button type="button" class="lb-nav next" aria-label="Nächstes Foto">›</button>';
      document.body.appendChild(lb);
      lbImg = lb.querySelector('img'); lbCap = lb.querySelector('.lb-cap'); lbCount = lb.querySelector('.lb-count');
      lb.querySelector('.lb-close').addEventListener('click', function () { lb.close(); });
      lb.querySelector('.prev').addEventListener('click', function () { lbShow(lbI - 1); });
      lb.querySelector('.next').addEventListener('click', function () { lbShow(lbI + 1); });
      lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'FIGURE') lb.close(); });
      lb.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { e.preventDefault(); lbShow(lbI + 1); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); lbShow(lbI - 1); }
      });
      var x0 = null;
      lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      lb.addEventListener('touchend', function (e) {
        if (x0 === null) return;
        var dx = e.changedTouches[0].clientX - x0; x0 = null;
        if (Math.abs(dx) > 40) lbShow(lbI + (dx < 0 ? 1 : -1));
      });
      lb.addEventListener('close', function () {
        document.documentElement.style.overflow = '';
        if (lbBack) lbBack.focus();
      });
    }
    lbList = list; lbBack = back; lbShow(i);
    document.documentElement.style.overflow = 'hidden';
    lb.showModal();
    lb.querySelector('.lb-close').focus();
  }
})();
