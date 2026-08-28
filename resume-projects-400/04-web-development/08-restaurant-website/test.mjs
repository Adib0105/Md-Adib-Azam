import assert from "node:assert/strict";
import {sample,calculate} from "./logic.js";
const result=calculate(structuredClone(sample));
assert.equal(typeof result,"object");
assert.ok(result && Object.keys(result).length>0);
console.log("PASS");
