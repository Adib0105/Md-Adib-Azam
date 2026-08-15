(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.CalendarLogic = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  function sortPosts(posts) {
    return posts.slice().sort(function (a, b) {
      return (a.date + a.time).localeCompare(b.date + b.time);
    });
  }
  function conflicts(posts) {
    var seen = {};
    return posts.filter(function (post) {
      var key = post.channel + "|" + post.date + "|" + post.time;
      seen[key] = (seen[key] || 0) + 1;
      return seen[key] > 1;
    });
  }
  function progress(posts) {
    if (!posts.length) return 0;
    return Math.round(100 * posts.filter(function (post) { return post.done; }).length / posts.length);
  }
  return { sortPosts: sortPosts, conflicts: conflicts, progress: progress };
});
