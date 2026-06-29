/* main.js — flagship interaction engine
   nav · reveals · parallax · cursor glow · embers · chakra-scroll · image swap */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- sticky nav ---- */
  var nav = document.getElementById("nav");
  function navState(){ if (nav) nav.classList.toggle("is-scrolled", window.scrollY > 30); }
  navState();

  /* ---- mobile menu ---- */
  var toggle = document.getElementById("navToggle"), menu = document.getElementById("mobileMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open)); menu.hidden = open;
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { toggle.setAttribute("aria-expanded","false"); menu.hidden = true; });
    });
  }

  /* ---- reveal on scroll ---- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add("is-in"); }); }

  /* ---- year ---- */
  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();

  /* ---- cursor glow ---- */
  var glow = document.getElementById("cursorGlow");
  if (glow && !reduce && window.matchMedia("(pointer:fine)").matches) {
    var gx = innerWidth/2, gy = innerHeight/2, cx = gx, cy = gy;
    window.addEventListener("mousemove", function (e) { gx = e.clientX; gy = e.clientY; glow.style.opacity = 1; });
    (function loop(){ cx += (gx-cx)*.12; cy += (gy-cy)*.12;
      glow.style.transform = "translate(" + cx + "px," + cy + "px) translate(-50%,-50%)";
      requestAnimationFrame(loop); })();
  }

  /* ---- parallax (skip centered/spinning art) ---- */
  var pEls = [].slice.call(document.querySelectorAll("[data-speed]")).filter(function (el) {
    return !/mandala|fol|sigil/.test(el.className);
  });
  function parallax(){
    var vh = innerHeight;
    pEls.forEach(function (el) {
      var r = el.getBoundingClientRect(), mid = r.top + r.height/2;
      var off = (mid - vh/2) * (parseFloat(el.dataset.speed) || 0) * -1;
      var mir = el.classList.contains("bamboo--r") ? "scaleX(-1) " : "";
      el.style.transform = mir + "translate3d(0," + off.toFixed(1) + "px,0)";
    });
  }

  /* ---- chakra scroll: progress + sequential lighting ---- */
  var chakra = document.getElementById("chakra");
  var prog = document.getElementById("chakraProgress");
  var rows = chakra ? [].slice.call(chakra.querySelectorAll(".chakra__row")) : [];
  function chakraScroll(){
    if (!chakra) return;
    var r = chakra.getBoundingClientRect(), vh = innerHeight;
    // 0 when top reaches 80% vh, 1 when bottom passes 30% vh
    var p = (vh*0.82 - r.top) / (r.height * 0.85);
    p = Math.max(0, Math.min(1, p));
    if (prog) prog.style.height = (p*100).toFixed(1) + "%";
    var lit = Math.round(p * rows.length);
    rows.forEach(function (row, i){ row.classList.toggle("lit", i < lit); });
  }

  var ticking = false;
  function onScroll(){ navState(); if (!ticking){ requestAnimationFrame(function(){ if(!reduce) parallax(); chakraScroll(); ticking=false; }); ticking=true; } }
  window.addEventListener("scroll", onScroll, { passive:true });
  window.addEventListener("resize", function(){ if(!reduce) parallax(); chakraScroll(); }, { passive:true });
  if (!reduce) parallax(); chakraScroll();

  /* ---- drifting embers (gold motes) ---- */
  var cv = document.getElementById("embers");
  if (cv && !reduce) {
    var ctx = cv.getContext("2d"), W, H, motes = [];
    function size(){ W = cv.width = innerWidth; H = cv.height = innerHeight; }
    function seed(){ motes = []; var n = Math.min(46, Math.round(W/30));
      for (var i=0;i<n;i++) motes.push({ x:Math.random()*W, y:Math.random()*H,
        r:Math.random()*1.8+0.4, s:Math.random()*0.35+0.08, d:Math.random()*Math.PI*2, a:Math.random()*0.5+0.15 }); }
    size(); seed(); addEventListener("resize", function(){ size(); seed(); }, {passive:true});
    (function draw(){
      ctx.clearRect(0,0,W,H);
      for (var i=0;i<motes.length;i++){ var m=motes[i];
        m.y -= m.s; m.x += Math.sin(m.d += 0.01)*0.3;
        if (m.y < -10){ m.y = H+10; m.x = Math.random()*W; }
        ctx.beginPath(); ctx.arc(m.x,m.y,m.r,0,6.283);
        ctx.fillStyle = "rgba(201,162,75," + m.a + ")"; ctx.shadowBlur = 8; ctx.shadowColor = "rgba(201,162,75,.6)";
        ctx.fill();
      }
      requestAnimationFrame(draw);
    })();
  }

  /* ---- image auto-swap (drop files in assets/img/) ---- */
  var IMG_MAP = {
    "Brittany — portrait (warm, low light)": "assets/img/portrait.jpg",
    "Treatment room / warm linens / candlelight": "assets/img/room.jpg",
    "Hands / warm stones / oil": "assets/img/detail.jpg",
    "gallery-1.jpg":"assets/img/gallery-1.jpg","gallery-2.jpg":"assets/img/gallery-2.jpg",
    "gallery-3.jpg":"assets/img/gallery-3.jpg","gallery-4.jpg":"assets/img/gallery-4.jpg",
    "gallery-5.jpg":"assets/img/gallery-5.jpg","gallery-6.jpg":"assets/img/gallery-6.jpg",
    "Photo of the space or a map": "assets/img/space.jpg"
  };
  document.querySelectorAll(".ph[data-swap]").forEach(function (ph) {
    var src = IMG_MAP[ph.getAttribute("data-swap")]; if (!src) return;
    var probe = new Image();
    probe.onload = function(){ ph.style.backgroundImage = "url('"+src+"')"; ph.classList.add("has-img"); };
    probe.src = src;
  });
})();
