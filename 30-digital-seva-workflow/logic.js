(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.WorkflowLogic = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  var statuses = ["Received", "In progress", "Ready", "Delivered"];
  function nextStatus(current) {
    var index = statuses.indexOf(current);
    return index < 0 || index === statuses.length - 1 ? current : statuses[index + 1];
  }
  function validate(request) {
    if (!request.customer || request.customer.trim().length < 2) return "Customer name is required";
    if (!request.service) return "Select a service";
    return "";
  }
  function summary(requests) {
    return statuses.reduce(function (result, status) {
      result[status] = requests.filter(function (item) { return item.status === status; }).length;
      return result;
    }, {});
  }
  return { statuses: statuses, nextStatus: nextStatus, validate: validate, summary: summary };
});
