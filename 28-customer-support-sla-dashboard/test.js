const assert = require("assert");
const logic = require("./logic.js");
const sample = [
  { status: "Open", ageHours: 9, slaHours: 8, firstResponseMinutes: 10, agent: "A" },
  { status: "Resolved", ageHours: 2, slaHours: 8, firstResponseMinutes: 20, agent: "B" }
];
assert.deepStrictEqual(logic.metrics(sample), { total: 2, open: 1, breached: 1, averageResponse: 15 });
assert.deepStrictEqual(logic.workload(sample), { A: 1 });
console.log("SLA dashboard tests passed");
