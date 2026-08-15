var tickets = [
  { id: "T-201", customer: "Asha", status: "Open", agent: "Neha", ageHours: 9, slaHours: 8, firstResponseMinutes: 18 },
  { id: "T-202", customer: "Ravi", status: "Pending", agent: "Imran", ageHours: 5, slaHours: 8, firstResponseMinutes: 24 },
  { id: "T-203", customer: "Sara", status: "Resolved", agent: "Neha", ageHours: 3, slaHours: 8, firstResponseMinutes: 12 },
  { id: "T-204", customer: "Kabir", status: "Open", agent: "Imran", ageHours: 13, slaHours: 12, firstResponseMinutes: 31 },
  { id: "T-205", customer: "Mina", status: "Resolved", agent: "Rupa", ageHours: 6, slaHours: 8, firstResponseMinutes: 15 }
];

function render(filter) {
  var visible = filter === "All"
    ? tickets
    : tickets.filter(function (ticket) { return ticket.status === filter; });
  var values = SLALogic.metrics(visible);
  document.getElementById("total").textContent = values.total;
  document.getElementById("open").textContent = values.open;
  document.getElementById("breached").textContent = values.breached;
  document.getElementById("response").textContent = values.averageResponse + " min";
  document.getElementById("rows").innerHTML = visible.map(function (ticket) {
    var breach = ticket.status !== "Resolved" && ticket.ageHours > ticket.slaHours;
    return "<tr><td>" + ticket.id + "</td><td>" + ticket.customer +
      "</td><td>" + ticket.agent + "</td><td><span class='status'>" +
      ticket.status + "</span></td><td class='" + (breach ? "danger" : "") +
      "'>" + ticket.ageHours + "h / " + ticket.slaHours + "h</td></tr>";
  }).join("");
}

document.getElementById("filter").addEventListener("change", function (event) {
  render(event.target.value);
});
render("All");
