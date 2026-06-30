/* booking.js — session builder, live total, and secure Stripe checkout
   ---------------------------------------------------------------------
   HOW PAYMENT WORKS (read CONFIG below):
   1) Preferred: a serverless function creates a Stripe Checkout Session and
      returns { url }. Set CONFIG.checkoutEndpoint to that function's URL.
      (Deploy /api/create-checkout-session.js to Vercel or Cloudflare — see
       README-DEPLOY.md.) Card data NEVER touches this site.
   2) No backend yet? Leave checkoutEndpoint empty. The form will still work
      and will email the request to Brittany so no booking is lost.
   --------------------------------------------------------------------- */
(function () {
  "use strict";

  var CONFIG = {
    // e.g. "https://beconing-arts.vercel.app/api/create-checkout-session"
    checkoutEndpoint: "",          // ← paste your deployed function URL to go live
    fallbackEmail: "hello@beconingarts.com",
    currency: "usd",
    firstVisitDiscount: 20,
    aromaPrice: 15
  };

  var form = document.getElementById("bookForm");
  if (!form) return;

  var svc = document.getElementById("svc");
  var aroma = document.getElementById("addAroma");
  var firstVisit = document.getElementById("firstVisit");
  var totalEl = document.getElementById("total");
  var summaryBody = document.getElementById("summaryBody");
  var msg = document.getElementById("bookMsg");
  var payBtn = document.getElementById("payBtn");

  function parseSvc() {
    if (!svc.value) return null;
    var p = svc.value.split("|"); // "Name|minutes|price"
    return { name: p[0], minutes: +p[1], price: +p[2] };
  }

  function computeTotal() {
    var s = parseSvc();
    var base = s ? s.price : 0;
    var add = aroma.checked ? CONFIG.aromaPrice : 0;
    var disc = (firstVisit.checked && base > 0) ? CONFIG.firstVisitDiscount : 0;
    return Math.max(0, base + add - disc);
  }

  function money(n) { return "$" + n.toFixed(0); }

  function render() {
    var s = parseSvc();
    var total = computeTotal();
    totalEl.textContent = money(total);

    if (!s) {
      summaryBody.innerHTML = '<p class="muted">Nothing selected yet — pick a service to begin.</p>';
      return;
    }
    var rows = '<p class="line"><span>' + s.name + ' · ' + s.minutes + ' min</span><span>' + money(s.price) + '</span></p>';
    if (aroma.checked) rows += '<p class="line"><span>Aromatherapy add-on</span><span>+' + money(CONFIG.aromaPrice) + '</span></p>';
    if (firstVisit.checked) rows += '<p class="line"><span>First-visit discount</span><span>−' + money(CONFIG.firstVisitDiscount) + '</span></p>';
    var d = document.getElementById("date").value;
    var t = document.getElementById("time").value;
    if (d || t) rows += '<p class="line"><span>When</span><span>' + (d || "—") + ' ' + (t || "") + '</span></p>';
    rows += '<p class="line" style="border-top:1px solid rgba(250,247,241,.25);margin-top:.5rem;padding-top:.5rem"><span><strong>Total</strong></span><span><strong>' + money(total) + '</strong></span></p>';
    summaryBody.innerHTML = rows;
  }

  ["change", "input"].forEach(function (ev) { form.addEventListener(ev, render); });
  // sensible date floor = today
  var dateInput = document.getElementById("date");
  if (dateInput) dateInput.min = new Date().toISOString().split("T")[0];
  render();

  function setMsg(text, kind) {
    msg.textContent = text;
    msg.className = "book__msg" + (kind ? " is-" + kind : "");
  }

  function payload() {
    var s = parseSvc();
    return {
      service: s ? s.name : "",
      minutes: s ? s.minutes : 0,
      basePrice: s ? s.price : 0,
      aromatherapy: aroma.checked,
      firstVisit: firstVisit.checked,
      amount: computeTotal(),                 // dollars
      amountCents: Math.round(computeTotal() * 100),
      currency: CONFIG.currency,
      date: document.getElementById("date").value,
      time: document.getElementById("time").value,
      name: document.getElementById("name").value.trim(),
      email: document.getElementById("email").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      notes: document.getElementById("notes").value.trim()
    };
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var data = payload();
    if (!data.service) { setMsg("Please choose a service.", "error"); return; }

    if (CONFIG.checkoutEndpoint) {
      // ---- LIVE PATH: Stripe Checkout via serverless function ----
      payBtn.disabled = true;
      setMsg("Securing your session…");
      fetch(CONFIG.checkoutEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res && res.url) { window.location.href = res.url; }
          else { throw new Error(res && res.error ? res.error : "No checkout URL returned"); }
        })
        .catch(function (err) {
          payBtn.disabled = false;
          setMsg("Couldn't start checkout (" + err.message + "). Try again or email " + CONFIG.fallbackEmail + ".", "error");
        });
    } else {
      // ---- FALLBACK: no backend configured yet → email the request ----
      var subject = encodeURIComponent("Booking request — " + data.service + " (" + data.minutes + " min)");
      var body = encodeURIComponent(
        "New booking request from the website\n\n" +
        "Service: " + data.service + " — " + data.minutes + " min\n" +
        "Aromatherapy: " + (data.aromatherapy ? "yes (+$15)" : "no") + "\n" +
        "First visit: " + (data.firstVisit ? "yes (−$20)" : "no") + "\n" +
        "Estimated total: $" + data.amount + "\n" +
        "Preferred: " + data.date + " " + data.time + "\n\n" +
        "Name: " + data.name + "\nEmail: " + data.email + "\nPhone: " + data.phone + "\n\n" +
        "Notes: " + data.notes + "\n"
      );
      window.location.href = "mailto:" + CONFIG.fallbackEmail + "?subject=" + subject + "&body=" + body;
      setMsg("Opening your email to send the request — Brittany will confirm your time & payment. (Live card checkout activates once Stripe is connected.)", "ok");
    }
  });
})();
