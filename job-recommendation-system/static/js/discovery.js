"use strict";
document.querySelectorAll('[data-marquee-pause]').forEach(button => {
  button.addEventListener('click', () => {
    const paused = button.closest('.opportunity-marquee').classList.toggle('is-paused');
    button.setAttribute('aria-pressed', String(paused));
    button.textContent = paused ? 'Resume motion' : 'Pause motion';
  });
});
