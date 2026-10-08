"use strict";

// Local, fixed FAQs only. No fetch, storage, profile access or HTML insertion.
(() => {
  const root = document.getElementById("project-chat");
  const source = document.getElementById("project-chat-faqs");
  if (!root || !source) return;
  const faqs = JSON.parse(source.textContent).map(faq => ({
    ...faq, intents: faq.patterns.map(pattern => new RegExp(pattern, "u"))
  }));
  const panel = document.getElementById("project-chat-panel");
  const launcher = document.getElementById("project-chat-launcher");
  const messages = document.getElementById("project-chat-messages");
  const form = document.getElementById("project-chat-form");
  const input = document.getElementById("project-chat-question");
  const send = document.getElementById("project-chat-send");
  const typing = document.getElementById("project-chat-typing");
  const status = document.getElementById("project-chat-status");
  const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
  let open = false, busy = false, replyTimer = null, hideTimer = null, openFrame = null;

  function setOpen(value) {
    open = value;
    clearTimeout(hideTimer);
    cancelAnimationFrame(openFrame);
    launcher.setAttribute("aria-expanded", String(open));
    panel.inert = !open;
    if (open) {
      panel.hidden = false;
      if (preference.matches) root.classList.add("is-open");
      else openFrame = requestAnimationFrame(() => root.classList.add("is-open"));
      input.focus({preventScroll: true});
    } else {
      root.classList.remove("is-open");
      launcher.focus({preventScroll: true});
      if (preference.matches) panel.hidden = true;
      else hideTimer = setTimeout(() => { if (!open) panel.hidden = true; }, 190);
    }
  }

  function appendMessage(text, user = false, links = []) {
    const bubble = document.createElement("div");
    bubble.className = `project-chat-message${user ? " is-user" : ""}`;
    bubble.setAttribute("aria-label", user ? "You" : "JobMatch guide");
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    bubble.appendChild(paragraph);
    if (links.length) {
      const navigation = document.createElement("div");
      navigation.className = "project-chat-links";
      for (const link of links) {
        const target = new URL(link.href, window.location.origin);
        if (target.origin !== window.location.origin || !link.href.startsWith("/")) continue;
        const anchor = document.createElement("a");
        anchor.href = target.pathname + target.hash;
        anchor.textContent = link.label;
        navigation.appendChild(anchor);
      }
      bubble.appendChild(navigation);
    }
    messages.appendChild(bubble);
    while (messages.children.length > 60) messages.firstElementChild.remove();
    messages.scrollTop = messages.scrollHeight;
  }

  function setBusy(value) {
    busy = value;
    send.disabled = busy;
    typing.hidden = !busy;
    messages.setAttribute("aria-busy", String(busy));
  }

  function ask(question) {
    const text = question.trim().slice(0, 300);
    if (!text || busy) return;
    input.value = "";
    status.textContent = "";
    appendMessage(text, true);
    const normalized = text.normalize("NFKC").toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, " ").replace(/\s+/g, " ").trim();
    const faq = faqs.find(item => item.intents.some(intent => intent.test(normalized)));
    setBusy(true);
    replyTimer = setTimeout(() => {
      const fallback = "I can help with JobMatch features, navigation, matching and the college project team. I cannot read account details or private resumes. Try asking about resume upload, match scores or the project team.";
      appendMessage(faq ? faq.answer : fallback, false, faq ? faq.links : []);
      setBusy(false);
      replyTimer = null;
    }, preference.matches ? 0 : 320);
  }

  launcher.addEventListener("click", () => setOpen(!open));
  for (const id of ["project-chat-minimize", "project-chat-close"]) {
    document.getElementById(id).addEventListener("click", () => setOpen(false));
  }
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && open) { event.preventDefault(); setOpen(false); }
  });
  form.addEventListener("submit", event => { event.preventDefault(); ask(input.value); });
  root.querySelectorAll("[data-project-question]").forEach(button => {
    button.addEventListener("click", () => { ask(button.dataset.projectQuestion); input.focus(); });
  });
  document.getElementById("project-chat-clear").addEventListener("click", () => {
    clearTimeout(replyTimer);
    replyTimer = null;
    setBusy(false);
    messages.replaceChildren();
    welcome();
    input.value = "";
    status.textContent = "Chat cleared.";
    input.focus();
  });
  preference.addEventListener("change", event => {
    if (!event.matches) return;
    cancelAnimationFrame(openFrame);
    clearTimeout(hideTimer);
    if (open) root.classList.add("is-open");
    else panel.hidden = true;
  });
  function welcome() {
    appendMessage("Hi! Ask me about JobMatch, resume upload, matching or the college project team. I use local FAQs and keep this chat in your browser.");
  }
  welcome();
  launcher.hidden = false;
})();
