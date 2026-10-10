// Progressive enhancement only: the page is fully readable without this script.
(function () {
  var root = document.documentElement;
  root.classList.remove("no-js");
  root.classList.add("js");

  // Header border once the page scrolls
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Process tabs (WAI-ARIA tabs pattern with arrow-key navigation)
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".step-tab"));
  var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });

  function select(index, focus) {
    tabs.forEach(function (tab, i) {
      var active = i === index;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
      if (panels[i]) panels[i].hidden = !active;
    });
    if (focus) tabs[index].focus({ preventScroll: true });
    // Scroll only the tab strip horizontally; scrollIntoView would also jump the page vertically
    var strip = tabs[index].parentElement;
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    strip.scrollTo({ left: tabs[index].offsetLeft - 16, behavior: reduce ? "auto" : "smooth" });
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener("click", function () { select(i, false); });
    tab.addEventListener("keydown", function (e) {
      var next = null;
      if (e.key === "ArrowRight") next = (i + 1) % tabs.length;
      if (e.key === "ArrowLeft") next = (i - 1 + tabs.length) % tabs.length;
      if (e.key === "Home") next = 0;
      if (e.key === "End") next = tabs.length - 1;
      if (next !== null) { e.preventDefault(); select(next, true); }
    });
  });
  if (tabs.length) select(0, false);
  root.classList.add("tabs-ready");

  // "Back to step 01" link inside the last panel
  var restart = document.querySelector("[data-restart]");
  if (restart) restart.addEventListener("click", function (e) { e.preventDefault(); select(0, true); });

  // Scroll reveal
  var items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { entry.target.classList.add("in"); io.unobserve(entry.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px" });
  items.forEach(function (el) { io.observe(el); });
})();
