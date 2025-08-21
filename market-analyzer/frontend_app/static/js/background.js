// /static/js/background.js
(function initParticles(){
  const el = document.getElementById('particles-js');
  if (!el || typeof particlesJS !== 'function') return;

  // respeita utilizadores com redução de movimento
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    el.style.display = 'none';
    return;
  }

  // usa a cor do tema se quiseres
  const root = getComputedStyle(document.documentElement);
  const particleColor = (root.getPropertyValue('--p-text-color') || '#ffffff').trim();

  particlesJS('particles-js', {
    particles: {
      number: { value: 40, density: { enable: true, value_area: 1000 } },
      color: { value: particleColor },
      shape: { type: 'circle' },
      opacity: { value: 0.18 },
      size: { value: 2, random: true },   // 👈 > 0 para serem visíveis
      line_linked: {
        enable: true, distance: 150,
        color: particleColor, opacity: 0.15, width: 1
      },
      move: { enable: true, speed: 0.6, out_mode: 'out' }
    },
    interactivity: {
      detect_on: 'canvas',
      events: { onhover: { enable: true, mode: 'repulse' }, resize: true },
      modes: { repulse: { distance: 120, duration: 0.4 } }
    },
    retina_detect: true
  });
})();
