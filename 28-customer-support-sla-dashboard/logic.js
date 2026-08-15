(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.SLALogic = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  function metrics(tickets) {
    var open = tickets.filter(function (t) { return t.status !== "Resolved"; });
    var breached = open.filter(function (t) { return t.ageHours > t.slaHours; });
    var responses = tickets.map(function (t) { return Number(t.firstResponseMinutes); });
    var average = responses.length
      ? responses.reduce(function (a, b) { return a + b; }, 0) / responses.length
      : 0;
    return {
      total: tickets.length,
      open: open.length,
      breached: breached.length,
      averageResponse: Math.round(average)
    };
  }

  function workload(tickets) {
    return tickets.reduce(function (result, ticket) {
      if (ticket.status !== "Resolved") {
        result[ticket.agent] = (result[ticket.agent] || 0) + 1;
      }
      return result;
    }, {});
  }

  return { metrics: metrics, workload: workload };
});
