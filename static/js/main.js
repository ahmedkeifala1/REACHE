/* REACHE Last-Mile — header behaviour, mobile nav, hero word rotator. */
(function () {
  "use strict";

  var header = document.getElementById("siteHeader");
  var navToggle = document.getElementById("navToggle");
  var mainNav = document.getElementById("mainNav");
  var searchToggle = document.getElementById("searchToggle");
  var searchBar = document.getElementById("searchBar");

  /* Solid header once the hero has scrolled past. */
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-solid", window.scrollY > 60);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile menu. */
  if (navToggle && mainNav) {
    navToggle.addEventListener("click", function () {
      var open = mainNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
  }

  /* On touch layouts the first tap on a parent opens its submenu. */
  function isMobile() {
    return window.matchMedia("(max-width: 980px)").matches;
  }
  Array.prototype.forEach.call(
    document.querySelectorAll(".has-children > a"),
    function (link) {
      link.addEventListener("click", function (event) {
        if (!isMobile()) return;
        var sub = link.parentNode.querySelector(".sub-menu");
        if (sub && !sub.classList.contains("is-open")) {
          event.preventDefault();
          sub.classList.add("is-open");
        }
      });
    }
  );

  /* Search bar toggle. */
  if (searchToggle && searchBar) {
    searchToggle.addEventListener("click", function () {
      searchBar.classList.toggle("is-open");
      var input = searchBar.querySelector("input");
      if (searchBar.classList.contains("is-open") && input) input.focus();
    });
  }

  /* Hero headline word rotator. */
  var rotator = document.getElementById("heroRotator");
  if (rotator) {
    var words = (rotator.getAttribute("data-words") || "")
      .split(",")
      .map(function (w) {
        return w.trim();
      })
      .filter(Boolean);

    if (words.length > 1) {
      var index = 0;
      rotator.style.transition = "opacity .35s ease";
      setInterval(function () {
        rotator.style.opacity = "0";
        setTimeout(function () {
          index = (index + 1) % words.length;
          rotator.textContent = words[index];
          rotator.style.opacity = "1";
        }, 350);
      }, 3200);
    }
  }

  /* Count up the impact figures when the stat band comes into view. */
  var statBand = document.querySelector(".stats");
  if (statBand && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          observer.unobserve(entry.target);
          Array.prototype.forEach.call(
            entry.target.querySelectorAll(".stat__value"),
            countUp
          );
        });
      },
      { threshold: 0.35 }
    );
    observer.observe(statBand);
  }

  function countUp(el) {
    var raw = el.textContent.trim();

    /* Only a figure that is one run of digits, optionally wrapped in symbols,
       can be counted up: "6,800" and "$1" animate, but "4.5M", "354→300"
       and "70–80%" have two runs and would be rebuilt as nonsense, so they
       are left as the editor typed them. */
    if (!/^[^0-9]*[0-9][0-9,]*[^0-9]*$/.test(raw)) return;

    var digits = raw.replace(/[^0-9]/g, "");
    if (!digits) return;

    var target = parseInt(digits, 10);
    var prefix = raw.slice(0, raw.search(/[0-9]/));
    var suffix = raw.slice(raw.lastIndexOf(digits.slice(-1)) + 1);
    var start = null;
    var duration = 1600;

    function step(timestamp) {
      if (start === null) start = timestamp;
      var progress = Math.min((timestamp - start) / duration, 1);
      // Ease-out so the number settles rather than stopping abruptly.
      var eased = 1 - Math.pow(1 - progress, 3);
      var value = Math.round(target * eased);
      el.textContent = prefix + value.toLocaleString("en-US") + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
})();
