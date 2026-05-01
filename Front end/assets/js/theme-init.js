(function () {
  try {
    var key = "portfolio-theme";
    var stored = localStorage.getItem(key);
    if (
      stored === "dark" ||
      (stored !== "light" &&
        !stored &&
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  } catch (e) {}
})();
