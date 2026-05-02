(function () {
  var panel = document.getElementById("project-panel-python");
  if (!panel) return;

  function loadCode(details) {
    var pre = details.querySelector("pre[data-code-src]");
    if (!pre) return;
    var code = pre.querySelector("code.project-python-code__inner");
    if (!code || code.getAttribute("data-loaded") === "1") return;
    var src = pre.getAttribute("data-code-src");
    if (!src) return;
    code.textContent = "Loading...";
    fetch(src, { credentials: "same-origin" })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.text();
      })
      .then(function (text) {
        code.textContent = text;
        code.setAttribute("data-loaded", "1");
      })
      .catch(function (err) {
        code.textContent =
          "Could not load source: " +
          (err && err.message ? err.message : String(err)) +
          ". Use the main.py download link above.";
      });
  }

  panel.addEventListener(
    "toggle",
    function (ev) {
      var el = ev.target;
      if (!el || el.tagName !== "DETAILS" || !el.open) return;
      loadCode(el);
    },
    true
  );
})();
