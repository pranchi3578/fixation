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

  // ─── Writing Effect for Scroll Text ───
  var scrollLines = document.querySelectorAll('.scroll-line');
  scrollLines.forEach(function(line) {
    var content = line.innerHTML;
    line.innerHTML = '<span class="write-span">' + content + '</span>';
  });

  // ─── Church Doors Reveal (Amen Theme) ───
  var coverLetter = document.getElementById('coverLetter');
  if (coverLetter && typeof gsap !== 'undefined') {
    coverLetter.addEventListener('click', function() {
      // 1. Start music immediately on tap
      startMusic();

      // Break seal animation
      gsap.to('#waxSeal', {
        scale: 1.5,
        opacity: 0,
        duration: 0.4,
        ease: "back.in(2)"
      });
      
      gsap.to('#sealText', {
        opacity: 0,
        duration: 0.3
      });

      // Expand the scroll cylinder vertically to simulate unrolling before fade out
      gsap.to('#rolledCylinder', {
        height: "100vh",
        width: "420px",
        borderRadius: "0px",
        duration: 1.2,
        delay: 0.3,
        ease: "power3.inOut"
      });

      // Fade out the whole wrapper to reveal the real scene-scroll behind
      gsap.to(coverLetter, {
        opacity: 0,
        duration: 0.8,
        delay: 1.2,
        ease: "power2.inOut",
        onComplete: function() {
          coverLetter.style.display = 'none';
          document.body.classList.remove('no-scroll');
          
          // Animate the scroll text left-to-right as if being written
          gsap.to('.write-span', {
            clipPath: 'inset(0 0% 0 0)',
            opacity: 1,
            duration: 1.8,
            stagger: 1.2,
            ease: "power2.inOut",
            onComplete: function() {
              // Timeline for the Fixation -> Malayalam rub-off effect
              var tl = gsap.timeline({
                onComplete: function() {
                  // Make the SVG container visible
                  gsap.to('.couple-line-art', { opacity: 1, duration: 0.5 });
                  
                  // Animate the line art drawing itself!
                  gsap.to('.draw-line', {
                    strokeDashoffset: 0,
                    duration: 3,
                    stagger: 0.2,
                    ease: "power2.inOut",
                    onComplete: function() {
                      gsap.to('#artText', { opacity: 1, duration: 1 });
                      var scrollPrompt = document.getElementById('scrollPrompt');
                      if (scrollPrompt && !window.scrolledAlready) {
                        scrollPrompt.classList.remove('hidden');
                      }
                    }
                  });
                }
              });

              // 1. Write "Fixation" left-to-right
              tl.to('#fixEnSpan', { clipPath: 'inset(0 0% 0 0)', opacity: 1, duration: 1.2, ease: "power2.inOut" })
                // 2. Pause for a split second
                .to({}, { duration: 0.5 })
                // 3. Rub it off! (Wipe it away quickly)
                .to('#fixEnSpan', { clipPath: 'inset(0 100% 0 0)', opacity: 0, duration: 0.5, ease: "power1.in" })
                // 4. Write "ഉറപ്പീരു" left-to-right
                .to('#fixMlSpan', { clipPath: 'inset(0 0% 0 0)', opacity: 1, duration: 1.2, ease: "power2.inOut" });
            }
          });
        }
      });
    });
  }

  // ─── GSAP ScrollTrigger: Reveal on Scroll ───
  if (typeof gsap !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    // Animate Scenes
    gsap.utils.toArray('.scene:not(.scene-scroll)').forEach(function(scene) {
      gsap.fromTo(scene, 
        { opacity: 0, y: 50 },
        { 
          opacity: 1, 
          y: 0, 
          duration: 1.2, 
          ease: "power2.out",
          scrollTrigger: {
            trigger: scene,
            start: "top 85%",
          }
        }
      );
    });

    // Milestones
    gsap.utils.toArray('.milestone').forEach(function(milestone, i) {
      gsap.fromTo(milestone,
        { opacity: 0, x: i % 2 === 0 ? -50 : 50, y: 40 },
        {
          opacity: 1, x: 0, y: 0, duration: 1, ease: "power2.out",
          scrollTrigger: {
            trigger: milestone,
            start: "top 85%",
          }
        }
      );
      
      var img = milestone.querySelector('.milestone-img');
      if (img) {
        gsap.fromTo(img,
          { scale: 1.2 },
          {
            scale: 1, ease: "none",
            scrollTrigger: {
              trigger: milestone,
              start: "top bottom",
              end: "bottom top",
              scrub: true
            }
          }
        );
      }
    });

    // Church Image
    gsap.fromTo('.church-img',
      { filter: "brightness(0.5)", scale: 0.95 },
      {
        filter: "brightness(1)", scale: 1, duration: 1.5,
        scrollTrigger: { trigger: '.scene-church', start: "top 70%" }
      }
    );

    // AAMEN Text
    gsap.fromTo('.aamen-text-ml',
      { scale: 0.5, opacity: 0, filter: "blur(10px)" },
      {
        scale: 1, opacity: 1, filter: "blur(0px)", duration: 2, ease: "power3.out",
        scrollTrigger: { trigger: '.scene-aamen', start: "top 70%" }
      }
    );

    // Invite Card
    gsap.fromTo('.invite-card',
      { y: 100, opacity: 0, rotationX: 15 },
      {
        y: 0, opacity: 1, rotationX: 0, duration: 1.2, transformPerspective: 1000, ease: "power3.out",
        scrollTrigger: { trigger: '.scene-invite', start: "top 80%" }
      }
    );

    // ─── Floating Dust Motes (Amen Magic) ───
    function createDust() {
      const container = document.body;
      const count = 15;
      for (let i = 0; i < count; i++) {
        const dust = document.createElement('div');
        dust.className = 'dust-mote';
        container.appendChild(dust);
        
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * window.innerHeight;
        
        gsap.set(dust, {
          x: startX,
          y: startY,
          opacity: Math.random() * 0.4,
          scale: Math.random() * 0.5 + 0.5
        });
        
        gsap.to(dust, {
          x: "+=" + (Math.random() * 200 - 100),
          y: "+=" + (Math.random() * 200 - 100),
          opacity: 0,
          duration: 5 + Math.random() * 5,
          repeat: -1,
          yoyo: true,
          ease: "sine.inOut"
        });
      }
    }
    createDust();

    // Glow removed for premium white theme
  }

  // ─── Scroll Prompt: hide after first scroll ───
  var scrollPrompt = document.getElementById('scrollPrompt');
  window.scrolledAlready = false;
  window.addEventListener('scroll', function () {
    if (!window.scrolledAlready && window.scrollY > 80) {
      window.scrolledAlready = true;
      if (scrollPrompt) scrollPrompt.classList.add('hidden');
    }
  }, { passive: true });

  // ─── Scene 1: Line Art (No longer interactive bell) ───
  var artContainer = document.getElementById('artContainer');
  if (artContainer) {
    // If we wanted to make it interactive later, we could add it here
  }

  // ─── Scene 5: Golden Particles ───
  var aamenScene = document.getElementById('scene-aamen');
  var particlesCreated = false;

  if (typeof gsap !== 'undefined') {
    ScrollTrigger.create({
      trigger: '.scene-aamen',
      start: "top 70%",
      onEnter: function() {
        if (!particlesCreated) {
          particlesCreated = true;
          createParticles();
        }
      }
    });
  }

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

    // Fill canvas with rich gold leaf texture
    function initCanvas() {
      canvas.width = canvas.parentElement.offsetWidth;
      canvas.height = canvas.parentElement.offsetHeight;
      
      // Rich gold gradient
      var grd = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      grd.addColorStop(0, '#cfa144');
      grd.addColorStop(0.3, '#f5edd6');
      grd.addColorStop(0.6, '#8b6b4a');
      grd.addColorStop(1, '#cfa144');
      
      ctx.fillStyle = grd;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Add subtle noise texture for "leaf" effect
      ctx.fillStyle = 'rgba(0,0,0,0.08)';
      for (var i = 0; i < 1500; i++) {
        ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 1.5, 1.5);
      }
      
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

    function createFlake(x, y) {
      if (typeof gsap === 'undefined') return;
      var rect = canvas.getBoundingClientRect();
      var flake = document.createElement('div');
      flake.className = 'gold-flake';
      flake.style.left = (rect.left + x) + 'px';
      flake.style.top = (rect.top + y) + 'px';
      document.body.appendChild(flake);
      
      gsap.to(flake, {
        x: "+=" + (Math.random() * 60 - 30),
        y: "+=" + (Math.random() * 150 + 50),
        rotation: Math.random() * 360,
        opacity: 0,
        duration: 0.8 + Math.random(),
        ease: "power1.in",
        onComplete: function() { flake.remove(); }
      });
    }

    function scratch(e) {
      if (!isDrawing || revealed) return;
      e.preventDefault();
      var pos = getMousePos(e);
      ctx.beginPath();
      // Make the brush massive so it's very easy
      ctx.arc(pos.x, pos.y, 50 + Math.random() * 10, 0, Math.PI * 2);
      ctx.fill();
      
      if (Math.random() > 0.4) {
        createFlake(pos.x, pos.y);
      }
      
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
        // Anti-aliasing can leave alpha > 0, so check < 50
        if (pixels[i] < 50) transparent++;
      }
      var percent = (transparent / (pixels.length / 4)) * 100;
      
      // If just 5% scratched, reveal!
      if (percent > 5 && !revealed) {
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
