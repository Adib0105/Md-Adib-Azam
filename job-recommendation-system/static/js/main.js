"use strict";
document.addEventListener("DOMContentLoaded", () => {
  const menu = document.querySelector(".mobile-menu");
  const sidebar = document.getElementById("sidebar");
  if (menu && sidebar) {
    menu.addEventListener("click", () => {
      const open = sidebar.classList.toggle("open");
      menu.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", event => {
      if (!sidebar.contains(event.target) && !menu.contains(event.target)) {
        sidebar.classList.remove("open");
        menu.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape") {
        sidebar.classList.remove("open");
        menu.setAttribute("aria-expanded", "false");
      }
    });
  }
  document.querySelectorAll(".notice .dismiss").forEach(button => {
    button.addEventListener("click", () => button.closest(".notice").remove());
  });
  document.querySelectorAll("form[data-confirm]").forEach(form => {
    form.addEventListener("submit", event => {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });
  const editors = new Map();
  document.querySelectorAll("input[data-tags]").forEach(source => {
    let values = source.value.split(/[,;|\n]/).map(s => s.trim()).filter(Boolean);
    const wrapper = document.createElement("div");
    wrapper.className = "tag-editor";
    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Add a skill…";
    input.setAttribute("aria-label", "Add a skill. Press Enter or comma to add.");
    input.autocomplete = "off";
    const dictionary = document.getElementById(source.dataset.dictionary);
    if (dictionary) {
      const list = document.createElement("datalist");
      list.id = `${source.id}-options`;
      JSON.parse(dictionary.textContent).forEach(skill => {
        const option = document.createElement("option");
        option.value = skill;
        list.appendChild(option);
      });
      source.after(list);
      input.setAttribute("list", list.id);
    }
    function render() {
      wrapper.querySelectorAll(".tag").forEach(tag => tag.remove());
      values.forEach(value => {
        const chip = document.createElement("span");
        chip.className = "tag";
        const label = document.createElement("span");
        label.textContent = value;
        const remove = document.createElement("button");
        remove.type = "button";
        remove.textContent = "×";
        remove.setAttribute("aria-label", `Remove ${value}`);
        remove.addEventListener("click", () => {
          values = values.filter(item => item !== value);
          render();
          input.focus();
        });
        chip.append(label, remove);
        wrapper.insertBefore(chip, input);
      });
      source.value = values.join(", ");
    }
    function add(text) {
      for (const value of text.split(/[,;|\n]/).map(s => s.trim().slice(0, 100)).filter(Boolean)) {
        if (!values.some(item => item.toLowerCase() === value.toLowerCase())) values.push(value);
      }
      render();
    }
    wrapper.appendChild(input);
    source.after(wrapper);
    source.type = "hidden";
    const sourceLabel = document.querySelector(`label[for="${source.id}"]`);
    input.id = `${source.id}-entry`;
    if (sourceLabel) sourceLabel.htmlFor = input.id;
    render();
    input.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === ",") {
        event.preventDefault();
        add(input.value);
        input.value = "";
      }
    });
    input.addEventListener("blur", () => {
      if (input.value.trim()) { add(input.value); input.value = ""; }
    });
    source.form.addEventListener("submit", () => { add(input.value); input.value = ""; });
    editors.set(source.id, add);
  });
  document.querySelectorAll("[data-add-skill]").forEach(button => {
    button.addEventListener("click", () => {
      const add = editors.get(button.dataset.target);
      if (add) add(button.dataset.addSkill);
    });
  });
  document.querySelectorAll("input[type=file]").forEach(input => {
    input.addEventListener("change", () => {
      const file = input.files[0];
      input.setCustomValidity(file && file.size > 5 * 1024 * 1024 ? "Choose a file no larger than 5 MB." : "");
      if (file && !/\.(pdf|docx)$/i.test(file.name)) input.setCustomValidity("Choose a PDF or DOCX resume.");
      input.reportValidity();
    });
  });
  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", event => {
      if (event.defaultPrevented || !form.checkValidity()) return;
      const button = event.submitter;
      if (button && !button.classList.contains("icon-btn")) {
        button.classList.add("loading");
        button.setAttribute("aria-busy", "true");
        // Keep submit buttons enabled so name/value (confirm/discard) is sent.
        window.setTimeout(() => { button.classList.remove("loading"); button.removeAttribute("aria-busy"); }, 12000);
      }
    });
  });
  const motion = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (motion) document.querySelectorAll(".score-ring").forEach(ring => {
    const end = Number(ring.style.getPropertyValue("--score"));
    const start = performance.now();
    function animate(now) {
      const fraction = Math.min((now - start) / 650, 1);
      ring.style.setProperty("--score", end * (1 - Math.pow(1 - fraction, 3)));
      if (fraction < 1) requestAnimationFrame(animate);
    }
    requestAnimationFrame(animate);
  });
  const chartSource = document.getElementById("charts-data");
  if (chartSource && window.Chart) {
    Chart.defaults.font.family = '"Manrope", "Segoe UI", Arial, sans-serif';
    const charts = JSON.parse(chartSource.textContent);
    const palette = ["#719661", "#a2b98b", "#c5d3aa", "#dfcda3", "#bba8c7", "#86adb2", "#d4a895", "#b2c9a5", "#91a780", "#e3d5b4"];
    document.querySelectorAll("canvas[data-chart]").forEach(canvas => {
      const series = charts[canvas.dataset.chart];
      if (!series) return;
      const donut = series.type === "doughnut";
      new Chart(canvas, {
        type: series.type,
        data: {labels: series.labels, datasets: [{label: canvas.dataset.chart, data: series.values,
          backgroundColor: series.type === "line" ? "#72956120" : palette,
          borderColor: series.type === "line" ? "#729561" : "#fff",
          borderWidth: donut ? 3 : 1, borderRadius: donut ? 0 : 5, fill: series.type === "line", tension: 0.2,
          maxBarThickness: 24}]},
        options: {
          responsive: true, maintainAspectRatio: false, animation: motion ? {duration: 500} : false,
          indexAxis: series.type === "bar" ? "y" : "x", cutout: donut ? "72%" : undefined,
          plugins: {legend: {display: donut, position: "bottom", labels: {usePointStyle: true, pointStyle: "circle", boxWidth: 6, padding: 15, color: "#75896a", font: {size: 10}}}, tooltip: {backgroundColor: "#254a35", padding: 12, cornerRadius: 7}},
          scales: donut ? {} : {
            x: {beginAtZero: true, grid: {color: "#f0f3e8", display: series.type === "bar"}, border: {display: false}, ticks: {color: "#7c906e", font: {size: 9}}},
            y: {beginAtZero: true, grid: {display: series.type === "line", color: "#f0f3e8"}, border: {display: false}, ticks: {color: "#748968", font: {size: 10}}}
          }
        }
      });
    });
  }
});
