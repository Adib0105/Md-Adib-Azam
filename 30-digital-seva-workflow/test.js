const assert = require("assert");
const logic = require("./logic.js");
assert.strictEqual(logic.nextStatus("Received"), "In progress");
assert.strictEqual(logic.nextStatus("Delivered"), "Delivered");
assert.ok(logic.validate({ customer: "", service: "Print" }));
assert.deepStrictEqual(logic.summary([{ status: "Ready" }, { status: "Ready" }])["Ready"], 2);
console.log("Digital seva workflow tests passed");
