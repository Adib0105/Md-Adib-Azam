var key = "digital-seva-demo";
var requests = JSON.parse(localStorage.getItem(key) || "[]");
var form = document.getElementById("request-form");

function save() {
  localStorage.setItem(key, JSON.stringify(requests));
}

function render() {
  var query = document.getElementById("search").value.toLowerCase();
  var visible = requests.filter(function (item) {
    return (item.customer + " " + item.service + " " + item.id).toLowerCase().includes(query);
  });
  document.getElementById("list").innerHTML = visible.map(function (item) {
    return "<article class='request'><div><small>" + item.id + "</small><h3>" +
      item.customer + "</h3><p>" + item.service + "</p></div><button data-id='" +
      item.id + "'>" + item.status + " →</button></article>";
  }).join("") || "<p class='empty'>No matching requests.</p>";
  var counts = WorkflowLogic.summary(requests);
  document.getElementById("summary").innerHTML = WorkflowLogic.statuses.map(function (status) {
    return "<span><strong>" + counts[status] + "</strong>" + status + "</span>";
  }).join("");
}

form.addEventListener("submit", function (event) {
  event.preventDefault();
  var item = {
    id: "SR-" + String(Date.now()).slice(-6),
    customer: form.customer.value.trim(),
    service: form.service.value,
    status: "Received"
  };
  var error = WorkflowLogic.validate(item);
  document.getElementById("error").textContent = error;
  if (error) return;
  requests.unshift(item);
  save();
  form.reset();
  render();
});

document.getElementById("list").addEventListener("click", function (event) {
  var id = event.target.dataset.id;
  if (!id) return;
  requests = requests.map(function (item) {
    return item.id === id ? Object.assign({}, item, { status: WorkflowLogic.nextStatus(item.status) }) : item;
  });
  save();
  render();
});
document.getElementById("search").addEventListener("input", render);
render();
