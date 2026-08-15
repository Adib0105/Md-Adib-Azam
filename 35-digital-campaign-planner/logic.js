(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.CampaignLogic = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  function calculate(input) {
    var impressions = Number(input.impressions);
    var budget = Number(input.budget);
    var clicks = impressions * Number(input.ctr) / 100;
    var leads = clicks * Number(input.leadRate) / 100;
    var customers = leads * Number(input.closeRate) / 100;
    var revenue = customers * Number(input.orderValue);
    return {
      clicks: Math.round(clicks),
      leads: Math.round(leads),
      customers: Math.round(customers),
      revenue: Math.round(revenue),
      cpc: clicks ? budget / clicks : 0,
      cpa: customers ? budget / customers : 0,
      roas: budget ? revenue / budget : 0,
      breakEvenCustomers: Number(input.orderValue) ? Math.ceil(budget / Number(input.orderValue)) : 0
    };
  }
  return { calculate: calculate };
});
