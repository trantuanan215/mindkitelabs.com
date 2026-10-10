// Google Ads tag with Consent Mode v2 and a cookie banner.
// Nothing loads and no banner shows until ADS_ID is filled in, so the site stays tracking-free by default.
(function () {
  var ADS_ID = "";              // e.g. "AW-123456789" from Google Ads → Goals → Conversions → Tag setup
  var CONTACT_LABEL = "";       // conversion label for "contact email click", e.g. "AbCdEfGhIj"
  var STORE_KEY = "mk-consent"; // "granted" | "denied"
  if (!ADS_ID) return;

  var TEXT = {
    vi: { msg: "Chúng tôi dùng cookie quảng cáo của Google để đo hiệu quả quảng cáo, chỉ khi bạn đồng ý.", ok: "Đồng ý", no: "Từ chối", more: "Chi tiết", link: "Cài đặt cookie", policy: "/privacy.html" },
    en: { msg: "We use Google advertising cookies to measure ad performance, only with your consent.", ok: "Accept", no: "Decline", more: "Details", link: "Cookie settings", policy: "/en/privacy.html" },
    th: { msg: "เราใช้คุกกี้โฆษณาของ Google เพื่อวัดผลโฆษณา เฉพาะเมื่อคุณยินยอมเท่านั้น", ok: "ยอมรับ", no: "ปฏิเสธ", more: "รายละเอียด", link: "ตั้งค่าคุกกี้", policy: "/en/privacy.html" }
  };
  var t = TEXT[document.documentElement.lang] || TEXT.en;

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied", wait_for_update: 500 });
  gtag("set", "ads_data_redaction", true);

  function read() { try { return localStorage.getItem(STORE_KEY); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem(STORE_KEY, v); } catch (e) {} }
  function apply(v) {
    var g = v === "granted" ? "granted" : "denied";
    gtag("consent", "update", { ad_storage: g, ad_user_data: g, ad_personalization: g });
  }
  var choice = read();
  if (choice) apply(choice);

  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + ADS_ID;
  document.head.appendChild(s);
  gtag("js", new Date());
  gtag("config", ADS_ID);

  // Conversion: visitor clicks any contact email link
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="mailto:"]');
    if (a && CONTACT_LABEL) gtag("event", "conversion", { send_to: ADS_ID + "/" + CONTACT_LABEL });
  });

  function banner() {
    if (document.querySelector(".consent")) return;
    var box = document.createElement("div");
    box.className = "consent";
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", t.link);
    box.innerHTML = '<p>' + t.msg + ' <a href="' + t.policy + '">' + t.more + '</a></p>' +
      '<div class="consent-actions"><button type="button" class="btn btn-ghost" data-v="denied">' + t.no + '</button>' +
      '<button type="button" class="btn btn-primary" data-v="granted">' + t.ok + '</button></div>';
    box.addEventListener("click", function (e) {
      var v = e.target.getAttribute && e.target.getAttribute("data-v");
      if (!v) return;
      save(v); apply(v); box.remove();
    });
    document.body.appendChild(box);
  }

  function footerLink() {
    var note = document.querySelector(".footer-note");
    if (!note) return;
    var a = document.createElement("button");
    a.type = "button";
    a.className = "consent-link";
    a.textContent = t.link;
    a.addEventListener("click", banner);
    note.appendChild(document.createTextNode(" · "));
    note.appendChild(a);
  }

  function init() { footerLink(); if (!choice) banner(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
