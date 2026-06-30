/* api/create-checkout-session.js
 * Serverless Stripe Checkout for Beconing Arts Massage Therapy.
 * Works as a Vercel Serverless Function out of the box.
 * (Cloudflare Workers / Netlify notes in README-DEPLOY.md.)
 *
 * SECURITY: the server NEVER trusts the price sent by the browser. It
 * recomputes the amount from this trusted table. The client amount is
 * ignored. Card data is handled entirely by Stripe's hosted Checkout.
 *
 * REQUIRED ENV VARS (set in your host dashboard — never commit them):
 *   STRIPE_SECRET_KEY   = sk_live_... (or sk_test_... while testing)
 *   SITE_URL            = https://your-domain.com   (for redirect URLs)
 */
const Stripe = require("stripe");

// Trusted price table (USD cents). Edit here to change real pricing.
const PRICES = {
  "Relaxation (Swedish)": { 60: 7500, 90: 11000 },
  "Therapeutic / Custom": { 60: 8500, 90: 12000 },
  "Deep Tissue":          { 60: 9000, 90: 12500 },
  "Prenatal":             { 60: 8500 },
  "Hot Stone":            { 75: 11500 }
};
const AROMA_CENTS = 1500;
const FIRST_VISIT_DISCOUNT_CENTS = 2000;

module.exports = async function handler(req, res) {
  // CORS (safe for a public booking endpoint)
  res.setHeader("Access-Control-Allow-Origin", process.env.SITE_URL || "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  try {
    const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
    const b = typeof req.body === "string" ? JSON.parse(req.body) : (req.body || {});

    const svc = String(b.service || "");
    const minutes = parseInt(b.minutes, 10);
    const table = PRICES[svc];
    if (!table || !table[minutes]) {
      return res.status(400).json({ error: "Unknown service or duration." });
    }

    const base = table[minutes];
    const line_items = [{
      quantity: 1,
      price_data: {
        currency: "usd",
        unit_amount: base,
        product_data: {
          name: `${svc} — ${minutes} min`,
          description: "Beconing Arts Massage Therapy session"
        }
      }
    }];
    if (b.aromatherapy === true) {
      line_items.push({
        quantity: 1,
        price_data: {
          currency: "usd",
          unit_amount: AROMA_CENTS,
          product_data: { name: "Aromatherapy add-on" }
        }
      });
    }

    // First-visit discount via Stripe coupon (created on the fly, one-time)
    let discounts;
    if (b.firstVisit === true) {
      const coupon = await stripe.coupons.create({
        amount_off: FIRST_VISIT_DISCOUNT_CENTS,
        currency: "usd",
        duration: "once",
        name: "First-visit $20 off"
      });
      discounts = [{ coupon: coupon.id }];
    }

    const site = process.env.SITE_URL || "";
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      line_items,
      discounts,
      customer_email: b.email || undefined,
      phone_number_collection: { enabled: true },
      success_url: `${site}/thank-you.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${site}/#book`,
      metadata: {
        service: svc,
        minutes: String(minutes),
        preferred_date: String(b.date || ""),
        preferred_time: String(b.time || ""),
        client_name: String(b.name || ""),
        client_phone: String(b.phone || ""),
        notes: String(b.notes || "").slice(0, 480),
        first_visit: b.firstVisit ? "yes" : "no",
        aromatherapy: b.aromatherapy ? "yes" : "no"
      }
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error("checkout error:", err);
    return res.status(500).json({ error: "Could not create checkout session." });
  }
};
