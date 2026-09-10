/* ═══════════════════════════════════════════════════════════════
   Joel & Sandra — wedding invitation

   The invitation itself needs no JavaScript: every date, name and
   address is in the markup. This file adds the countdown and the
   calendar links, nothing more.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var WEDDING = {
    date: '2026-11-07',
    massTime: '16:00',
    receptionTime: '18:00',
    endTime: '21:30',
    title: 'Joel & Sandra — Wedding',
    details: 'Holy Mass at Holy Family Forane Church, Ponkunnam at four in the afternoon, followed by the reception at Base 11, Pala, at six.',
    location: 'Holy Family Forane Church, Ponkunnam, Kottayam, Kerala'
  };

  /* `people` fills the "Ask Us" section. Leave it empty and that whole
     section removes itself rather than sitting there blank. */
  var CONTACT = {
    people: []      // e.g. { name: 'Joel', phone: '+91 98470 00000' }
  };

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');

  function $(id) { return document.getElementById(id); }

  /* ═══ TIME ═════════════════════════════════════════════════ */
  /* Kerala is IST, UTC+5:30. Building the instant in UTC means the
     countdown is the same number everywhere — a guest in London sees the
     time left until the Mass, not until four o'clock where they are. */
  function istInstant(iso, hhmm) {
    var t = hhmm.split(':');
    return Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10),
                    +t[0] - 5, +t[1] - 30);
  }
  function stamp(ms) { return new Date(ms).toISOString().replace(/[-:]|\.\d{3}/g, ''); }

  var startsAt = istInstant(WEDDING.date, WEDDING.massTime);

  /* ═══ CALENDAR ═════════════════════════════════════════════ */
  var href = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
    + '&text=' + encodeURIComponent(WEDDING.title)
    + '&dates=' + stamp(startsAt) + '/' + stamp(istInstant(WEDDING.date, WEDDING.endTime))
    + '&details=' + encodeURIComponent(WEDDING.details)
    + '&location=' + encodeURIComponent(WEDDING.location);

  ['calendar', 'calendarTop'].forEach(function (id) {
    var el = $(id);
    if (!el) return;
    el.href = href;
    el.target = '_blank';
    el.rel = 'noopener';
  });

  /* ═══ COUNTDOWN ════════════════════════════════════════════ */
  var cells = { d: $('cd'), h: $('ch'), m: $('cm'), s: $('cs') };
  function pad(n) { return n < 10 ? '0' + n : String(n); }

  function tick() {
    var left = startsAt - Date.now();
    if (left <= 0) {
      // The day itself and every day after. Never a negative countdown,
      // and never a row of zeroes left standing.
      var wrap = $('count');
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
  if (cells.d && cells.h && cells.m && cells.s && tick()) window.setInterval(tick, 1000);

  /* ═══ ASK US ═══════════════════════════════════════════════ */
  var contacts = $('contacts');
  if (contacts) {
    if (CONTACT.people.length) {
      CONTACT.people.forEach(function (person) {
        var box = document.createElement('div');
        var name = document.createElement('p');
        name.className = 'meta';
        name.textContent = person.name;
        var tel = document.createElement('a');
        tel.href = 'tel:' + String(person.phone).replace(/[^\d+]/g, '');
        tel.textContent = person.phone;
        box.appendChild(name);
        box.appendChild(tel);
        contacts.appendChild(box);
      });
    } else {
      // Nothing to show yet — take the section away rather than leave a hole.
      var panel = contacts.closest('.panel');
      if (panel) panel.remove();
    }
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

    // An observer only fires for what crosses the viewport, so an anchor
    // jump or a restored scroll position can strand a block at opacity 0.
    var queued = false;
    window.addEventListener('scroll', function () {
      if (queued) return;
      queued = true;
      window.requestAnimationFrame(function () {
        queued = false;
        blocks.forEach(function (b) {
          if (b.classList.contains('in')) return;
          if (b.getBoundingClientRect().top < window.innerHeight) { reveal(b); io.unobserve(b); }
        });
      });
    }, { passive: true });
  } else {
    blocks.forEach(reveal);
  }
})();
