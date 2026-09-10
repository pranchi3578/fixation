/* ═══════════════════════════════════════════════════════════════
   Joel & Sandra — wedding invitation

   Deliberately small. One observer for the fade, one calendar link, one
   sound toggle. The invitation is complete and readable with this file
   removed — nothing here carries information.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var WEDDING = {
    date: '2026-11-07',
    massTime: '15:30',
    // Not yet confirmed. The page reads "To follow"; when you have the
    // real time, set it here and in wedding.html together.
    receptionTime: null,
    receptionEnd: '21:30',
    title: 'Joel & Sandra — Wedding',
    details: 'Holy Mass at Ponkunnam Church at half past three, followed by the reception at Base 11, Pala.',
    location: 'Ponkunnam Church, Kottayam, Kerala'
  };

  /* Drop a file into assets/audio/ and point `src` at it. `fallback` plays
     if that file is missing, and the toggle removes itself if neither
     loads rather than sitting there dead. */
  var TRACK = {
    src: 'assets/audio/wedding.mp3',
    fallback: 'song_trimmed.mp3'
  };

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');

  /* ═══ CALENDAR ═════════════════════════════════════════════ */
  // Google Calendar wants UTC. Kerala is IST, UTC+5:30.
  function utc(iso, hhmm) {
    var t = hhmm.split(':');
    return new Date(Date.UTC(
      +iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10),
      +t[0] - 5, +t[1] - 30
    )).toISOString().replace(/[-:]|\.\d{3}/g, '');
  }

  var cal = document.getElementById('calendar');
  if (cal && WEDDING.date) {
    cal.href = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
      + '&text=' + encodeURIComponent(WEDDING.title)
      + '&dates=' + utc(WEDDING.date, WEDDING.massTime)
      + '/' + utc(WEDDING.date, WEDDING.receptionEnd)
      + '&details=' + encodeURIComponent(WEDDING.details)
      + '&location=' + encodeURIComponent(WEDDING.location);
    cal.target = '_blank';
    cal.rel = 'noopener';
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
    // viewport, so an anchor jump, a restored scroll position or a fast
    // flick can leave a block stranded at opacity 0 with the content
    // invisible. On every scroll, anything the page has already moved
    // past is revealed outright.
    var pending = false;
    window.addEventListener('scroll', function () {
      if (pending) return;
      pending = true;
      window.requestAnimationFrame(function () {
        pending = false;
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

  /* ═══ SOUND ════════════════════════════════════════════════ */
  /* Off by default. It cannot autoplay and it should not try. */
  var sound = document.getElementById('sound');
  var track = document.getElementById('track');
  var fellBack = false;

  function play() {
    track.volume = 0.5;
    var p = track.play();
    return (p && p.then) ? p : Promise.resolve();
  }

  function mark(on) {
    sound.setAttribute('aria-pressed', on ? 'true' : 'false');
    sound.setAttribute('aria-label', on ? 'Mute music' : 'Play music');
  }

  if (sound && track) {
    track.src = TRACK.src;
    sound.hidden = false;

    sound.addEventListener('click', function () {
      if (sound.getAttribute('aria-pressed') === 'true') {
        track.pause();
        mark(false);
        return;
      }
      mark(true);
      play().catch(function () {
        if (fellBack || !TRACK.fallback) { mark(false); sound.hidden = true; return; }
        fellBack = true;
        track.src = TRACK.fallback;
        play().catch(function () { mark(false); sound.hidden = true; });
      });
    });
  }
})();
