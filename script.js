// ═══ AAMEN Invitation — Interactions ═══

// ─── Audio: "Ee Solomanum Shoshannayum" ───
var songAudio = new Audio('song_trimmed.mp3');
songAudio.preload = 'auto';
songAudio.loop = true;
songAudio.volume = 0.4;
var soundOn = false;
var LYRICS_START = 0; // The file is already trimmed, so start from 0

function startMusic() {
  // Play first to initialize the audio context, then immediately seek.
  // This prevents browsers from ignoring the seek or delaying playback.
  songAudio.play().then(function () {
    songAudio.currentTime = LYRICS_START;
    soundOn = true;
    updateSoundIcon();
    console.log('[AAMEN] Playing from', songAudio.currentTime, 's');
  }).catch(function (err) {
    console.warn('[AAMEN] Play blocked:', err.message);
  });
}

function toggleMusic() {
  if (soundOn) {
    songAudio.pause();
    soundOn = false;
  } else {
    songAudio.play();
    soundOn = true;
  }
  updateSoundIcon();
}

function updateSoundIcon() {
  var btn = document.getElementById('soundToggle');
  if (btn) btn.textContent = soundOn ? '🔊' : '🔇';
}

// ─── DOM-dependent code ───
document.addEventListener('DOMContentLoaded', function () {

  // ─── Intersection Observer: Reveal on Scroll ───
  var scenes = document.querySelectorAll('.scene:not(.scene-bell)');
  var milestones = document.querySelectorAll('.milestone');

  var revealObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
  );

  scenes.forEach(function (s) { revealObserver.observe(s); });
  milestones.forEach(function (m) { revealObserver.observe(m); });

  // ─── Scroll Prompt: hide after first scroll ───
  var scrollPrompt = document.getElementById('scrollPrompt');
  var scrolled = false;
  window.addEventListener('scroll', function () {
    if (!scrolled && window.scrollY > 80) {
      scrolled = true;
      scrollPrompt.classList.add('hidden');
    }
  }, { passive: true });

  // ─── Scene 1: Bell Ring ───
  var bellContainer = document.getElementById('bellContainer');
  var bellIcon = document.getElementById('bellIcon');
  var goldenBurst = document.getElementById('goldenBurst');
  var bellRung = false;

  bellContainer.addEventListener('click', function () {
    // Ring animation
    bellIcon.classList.remove('ringing');
    void bellIcon.offsetWidth; // reflow
    bellIcon.classList.add('ringing');

    // Golden burst
    goldenBurst.classList.add('active');
    setTimeout(function () {
      goldenBurst.classList.remove('active');
    }, 2500);

    // Vibration
    if (navigator.vibrate) {
      navigator.vibrate([50, 30, 50]);
    }

    // Start "Ee Solomanum Shoshannayum" on first bell tap
    if (!bellRung) {
      bellRung = true;
      startMusic();
      var tapText = bellContainer.querySelector('.bell-tap');
      if (tapText) tapText.style.opacity = '0';
    }
  });

  // ─── Scene 5: Golden Particles ───
  var aamenScene = document.getElementById('scene-aamen');
  var particlesCreated = false;

  var particleObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && !particlesCreated) {
          particlesCreated = true;
          createParticles();
        }
      });
    },
    { threshold: 0.3 }
  );
  particleObserver.observe(aamenScene);

  function createParticles() {
    var count = 30;
    for (var i = 0; i < count; i++) {
      var p = document.createElement('div');
      p.className = 'particle';
      p.style.left = Math.random() * 100 + '%';
      p.style.animationDuration = (3 + Math.random() * 5) + 's';
      p.style.animationDelay = Math.random() * 4 + 's';
      p.style.width = (2 + Math.random() * 4) + 'px';
      p.style.height = p.style.width;
      p.style.opacity = String(0.2 + Math.random() * 0.5);
      aamenScene.appendChild(p);
    }
  }

  // ─── Scene 6: Save to Calendar (.ics) ───
  var btnCalendar = document.getElementById('btnCalendar');
  if (btnCalendar) {
    btnCalendar.addEventListener('click', function () {
      var icsContent = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Joel & Sandra//Nischayam//EN',
        'BEGIN:VEVENT',
        'DTSTART:20260523T130000Z',
        'DTEND:20260523T170000Z',
        'SUMMARY:Joel & Sandra — Nischayam (Fixation)',
        'DESCRIPTION:Fixation ceremony of Joel Francis Jose & Sandra Binoy at Tharavad The Farmhouse\\, Kanjirappally.',
        'LOCATION:Tharavad The Farmhouse\\, Kanjirappally\\, Kottayam\\, Kerala',
        'BEGIN:VALARM',
        'TRIGGER:-PT2H',
        'ACTION:DISPLAY',
        'DESCRIPTION:Joel & Sandra Nischayam in 2 hours!',
        'END:VALARM',
        'END:VEVENT',
        'END:VCALENDAR'
      ].join('\r\n');

      var blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
      var link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'Joel_Sandra_Nischayam.ics';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
    });
  }

  // ─── Sound Toggle ───
  var soundToggle = document.getElementById('soundToggle');
  if (soundToggle) {
    soundToggle.addEventListener('click', function () {
      toggleMusic();
    });
  }

});
