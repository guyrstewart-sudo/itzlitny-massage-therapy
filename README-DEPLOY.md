# itz_litny massage therapy — launch & deploy runbook

Everything is built. This guide takes the site from these files to **live, taking real bookings**. Three stages: (1) publish the site, (2) connect a domain, (3) turn on Stripe payments.

---

## What's in this folder
```
index.html              ← the website
thank-you.html          ← post-payment confirmation page
assets/css/styles.css   ← styles (brand palette + type)
assets/js/main.js       ← nav, animations, image auto-swap
assets/js/booking.js    ← booking form + checkout (CONFIG at top)
assets/img/             ← favicon + share image; drop real photos here
api/create-checkout-session.js  ← Stripe serverless function
package.json            ← dependency for the function (stripe)
brand/                  ← brand portfolio book (PDF) + foundation spec
```

---

## Stage 1 — Publish on GitHub Pages (free)
1. Create a new GitHub repo (e.g. `itzlitny-site`).
2. Upload everything in this folder to the repo root (drag-and-drop in the browser works).
3. Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
4. Wait ~1 minute. Your site is live at `https://<username>.github.io/itzlitny-site/`.

> The site is fully functional here immediately. Until Stripe is connected (Stage 3), the booking button opens an email to `hello@itzlitny.com` so no request is ever lost.

---

## Stage 2 — Custom domain (optional, recommended)
1. Buy a domain (Namecheap, Cloudflare, Google Domains, etc.) — e.g. `itzlitny.com`.
2. In the repo, add a file named `CNAME` containing just: `itzlitny.com`
3. At your registrar, add DNS records pointing to GitHub Pages:
   - Four `A` records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - One `CNAME` for `www` → `<username>.github.io`
4. Back in **Settings → Pages**, enter the custom domain and tick **Enforce HTTPS**.

---

## Stage 3 — Turn on real Stripe payments
GitHub Pages can't run server code, so the payment logic lives in one tiny serverless function. Easiest host: **Vercel** (free tier, ~10 min).

> **Important:** Only Brittany should create the Stripe account and paste the secret key. I never handle live keys, and you should never commit them to GitHub.

### 3a. Stripe account
1. Brittany creates a Stripe account at stripe.com and completes verification.
2. Dashboard → **Developers → API keys** → copy the **Secret key** (`sk_live_…`; use `sk_test_…` to test first).

### 3b. Deploy the function on Vercel
1. Go to vercel.com → **Add New → Project** → import the same GitHub repo.
2. Vercel auto-detects `/api/create-checkout-session.js` and `package.json`.
3. In **Project → Settings → Environment Variables**, add:
   - `STRIPE_SECRET_KEY` = `sk_live_…`
   - `SITE_URL` = `https://itzlitny.com` (your live site URL)
4. Deploy. Your function URL will be:
   `https://<project>.vercel.app/api/create-checkout-session`

### 3c. Connect the site to the function
1. Open `assets/js/booking.js`.
2. Set the endpoint near the top:
   ```js
   var CONFIG = {
     checkoutEndpoint: "https://<project>.vercel.app/api/create-checkout-session",
     ...
   };
   ```
3. Commit/upload the change. Done — the booking button now opens **Stripe's secure hosted checkout**, and on success the client lands on `thank-you.html`.

### 3d. Confirm prices (server-side source of truth)
Real prices live in **`api/create-checkout-session.js`** in the `PRICES` table (in cents). Edit there — the browser never sets the price, which prevents tampering. Keep the menu text in `index.html` in sync for display.

---

## Booking notifications & calendar
The function stores name / date / time / notes in Stripe **metadata**, visible on each payment in the Stripe Dashboard. To also get an email or a calendar hold per booking:
- Add a **Stripe webhook** (event `checkout.session.completed`) → Zapier/Make → Gmail + Google Calendar, **or**
- Simplest no-code alternative: replace the custom form with an embedded **Calendly** or **Square Appointments** booking widget (both handle scheduling + payment + reminders). If you'd rather go that route, say so and I'll swap the booking section to an embed.

---

## Going-live checklist
- [ ] Site published on GitHub Pages
- [ ] Real photos dropped into `assets/img/` (see README-IMAGES.txt)
- [ ] Final pricing confirmed in `api/create-checkout-session.js` **and** `index.html`
- [ ] Real contact email / location / hours updated in `index.html`
- [ ] Stripe account verified; `STRIPE_SECRET_KEY` + `SITE_URL` set on Vercel
- [ ] `checkoutEndpoint` set in `booking.js`
- [ ] Test booking with a Stripe **test** card `4242 4242 4242 4242`
- [ ] Confirm "Massage" vs "Message" spelling for print/brand
- [ ] Switch Stripe to live mode

---

## Honest notes
- **Images:** built with on-brand placeholder slots. Brittany's personal Instagram photos are her copyright — use only what she approves.
- **Pricing:** placeholder/introductory — confirm before launch.
- **Custom backend:** the Stripe piece needs the one serverless function above because static hosting can't process payments by itself. That function + Stripe Checkout is the secure, standard way to do it; card data never touches your site.
