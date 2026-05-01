(function () {
  const section = document.querySelector("#hobbies.projects.section");
  if (!section) return;

  const buttons = section.querySelectorAll(".project-tab-btn");
  const panels = section.querySelectorAll(".project-panel");
  if (!buttons.length || !panels.length) return;

  const slugToPanelId = {
    logo: "hobby-panel-logo",
    video: "hobby-panel-video",
    gaming: "hobby-panel-gaming",
    shows: "hobby-panel-shows"
  };

  function activate(slug, updateHash) {
    const panelId = slugToPanelId[slug];
    if (!panelId) return;

    buttons.forEach(function (btn) {
      var on = btn.dataset.project === slug;
      btn.classList.toggle("active", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });

    panels.forEach(function (panel) {
      var on = panel.id === panelId;
      panel.classList.toggle("active", on);
      panel.setAttribute("aria-hidden", on ? "false" : "true");
      if (!on) {
        panel.querySelectorAll("video").forEach(function (vid) {
          vid.pause();
        });
      }
    });

    if (slug === "video" || slug === "gaming") {
      requestAnimationFrame(function () {
        window.dispatchEvent(new Event("resize"));
      });
    }

    if (updateHash && history.replaceState) {
      var path = window.location.pathname + window.location.search + "#" + slug;
      history.replaceState(null, "", path);
    }
  }

  var hash = window.location.hash.slice(1);
  if (hash && slugToPanelId[hash]) {
    activate(hash, false);
  } else {
    activate("logo", false);
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      activate(btn.dataset.project, true);
    });
  });

  window.addEventListener("hashchange", function () {
    var h = window.location.hash.slice(1);
    if (h && slugToPanelId[h]) {
      activate(h, false);
    }
  });
})();
