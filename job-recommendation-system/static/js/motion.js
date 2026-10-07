"use strict";

// Progressive enhancement: content is always visible without JavaScript.
// Off-screen sections animate once when they enter view; nothing loops.
document.addEventListener("DOMContentLoaded", () => {
  const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (preference.matches || !("IntersectionObserver" in window) || !("animate" in Element.prototype)) return;

  const animations = new Set();
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      observer.unobserve(entry.target);
      if (preference.matches) continue;
      const siblings = Array.from(entry.target.parentElement.children);
      const delay = Math.min(siblings.indexOf(entry.target) % 4, 3) * 55;
      const animation = entry.target.animate([
        { opacity: 0, transform: "translateY(14px)" },
        { opacity: 1, transform: "translateY(0)" }
      ], { duration: 620, delay, easing: "cubic-bezier(.22, 1, .36, 1)", fill: "backwards" });
      animations.add(animation);
      animation.onfinish = animation.oncancel = () => animations.delete(animation);
      // Keyboard navigation should never wait for decorative motion.
      entry.target.addEventListener("focusin", () => animation.finish(), { once: true });
    }
  }, { threshold: 0.08 });

  const selectors = ".hero-copy, .page-heading, .stat-card, .feature-card, .job-card, .path-card, .category-grid > a, .how-section, .landing-cta, .chart-card, .simulation-card";
  document.querySelectorAll(selectors).forEach(element => observer.observe(element));
  preference.addEventListener("change", event => {
    if (event.matches) {
      observer.disconnect();
      animations.forEach(animation => animation.cancel());
      animations.clear();
    }
  });
});
