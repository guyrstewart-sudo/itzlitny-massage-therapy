#!/usr/bin/env python3
"""
Build the itz_litny massage therapy brand portfolio book (PDF).

Renders an HTML/CSS document to PDF with WeasyPrint, using locally embedded
Google Fonts (Cormorant Garamond, Nunito Sans, Marcellus) shipped in ./fonts.

Usage:
    python3 build_portfolio.py

Output:
    itz_litny-brand-portfolio.pdf  (next to this script)
"""
import base64
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
FONT_DIR = HERE / "fonts"
OUT_PDF = HERE / "itz_litny-brand-portfolio.pdf"
HTML_OUT = HERE / "itz_litny-brand-portfolio.html"

# ---------------------------------------------------------------------------
# Brand system
# ---------------------------------------------------------------------------
PALETTE = {
    "oat":      "#FAF7F1",  # Oat Milk      - canvas
    "sand":     "#EFE7D9",  # Warm Sand     - surface
    "sage":     "#7C8B6F",  # Sage          - primary
    "euc":      "#5E6B53",  # Eucalyptus    - primary deep
    "clay":     "#BE8163",  # Clay          - warmth accent
    "teal":     "#8FB0A9",  # Healing Teal  - calm / water accent
    "ink":      "#34382F",  # Forest Ink    - text
    "stone":    "#8A8A7C",  # Stone         - muted text
}


def font_face(family, file, weight, style="normal"):
    """Embed a woff2 font file as a base64 @font-face rule."""
    p = FONT_DIR / file
    data = base64.b64encode(p.read_bytes()).decode("ascii")
    return (
        "@font-face{"
        f"font-family:'{family}';font-style:{style};font-weight:{weight};"
        f"font-display:swap;"
        f"src:url(data:font/woff2;base64,{data}) format('woff2');"
        "}"
    )


def build_font_css():
    faces = [
        ("Cormorant Garamond", "cormorant-garamond-latin-300-normal.woff2", 300),
        ("Cormorant Garamond", "cormorant-garamond-latin-400-normal.woff2", 400),
        ("Cormorant Garamond", "cormorant-garamond-latin-500-normal.woff2", 500),
        ("Cormorant Garamond", "cormorant-garamond-latin-600-normal.woff2", 600),
        ("Cormorant Garamond", "cormorant-garamond-latin-700-normal.woff2", 700),
        ("Cormorant Garamond", "cormorant-garamond-latin-400-italic.woff2", 400, "italic"),
        ("Cormorant Garamond", "cormorant-garamond-latin-500-italic.woff2", 500, "italic"),
        ("Cormorant Garamond", "cormorant-garamond-latin-600-italic.woff2", 600, "italic"),
        ("Nunito Sans", "nunito-sans-latin-300-normal.woff2", 300),
        ("Nunito Sans", "nunito-sans-latin-400-normal.woff2", 400),
        ("Nunito Sans", "nunito-sans-latin-400-italic.woff2", 400, "italic"),
        ("Nunito Sans", "nunito-sans-latin-600-normal.woff2", 600),
        ("Nunito Sans", "nunito-sans-latin-700-normal.woff2", 700),
        ("Nunito Sans", "nunito-sans-latin-800-normal.woff2", 800),
        ("Marcellus", "marcellus-latin-400-normal.woff2", 400),
    ]
    return "\n".join(font_face(*f) for f in faces)


# ---------------------------------------------------------------------------
# SVG building blocks
# ---------------------------------------------------------------------------
def logo_mark(color, size=120, stroke=2.2):
    """Monoline leaf / lotus that also reads as a water droplet (Aquarius).

    A single teardrop outline with an interior leaf vein/lotus curve.
    """
    return f'''<svg viewBox="0 0 100 130" width="{size}" height="{size*1.3:.0f}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="itz_litny logo">
  <!-- droplet / lotus petal outline -->
  <path d="M50 8 C50 8 84 52 84 84 a34 34 0 0 1 -68 0 C16 52 50 8 50 8 Z"
        stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- central leaf vein -->
  <path d="M50 36 C50 60 50 78 50 104" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"/>
  <!-- left frond -->
  <path d="M50 62 C40 64 33 70 31 80" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"/>
  <!-- right frond -->
  <path d="M50 62 C60 64 67 70 69 80" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"/>
  <!-- upper left frond -->
  <path d="M50 48 C43 50 38 55 36 62" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"/>
  <!-- upper right frond -->
  <path d="M50 48 C57 50 62 55 64 62" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"/>
</svg>'''


def aquarius_glyph(color, size=46, sw=2.0):
    """The Aquarius water-bearer waves ♒ drawn as two stacked wavy lines."""
    return f'''<svg viewBox="0 0 80 40" width="{size}" height="{size/2:.0f}" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M6 14 q8 -10 16 0 t16 0 t16 0 t16 0" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>
  <path d="M6 26 q8 -10 16 0 t16 0 t16 0 t16 0" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>
</svg>'''


def organic_blob(color, opacity=1.0, seed=0):
    """A soft organic blob shape used as background ornament."""
    paths = [
        "M44 -57 C58 -45 67 -29 70 -11 C73 7 70 26 59 39 C48 52 30 59 12 62 C-7 65 -27 64 -42 53 C-57 42 -67 21 -66 1 C-65 -19 -53 -38 -38 -50 C-23 -62 -5 -67 12 -67 C25 -67 33 -65 44 -57 Z",
        "M48 -52 C62 -40 70 -20 69 -1 C68 18 58 37 43 49 C28 61 8 66 -11 64 C-30 62 -48 53 -59 38 C-70 23 -74 2 -68 -16 C-62 -34 -46 -49 -28 -57 C-10 -65 10 -66 27 -62 C36 -60 42 -57 48 -52 Z",
        "M42 -55 C57 -46 70 -33 73 -16 C76 1 69 20 57 34 C45 48 28 57 9 61 C-10 65 -31 64 -45 52 C-59 40 -66 18 -63 -2 C-60 -22 -47 -41 -30 -51 C-13 -61 7 -62 23 -61 C31 -60 36 -59 42 -55 Z",
    ]
    d = paths[seed % len(paths)]
    return f'''<svg viewBox="-90 -90 180 180" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%">
  <path d="{d}" fill="{color}" opacity="{opacity}"/>
</svg>'''


def leaf_line(color, sw=1.6, size=60):
    """Small decorative monoline sprig used as a divider accent."""
    return f'''<svg viewBox="0 0 120 40" width="{size*2}" height="{int(size*0.66)}" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M4 20 H116" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity="0.5"/>
  <path d="M60 20 C56 10 50 6 42 6 C50 10 54 16 56 20 C54 24 50 30 42 34 C50 34 56 30 60 20 Z" fill="{color}" opacity="0.85"/>
  <circle cx="60" cy="20" r="2.2" fill="{color}"/>
</svg>'''


# ---------------------------------------------------------------------------
# Page helpers
# ---------------------------------------------------------------------------
def footer(page_no, label):
    return f'''<div class="footer">
      <span class="f-mark">itz_litny</span>
      <span class="f-label">{label}</span>
      <span class="f-no">{page_no:02d}</span>
    </div>'''


def kicker(text):
    return f'<div class="kicker">{text}</div>'


def swatch(name, hexv, role, dark_text=False):
    tc = "ink" if dark_text else "oat"
    return f'''<div class="swatch">
      <div class="swatch-chip" style="background:{hexv}">
        <span class="swatch-hex" style="color:{'#34382F' if dark_text else '#FAF7F1'}">{hexv}</span>
      </div>
      <div class="swatch-meta">
        <div class="swatch-name">{name}</div>
        <div class="swatch-role">{role}</div>
      </div>
    </div>'''


P = PALETTE

# ===========================================================================
# PAGES
# ===========================================================================
pages = []

# --- 01 COVER ---------------------------------------------------------------
pages.append(f'''
<section class="page cover">
  <div class="cover-blob blob-1">{organic_blob(P["sage"], 0.16, 1)}</div>
  <div class="cover-blob blob-2">{organic_blob(P["teal"], 0.18, 2)}</div>
  <div class="cover-blob blob-3">{organic_blob(P["clay"], 0.12, 0)}</div>
  <div class="cover-inner">
    <div class="cover-logo">{logo_mark(P["euc"], 132)}</div>
    <div class="cover-wordmark">itz_litny</div>
    <div class="cover-desc">massage&nbsp;therapy</div>
    <div class="cover-rule"></div>
    <h1 class="cover-tag">Come home<br>to your body.</h1>
    <div class="cover-sub">where an artist&rsquo;s eye meets healing hands</div>
  </div>
  <div class="cover-foot">
    <span>Brand Portfolio</span>
    <span class="dot">&bull;</span>
    <span>Brittany &mdash; Massage Therapist</span>
    <span class="dot">&bull;</span>
    <span>Vol. 01</span>
  </div>
</section>
''')

# --- 02 WELCOME / BRAND STORY ----------------------------------------------
pages.append(f'''
<section class="page">
  <div class="page-pad">
    {kicker("01 &nbsp;/&nbsp; Welcome")}
    <h2 class="h-display">An artist&rsquo;s eye,<br><span class="italic">healing hands.</span></h2>
    <div class="two-col">
      <div class="col-main">
        <p class="lead">You&rsquo;re safe here. Let&rsquo;s slow down together.</p>
        <p>itz_litny began the way most good things do &mdash; quietly, and from the inside out. Brittany is a newly-credentialed massage therapist who came to bodywork already fluent in another language: color, intuition, and the slow craft of making something with her hands.</p>
        <p>That artist&rsquo;s sensibility is the whole point. She reads a body the way a painter reads a canvas &mdash; noticing where the light gathers, where the tension lives, what wants to soften next. The result is bodywork that feels composed rather than clinical: unhurried, attentive, and entirely yours.</p>
        <p>This book holds the brand that grew from that practice &mdash; the words, the colors, and the feeling we return to every time. A genuine safe space, translated into a system.</p>
      </div>
      <div class="col-side">
        <div class="story-card">
          <div class="story-blob">{organic_blob(P["teal"], 0.9, 1)}</div>
          <div class="story-quote">&ldquo;Healing doesn&rsquo;t have to be earned &mdash; it&rsquo;s already yours.&rdquo;</div>
        </div>
        <div class="side-fact">
          <div class="fact-k">The feeling</div>
          <div class="fact-v">Natural &middot; organic &middot; holistic. Calm, nurturing, meditative.</div>
        </div>
        <div class="side-fact">
          <div class="fact-k">The promise</div>
          <div class="fact-v">Sixty minutes that belong entirely to you.</div>
        </div>
      </div>
    </div>
  </div>
  {footer(2, "Welcome")}
</section>
''')

# --- 03 MISSION & VALUES ----------------------------------------------------
def value_card(num, title, body, color):
    return f'''<div class="value-card">
      <div class="value-num" style="color:{color}">{num}</div>
      <div class="value-title">{title}</div>
      <div class="value-body">{body}</div>
    </div>'''

pages.append(f'''
<section class="page page-sand">
  <div class="page-pad">
    {kicker("02 &nbsp;/&nbsp; Mission &amp; Values")}
    <h2 class="h-display">Why we<br><span class="italic">do this.</span></h2>
    <div class="mission-band">
      <div class="mission-leaf">{leaf_line(P["clay"], 1.6, 54)}</div>
      <p class="mission-text">To offer a genuine safe space where rest is not a reward but a return &mdash;
      bodywork that helps you come home to your body, exactly as it is today.</p>
    </div>
    <div class="values-grid">
      {value_card("01", "Safety first", "The room, the touch, the pace &mdash; all built so your nervous system can finally exhale.", P["sage"])}
      {value_card("02", "Unhurried care", "Time is the medicine. We never rush a body toward someone else&rsquo;s clock.", P["clay"])}
      {value_card("03", "An artist&rsquo;s attention", "Intuition and craft. We read what&rsquo;s there and respond, rather than apply a script.", P["teal"])}
      {value_card("04", "Self-love, embodied", "Healing as something already yours &mdash; not earned, not performed, just received.", P["euc"])}
    </div>
  </div>
  {footer(3, "Mission &amp; Values")}
</section>
''')

# --- 04 WHO SHE SERVES ------------------------------------------------------
def audience_card(title, body, color):
    return f'''<div class="aud-card">
      <div class="aud-dot" style="background:{color}"></div>
      <div class="aud-title">{title}</div>
      <div class="aud-body">{body}</div>
    </div>'''

pages.append(f'''
<section class="page">
  <div class="page-pad">
    {kicker("03 &nbsp;/&nbsp; Who She Serves")}
    <h2 class="h-display">For the ones<br><span class="italic">ready to soften.</span></h2>
    <p class="section-intro">itz_litny is for people who suspect that rest is allowed &mdash; and want a practitioner who treats it that way. Different bodies, one shared wish: to feel at home again.</p>
    <div class="aud-grid">
      {audience_card("The over-carried", "Caregivers, parents, and the quietly depleted who give all day and rarely receive. Here, you&rsquo;re the one being held.", P["sage"])}
      {audience_card("The reawakening", "Anyone reconnecting with their body after stress, burnout, or a long stretch of just getting through. We start gently.", P["teal"])}
      {audience_card("The expecting", "Prenatal clients who want supported, knowledgeable, deeply comfortable care through a changing body.", P["clay"])}
      {audience_card("The seekers", "Wellness-minded folks drawn to natural, holistic, intuitive care &mdash; and to a space that feels like art, not a clinic.", P["euc"])}
    </div>
    <div class="aud-foot">
      <div class="aud-foot-blob">{organic_blob(P["sand"], 1, 2)}</div>
      <div class="aud-foot-text"><span class="italic">&ldquo;Whoever you are when you walk in, you&rsquo;re welcome to set it all down.&rdquo;</span></div>
    </div>
  </div>
  {footer(4, "Who She Serves")}
</section>
''')

# --- 05 BRAND PERSONALITY / VOICE ------------------------------------------
def slider(label, left, right, pos):
    return f'''<div class="slider-row">
      <span class="slider-left">{left}</span>
      <div class="slider-track"><span class="slider-knob" style="left:{pos}%"></span></div>
      <span class="slider-right">{right}</span>
    </div>'''

pages.append(f'''
<section class="page page-sand">
  <div class="page-pad">
    {kicker("04 &nbsp;/&nbsp; Personality &amp; Voice")}
    <h2 class="h-display">How we<br><span class="italic">sound.</span></h2>
    <p class="section-intro">Warm, grounded, unhurried, affirming. Always second person, present tense. Embodied, sensory language &mdash; never clinical, never salesy.</p>

    <div class="voice-cols">
      <div class="voice-sliders">
        <div class="mini-h">Personality dials</div>
        {slider("", "Clinical", "Nurturing", 84)}
        {slider("", "Trendy", "Timeless", 78)}
        {slider("", "Loud", "Calm", 88)}
        {slider("", "Formal", "Warm", 80)}
        {slider("", "Performative", "Sincere", 86)}
      </div>
      <div class="voice-words">
        <div class="mini-h">We are</div>
        <div class="chips">
          <span class="chip">warm</span><span class="chip">grounded</span><span class="chip">unhurried</span>
          <span class="chip">affirming</span><span class="chip">sensory</span><span class="chip">safe</span>
          <span class="chip">intuitive</span><span class="chip">soft</span>
        </div>
      </div>
    </div>

    <div class="dodont">
      <div class="do-col">
        <div class="dd-head dd-do">Do</div>
        <ul>
          <li>&ldquo;You&rsquo;re safe here. Let&rsquo;s slow down together.&rdquo;</li>
          <li>&ldquo;Sixty minutes that belong entirely to you.&rdquo;</li>
          <li>Speak <em>to</em> the person, in the present: <em>you feel, you rest, you arrive.</em></li>
          <li>Use the body and the senses &mdash; breath, warmth, weight, ease.</li>
        </ul>
      </div>
      <div class="dont-col">
        <div class="dd-head dd-dont">Don&rsquo;t</div>
        <ul>
          <li>&ldquo;Book now &mdash; limited slots, don&rsquo;t miss out!&rdquo;</li>
          <li>&ldquo;Our modalities target myofascial dysfunction.&rdquo;</li>
          <li>Don&rsquo;t shout, upsell, or manufacture urgency.</li>
          <li>Don&rsquo;t sound clinical, generic, or like everyone else.</li>
        </ul>
      </div>
    </div>
  </div>
  {footer(5, "Personality &amp; Voice")}
</section>
''')

# --- 06 LOGO SYSTEM ---------------------------------------------------------
pages.append(f'''
<section class="page">
  <div class="page-pad">
    {kicker("05 &nbsp;/&nbsp; Logo System")}
    <h2 class="h-display">The mark.</h2>
    <p class="section-intro">A single monoline gesture: an abstract leaf and lotus that doubles as a soft water droplet &mdash; a quiet nod to Brittany&rsquo;s Aquarius nature. Growth and water, in one breath.</p>

    <div class="logo-hero">
      <div class="logo-hero-mark">{logo_mark(P["euc"], 150)}</div>
      <div class="logo-hero-lockup">
        <div class="lh-word">itz_litny</div>
        <div class="lh-desc">massage therapy</div>
      </div>
    </div>

    <div class="logo-grid">
      <div class="logo-tile">
        <div class="lt-vis lt-clear">
          <div class="clear-box">{logo_mark(P["euc"], 70)}</div>
        </div>
        <div class="lt-cap"><strong>Clear space</strong><br>Keep at least the height of the droplet clear on every side.</div>
      </div>
      <div class="logo-tile">
        <div class="lt-vis" style="background:{P['oat']}">{logo_mark(P["ink"], 70)}</div>
        <div class="lt-cap"><strong>Mono &mdash; ink</strong><br>One-color Forest Ink for stamps &amp; fine print.</div>
      </div>
      <div class="logo-tile">
        <div class="lt-vis" style="background:{P['euc']}">{logo_mark(P["oat"], 70)}</div>
        <div class="lt-cap"><strong>Reversed</strong><br>Oat Milk on Eucalyptus for dark surfaces.</div>
      </div>
      <div class="logo-tile">
        <div class="lt-vis" style="background:{P['clay']}">{logo_mark(P["oat"], 70)}</div>
        <div class="lt-cap"><strong>On color</strong><br>Stays legible on warm accent fields.</div>
      </div>
      <div class="logo-tile">
        <div class="lt-vis" style="background:{P['oat']}">
          <div class="favi">{logo_mark(P["euc"], 34)}</div>
        </div>
        <div class="lt-cap"><strong>Favicon</strong><br>Reduces cleanly to 16&nbsp;px.</div>
      </div>
      <div class="logo-tile">
        <div class="lt-vis lt-dont" style="background:{P['oat']}">
          <div class="dont-mark">{logo_mark(P["clay"], 60)}</div>
          <div class="slash"></div>
        </div>
        <div class="lt-cap"><strong>Don&rsquo;t</strong><br>No stretching, recoloring off-palette, or shadows.</div>
      </div>
    </div>
  </div>
  {footer(6, "Logo System")}
</section>
''')

# --- 07 COLOR PALETTE -------------------------------------------------------
pages.append(f'''
<section class="page page-sand">
  <div class="page-pad">
    {kicker("06 &nbsp;/&nbsp; Color")}
    <h2 class="h-display">A palette<br><span class="italic">that breathes.</span></h2>
    <p class="section-intro">Warm neutrals to rest on, sage and eucalyptus to ground, clay for warmth, and a healing teal that carries the water. Lots of Oat Milk between everything.</p>
    <div class="swatch-grid">
      {swatch("Oat Milk", "#FAF7F1", "Canvas", dark_text=True)}
      {swatch("Warm Sand", "#EFE7D9", "Surface", dark_text=True)}
      {swatch("Sage", "#7C8B6F", "Primary")}
      {swatch("Eucalyptus", "#5E6B53", "Primary deep")}
      {swatch("Clay", "#BE8163", "Accent &middot; warmth")}
      {swatch("Healing Teal", "#8FB0A9", "Accent &middot; water &#9810;")}
      {swatch("Forest Ink", "#34382F", "Text")}
      {swatch("Stone", "#8A8A7C", "Muted text")}
    </div>
    <div class="color-notes">
      <div class="cn"><span class="cn-dot" style="background:{P['oat']};border:1px solid #ddd"></span>Lead with Oat Milk &amp; Warm Sand. Let them hold most of the space.</div>
      <div class="cn"><span class="cn-dot" style="background:{P['euc']}"></span>Use Sage / Eucalyptus for structure, headings, and the mark.</div>
      <div class="cn"><span class="cn-dot" style="background:{P['clay']}"></span>Clay &amp; Teal are accents &mdash; small doses, never the whole room.</div>
    </div>
  </div>
  {footer(7, "Color")}
</section>
''')

# --- 08 TYPOGRAPHY ----------------------------------------------------------
pages.append(f'''
<section class="page">
  <div class="page-pad">
    {kicker("07 &nbsp;/&nbsp; Typography")}
    <h2 class="h-display">Type that<br><span class="italic">slows you down.</span></h2>

    <div class="type-spec">
      <div class="ts-left">
        <div class="ts-tag">Display</div>
        <div class="ts-name">Cormorant Garamond</div>
      </div>
      <div class="ts-right">
        <div class="ts-big">Come home<br>to your body.</div>
        <div class="ts-alpha cormorant">Aa Bb Cc Dd Ee Ff Gg &mdash; 1234567890</div>
        <div class="ts-meta">Light&nbsp;300 &middot; Regular&nbsp;400 &middot; Medium&nbsp;500 &middot; SemiBold&nbsp;600 &middot; Italic</div>
      </div>
    </div>

    <div class="type-spec">
      <div class="ts-left">
        <div class="ts-tag">Body &amp; UI</div>
        <div class="ts-name nunito">Nunito Sans</div>
      </div>
      <div class="ts-right">
        <p class="ts-body">Humanist, soft, and highly readable. Nunito Sans carries every word that isn&rsquo;t a headline &mdash; service descriptions, intake notes, captions, and the web. It keeps the brand warm and effortless at small sizes.</p>
        <div class="ts-alpha nunito">Aa Bb Cc Dd Ee Ff Gg &mdash; 1234567890</div>
        <div class="ts-meta">Light&nbsp;300 &middot; Regular&nbsp;400 &middot; SemiBold&nbsp;600 &middot; Bold&nbsp;700 &middot; ExtraBold&nbsp;800</div>
      </div>
    </div>

    <div class="type-spec last">
      <div class="ts-left">
        <div class="ts-tag">Accent</div>
        <div class="ts-name marcellus">Marcellus</div>
      </div>
      <div class="ts-right">
        <div class="ts-accent marcellus">where an artist&rsquo;s eye meets healing hands</div>
        <div class="ts-meta">Taglines &amp; short accents only &mdash; tracked a touch wider.</div>
      </div>
    </div>

    <div class="type-scale">
      <span><b>H1</b> Cormorant 64/1.05</span>
      <span><b>H2</b> Cormorant 40/1.1</span>
      <span><b>Body</b> Nunito 10.5/1.65</span>
      <span><b>Caption</b> Nunito 8/1.5 &middot; tracked</span>
    </div>
  </div>
  {footer(8, "Typography")}
</section>
''')

# --- 09 PHOTOGRAPHY DIRECTION ----------------------------------------------
def photo_tile(label, c1, c2, seed):
    return f'''<div class="photo-tile" style="background:linear-gradient(135deg,{c1},{c2})">
      <div class="pt-blob">{organic_blob(P["oat"], 0.22, seed)}</div>
      <span class="pt-label">{label}</span>
    </div>'''

pages.append(f'''
<section class="page page-sand">
  <div class="page-pad">
    {kicker("08 &nbsp;/&nbsp; Imagery")}
    <h2 class="h-display">Photography<br><span class="italic">direction.</span></h2>
    <p class="section-intro">Soft natural light, warm neutrals, generous negative space. Hands, linen, plants, stones, candlelight, skin texture. Tender and human &mdash; never harsh or clinical. <em>Blocks below are placeholders; Brittany&rsquo;s approved photos drop into the labeled slots.</em></p>
    <div class="photo-grid">
      {photo_tile("hands &amp; linen", P["sand"], P["clay"], 0)}
      {photo_tile("plants &amp; light", P["sage"], P["teal"], 1)}
      {photo_tile("stones &amp; warmth", P["clay"], P["sand"], 2)}
      {photo_tile("candle glow", P["euc"], P["sage"], 1)}
      {photo_tile("skin texture", P["teal"], P["oat"], 0)}
      {photo_tile("the room", P["sand"], P["sage"], 2)}
    </div>
    <div class="photo-rules">
      <div class="pr"><span class="pr-y">Lean in</span> warm light, shallow focus, calm hands, breathing room, real texture.</div>
      <div class="pr"><span class="pr-n">Avoid</span> cool blue tones, clutter, stock-y poses, harsh flash, anything sterile.</div>
    </div>
  </div>
  {footer(9, "Imagery")}
</section>
''')

# --- 10 SERVICE MENU --------------------------------------------------------
def menu_row(name, desc, dur, price):
    return f'''<div class="menu-row">
      <div class="menu-name">{name}<span class="menu-desc">{desc}</span></div>
      <div class="menu-dur">{dur}</div>
      <div class="menu-price">{price}</div>
    </div>'''

pages.append(f'''
<section class="page">
  <div class="page-pad">
    {kicker("09 &nbsp;/&nbsp; Services")}
    <h2 class="h-display">The menu.</h2>
    <p class="section-intro">Choose by feeling, not jargon. Every session is tailored once you&rsquo;re on the table. <em>Pricing is placeholder &mdash; Brittany sets final rates.</em></p>
    <div class="menu">
      {menu_row("Relaxation", "Classic Swedish &mdash; long, soothing, full-body ease.", "60 / 90 min", "$75 / $110")}
      {menu_row("Therapeutic / Custom", "Built around what your body asks for that day.", "60 / 90 min", "$85 / $120")}
      {menu_row("Deep Tissue", "Slow, focused pressure for held-on tension.", "60 / 90 min", "$90 / $125")}
      {menu_row("Prenatal", "Supported, gentle care for a changing body.", "60 min", "$85")}
      {menu_row("Hot Stone", "Warm stones melt you open from the outside in.", "75 min", "$115")}
    </div>
    <div class="menu-extras">
      <div class="extra">
        <div class="extra-k">Aromatherapy add-on</div>
        <div class="extra-v">+ $15</div>
      </div>
      <div class="extra extra-clay">
        <div class="extra-k">First-visit intro</div>
        <div class="extra-v">$20 off</div>
      </div>
    </div>
    <div class="menu-foot italic">&ldquo;Whichever you choose, the hour is yours to set everything down.&rdquo;</div>
  </div>
  {footer(10, "Services")}
</section>
''')

# --- 11 TAGLINE & MESSAGING -------------------------------------------------
def msg_card(big, small, bg, fg, sub):
    return f'''<div class="msg-card" style="background:{bg};color:{fg}">
      <div class="msg-big">{big}</div>
      <div class="msg-small" style="color:{sub}">{small}</div>
    </div>'''

pages.append(f'''
<section class="page page-sand">
  <div class="page-pad">
    {kicker("10 &nbsp;/&nbsp; Messaging")}
    <h2 class="h-display">Words we<br><span class="italic">live by.</span></h2>
    <div class="tag-hero">
      <div class="tag-hero-main marcellus">Come home to your body.</div>
      <div class="tag-hero-sub">where an artist&rsquo;s eye meets healing hands</div>
      <div class="tag-hero-alt italic">alt &middot; &ldquo;Awoken, yet at ease.&rdquo;</div>
    </div>
    <div class="msg-grid">
      {msg_card("You&rsquo;re safe here. Let&rsquo;s slow down together.", "Welcome / intake", P["euc"], P["oat"], "#cdd3c4")}
      {msg_card("Sixty minutes that belong entirely to you.", "Booking / services", P["teal"], P["ink"], "#34382f")}
      {msg_card("Healing doesn&rsquo;t have to be earned &mdash; it&rsquo;s already yours.", "Social / reflection", P["clay"], P["oat"], "#f3e3d8")}
      {msg_card("Rest is not a reward. It&rsquo;s a return.", "About / values", P["sage"], P["oat"], "#e3e8dc")}
    </div>
  </div>
  {footer(11, "Messaging")}
</section>
''')

# --- 12 APPLICATIONS / MOCKUPS ---------------------------------------------
pages.append(f'''
<section class="page">
  <div class="page-pad">
    {kicker("11 &nbsp;/&nbsp; Applications")}
    <h2 class="h-display">In the<br><span class="italic">world.</span></h2>
    <p class="section-intro">A consistent system across every surface &mdash; web, social, and the small printed things you hold in your hands.</p>
    <div class="mock-grid">
      <!-- Website -->
      <div class="mock mock-web">
        <div class="mock-cap">Website</div>
        <div class="browser">
          <div class="browser-bar"><span></span><span></span><span></span></div>
          <div class="browser-body">
            <div class="web-nav"><span class="web-logo">{logo_mark(P["euc"], 22)}</span><span class="web-word">itz_litny</span><span class="web-links">services &nbsp; about &nbsp; book</span></div>
            <div class="web-hero">
              <div class="web-hero-blob">{organic_blob(P["teal"], 0.25, 1)}</div>
              <div class="web-h1">Come home<br>to your body.</div>
              <div class="web-btn">Book a session</div>
            </div>
          </div>
        </div>
      </div>
      <!-- Instagram -->
      <div class="mock mock-ig">
        <div class="mock-cap">Instagram</div>
        <div class="ig">
          <div class="ig-post" style="background:{P['sage']}">
            <div class="ig-blob">{organic_blob(P["oat"], 0.2, 0)}</div>
            <div class="ig-text marcellus">Rest is<br>a return.</div>
          </div>
          <div class="ig-post" style="background:{P['clay']}">
            <div class="ig-mark">{logo_mark(P["oat"], 40)}</div>
          </div>
          <div class="ig-post" style="background:{P['sand']}">
            <div class="ig-text2">Sixty minutes<br>that belong<br>to you.</div>
          </div>
        </div>
      </div>
      <!-- Business card -->
      <div class="mock mock-card">
        <div class="mock-cap">Business card</div>
        <div class="bcards">
          <div class="bcard bcard-front">
            <div class="bc-mark">{logo_mark(P["oat"], 44)}</div>
            <div class="bc-word">itz_litny</div>
            <div class="bc-desc">massage therapy</div>
          </div>
          <div class="bcard bcard-back">
            <div class="bc-tag marcellus">Come home to your body.</div>
            <div class="bc-info">Brittany &middot; LMT<br>by appointment</div>
          </div>
        </div>
      </div>
      <!-- Gift / candle label -->
      <div class="mock mock-label">
        <div class="mock-cap">Gift card &amp; candle label</div>
        <div class="labels">
          <div class="gift">
            <div class="gift-k">gift of rest</div>
            <div class="gift-mark">{logo_mark(P["euc"], 30)}</div>
            <div class="gift-v">one session, on us</div>
          </div>
          <div class="candle">
            <div class="candle-ring">{logo_mark(P["euc"], 34)}</div>
            <div class="candle-word">itz_litny</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  {footer(12, "Applications")}
</section>
''')

# --- 13 CLOSING -------------------------------------------------------------
pages.append(f'''
<section class="page closing">
  <div class="close-blob cb1">{organic_blob(P["sage"], 0.16, 2)}</div>
  <div class="close-blob cb2">{organic_blob(P["clay"], 0.13, 0)}</div>
  <div class="close-inner">
    <div class="close-mark">{logo_mark(P["euc"], 96)}</div>
    <h1 class="close-tag">Come home<br>to your body.</h1>
    <div class="close-aq">{aquarius_glyph(P["teal"], 56)}</div>
    <div class="close-sub">itz_litny &mdash; massage therapy</div>
    <div class="close-line"></div>
    <div class="close-note">An artist&rsquo;s eye. Healing hands. A safe space, every time.</div>
  </div>
</section>
''')

# ===========================================================================
# CSS
# ===========================================================================
FONT_CSS = build_font_css()

CSS = f'''
{FONT_CSS}

@page {{
  size: 8.5in 11in;
  margin: 0;
}}

* {{ margin:0; padding:0; box-sizing:border-box; }}

html {{ -weasy-hyphens: none; }}

body {{
  font-family:'Nunito Sans', sans-serif;
  color:{P["ink"]};
  background:{P["oat"]};
  font-weight:400;
  -weasy-font-feature-settings:"kern" 1, "liga" 1;
}}

.italic {{ font-style:italic; }}
.cormorant {{ font-family:'Cormorant Garamond', serif; }}
.nunito {{ font-family:'Nunito Sans', sans-serif; }}
.marcellus {{ font-family:'Marcellus', serif; }}

.page {{
  position:relative;
  width:8.5in;
  height:11in;
  background:{P["oat"]};
  overflow:hidden;
  page-break-after:always;
}}
.page:last-child {{ page-break-after:auto; }}
.page-sand {{ background:{P["sand"]}; }}

.page-pad {{
  position:relative;
  z-index:2;
  padding:0.85in 0.85in 0.7in 0.85in;
  height:100%;
}}

/* ---- shared type ---- */
.kicker {{
  font-family:'Nunito Sans', sans-serif;
  font-weight:700;
  font-size:8.5pt;
  letter-spacing:0.26em;
  text-transform:uppercase;
  color:{P["clay"]};
  margin-bottom:0.18in;
}}
.h-display {{
  font-family:'Cormorant Garamond', serif;
  font-weight:500;
  font-size:42pt;
  line-height:1.04;
  color:{P["euc"]};
  letter-spacing:-0.01em;
  margin-bottom:0.22in;
}}
.h-display .italic {{ color:{P["clay"]}; font-weight:500; }}
.section-intro {{
  font-size:11pt;
  line-height:1.6;
  color:{P["ink"]};
  max-width:5.4in;
  margin-bottom:0.4in;
  font-weight:300;
}}
.section-intro em {{ color:{P["stone"]}; font-style:italic; }}

/* ---- footer ---- */
.footer {{
  position:absolute;
  left:0.85in; right:0.85in; bottom:0.5in;
  display:flex; align-items:center; justify-content:space-between;
  font-size:8pt; letter-spacing:0.18em; text-transform:uppercase;
  color:{P["stone"]};
  border-top:1px solid rgba(138,138,124,0.3);
  padding-top:0.12in;
  z-index:5;
}}
.f-mark {{ font-weight:800; letter-spacing:0.12em; color:{P["euc"]}; text-transform:none; font-size:9pt; }}
.f-label {{ font-weight:600; }}
.f-no {{ font-weight:700; color:{P["clay"]}; }}

/* =================== COVER =================== */
.cover {{ background:{P["oat"]}; }}
.cover-blob {{ position:absolute; z-index:1; }}
.blob-1 {{ width:7in; height:7in; top:-2.4in; right:-2.2in; }}
.blob-2 {{ width:6in; height:6in; bottom:-2.2in; left:-2.4in; }}
.blob-3 {{ width:3.4in; height:3.4in; bottom:1.6in; right:0.4in; }}
.cover-inner {{
  position:relative; z-index:3;
  height:100%;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center;
  padding:0 0.9in;
}}
.cover-logo {{ margin-bottom:0.18in; }}
.cover-wordmark {{
  font-family:'Nunito Sans', sans-serif; font-weight:800;
  font-size:23pt; letter-spacing:0.02em; color:{P["euc"]};
}}
.cover-desc {{
  font-family:'Nunito Sans', sans-serif; font-weight:600;
  font-size:9.5pt; letter-spacing:0.42em; text-transform:uppercase;
  color:{P["stone"]}; margin-top:0.06in;
}}
.cover-rule {{
  width:0.55in; height:1.6px; background:{P["clay"]}; margin:0.34in 0;
}}
.cover-tag {{
  font-family:'Cormorant Garamond', serif; font-weight:500;
  font-size:54pt; line-height:1.0; color:{P["ink"]};
  letter-spacing:-0.015em;
}}
.cover-sub {{
  font-family:'Marcellus', serif;
  font-size:12pt; letter-spacing:0.04em; color:{P["sage"]};
  margin-top:0.3in;
}}
.cover-foot {{
  position:absolute; bottom:0.62in; left:0; right:0; z-index:3;
  text-align:center;
  font-size:8pt; letter-spacing:0.2em; text-transform:uppercase;
  color:{P["stone"]}; font-weight:600;
}}
.cover-foot .dot {{ margin:0 0.14in; color:{P["clay"]}; }}

/* =================== WELCOME =================== */
.lead {{
  font-family:'Cormorant Garamond', serif; font-style:italic;
  font-size:19pt; line-height:1.3; color:{P["sage"]};
  margin-bottom:0.2in; font-weight:500;
}}
.two-col {{ display:flex; gap:0.5in; }}
.col-main {{ flex:1.45; }}
.col-main p {{ font-size:10.5pt; line-height:1.66; margin-bottom:0.16in; font-weight:300; color:{P["ink"]}; }}
.col-side {{ flex:1; }}
.story-card {{
  position:relative; background:{P["euc"]}; border-radius:16px;
  padding:0.42in 0.34in; overflow:hidden; margin-bottom:0.26in;
}}
.story-blob {{ position:absolute; width:3in; height:3in; bottom:-1.4in; right:-1.2in; opacity:0.35; }}
.story-quote {{
  position:relative; z-index:2;
  font-family:'Cormorant Garamond', serif; font-style:italic;
  font-size:17pt; line-height:1.34; color:{P["oat"]};
}}
.side-fact {{ border-top:1px solid rgba(138,138,124,0.35); padding:0.16in 0; }}
.fact-k {{ font-size:7.5pt; letter-spacing:0.2em; text-transform:uppercase; font-weight:700; color:{P["clay"]}; margin-bottom:0.05in; }}
.fact-v {{ font-size:10pt; line-height:1.45; color:{P["ink"]}; font-weight:400; }}

/* =================== MISSION =================== */
.mission-band {{
  background:{P["oat"]}; border-radius:16px;
  padding:0.46in 0.5in; text-align:center; margin-bottom:0.4in;
  border:1px solid rgba(124,139,111,0.25);
}}
.mission-leaf {{ display:flex; justify-content:center; margin-bottom:0.16in; }}
.mission-text {{
  font-family:'Cormorant Garamond', serif; font-weight:500;
  font-size:21pt; line-height:1.34; color:{P["euc"]};
  max-width:5.6in; margin:0 auto;
}}
.values-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:0.28in; }}
.value-card {{
  background:{P["oat"]}; border-radius:14px; padding:0.34in 0.36in;
  border:1px solid rgba(138,138,124,0.18);
}}
.value-num {{ font-family:'Cormorant Garamond', serif; font-size:30pt; font-weight:600; line-height:1; margin-bottom:0.08in; }}
.value-title {{ font-family:'Nunito Sans'; font-weight:800; font-size:12pt; color:{P["ink"]}; margin-bottom:0.07in; }}
.value-body {{ font-size:10pt; line-height:1.55; color:{P["stone"]}; font-weight:400; }}

/* =================== AUDIENCE =================== */
.aud-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:0.3in; margin-bottom:0.4in; }}
.aud-card {{
  background:{P["sand"]}; border-radius:14px; padding:0.34in 0.36in;
}}
.aud-dot {{ width:0.22in; height:0.22in; border-radius:50%; margin-bottom:0.14in; }}
.aud-title {{ font-family:'Cormorant Garamond', serif; font-weight:600; font-size:18pt; color:{P["euc"]}; margin-bottom:0.08in; }}
.aud-body {{ font-size:10pt; line-height:1.55; color:{P["ink"]}; font-weight:300; }}
.aud-foot {{
  position:relative; background:{P["euc"]}; border-radius:16px;
  padding:0.4in 0.5in; overflow:hidden; text-align:center;
}}
.aud-foot-blob {{ position:absolute; width:3.4in; height:3.4in; top:-1.6in; left:-1.2in; opacity:0.16; }}
.aud-foot-text {{ position:relative; z-index:2; font-family:'Cormorant Garamond', serif; font-size:18pt; color:{P["oat"]}; }}

/* =================== VOICE =================== */
.mini-h {{ font-size:8pt; letter-spacing:0.2em; text-transform:uppercase; font-weight:700; color:{P["clay"]}; margin-bottom:0.2in; }}
.voice-cols {{ display:flex; gap:0.55in; margin-bottom:0.4in; }}
.voice-sliders {{ flex:1.3; }}
.slider-row {{ display:flex; align-items:center; gap:0.14in; margin-bottom:0.2in; }}
.slider-left, .slider-right {{ font-size:9pt; color:{P["stone"]}; width:1.0in; font-weight:600; }}
.slider-left {{ text-align:right; }}
.slider-track {{ flex:1; height:3px; background:rgba(138,138,124,0.3); border-radius:3px; position:relative; }}
.slider-knob {{ position:absolute; top:50%; width:14px; height:14px; border-radius:50%; background:{P["sage"]}; transform:translate(-50%,-50%); border:2px solid {P["oat"]}; }}
.voice-words {{ flex:1; }}
.chips {{ display:flex; flex-wrap:wrap; gap:0.1in; }}
.chip {{
  font-size:9.5pt; font-weight:600; color:{P["euc"]};
  background:{P["oat"]}; border:1px solid rgba(124,139,111,0.4);
  border-radius:30px; padding:0.07in 0.18in;
}}
.page-sand .chip {{ background:rgba(255,255,255,0.5); }}
.dodont {{ display:flex; gap:0.4in; }}
.do-col, .dont-col {{ flex:1; border-radius:14px; padding:0.3in 0.34in; }}
.do-col {{ background:rgba(124,139,111,0.16); }}
.dont-col {{ background:rgba(190,129,99,0.14); }}
.dd-head {{ font-family:'Cormorant Garamond', serif; font-size:18pt; font-weight:600; margin-bottom:0.14in; }}
.dd-do {{ color:{P["euc"]}; }}
.dd-dont {{ color:{P["clay"]}; }}
.dodont ul {{ list-style:none; }}
.dodont li {{ font-size:9.5pt; line-height:1.5; margin-bottom:0.13in; padding-left:0.2in; position:relative; color:{P["ink"]}; font-weight:400; }}
.dodont li:before {{ content:""; position:absolute; left:0; top:0.09in; width:0.08in; height:0.08in; border-radius:50%; }}
.do-col li:before {{ background:{P["sage"]}; }}
.dont-col li:before {{ background:{P["clay"]}; }}
.dodont em {{ font-style:italic; color:{P["stone"]}; }}

/* =================== LOGO =================== */
.logo-hero {{
  display:flex; align-items:center; gap:0.5in;
  background:{P["sand"]}; border-radius:18px; padding:0.5in 0.6in;
  margin-bottom:0.36in;
}}
.page .logo-hero {{ background:{P["sand"]}; }}
.logo-hero-lockup {{ border-left:1.5px solid rgba(94,107,83,0.3); padding-left:0.5in; }}
.lh-word {{ font-family:'Nunito Sans'; font-weight:800; font-size:30pt; color:{P["euc"]}; letter-spacing:0.01em; }}
.lh-desc {{ font-weight:600; font-size:10pt; letter-spacing:0.36em; text-transform:uppercase; color:{P["stone"]}; margin-top:0.04in; }}
.logo-grid {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.24in; }}
.logo-tile {{ }}
.lt-vis {{
  height:1.5in; border-radius:12px; display:flex; align-items:center; justify-content:center;
  position:relative; overflow:hidden; margin-bottom:0.12in;
}}
.lt-clear {{ background:{P["oat"]}; border:1px solid rgba(138,138,124,0.25); }}
.page-sand .lt-clear {{ background:#fff; }}
.clear-box {{ border:1px dashed rgba(190,129,99,0.6); padding:0.2in; border-radius:6px; display:flex; }}
.favi {{ background:{P["sand"]}; padding:0.1in; border-radius:6px; display:flex; }}
.lt-dont .dont-mark {{ filter:saturate(1.4); }}
.lt-dont .slash {{ position:absolute; width:140%; height:2px; background:{P["clay"]}; transform:rotate(-32deg); }}
.lt-cap {{ font-size:8.5pt; line-height:1.4; color:{P["stone"]}; }}
.lt-cap strong {{ color:{P["ink"]}; font-weight:700; }}

/* =================== COLOR =================== */
.swatch-grid {{ display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:0.22in; margin-bottom:0.42in; }}
.swatch-chip {{
  height:1.35in; border-radius:12px; position:relative;
  border:1px solid rgba(52,56,47,0.08);
  display:flex; align-items:flex-end; padding:0.14in;
}}
.swatch-hex {{ font-size:8.5pt; font-weight:700; letter-spacing:0.04em; }}
.swatch-meta {{ padding:0.1in 0.02in 0; }}
.swatch-name {{ font-family:'Cormorant Garamond', serif; font-weight:600; font-size:14pt; color:{P["ink"]}; }}
.swatch-role {{ font-size:8pt; letter-spacing:0.14em; text-transform:uppercase; color:{P["stone"]}; font-weight:600; margin-top:0.02in; }}
.color-notes {{ display:flex; flex-direction:column; gap:0.14in; }}
.cn {{ display:flex; align-items:center; font-size:10pt; color:{P["ink"]}; font-weight:400; }}
.cn-dot {{ width:0.18in; height:0.18in; border-radius:50%; margin-right:0.16in; flex:none; }}

/* =================== TYPOGRAPHY =================== */
.type-spec {{ display:flex; gap:0.5in; padding:0.28in 0; border-bottom:1px solid rgba(138,138,124,0.25); }}
.type-spec.last {{ border-bottom:none; }}
.ts-left {{ width:1.7in; flex:none; padding-top:0.05in; }}
.ts-tag {{ font-size:8pt; letter-spacing:0.2em; text-transform:uppercase; font-weight:700; color:{P["clay"]}; margin-bottom:0.06in; }}
.ts-name {{ font-family:'Cormorant Garamond', serif; font-size:16pt; font-weight:600; color:{P["euc"]}; }}
.ts-name.nunito {{ font-family:'Nunito Sans'; font-weight:800; font-size:14pt; }}
.ts-name.marcellus {{ font-family:'Marcellus'; font-size:15pt; }}
.ts-right {{ flex:1; }}
.ts-big {{ font-family:'Cormorant Garamond', serif; font-weight:500; font-size:34pt; line-height:1.02; color:{P["ink"]}; margin-bottom:0.1in; }}
.ts-alpha {{ font-size:13pt; color:{P["sage"]}; margin-bottom:0.08in; }}
.ts-alpha.nunito {{ font-size:11pt; font-weight:600; }}
.ts-meta {{ font-size:8.5pt; letter-spacing:0.1em; color:{P["stone"]}; font-weight:600; }}
.ts-body {{ font-size:11pt; line-height:1.6; color:{P["ink"]}; font-weight:400; margin-bottom:0.1in; }}
.ts-accent {{ font-family:'Marcellus'; font-size:18pt; color:{P["clay"]}; letter-spacing:0.02em; margin-bottom:0.08in; }}
.type-scale {{ display:flex; flex-wrap:wrap; gap:0.3in; margin-top:0.3in; }}
.type-scale span {{ font-size:9pt; color:{P["stone"]}; }}
.type-scale b {{ color:{P["euc"]}; font-weight:800; margin-right:0.06in; }}

/* =================== PHOTOGRAPHY =================== */
.photo-grid {{ display:grid; grid-template-columns:1fr 1fr 1fr; grid-template-rows:1.7in 1.7in; gap:0.2in; margin-bottom:0.36in; }}
.photo-tile {{ border-radius:14px; position:relative; overflow:hidden; }}
.pt-blob {{ position:absolute; width:140%; height:140%; top:-20%; left:-20%; }}
.pt-label {{ position:absolute; left:0.18in; bottom:0.16in; font-size:9pt; font-weight:700; letter-spacing:0.04em; color:{P["ink"]}; background:rgba(250,247,241,0.82); padding:0.05in 0.13in; border-radius:20px; }}
.photo-rules {{ display:flex; flex-direction:column; gap:0.12in; }}
.pr {{ font-size:10pt; line-height:1.5; color:{P["ink"]}; font-weight:400; }}
.pr-y, .pr-n {{ font-weight:800; margin-right:0.1in; }}
.pr-y {{ color:{P["sage"]}; }}
.pr-n {{ color:{P["clay"]}; }}

/* =================== MENU =================== */
.menu {{ margin-bottom:0.3in; }}
.menu-row {{ display:flex; align-items:baseline; padding:0.2in 0; border-bottom:1px solid rgba(138,138,124,0.25); }}
.menu-name {{ flex:1; font-family:'Cormorant Garamond', serif; font-weight:600; font-size:19pt; color:{P["euc"]}; }}
.menu-desc {{ display:block; font-family:'Nunito Sans'; font-weight:300; font-size:9.5pt; color:{P["stone"]}; margin-top:0.03in; }}
.menu-dur {{ width:1.5in; text-align:center; font-size:9.5pt; font-weight:600; color:{P["stone"]}; letter-spacing:0.04em; }}
.menu-price {{ width:1.4in; text-align:right; font-family:'Cormorant Garamond', serif; font-size:16pt; font-weight:600; color:{P["clay"]}; }}
.menu-extras {{ display:flex; gap:0.28in; margin-bottom:0.3in; }}
.extra {{ flex:1; background:rgba(124,139,111,0.14); border-radius:12px; padding:0.24in 0.3in; display:flex; align-items:center; justify-content:space-between; }}
.extra-clay {{ background:rgba(190,129,99,0.16); }}
.extra-k {{ font-weight:700; font-size:10.5pt; color:{P["ink"]}; }}
.extra-v {{ font-family:'Cormorant Garamond', serif; font-size:17pt; font-weight:600; color:{P["euc"]}; }}
.extra-clay .extra-v {{ color:{P["clay"]}; }}
.menu-foot {{ text-align:center; font-family:'Cormorant Garamond', serif; font-size:15pt; color:{P["sage"]}; }}

/* =================== MESSAGING =================== */
.tag-hero {{ text-align:center; margin-bottom:0.4in; }}
.tag-hero-main {{ font-family:'Marcellus'; font-size:36pt; color:{P["euc"]}; letter-spacing:0.01em; }}
.tag-hero-sub {{ font-family:'Cormorant Garamond', serif; font-style:italic; font-size:15pt; color:{P["clay"]}; margin-top:0.1in; }}
.tag-hero-alt {{ font-size:10pt; color:{P["stone"]}; margin-top:0.14in; letter-spacing:0.04em; }}
.msg-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:0.26in; }}
.msg-card {{ border-radius:14px; padding:0.4in 0.4in; min-height:1.7in; display:flex; flex-direction:column; justify-content:space-between; }}
.msg-big {{ font-family:'Cormorant Garamond', serif; font-weight:500; font-size:22pt; line-height:1.18; }}
.msg-small {{ font-size:8pt; letter-spacing:0.18em; text-transform:uppercase; font-weight:700; margin-top:0.18in; }}

/* =================== APPLICATIONS =================== */
.mock-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:0.3in; }}
.mock-cap {{ font-size:8pt; letter-spacing:0.18em; text-transform:uppercase; font-weight:700; color:{P["clay"]}; margin-bottom:0.1in; }}
/* browser */
.browser {{ border-radius:10px; overflow:hidden; border:1px solid rgba(138,138,124,0.3); background:#fff; }}
.browser-bar {{ background:{P["sand"]}; padding:0.08in 0.12in; display:flex; gap:0.05in; }}
.browser-bar span {{ width:0.08in; height:0.08in; border-radius:50%; background:{P["stone"]}; opacity:0.5; }}
.browser-body {{ }}
.web-nav {{ display:flex; align-items:center; gap:0.08in; padding:0.1in 0.14in; border-bottom:1px solid rgba(138,138,124,0.18); }}
.web-logo {{ display:flex; }}
.web-word {{ font-weight:800; font-size:9pt; color:{P["euc"]}; }}
.web-links {{ margin-left:auto; font-size:7pt; letter-spacing:0.1em; text-transform:uppercase; color:{P["stone"]}; font-weight:600; }}
.web-hero {{ position:relative; height:1.5in; background:{P["oat"]}; display:flex; flex-direction:column; align-items:center; justify-content:center; overflow:hidden; }}
.web-hero-blob {{ position:absolute; width:2.4in; height:2.4in; top:-1in; right:-0.9in; }}
.web-h1 {{ position:relative; z-index:2; font-family:'Cormorant Garamond', serif; font-weight:500; font-size:19pt; line-height:1.05; color:{P["ink"]}; text-align:center; }}
.web-btn {{ position:relative; z-index:2; margin-top:0.14in; background:{P["euc"]}; color:{P["oat"]}; font-size:7.5pt; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; padding:0.08in 0.2in; border-radius:30px; }}
/* instagram */
.ig {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.08in; }}
.ig-post {{ aspect-ratio:1; border-radius:8px; position:relative; overflow:hidden; display:flex; align-items:center; justify-content:center; height:1.35in; }}
.ig-blob {{ position:absolute; width:160%; height:160%; top:-30%; left:-30%; }}
.ig-text {{ position:relative; z-index:2; font-family:'Marcellus'; font-size:14pt; color:{P["oat"]}; text-align:center; line-height:1.1; }}
.ig-text2 {{ font-family:'Cormorant Garamond', serif; font-size:12pt; color:{P["euc"]}; text-align:center; line-height:1.15; font-weight:500; }}
.ig-mark {{ display:flex; }}
/* business card */
.bcards {{ display:flex; gap:0.16in; }}
.bcard {{ flex:1; aspect-ratio:1.75; border-radius:10px; padding:0.2in; display:flex; flex-direction:column; height:1.45in; }}
.bcard-front {{ background:{P["euc"]}; align-items:center; justify-content:center; text-align:center; }}
.bc-mark {{ display:flex; }}
.bc-word {{ font-weight:800; font-size:13pt; color:{P["oat"]}; margin-top:0.08in; }}
.bc-desc {{ font-size:6.5pt; letter-spacing:0.28em; text-transform:uppercase; color:{P["teal"]}; margin-top:0.03in; }}
.bcard-back {{ background:{P["sand"]}; justify-content:space-between; }}
.bc-tag {{ font-family:'Marcellus'; font-size:13pt; color:{P["euc"]}; line-height:1.15; }}
.bc-info {{ font-size:8pt; line-height:1.4; color:{P["stone"]}; font-weight:600; }}
/* labels */
.labels {{ display:flex; gap:0.16in; }}
.gift {{ flex:1.4; background:{P["clay"]}; border-radius:10px; padding:0.22in; color:{P["oat"]}; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; height:1.45in; }}
.gift-k {{ font-family:'Cormorant Garamond', serif; font-style:italic; font-size:13pt; }}
.gift-mark {{ display:flex; margin:0.08in 0; }}
.gift-mark svg path {{ stroke:{P["oat"]}!important; }}
.gift-v {{ font-size:7.5pt; letter-spacing:0.14em; text-transform:uppercase; font-weight:700; }}
.candle {{ flex:1; background:{P["oat"]}; border:1px solid rgba(94,107,83,0.35); border-radius:10px; display:flex; flex-direction:column; align-items:center; justify-content:center; height:1.45in; }}
.candle-ring {{ display:flex; border:1.5px solid rgba(94,107,83,0.4); border-radius:50%; padding:0.12in; }}
.candle-word {{ font-weight:800; font-size:10pt; color:{P["euc"]}; margin-top:0.1in; }}

/* =================== CLOSING =================== */
.closing {{ background:{P["euc"]}; }}
.close-blob {{ position:absolute; z-index:1; }}
.cb1 {{ width:7in; height:7in; top:-2.6in; left:-2.6in; }}
.cb2 {{ width:6in; height:6in; bottom:-2.6in; right:-2.4in; }}
.close-inner {{ position:relative; z-index:3; height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
.close-mark {{ margin-bottom:0.2in; }}
.close-mark svg path {{ stroke:{P["oat"]}!important; }}
.close-tag {{ font-family:'Cormorant Garamond', serif; font-weight:500; font-size:50pt; line-height:1.0; color:{P["oat"]}; letter-spacing:-0.015em; }}
.close-aq {{ margin:0.3in 0 0.16in; display:flex; justify-content:center; }}
.close-sub {{ font-family:'Nunito Sans'; font-weight:700; font-size:10pt; letter-spacing:0.32em; text-transform:uppercase; color:{P["teal"]}; }}
.close-line {{ width:0.6in; height:1.5px; background:{P["clay"]}; margin:0.28in 0; }}
.close-note {{ font-family:'Cormorant Garamond', serif; font-style:italic; font-size:15pt; color:{P["sand"]}; max-width:4.2in; }}
'''

# ===========================================================================
# Assemble + render
# ===========================================================================
def main():
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>itz_litny &mdash; Brand Portfolio</title>
<style>{CSS}</style>
</head>
<body>
{''.join(pages)}
</body>
</html>'''

    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"HTML written: {HTML_OUT}  ({len(html)/1024:.0f} KB)")

    from weasyprint import HTML
    HTML(string=html, base_url=str(HERE)).write_pdf(str(OUT_PDF))
    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"PDF written:  {OUT_PDF}  ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
