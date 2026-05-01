(function() {
  "use strict";

  /**
   * Dark / light theme toggle (registered first so it still works if later init throws — e.g. on GitHub Pages).
   */
  const THEME_STORAGE_KEY = "portfolio-theme";

  function syncThemeToggleButton() {
    const btn = document.getElementById("theme-toggle");
    if (!btn) return;
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    btn.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    btn.setAttribute("title", isDark ? "Light mode" : "Dark mode");
    const icon = btn.querySelector("i");
    if (icon) {
      icon.className = isDark ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
    }
  }

  function applyTheme(theme) {
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    try {
      localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch (e) {}
    syncThemeToggleButton();
  }

  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      const isDark = document.documentElement.getAttribute("data-theme") === "dark";
      applyTheme(isDark ? "light" : "dark");
    });
    syncThemeToggleButton();
  }

  /**
   * Footer running animal + picker (runs early so GLightbox / Swiper / Isotope errors on heavy pages cannot skip it — e.g. GitHub Pages gallery).
   */
  function initFooterMascot() {
    const footer = document.getElementById("footer");
    if (!footer || footer.querySelector(".footer-mascot")) return;
    const container = footer.querySelector(".container");
    if (!container) return;

    const STORAGE_KEY = "footer-mascot-animal";
    const animals = [
      { id: "dog", label: "Dog", char: "🐕" },
      { id: "cat", label: "Cat", char: "🐈" },
      { id: "rabbit", label: "Rabbit", char: "🐇" },
      { id: "horse", label: "Horse", char: "🐎" },
      { id: "turtle", label: "Turtle", char: "🐢" },
      { id: "penguin", label: "Penguin", char: "🐧" },
      { id: "dino", label: "Dinosaur", char: "🦖" }
    ];

    const TRACK_MODE_CLASSES = [
      "footer-mascot-track--cat",
      "footer-mascot-track--dog",
      "footer-mascot-track--horse",
      "footer-mascot-track--rabbit",
      "footer-mascot-track--turtle",
      "footer-mascot-track--penguin",
      "footer-mascot-track--dino"
    ];

    const catSilhouetteHtml =
      '<span class="fmc" aria-hidden="true">' +
      '<span class="fmc-tail"></span>' +
      '<span class="fmc-torso"></span>' +
      '<span class="fmc-head"></span>' +
      '<span class="fmc-ear fmc-ear--l"></span>' +
      '<span class="fmc-ear fmc-ear--r"></span>' +
      '<span class="fmc-leg fmc-leg--1"></span>' +
      '<span class="fmc-leg fmc-leg--2"></span>' +
      '<span class="fmc-leg fmc-leg--3"></span>' +
      '<span class="fmc-leg fmc-leg--4"></span>' +
      "</span>";

    const optionsHtml = animals
      .map(function (a) {
        return '<option value="' + a.id + '">' + a.label + "</option>";
      })
      .join("");

    const wrap = document.createElement("div");
    wrap.className = "footer-mascot";
    wrap.innerHTML =
      '<div class="footer-mascot-controls">' +
      '<label class="footer-mascot-label" for="footer-mascot-select">Runner</label>' +
      '<select id="footer-mascot-select" class="form-select form-select-sm footer-mascot-select" aria-label="Choose footer animal">' +
      optionsHtml +
      "</select></div>" +
      '<div class="footer-mascot-track" tabindex="0" role="img" aria-label="Animated runner. Click or press Enter for a hop." title="Click for a hop">' +
      '<div class="footer-mascot-lane">' +
      '<span class="footer-mascot-runner">' +
      '<span class="footer-mascot-bounce">' +
      '<span class="footer-mascot-char" id="footer-mascot-char"></span>' +
      "</span></span></div></div>";

    container.appendChild(wrap);

    const select = document.getElementById("footer-mascot-select");
    const charEl = document.getElementById("footer-mascot-char");
    const track = wrap.querySelector(".footer-mascot-track");
    const bounceEl = wrap.querySelector(".footer-mascot-bounce");
    if (!select || !charEl || !track) return;

    function syncTrackMode(id) {
      TRACK_MODE_CLASSES.forEach(function (cls) {
        track.classList.remove(cls);
      });
      track.classList.add("footer-mascot-track--" + id);
    }

    const byId = {};
    animals.forEach(function (a) {
      byId[a.id] = a.char;
    });

    function setAnimal(id) {
      var mode = byId[id] ? id : "dog";
      charEl.className = "footer-mascot-char" + (mode === "cat" ? " footer-mascot-char--css-cat" : "");
      if (mode === "cat") {
        charEl.innerHTML = catSilhouetteHtml;
      } else {
        charEl.innerHTML = "";
        charEl.textContent = byId[mode];
      }
      syncTrackMode(mode);
      if (select.value !== mode) {
        select.value = mode;
      }
      try {
        localStorage.setItem(STORAGE_KEY, mode);
      } catch (e) {}
    }

    function triggerHop() {
      if (!bounceEl || bounceEl.classList.contains("footer-mascot-bounce--jump")) return;
      if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      bounceEl.classList.add("footer-mascot-bounce--jump");
      window.setTimeout(function () {
        bounceEl.classList.remove("footer-mascot-bounce--jump");
      }, 560);
    }

    track.addEventListener("click", function (e) {
      if (e.target.closest(".footer-mascot-select")) return;
      triggerHop();
    });
    track.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        triggerHop();
      }
    });

    var stored = "dog";
    try {
      stored = localStorage.getItem(STORAGE_KEY) || "dog";
    } catch (e) {}
    if (!byId[stored]) stored = "dog";
    select.value = stored;
    setAnimal(stored);

    select.addEventListener("change", function () {
      setAnimal(select.value);
    });
  }

  try {
    initFooterMascot();
  } catch (e) {}

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader || !selectBody) return;
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    if (!mobileNavToggleBtn) return;
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      const parent = this.parentNode;
      const submenu = parent && parent.nextElementSibling;
      if (!submenu) return;
      parent.classList.toggle('active');
      submenu.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  if (scrollTop) {
    scrollTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Skills progress bar fill: red (0%) → yellow (50%) → deep green (100%)
   */
  function skillBarFillForPercent(p) {
    var pct = Math.max(0, Math.min(100, Number(p) || 0));
    var h;
    var s;
    var l;
    if (pct <= 50) {
      var t = pct / 50;
      h = 0 + 52 * t;
      s = 86 + 9 * t;
      l = 43 + 5 * t;
    } else {
      var t2 = (pct - 50) / 50;
      h = 52 + 93 * t2;
      s = 95 - 23 * t2;
      l = 48 - 15 * t2;
    }
    return "hsl(" + h + ", " + s + "%, " + l + "%)";
  }

  document.querySelectorAll(".skills-animation .progress-bar").forEach(function (el) {
    var v = parseInt(el.getAttribute("aria-valuenow"), 10);
    el.style.backgroundColor = skillBarFillForPercent(v);
  });

  /**
   * Animate the skills items on reveal
   */
  let skillsAnimation = document.querySelectorAll('.skills-animation');
  skillsAnimation.forEach((item) => {
    new Waypoint({
      element: item,
      offset: '80%',
      handler: function(direction) {
        let progress = item.querySelectorAll('.progress .progress-bar');
        progress.forEach(el => {
          el.style.width = el.getAttribute('aria-valuenow') + '%';
        });
      }
    });
  });

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      const cfgEl = swiperElement.querySelector(".swiper-config");
      if (!cfgEl) return;
      let config;
      try {
        config = JSON.parse(cfgEl.innerHTML.trim());
      } catch (err) {
        return;
      }

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Initiate glightbox
   */
  try {
    if (typeof GLightbox === "function") {
      GLightbox({
        selector: ".glightbox"
      });
    }
  } catch (e) {}

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
    const isoContainer = isotopeItem.querySelector('.isotope-container');
    if (!isoContainer) return;

    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
    imagesLoaded(isoContainer, function() {
      initIsotope = new Isotope(isoContainer, {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });
    });

    isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
      filters.addEventListener('click', function() {
        isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
        this.classList.add('filter-active');
        initIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        if (typeof aosInit === 'function') {
          aosInit();
        }
      }, false);
    });

  });

})();