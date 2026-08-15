var storageKey = "content-calendar-demo";
var starter = [
  { id: 1, title: "Python project carousel", channel: "LinkedIn", date: "2026-08-18", time: "10:00", campaign: "Portfolio", done: false },
  { id: 2, title: "Service tips reel", channel: "Instagram", date: "2026-08-19", time: "18:30", campaign: "Digital Seva", done: false }
];
var posts = JSON.parse(localStorage.getItem(storageKey) || JSON.stringify(starter));
var form = document.getElementById("post-form");

function persist() { localStorage.setItem(storageKey, JSON.stringify(posts)); }
function render() {
  var ordered = CalendarLogic.sortPosts(posts);
  document.getElementById("progress").textContent = CalendarLogic.progress(posts) + "%";
  document.getElementById("queue").innerHTML = ordered.map(function (post) {
    return "<article class='post " + (post.done ? "done" : "") + "'><div class='date'><strong>" +
      post.date.slice(8) + "</strong><span>" + post.date.slice(5, 7) + "</span></div><div><small>" +
      post.channel + " · " + post.time + "</small><h3>" + post.title + "</h3><p>" +
      post.campaign + "</p></div><button data-id='" + post.id + "'>" +
      (post.done ? "Published" : "Mark done") + "</button></article>";
  }).join("");
}

form.addEventListener("submit", function (event) {
  event.preventDefault();
  var data = new FormData(form);
  posts.push({
    id: Date.now(),
    title: data.get("title").trim(),
    channel: data.get("channel"),
    date: data.get("date"),
    time: data.get("time"),
    campaign: data.get("campaign").trim() || "General",
    done: false
  });
  persist(); form.reset(); render();
});
document.getElementById("queue").addEventListener("click", function (event) {
  if (!event.target.dataset.id) return;
  var id = Number(event.target.dataset.id);
  posts = posts.map(function (post) {
    return post.id === id ? Object.assign({}, post, { done: !post.done }) : post;
  });
  persist(); render();
});
render();
