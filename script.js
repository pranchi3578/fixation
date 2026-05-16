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
    function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target); // Stop observing once visible
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
    function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && !particlesCreated) {
          particlesCreated = true;
          createParticles();
          observer.unobserve(entry.target);
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

  // ─── Scene 6: Scratch & Reveal + Countdown ───
  var canvas = document.getElementById('scratchCanvas');
  if (canvas) {
    var ctx = canvas.getContext('2d');
    var isDrawing = false;
    var revealed = false;

    // Fill canvas with gold color
    function initCanvas() {
      canvas.width = canvas.parentElement.offsetWidth;
      canvas.height = canvas.parentElement.offsetHeight;
      ctx.fillStyle = '#CFA144'; // gold-light
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.globalCompositeOperation = 'destination-out';
    }

    // Call init on load and resize
    initCanvas();
    window.addEventListener('resize', initCanvas);

    function getMousePos(e) {
      var rect = canvas.getBoundingClientRect();
      var clientX = e.touches ? e.touches[0].clientX : e.clientX;
      var clientY = e.touches ? e.touches[0].clientY : e.clientY;
      return {
        x: clientX - rect.left,
        y: clientY - rect.top
      };
    }

    function scratch(e) {
      if (!isDrawing || revealed) return;
      e.preventDefault();
      var pos = getMousePos(e);
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, 25, 0, Math.PI * 2);
      ctx.fill();
      checkReveal();
    }

    canvas.addEventListener('mousedown', function (e) { isDrawing = true; scratch(e); });
    canvas.addEventListener('mousemove', scratch);
    canvas.addEventListener('mouseup', function () { isDrawing = false; });
    canvas.addEventListener('mouseleave', function () { isDrawing = false; });

    canvas.addEventListener('touchstart', function (e) { isDrawing = true; scratch(e); }, { passive: false });
    canvas.addEventListener('touchmove', scratch, { passive: false });
    canvas.addEventListener('touchend', function () { isDrawing = false; });

    // Check how much is scratched
    function checkReveal() {
      var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      var pixels = imageData.data;
      var transparent = 0;
      for (var i = 3; i < pixels.length; i += 4) {
        if (pixels[i] === 0) transparent++;
      }
      var percent = (transparent / (pixels.length / 4)) * 100;
      
      // If 40% scratched, reveal!
      if (percent > 40 && !revealed) {
        revealed = true;
        document.getElementById('scratchCoverText').style.opacity = '0';
        canvas.style.opacity = '0';
        document.getElementById('scratchRevealed').style.opacity = '1';
        setTimeout(function() {
          canvas.style.pointerEvents = 'none';
        }, 500);
        startCountdown();
      }
    }

    // Countdown Logic
    function startCountdown() {
      var eventDate = new Date("May 23, 2026 18:30:00").getTime();
      var countEl = document.getElementById('countdownText');
      
      function update() {
        var now = new Date().getTime();
        var distance = eventDate - now;

        if (distance < 0) {
          countEl.innerHTML = "It's Time!";
          return;
        }

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        countEl.innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s left";
      }
      update();
      setInterval(update, 1000);
    }
  }

  // ─── Sound Toggle ───
  var soundToggle = document.getElementById('soundToggle');
  if (soundToggle) {
    soundToggle.addEventListener('click', function () {
      toggleMusic();
    });
  }

});
