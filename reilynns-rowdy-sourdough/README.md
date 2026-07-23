# Reilynn's Rowdy Sourdough — Website

A warm, mobile-friendly **pre-sale landing page** for Reilynn's Rowdy Sourdough.
Baked with love, no preservatives, no fillers. 🍞

Plain HTML/CSS/JS — no build step, no dependencies. Just open it and it works.

## Files

```
index.html        The whole page
css/styles.css    Brand styling (cream + sourdough brown, from your logo)
js/main.js         Mobile menu + footer year
images/            Put your real photos here (see images/README.txt)
```

## Preview it locally

Just double-click `index.html` to open it in your browser. That's it.

(Optional) To preview with a local web server, from this folder run:

```bash
# Python (usually already installed)
python -m http.server 8000
# then open http://localhost:8000
```

## Before launch — fill these in

1. **Photos** — drop `hero.jpg` (and optionally `logo.png`) into the `images/` folder. See `images/README.txt`.
2. **Contact info** — in `index.html`, find the `Contact` section and replace the
   `[Your name here]`, `[your@email.com]`, `[your number]`, and `[@yourhandle]` placeholders.
3. **Pricing** — pricing is intentionally left off for now (pre-sale). Your flyer
   mentioned "$10 / half loaf, $2 / slice, cash in box or Zelle 973-294-3316" —
   just say the word and we'll add that in.

## Publishing it (build first, then buy the domain — totally fine!)

Recommended order:

1. **Deploy the site** to a free host to get a live temporary URL:
   - **Netlify** or **Vercel**: drag-and-drop this folder at netlify.com/drop or
     import it — you'll get a URL like `reilynns-rowdy-sourdough.netlify.app`.
   - **GitHub Pages**: push this folder to a GitHub repo, then enable Pages.
2. **Buy your domain** (e.g. `reilynnsrowdysourdough.com`) from Namecheap,
   Cloudflare, or Google Domains — usually ~$10–15/year.
3. **Point the domain** at your host by adding the DNS records the host gives you.
   HTTPS is free and automatic on all three hosts above.

You only need to pay for the domain once you're happy with how the site looks.

---

Homemade in a home kitchen with love.
