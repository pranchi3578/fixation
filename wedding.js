/* ═══════════════════════════════════════════════════════════════
   Joel & Sandra — wedding invitation

   The invitation itself needs no JavaScript: every date, name and
   address is in the markup. This file adds the countdown, the calendar
   link and the R.S.V.P.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var WEDDING = {
    date: '2026-11-07',
    massTime: '16:00',
    receptionTime: null,      // not yet confirmed; the page reads "To follow"
    endTime: '21:30',
    title: 'Joel & Sandra — Wedding',
    details: 'Holy Mass at Holy Family Forane Church, Ponkunnam at four in the afternoon, followed by the reception at Base 11, Pala.',
    location: 'Holy Family Forane Church, Ponkunnam, Kottayam, Kerala'
  };

  /* ─────────────────────────────────────────────────────────────
     WHERE REPLIES GO.

     `whatsapp` is a number in international form with no plus and no
     spaces — '919876543210'. Set it and the reply opens straight in
     WhatsApp, already written. `email` is the fallback if you would
     rather they arrive in an inbox.

     With neither set the form still works: the guest gets their reply
     written out with a copy button, so nobody ever hits a dead end.

     `people` fills the "Ask Us" section. Leave it empty and that whole
     section removes itself rather than sitting there blank.
     ───────────────────────────────────────────────────────────── */
  var CONTACT = {
    whatsapp: null,
    email: null,
    rsvpBy: '2026-10-10',
    people: []      // e.g. { name: 'Joel', phone: '+91 98470 00000' }
  };

  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'];

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
  function longDate(iso) {
    return (+iso.slice(8, 10)) + ' ' + MONTHS[+iso.slice(5, 7) - 1] + ' ' + iso.slice(0, 4);
  }

  var startsAt = istInstant(WEDDING.date, WEDDING.massTime);

  /* ═══ CALENDAR ═════════════════════════════════════════════ */
  var cal = $('calendar');
  if (cal) {
    cal.href = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
      + '&text=' + encodeURIComponent(WEDDING.title)
      + '&dates=' + stamp(startsAt) + '/' + stamp(istInstant(WEDDING.date, WEDDING.endTime))
      + '&details=' + encodeURIComponent(WEDDING.details)
      + '&location=' + encodeURIComponent(WEDDING.location);
    cal.target = '_blank';
    cal.rel = 'noopener';
  }

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

  /* ═══ R.S.V.P. ═════════════════════════════════════════════ */
  var form = $('rsvpForm');

  if (form) {
    var by = $('rsvpBy');
    if (by) by.textContent = longDate(CONTACT.rsvpBy);

    var sent = $('rsvpSent');
    var sentText = $('sentText');
    var note = $('rsvpNote');
    var coming = form.querySelectorAll('[data-coming]');

    /* Someone who is not coming should not be asked how many of them are
       not coming, or what they would like to eat. */
    function syncColumns() {
      var picked = form.querySelector('input[name="attending"]:checked');
      var away = picked && picked.value.indexOf('declines') > -1;
      Array.prototype.forEach.call(coming, function (el) { el.hidden = !!away; });
    }
    form.addEventListener('change', function (e) {
      if (e.target.name === 'attending') syncColumns();
    });
    syncColumns();

    function fail(inputId, errId, bad) {
      var input = $(inputId), err = $(errId);
      if (err) err.hidden = !bad;
      if (input) {
        if (bad) input.setAttribute('aria-invalid', 'true');
        else input.removeAttribute('aria-invalid');
      }
      return bad;
    }

    function compose() {
      var picked = form.querySelector('input[name="attending"]:checked');
      var away = picked.value.indexOf('declines') > -1;
      var lines = [
        'R.S.V.P. — Joel & Sandra, 7 November 2026',
        '',
        'Name: ' + $('gName').value.trim()
      ];
      var phone = $('gPhone').value.trim();
      if (phone) lines.push('Phone: ' + phone);
      lines.push('Reply: ' + picked.value);

      if (!away) {
        lines.push('How many: ' + $('gParty').value);
        var events = Array.prototype.slice
          .call(form.querySelectorAll('input[name="events"]:checked'))
          .map(function (c) { return c.value; });
        lines.push('Coming to: ' + (events.length ? events.join(' and ') : 'to be confirmed'));
        var meal = form.querySelector('input[name="meal"]:checked');
        if (meal) lines.push('At the table: ' + meal.value);
      }
      var text = $('gNote').value.trim();
      if (text) lines.push('', 'Note: ' + text);
      return lines.join('\n');
    }

    function remember(name) {
      try {
        window.localStorage.setItem('js-rsvp', JSON.stringify({
          name: name, at: new Date().toISOString()
        }));
      } catch (e) { /* private window, blocked storage — not worth a word */ }
    }

    function showSent(message, copyable) {
      form.hidden = true;
      sent.hidden = false;

      if (copyable) {
        sentText.textContent = 'We have not opened the direct line yet, so here is '
          + 'your reply written out. Copy it and send it to either of us and it is done.';
        var box = document.createElement('textarea');
        box.className = 'input';
        box.readOnly = true;
        box.rows = 8;
        box.value = message;
        box.style.marginTop = '4px';
        sent.insertBefore(box, sent.lastElementChild);

        var copy = document.createElement('button');
        copy.type = 'button';
        copy.className = 'btn';
        copy.style.alignSelf = 'stretch';
        copy.textContent = 'Copy my reply';
        copy.addEventListener('click', function () {
          var done = function () { copy.textContent = 'Copied'; };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(message).then(done, function () {
              box.select(); done();
            });
          } else {
            box.select();
            try { document.execCommand('copy'); } catch (e) {}
            done();
          }
        });
        sent.insertBefore(copy, sent.lastElementChild);
      } else {
        sentText.textContent = 'Your reply is on its way to us. If the message did not '
          + 'open, send it again and we will catch it.';
      }
      sent.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var noName = fail('gName', 'errName', !$('gName').value.trim());
      var noReply = fail(null, 'errAttend', !form.querySelector('input[name="attending"]:checked'));
      if (noName || noReply) {
        (noName ? $('gName') : form.querySelector('input[name="attending"]')).focus();
        return;
      }

      var message = compose();
      remember($('gName').value.trim());

      if (CONTACT.whatsapp) {
        window.open('https://wa.me/' + CONTACT.whatsapp + '?text=' + encodeURIComponent(message),
                    '_blank', 'noopener');
        showSent(message, false);
      } else if (CONTACT.email) {
        window.location.href = 'mailto:' + CONTACT.email
          + '?subject=' + encodeURIComponent('R.S.V.P. — Joel & Sandra')
          + '&body=' + encodeURIComponent(message);
        showSent(message, false);
      } else {
        showSent(message, true);
      }
    });

    var again = $('rsvpAgain');
    if (again) {
      again.addEventListener('click', function () {
        window.location.reload();
      });
    }

    // A returning guest should be greeted, not asked all over again.
    try {
      var prior = JSON.parse(window.localStorage.getItem('js-rsvp') || 'null');
      if (prior && prior.name && note) {
        note.textContent = 'It looks like ' + prior.name + ' already replied. '
          + 'Sending again simply replaces it.';
      }
    } catch (e) { /* nothing worth saying */ }
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
