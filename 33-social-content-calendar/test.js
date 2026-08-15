const assert = require("assert");
const logic = require("./logic.js");
const posts = [
  { channel: "LinkedIn", date: "2026-08-20", time: "10:00", done: true },
  { channel: "LinkedIn", date: "2026-08-18", time: "10:00", done: false },
  { channel: "LinkedIn", date: "2026-08-18", time: "10:00", done: false }
];
assert.strictEqual(logic.sortPosts(posts)[0].date, "2026-08-18");
assert.strictEqual(logic.conflicts(posts).length, 1);
assert.strictEqual(logic.progress(posts), 33);
console.log("Content calendar tests passed");
