document.getElementById("year").textContent = new Date().getFullYear();
document.querySelector(".filters").addEventListener("click", function (event) {
  var filter = event.target.dataset.filter;
  if (!filter) return;
  document.querySelectorAll(".filters button").forEach(function (button) {
    button.classList.toggle("active", button === event.target);
  });
  document.querySelectorAll(".projects article").forEach(function (card) {
    var show = filter === "all" || card.dataset.category.split(" ").includes(filter);
    card.classList.toggle("hidden", !show);
  });
});
