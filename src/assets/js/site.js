// Menu toggle and the gallery lightbox. Everything works without this file;
// it only adds the small-screen menu and an in-page viewer for the parts.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var links = Array.prototype.slice.call(document.querySelectorAll('.bench a[data-full]'));
  if (!links.length || typeof HTMLDialogElement === 'undefined') return;

  var dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.innerHTML =
    '<figure><img alt=""><figcaption><span class="lightbox-caption"></span>' +
    '<span><button type="button" data-step="-1" aria-label="Previous part">Previous</button> ' +
    '<button type="button" data-step="1" aria-label="Next part">Next</button> ' +
    '<button type="button" data-close aria-label="Close">Close</button></span></figcaption></figure>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector('img');
  var cap = dlg.querySelector('.lightbox-caption');
  var current = 0;

  function show(i) {
    current = (i + links.length) % links.length;
    var a = links[current];
    img.src = a.getAttribute('data-full');
    img.alt = a.querySelector('img').alt;
    cap.textContent = a.getAttribute('data-caption') || '';
  }

  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      show(i);
      dlg.showModal();
    });
  });
  dlg.addEventListener('click', function (e) {
    var step = e.target.getAttribute && e.target.getAttribute('data-step');
    if (step) show(current + Number(step));
    else if (e.target.hasAttribute && e.target.hasAttribute('data-close')) dlg.close();
    else if (e.target === dlg) dlg.close();
  });
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') show(current + 1);
    if (e.key === 'ArrowLeft') show(current - 1);
  });
})();
