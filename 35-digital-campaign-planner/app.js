var form = document.getElementById("planner");
var money = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });
function update() {
  var data = Object.fromEntries(new FormData(form));
  var result = CampaignLogic.calculate(data);
  document.getElementById("clicks").textContent = result.clicks;
  document.getElementById("leads").textContent = result.leads;
  document.getElementById("customers").textContent = result.customers;
  document.getElementById("revenue").textContent = money.format(result.revenue);
  document.getElementById("roas").textContent = result.roas.toFixed(2) + "x";
  document.getElementById("cpa").textContent = money.format(result.cpa);
  document.getElementById("break-even").textContent = result.breakEvenCustomers + " customers";
}
form.addEventListener("input", update);
update();
