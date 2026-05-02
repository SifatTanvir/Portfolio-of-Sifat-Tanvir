(function () {
  const section = document.querySelector('#projects.projects.section');
  if (!section) return;

  const buttons = section.querySelectorAll('.project-tab-btn');
  const panels = section.querySelectorAll('.project-panel');
  if (!buttons.length || !panels.length) return;

  const slugToPanelId = {
    llm: 'project-panel-llm',
    android: 'project-panel-android',
    webgames: 'project-panel-webgames',
    python: 'project-panel-python',
  };

  function getAndroidSectionEl(hashWithoutHash) {
    if (!hashWithoutHash) return null;
    var el = document.getElementById(hashWithoutHash);
    if (!el || !el.closest) return null;
    return el.closest('#project-panel-android') ? el : null;
  }

  function getPythonSectionEl(hashWithoutHash) {
    if (!hashWithoutHash) return null;
    var el = document.getElementById(hashWithoutHash);
    if (!el || !el.closest) return null;
    return el.closest('#project-panel-python') ? el : null;
  }

  /** Open the Bootstrap collapse for a deep link like #python-rlhf (same page). */
  function expandPythonCardForHash(hashWithoutHash) {
    if (!hashWithoutHash || hashWithoutHash.indexOf('python-') !== 0) return;
    if (hashWithoutHash === 'python-overview') return;
    var suffix = hashWithoutHash.slice('python-'.length);
    if (!suffix) return;
    var collapseEl = document.getElementById('python-collapse-' + suffix);
    if (!collapseEl || typeof window.bootstrap === 'undefined' || !window.bootstrap.Collapse) return;
    window.bootstrap.Collapse.getOrCreateInstance(collapseEl, { toggle: false }).show();
  }

  function activate(slug, updateHash) {
    const panelId = slugToPanelId[slug];
    if (!panelId) return;

    buttons.forEach(function (btn) {
      const on = btn.dataset.project === slug;
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-selected', on ? 'true' : 'false');
    });

    panels.forEach(function (panel) {
      const on = panel.id === panelId;
      panel.classList.toggle('active', on);
      panel.setAttribute('aria-hidden', on ? 'false' : 'true');
    });

    if (slug === 'llm' || slug === 'webgames' || slug === 'android' || slug === 'python') {
      requestAnimationFrame(function () {
        window.dispatchEvent(new Event('resize'));
      });
    }

    if (updateHash && history.replaceState) {
      var path = window.location.pathname + window.location.search + '#' + slug;
      history.replaceState(null, '', path);
    }
  }

  var hash = window.location.hash.slice(1);
  if (hash && slugToPanelId[hash]) {
    activate(hash, false);
  } else if (hash) {
    var androidTarget = getAndroidSectionEl(hash);
    if (androidTarget) {
      activate('android', false);
      requestAnimationFrame(function () {
        window.dispatchEvent(new Event('resize'));
        androidTarget.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    } else {
      var pythonTarget = getPythonSectionEl(hash);
      if (pythonTarget) {
        activate('python', false);
        requestAnimationFrame(function () {
          window.dispatchEvent(new Event('resize'));
          expandPythonCardForHash(hash);
          pythonTarget.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      } else {
        activate('llm', false);
      }
    }
  } else {
    activate('llm', false);
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      activate(btn.dataset.project, true);
    });
  });

  window.addEventListener('hashchange', function () {
    var h = window.location.hash.slice(1);
    if (h && slugToPanelId[h]) {
      activate(h, false);
      return;
    }
    if (h) {
      var el = getAndroidSectionEl(h);
      if (el) {
        activate('android', false);
        requestAnimationFrame(function () {
          window.dispatchEvent(new Event('resize'));
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        return;
      }
      var py = getPythonSectionEl(h);
      if (py) {
        activate('python', false);
        requestAnimationFrame(function () {
          window.dispatchEvent(new Event('resize'));
          expandPythonCardForHash(h);
          py.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      }
    }
  });
})();
