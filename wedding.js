/* ═══════════════════════════════════════════════════════════════
   Joel & Sandra — wedding invitation

   Small on purpose: a countdown, two calendar links, and one observer
   for the fade. Nothing here carries information — the invitation is
   complete and readable with this file removed.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var WEDDING = {
    date: '2026-11-07',
    massTime: '15:30',
    // Not yet confirmed. The page reads "To follow" until it is.
    receptionTime: null,
    endTime: '21:30',
    title: 'Joel & Sandra — Wedding',
    details: 'Holy Mass at Ponkunnam Church at half past three, followed by the reception at Base 11, Pala.',
    location: 'Ponkunnam Church, Ponkunnam, Kottayam, Kerala'
  };

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');

  /* ═══ TIME ═════════════════════════════════════════════════ */
  /* Kerala is IST, UTC+5:30. Building the instant in UTC rather than
     local time means the countdown is the same number everywhere —
     a guest in London sees the time remaining until the Mass, not
     until half past three in their own afternoon. */
  function istInstant(iso, hhmm) {
    var t = hhmm.split(':');
    return Date.UTC(
      +iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10),
      +t[0] - 5, +t[1] - 30
    );
  }

  function stamp(ms) {
    return new Date(ms).toISOString().replace(/[-:]|\.\d{3}/g, '');
  }

  var startsAt = istInstant(WEDDING.date, WEDDING.massTime);

  /* ═══ CALENDAR ═════════════════════════════════════════════ */
  var href = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
    + '&text=' + encodeURIComponent(WEDDING.title)
    + '&dates=' + stamp(startsAt) + '/' + stamp(istInstant(WEDDING.date, WEDDING.endTime))
    + '&details=' + encodeURIComponent(WEDDING.details)
    + '&location=' + encodeURIComponent(WEDDING.location);

  ['calendar', 'calendarTop'].forEach(function (id) {
    var el = document.getElementById(id);
    if (!el) return;
    el.href = href;
    el.target = '_blank';
    el.rel = 'noopener';
  });

  /* ═══ COUNTDOWN ════════════════════════════════════════════ */
  var cells = {
    d: document.getElementById('cd'),
    h: document.getElementById('ch'),
    m: document.getElementById('cm'),
    s: document.getElementById('cs')
  };

  function pad(n) { return n < 10 ? '0' + n : String(n); }

  function tick() {
    var left = startsAt - Date.now();

    if (left <= 0) {
      // The day itself, and every day after it. Never show a negative
      // countdown, and never leave the row reading zero forever.
      var wrap = document.getElementById('count');
      if (wrap) {
        wrap.style.gridTemplateColumns = '1fr';
        wrap.innerHTML = '<div><span class="n">Today</span>'
          + '<span class="u">Joel &amp; Sandra are married</span></div>';
      }
      return false;
    }

    var s = Math.floor(left / 1000);
    cells.d.textContent = Math.floor(s / 86400);
    cells.h.textContent = pad(Math.floor(s / 3600) % 24);
    cells.m.textContent = pad(Math.floor(s / 60) % 60);
    cells.s.textContent = pad(s % 60);
    return true;
  }

  if (cells.d && cells.h && cells.m && cells.s) {
    if (tick()) window.setInterval(tick, 1000);
  }

  /* ═══ THE FADE ═════════════════════════════════════════════ */
  var blocks = document.querySelectorAll('.rise');

  function reveal(el) { el.classList.add('in'); }

  if (!reduced && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        reveal(e.target);
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    blocks.forEach(function (b) { io.observe(b); });

    // Safety net. An observer only fires for what actually crosses the
    // viewport, so an anchor jump or a restored scroll position can
    // strand a block at opacity 0. On scroll, anything the page has
    // already moved past is revealed outright.
    var queued = false;
    window.addEventListener('scroll', function () {
      if (queued) return;
      queued = true;
      window.requestAnimationFrame(function () {
        queued = false;
        blocks.forEach(function (b) {
          if (b.classList.contains('in')) return;
          if (b.getBoundingClientRect().top < window.innerHeight) {
            reveal(b);
            io.unobserve(b);
          }
        });
      });
    }, { passive: true });
  } else {
    blocks.forEach(reveal);
  }
})();
