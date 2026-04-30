(function () {
  function bindDeckZoomControls() {
    var el = document.querySelector('.project-deck-swiper');
    if (!el || !el.swiper) return;

    var swiper = el.swiper;
    var zoom = swiper.zoom;
    if (!zoom) return;

    var btnIn = document.getElementById('project-deck-zoom-in');
    var btnOut = document.getElementById('project-deck-zoom-out');
    var btnReset = document.getElementById('project-deck-zoom-reset');

    if (btnIn) {
      btnIn.addEventListener('click', function () {
        zoom.in();
      });
    }
    if (btnOut) {
      btnOut.addEventListener('click', function () {
        zoom.out();
      });
    }
    if (btnReset) {
      btnReset.addEventListener('click', function () {
        var i;
        for (i = 0; i < 12; i++) {
          zoom.out();
        }
        swiper.update();
      });
    }
  }

  window.addEventListener('load', bindDeckZoomControls);
})();
