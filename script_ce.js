/* ═══════════════════════════════════════════════════════════════
   Joel & Sandra — wedding invitation
   Chungking Express direction · see docs/chungking-express-design-plan.md

   No animation library. IntersectionObserver does the scene reveals and
   the 0.01 cm close; everything else is a handful of listeners. The page
   is fully readable with this file removed.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────────────
     THE ONE THING LEFT TO FILL IN.

     Set this to the wedding date and the stamp, the calendar button
     and the boarding pass all pick it up. Format: 'YYYY-MM-DD'.
     While it is null the invitation honestly reads "to be announced".

     The Mass is at 15:30 IST; END is the reception running to 21:30.
     ───────────────────────────────────────────────────────────── */
  var WEDDING_DATE = '2026-11-07';
  var MASS_TIME = '15:30';

  // MOCK — placeholder until the reception time is confirmed. Change the
  // time in index_ce.html alongside this and drop the <span class="mock">.
  var RECEPTION_TIME = '18:30';
  var RECEPTION_END = '21:30';

  /* ─────────────────────────────────────────────────────────────
     THE MUSIC.

     Drop a file into assets/audio/ and point `src` at it — see the
     README there for the Chungking Express options and what publishing
     one of them actually requires. `fallback` plays if `src` is missing,
     so the invitation is never silent while the track is being sorted
     out, and the toggle hides itself if neither loads.

     `credit` prints under the close. Set it to '' to print nothing.
     ───────────────────────────────────────────────────────────── */
  var TRACK = {
    src: 'assets/audio/chungking.mp3',
    fallback: 'song_trimmed.mp3',
    credit: ''
  };

  var CALENDAR = {
    title: 'Joel & Sandra — Wedding',
    details: 'Nuptial Mass at Ponkunnam Church at 3:30 PM, followed by the reception at Base 11, Pala.',
    location: 'Ponkunnam Church, Kottayam, Kerala'
  };

  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  root.classList.add('js');

  /* ═══ THE DATE ═════════════════════════════════════════════ */

  function formatDate(iso) {
    var parts = iso.split('-');
    var d = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
    var months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'];
    return d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear();
  }

  // Google Calendar wants UTC. Kerala is IST, UTC+5:30.
  function toUTCStamp(iso, hhmm) {
    var t = hhmm.split(':');
    var utc = Date.UTC(
      Number(iso.slice(0, 4)), Number(iso.slice(5, 7)) - 1, Number(iso.slice(8, 10)),
      Number(t[0]) - 5, Number(t[1]) - 30
    );
    return new Date(utc).toISOString().replace(/[-:]|\.\d{3}/g, '');
  }

  void RECEPTION_TIME;

  if (WEDDING_DATE) {
    var stamp = document.getElementById('dateText');
    if (stamp) stamp.textContent = formatDate(WEDDING_DATE);

    var cal = document.getElementById('calendar');
    if (cal) {
      cal.href = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
        + '&text=' + encodeURIComponent(CALENDAR.title)
        + '&dates=' + toUTCStamp(WEDDING_DATE, MASS_TIME)
        + '/' + toUTCStamp(WEDDING_DATE, RECEPTION_END)
        + '&details=' + encodeURIComponent(CALENDAR.details)
        + '&location=' + encodeURIComponent(CALENDAR.location);
      cal.removeAttribute('aria-disabled');
      cal.target = '_blank';
      cal.rel = 'noopener';
    }
  }

  /* ═══ COVER ════════════════════════════════════════════════ */

  var cover = document.getElementById('cover');
  var seal = document.getElementById('seal');
  var sound = document.getElementById('sound');
  var opened = false;

  function open() {
    if (opened) return;
    opened = true;
    cover.classList.add('is-open');
    document.body.classList.remove('is-sealed');
    if (sound) sound.hidden = false;
    // Move focus into the invitation so keyboard users land in the content.
    var first = document.getElementById('invitation');
    if (first) { first.setAttribute('tabindex', '-1'); first.focus({ preventScroll: true }); }
    window.setTimeout(function () { cover.remove(); }, 700);
  }

  if (seal) seal.addEventListener('click', open);
  if (cover) cover.addEventListener('click', open);

  /* ═══ SCENE REVEALS + THE 0.01 CM ══════════════════════════ */

  var scenes = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        if (entry.target.id === 'scene-hero') document.body.classList.add('is-close');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });

    scenes.forEach(function (s) { io.observe(s); });
  } else {
    scenes.forEach(function (s) { s.classList.add('is-in'); });
    document.body.classList.add('is-close');
  }

  /* ═══ THE PEEL ═════════════════════════════════════════════ */
  /*
     Pointer Events only — binding mouse and touch separately is what
     produces double-fire on iOS. The date is in the DOM from the start,
     so this is decoration over content that already exists: it opens
     itself after 6 seconds, and never runs at all under reduced motion.
  */

  var peel = document.getElementById('peel');
  var canvas = document.getElementById('peelCanvas');

  function openPeel() {
    if (!peel || peel.classList.contains('is-open')) return;
    peel.classList.add('is-open');
  }

  if (peel && canvas && canvas.getContext) {
    var ctx = canvas.getContext('2d');
    var drawing = false;
    var last = null;
    var checked = 0;

    function size() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var rect = peel.getBoundingClientRect();
      canvas.width = Math.max(1, Math.round(rect.width * dpr));
      canvas.height = Math.max(1, Math.round(rect.height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // Gold leaf over the date.
      var g = ctx.createLinearGradient(0, 0, rect.width, rect.height);
      g.addColorStop(0, '#C98A2E');
      g.addColorStop(0.42, '#F3D9A8');
      g.addColorStop(0.58, '#E8A33D');
      g.addColorStop(1, '#B87A26');
      ctx.globalCompositeOperation = 'source-over';
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, rect.width, rect.height);
    }

    function pointAt(e) {
      var rect = canvas.getBoundingClientRect();
      return { x: e.clientX - rect.left, y: e.clientY - rect.top };
    }

    function scratch(p) {
      ctx.globalCompositeOperation = 'destination-out';
      ctx.lineWidth = 38;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.beginPath();
      if (last) { ctx.moveTo(last.x, last.y); ctx.lineTo(p.x, p.y); }
      else { ctx.moveTo(p.x - 0.1, p.y); ctx.lineTo(p.x, p.y); }
      ctx.stroke();
      last = p;
    }

    function cleared() {
      var data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
      var clear = 0, total = 0;
      for (var i = 3; i < data.length; i += 4 * 24) {
        total++;
        if (data[i] < 24) clear++;
      }
      return total ? clear / total : 0;
    }

    canvas.addEventListener('pointerdown', function (e) {
      drawing = true;
      last = null;
      canvas.setPointerCapture(e.pointerId);
      scratch(pointAt(e));
    });

    canvas.addEventListener('pointermove', function (e) {
      if (!drawing) return;
      e.preventDefault();
      scratch(pointAt(e));
      if (++checked % 8 === 0 && cleared() > 0.42) openPeel();
    }, { passive: false });

    function stop(e) {
      if (!drawing) return;
      drawing = false;
      last = null;
      if (canvas.hasPointerCapture && canvas.hasPointerCapture(e.pointerId)) {
        canvas.releasePointerCapture(e.pointerId);
      }
      if (cleared() > 0.32) openPeel();
    }

    canvas.addEventListener('pointerup', stop);
    canvas.addEventListener('pointercancel', stop);

    var resizeTimer;
    window.addEventListener('resize', function () {
      if (peel.classList.contains('is-open')) return;
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(size, 180);
    });

    if (reduced) {
      openPeel();
    } else {
      size();
      window.setTimeout(openPeel, 6000);
    }
  }

  /* ═══ SOUND ════════════════════════════════════════════════ */
  /* Off by default. It cannot autoplay and it should not try. */

  var track = document.getElementById('track');
  var usingFallback = false;

  function setCredit() {
    var el = document.getElementById('credit');
    if (!el) return;
    var text = usingFallback ? '' : TRACK.credit;
    if (text) { el.textContent = text; el.hidden = false; }
    else { el.hidden = true; }
  }

  function play() {
    track.volume = 0.55;
    var attempt = track.play();
    return (attempt && attempt.then) ? attempt : Promise.resolve();
  }

  function markOn(on) {
    sound.setAttribute('aria-pressed', on ? 'true' : 'false');
    sound.setAttribute('aria-label', on ? 'Mute music' : 'Play music');
  }

  if (sound && track) {
    track.src = TRACK.src;
    setCredit();

    sound.addEventListener('click', function () {
      if (sound.getAttribute('aria-pressed') === 'true') {
        track.pause();
        markOn(false);
        return;
      }

      markOn(true);
      play().catch(function () {
        // The chosen file is missing or unplayable: fall back to the track
        // that ships with the repo. If that fails too, there is no music to
        // offer, so take the control away rather than leave a dead button.
        if (usingFallback || !TRACK.fallback) {
          markOn(false);
          sound.hidden = true;
          return;
        }
        usingFallback = true;
        track.src = TRACK.fallback;
        setCredit();
        play().catch(function () {
          markOn(false);
          sound.hidden = true;
        });
      });
    });
  }

  /* ═══ THE INK-IN ═══════════════════════════════════════════ */

  var ink = document.getElementById('inkLine');
  if (ink && !reduced && ink.getTotalLength) {
    var len = ink.getTotalLength();
    ink.style.strokeDasharray = len;
    ink.style.strokeDashoffset = len;
    var pass = document.getElementById('scene-pass');
    if (pass && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          ink.style.transition = 'stroke-dashoffset 1200ms cubic-bezier(.16,1,.3,1)';
          ink.style.strokeDashoffset = '0';
          obs.disconnect();
        });
      }, { threshold: 0.4 }).observe(pass);
    } else {
      ink.style.strokeDashoffset = '0';
    }
  }
})();
