/* ═══════════════════════════════════════════════════════════════
   Joel & Sandra — wedding invitation

   The invitation itself needs no JavaScript: every date, name and
   address is in the markup. This file adds the countdown and the
   calendar links, nothing more.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* Whose name comes first is set on the body, so the mirrored invitation
     can carry the other order without a second copy of this file. */
  var COUPLE = (document.body.getAttribute('data-couple') || 'Joel & Sandra')
                 .replace(/&amp;/g, '&');

  var WEDDING = {
    date: '2026-11-07',
    massTime: '16:00',
    receptionTime: '18:30',
    endTime: '21:30',
    title: COUPLE + ' — Wedding',
    details: 'Holy Mass at Holy Family Forane Church, Ponkunnam at four in the afternoon, followed by the reception at Base Eleven Convention Centre, Pala, at half past six.',
    location: 'Holy Family Forane Church, Ponkunnam, Kottayam, Kerala'
  };

  /* ─────────────────────────────────────────────────────────────
     THE MUSIC.

     Drop the file into assets/audio/ and point `src` at it — the README
     there names the track and how to trim it. The control stays hidden
     until the file is confirmed present, so a guest never taps a button
     with nothing behind it, and the page is silent until asked.
     ───────────────────────────────────────────────────────────── */
  var TRACK = {
    src: 'assets/audio/wedding.mp3',
    volume: 0.45
  };

  /* `people` fills the "Ask Us" section. Leave it empty and that whole
     section removes itself rather than sitting there blank. */
  var CONTACT = {
    people: []      // e.g. { name: 'Joel', phone: '+91 98470 00000' }
  };

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');
  // Tells the failsafe in the head that this file arrived; see wedding.html.
  window.__invitationReady = true;

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

  /* ═══ SOUND ════════════════════════════════════════════════ */
  /* Off by default. It cannot autoplay and it should not try. */
  var sound = $('sound');
  var track = $('track');
  var startMusic = function () {};   // replaced below once the file is known

  if (sound && track) {
    var fade = null;

    // Ramping the gain rather than cutting it in — an abrupt start on a
    // quiet page is startling.
    function ramp(to, done) {
      window.clearInterval(fade);
      var step = (to - track.volume) / 18;
      fade = window.setInterval(function () {
        var next = track.volume + step;
        if ((step > 0 && next >= to) || (step < 0 && next <= to)) {
          track.volume = to;
          window.clearInterval(fade);
          if (done) done();
          return;
        }
        track.volume = Math.max(0, Math.min(1, next));
      }, 45);
    }

    function mark(on) {
      sound.setAttribute('aria-pressed', on ? 'true' : 'false');
      sound.setAttribute('aria-label', on ? 'Mute music' : 'Play music');
    }

    sound.addEventListener('click', function () {
      if (sound.getAttribute('aria-pressed') === 'true') {
        ramp(0, function () { track.pause(); });
        mark(false);
        return;
      }
      track.volume = 0;
      var started = track.play();
      if (started && started.then) {
        started.then(function () { mark(true); ramp(TRACK.volume); },
                     function () { sound.hidden = true; });
      } else {
        mark(true);
        ramp(TRACK.volume);
      }
    });

    /* Opening the envelope is a user gesture, so the browser will let the
       track start here. If the file is not ready yet the flag is set and
       the music begins the moment the HEAD check lands. */
    var ready = false, wanted = false;

    startMusic = function () {
      wanted = true;
      if (!ready) return;
      track.volume = 0;
      var started = track.play();
      if (started && started.then) {
        started.then(function () { mark(true); ramp(TRACK.volume); }, function () {});
      } else {
        mark(true);
        ramp(TRACK.volume);
      }
    };

    function haveFile() {
      ready = true;
      track.src = TRACK.src;
      sound.hidden = false;
      if (wanted) startMusic();
    }

    // Confirm the file is there before offering the control at all.
    if (window.fetch) {
      window.fetch(TRACK.src, { method: 'HEAD' }).then(function (r) {
        if (r.ok) haveFile();
      }, function () { /* missing or offline — leave it hidden */ });
    } else {
      haveFile();
    }
  }

  /* ═══ THE ENVELOPE ═════════════════════════════════════════
     The movements are in the stylesheet; these are the cues. The flap
     takes a second to fall back, the card is drawn out behind it, and
     only then is the envelope set down and the page brought up.
     ═══════════════════════════════════════════════════════════ */
  var envelope = $('envelope');

  if (envelope) {
    var opened = false;

    function openEnvelope() {
      if (opened) return;
      opened = true;

      envelope.classList.add('is-open');
      document.body.classList.remove('sealed');
      startMusic();

      var lift = reduced ? 260 : 2620;   // the card is out and has been read   // the card is out; set the envelope down
      var goes = reduced ? 400 : 5400;   // three seconds out of the envelope   // the card fades into the page
      var ends = reduced ? 600 : 6020;   // nothing of it left

      window.setTimeout(function () { envelope.classList.add('is-lifting'); }, lift);
      window.setTimeout(function () { envelope.classList.add('is-gone'); }, goes);
      window.setTimeout(function () {
        envelope.remove();
        var first = document.querySelector('main');
        if (first) { first.setAttribute('tabindex', '-1'); first.focus({ preventScroll: true }); }
      }, ends);
    }

    envelope.addEventListener('click', openEnvelope);
    envelope.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openEnvelope(); }
    });
  } else {
    document.body.classList.remove('sealed');
  }

  /* ═══ THE NUDGE ════════════════════════════════════════════ */
  /* The cue on the cover goes away the moment it is heeded, and never
     comes back: a second showing would be nagging. */
  var cue = document.querySelector('.scroll-cue');
  if (cue) {
    var heeded = function () {
      if (window.scrollY < 40) return;
      document.documentElement.classList.add('moved');
      window.removeEventListener('scroll', heeded);
    };
    window.addEventListener('scroll', heeded, { passive: true });
    heeded();                      // a restored scroll position counts
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
