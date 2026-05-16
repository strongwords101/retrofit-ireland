# RetrofitList.ie — Launch Checklist

Everything required to go from demo to live. Roughly in priority order within each section.

---

## 🏗️ 1. Real Provider Data (`data/providers.json`)

The 14 fictional providers need to be replaced with real Irish companies.

### Research sources
- SEAI registered contractor database — seai.ie/find-a-contractor
- National Home Energy Upgrade Scheme (NHEUS) approved one-stop-shops — seai.ie
- Google Maps searches by county and service type
- Trade associations: HPAI (Heat Pump Association of Ireland), SEI, NSAI

### Target: aim for 5–10 real providers per category to start

- [x] External Wall Insulation contractors — 227 scraped from SEAI register
- [x] Internal Wall Insulation contractors — 815 scraped from SEAI register
- [x] Attic & Floor Insulation contractors — 813 scraped from SEAI register
- [x] Heat Pump installers — 602 scraped from SEAI register
- [x] Windows & Doors suppliers/installers — 572 scraped from SEAI register
- [x] Solar Thermal installers — 223 scraped from SEAI register
- [x] One-Stop-Shop Retrofit contractors — 32 added manually from SEAI approved list
- [ ] **BER Assessors** — register at `ndber.seai.ie` is reCAPTCHA-protected. Options: (a) use 2captcha or Anti-Captcha service (~$5–10 for full list), (b) wait for SEAI to publish as open data. Thousands of assessors nationwide — high value category.
- [ ] **Solar PV installers** — not on the main SEAI BEH register; separate SEAI portal also blocks scraping. Same captcha-solving approach needed, or source from SEAI Solar PV grant page manually.
- [ ] Airtightness Testing specialists — no central Irish register; best sources are ACAI.ie member list and NSAI-accredited testers. Manual curation required.
- [ ] MVHR / Ventilation specialists — no central register; source from manufacturer approved installer lists (Zehnder, Brink, etc.) or HPAI members. Manual curation required.

### For each provider, confirm before adding:
- [ ] Company is currently SEAI registered (check seai.ie register)
- [ ] Phone number is live
- [ ] Email address is active
- [ ] Website URL is working
- [ ] Description is accurate and approved (ideally by the company itself)

### Consider emailing companies directly
A short outreach email offering a free listing is also a good way to build relationships and ensure accuracy. Draft template needed.

---

## 📰 2. Real Articles & Guides (`data/articles.json`)

The 6 sample articles need to be replaced with accurate, well-researched content. The list below covers the core topics users search for — drawn from RetrofitIreland.ie's own topic list and common search queries.

### Priority articles to write / research
- [ ] **SEAI Better Energy Homes 2025 — Full Grant Guide** (verify current amounts at seai.ie — update any figures from the sample article)
- [ ] **SEAI One-Stop-Shop Scheme — How It Works and What It Pays**
- [ ] **Local Authority Home Improvement Grants — County-by-County Breakdown**
- [ ] **BER Ratings Explained — What A, B, C, D, E, F, G Mean and How to Improve**
- [ ] **Heat Pump Installation in Ireland — What You Need to Know Before You Buy**
- [ ] **How to Insulate Your Attic — Step by Step** (review existing sample for accuracy)
- [ ] **External Wall Insulation — Costs, Benefits, and Planning Rules**
- [ ] **Solar PV & Renewables — What Irish Homeowners Need to Know**
- [ ] **Windows & Doors Upgrades — Grants, U-Values, and What to Specify**
- [ ] **Landlord BER Requirements — What Irish Landlords Are Legally Required to Do**
- [ ] **Retrofit Costs & Savings — Realistic Numbers for Irish Homes**
- [ ] **Planning Permission for Retrofit Works — When You Need It**
- [ ] **What is Airtightness and Why Does It Matter?**
- [ ] **MVHR Ventilation — Do You Need It After a Deep Retrofit?**

### For each article:
- [ ] Verify all grant figures against current SEAI website (amounts change)
- [ ] Verify all regulatory references (Part L, planning regs) are current 2025 versions
- [ ] Add author name or use "RetrofitList.ie Editorial Team"
- [ ] Set accurate publish date

---

## 🌐 3. Domain & Hosting

- [ ] Register **RetrofitList.ie** (requires proof of Irish connection — use IE Domain Registry via a registrar like Blacknight or Hosting Ireland)
- [ ] Register **RetrofitList.com** as backup / redirect
- [ ] Decide on hosting: GitHub Pages (free, suits this static site) vs Cloudflare Pages vs Netlify
- [ ] Push repo to GitHub (`git push origin main` — already connected to `github.com/strongwords101/retrofit-ireland`)
- [ ] Enable GitHub Pages: Settings → Pages → Deploy from branch: main / root
- [ ] Once domain is live, add custom domain in GitHub Pages settings
- [ ] Set up DNS: point retrofitlist.ie → GitHub Pages IP addresses
- [ ] Enable HTTPS (GitHub Pages does this automatically for custom domains)
- [ ] Test all pages on production URL before announcing

---

## 📧 4. Email Setup

The about page and listing CTA currently reference these addresses — they need to actually exist and be monitored.

- [ ] Set up **listings@retrofitlist.ie** (for new listing requests)
- [ ] Set up **hello@retrofitlist.ie** (for general contact)
- [ ] Options: Google Workspace (€5/mo), Zoho Mail (free tier), or forward from domain registrar
- [ ] Test both mailto: links on the about page work

---

## 🔍 5. SEO & Discoverability

- [ ] **sitemap.xml** — list all pages with their URLs; submit to Google Search Console
- [ ] **robots.txt** — basic file allowing all crawlers
- [ ] **Open Graph meta tags** — so pages look good when shared on Facebook, WhatsApp, LinkedIn (og:title, og:description, og:image)
- [ ] **Twitter/X card meta tags** — similar to OG tags
- [ ] **Structured data (JSON-LD)** — mark up provider listings as LocalBusiness schema; helps Google show rich results
- [ ] **Google Search Console** — verify site ownership, submit sitemap, monitor indexing
- [ ] **Google Analytics or Plausible** — add tracking to understand traffic (Plausible is GDPR-friendly and privacy-first)
- [ ] **Canonical URLs** — add `<link rel="canonical">` to each page
- [ ] Create a proper **favicon** (the current one is an emoji SVG — fine for now, but a proper .ico or SVG icon would be better)
- [ ] Add **alt text audit** — check all images have descriptive alt text (currently no images, but when added)

---

## ⚖️ 6. Legal & GDPR

Required for any Irish/EU website, especially one collecting contact details via mailto links.

- [ ] **Privacy Policy page** (`privacy.html`) — what data is collected, how it's used, who to contact; even a basic static page is needed
- [ ] **Cookie notice** — if adding Google Analytics, GDPR requires consent; Plausible Analytics avoids this requirement entirely
- [ ] **Terms of Use** (`terms.html`) — brief page covering: listings accuracy disclaimer, no endorsement of listed companies, SEAI registration verification reminder
- [ ] Add Privacy Policy and Terms links to the footer
- [ ] Consider whether the "List Your Business" contact form needs a GDPR-compliant privacy notice

---

## 🎨 7. Design & Content Polish

- [ ] **Logo** — the current logo is CSS-drawn (SVG inline). A proper designed logo in SVG format would strengthen the brand
- [ ] **Homepage hero image** — consider a background image of Irish homes (royalty-free; unsplash.com has suitable options). Currently solid green gradient, which is fine
- [ ] **About page** — add a real "who is behind this?" section if comfortable being named; builds trust
- [ ] **404 page** (`404.html`) — GitHub Pages will serve this automatically if it exists at the root
- [ ] Review all copy for Irish English spelling (e.g. "authorise" not "authorize", "programme" not "program")
- [ ] Add a **"Last updated"** date to each article so readers know the information is current

---

## ⚙️ 8. Technical & Quality

- [ ] **Mobile testing** — open on real iPhone and Android devices, not just browser DevTools
- [ ] **Accessibility audit** — run Lighthouse in Chrome DevTools; aim for 90+ on Accessibility score
- [ ] **Performance audit** — run Lighthouse; check for slow load on mobile
- [ ] **Cross-browser test** — Chrome, Firefox, Safari, Edge
- [ ] **Test all filter combinations** on directory.html
- [ ] **Test article pagination** — click through all 6 articles from news.html
- [ ] **Test search → directory** flow from homepage
- [ ] Verify all external links (seai.ie references) are not broken
- [ ] Consider **lazy loading** provider cards if the directory grows large

---

## 🚀 9. Launch & Growth

### Before going public
- [ ] **Remove `noindex` / `nofollow`** — delete `<meta name="robots" content="noindex, nofollow">` from all 5 HTML files (index, directory, news, about, article) and change `robots.txt` from `Disallow: /` to `Allow: /`
- [ ] Remove all fictional/placeholder providers from `providers.json`
- [ ] Remove all sample articles that have not been verified for accuracy
- [ ] Do a final proofread of all static page copy (about.html especially)
- [ ] Test site on production URL from a different device / network

### Outreach to get initial listings
- [ ] Draft a short email template for cold outreach to retrofit companies
- [ ] Target One-Stop-Shop approved contractors first (publicly listed by SEAI — high credibility)
- [ ] Post in relevant Irish Facebook groups (home renovation, Irish homeowners groups)
- [ ] Consider reaching out to SEAI press office to let them know the directory exists

### Ongoing content
- [ ] Set a schedule for publishing new articles (even one per fortnight keeps the site fresh)
- [ ] Monitor SEAI announcements for grant changes — these make timely articles
- [ ] Look out for local authority scheme announcements
- [ ] Seasonal content: "Get your attic insulated before winter" type articles work well

---

## 🗺️ 10. Google Maps & Reviews Integration

Enrich the directory with real-world trust signals pulled from Google.

- [ ] **Google Places API** — match each scraped provider by name + county to a Google Places record; pull: `place_id`, formatted address, website URL, rating, review count, opening hours
- [ ] **Store enriched fields in providers.json** — add `google_place_id`, `google_rating`, `google_review_count`, `website` (auto-filled from Places), `address`
- [ ] **Display on cards** — show star rating and review count badge on provider cards (e.g. "★ 4.7 · 38 reviews")
- [ ] **Link to Google Maps** — "View on Google Maps" link using place_id
- [ ] **Refresh strategy** — ratings change; plan a weekly/monthly re-scrape or use Places API webhooks
- [ ] **API cost estimate** — Places API charges per lookup; estimate cost at scale and set a budget cap
- [ ] Spawn a separate Claude Cowork project to build and run the Places enrichment script

---

## 📚 11. Resources Hub — Comprehensive Content

Build out the full library of guides that Irish homeowners actually search for.

### Full list of required resource topics
- [ ] SEAI Better Energy Homes — full grant amounts and eligibility (verify figures)
- [ ] SEAI One-Stop-Shop / National Home Energy Upgrade Scheme — how it works
- [ ] Local Authority Home Improvement Grants — county-by-county breakdown
- [ ] BER Ratings Explained — A to G, what each means, how to improve
- [ ] Heat Pump Installation — what to know before you buy
- [ ] Attic Insulation — step-by-step guide
- [ ] External Wall Insulation — costs, benefits, planning rules
- [ ] Internal Wall Insulation (Dry-Lining & Cavity) — when to use each
- [ ] Solar PV & Renewables — what Irish homeowners need to know
- [ ] Windows & Doors Upgrades — grants, U-values, what to specify
- [ ] Landlord BER Requirements — legal obligations, upgrade deadlines
- [ ] Retrofit Costs & Savings — realistic numbers for Irish homes
- [ ] Planning Permission for Retrofit — when you need it, ACAs, protected structures
- [ ] Airtightness — what it is, how it's tested, why it matters
- [ ] MVHR Ventilation — do you need it after a deep retrofit?
- [ ] How to Choose a Retrofit Contractor — red flags, questions to ask, checking SEAI register
- [ ] Deep Retrofit vs. Shallow Retrofit — what's the difference and which is right for you?
- [ ] Green Mortgages in Ireland — banks offering better rates for high-BER homes

---

## 🏆 12. Skyscraper Content Strategy

Create content that is measurably better than the current #1 Google Ireland results for high-value keywords. Spawn as a dedicated Claude Cowork research project.

- [ ] **Define target keywords** (suggested starting list):
  - "SEAI grants Ireland 2025"
  - "heat pump grant Ireland"
  - "retrofit grant Ireland"
  - "BER assessment cost Ireland"
  - "external wall insulation cost Ireland"
  - "attic insulation grant Ireland"
  - "solar panels grant Ireland"
  - "one stop shop retrofit Ireland"
  - "how to improve BER rating Ireland"
  - "retrofit contractor Ireland"
  - (add 10 more long-tail variants)
- [ ] **Research phase** — for each keyword: find the current #1 Google Ireland result, audit its word count, structure, freshness, depth, and trust signals
- [ ] **Gap analysis** — identify what the top result is missing (outdated grant figures, no county breakdown, no real contractor data, etc.)
- [ ] **Write 5–10× better versions** — more current, more specific, richer with real data, properly structured with H2/H3, internal links to the directory
- [ ] **Spawn a Claude Cowork project** to handle the research and drafting pipeline for all 10–20 target keywords
- [ ] Each article to include: current grant amounts (verified at seai.ie), real contractor links (to directory), schema markup, last-verified date

---

## 🤖 13. Schema & Structured Data (SEO + AI Discovery)

Make the site readable by both search engines and AI answer engines (ChatGPT, Perplexity, Google AI Overviews).

- [ ] **LocalBusiness schema** (JSON-LD) on every provider card — include: name, address, telephone, email, url, areaServed, serviceType
- [ ] **FAQPage schema** on resource articles — mark up common questions so Google shows them as rich results
- [ ] **Article schema** on all news/guide pages — include: headline, datePublished, dateModified, author, publisher
- [ ] **BreadcrumbList schema** on all inner pages
- [ ] **WebSite schema** with SearchAction on homepage — enables Google Sitelinks search box
- [ ] **speakable** schema on key fact sections — helps AI assistants read and cite the content
- [ ] Add `<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">` to all pages
- [ ] Verify all schema with Google's Rich Results Test after implementation
- [ ] Add `hreflang="en-ie"` to signal Irish English content to search engines

---

## 🧪 14. Full Site UX Test

Do a structured end-to-end test before any public launch.

- [ ] **Homepage** — hero search works, links to directory with pre-filled search term; featured cards render; latest news renders; category grid all links work
- [ ] **Directory** — all filters work in combination; clear filter resets all; county dropdown auto-populates from data; results count is accurate; empty state shows correctly; cards show correct contact links
- [ ] **News listing** — all category pills filter correctly; "All" shows all articles sorted newest first
- [ ] **Article detail** — all 6 articles open correctly via `?id=` param; back link works; page title updates in browser tab
- [ ] **About page** — "Send a Listing Request" mailto link works; "Get in touch" mailto works; anchor links (#list-your-business, #contact) scroll correctly
- [ ] **Mobile** — test all pages on real iPhone and Android (not just DevTools); check hamburger menu, card layout, filter bar, hero search
- [ ] **Cross-browser** — Chrome, Firefox, Safari, Edge
- [ ] **Slow connection** — throttle to "Slow 3G" in DevTools; loading spinners should show; fetch should complete within 5 seconds
- [ ] **No-JS fallback** — disable JavaScript; confirm meaningful content is still visible
- [ ] **Accessibility** — run Lighthouse; fix any issues scoring below 90

---

## 📈 15. Google Search Console & Analytics

- [ ] **Verify site** in Google Search Console (HTML tag method works well with GitHub Pages)
- [ ] **Submit sitemap** — create sitemap.xml listing all 5 pages with their canonical URLs; submit in GSC
- [ ] **Request indexing** for each page after first deployment
- [ ] **Set up Google Analytics 4** or **Plausible Analytics** (recommended — GDPR-friendly, no cookie banner needed)
- [ ] Add tracking snippet to all pages
- [ ] Set up a GSC alert for any crawl errors or manual actions
- [ ] Monitor Core Web Vitals report — LCP, CLS, INP targets

---

## ✍️ 16. Editorial Content Plan — 25 Articles Over 12 Months

One article every ~2 weeks keeps the site fresh for Google and gives homeowners reason to return.

### Proposed schedule (adjust dates to match launch)

| # | Title | Category | Target month |
|---|---|---|---|
| 1 | SEAI Grants 2025 — Complete Guide | SEAI Grants | Month 1 |
| 2 | How to Insulate Your Attic | How-To | Month 1 |
| 3 | What Is a BER Rating? | How-To | Month 2 |
| 4 | Heat Pumps in Ireland — The Full Story | How-To | Month 2 |
| 5 | Local Authority Grants — County Breakdown | Local Auth | Month 3 |
| 6 | External Wall Insulation — Costs & Grants | How-To | Month 3 |
| 7 | Planning Permission for Retrofit Works | Planning | Month 4 |
| 8 | One-Stop-Shop Retrofit — Is It Worth It? | How-To | Month 4 |
| 9 | Solar PV in Ireland — 2025 Guide | How-To | Month 5 |
| 10 | Landlord BER Requirements | Planning | Month 5 |
| 11 | Green Mortgages — Which Banks Offer Them? | Market News | Month 6 |
| 12 | Retrofit Costs — Real Numbers | How-To | Month 6 |
| 13 | Windows & Doors — Grants and What to Buy | How-To | Month 7 |
| 14 | Airtightness Testing — What to Expect | How-To | Month 7 |
| 15 | SEAI Grant Updates — Mid-Year Review | SEAI Grants | Month 8 |
| 16 | MVHR Ventilation Explained | How-To | Month 8 |
| 17 | How to Choose a Retrofit Contractor | How-To | Month 9 |
| 18 | Internal Wall Insulation — Dry-Lining vs Cavity | How-To | Month 9 |
| 19 | Deep Retrofit vs Shallow Retrofit | How-To | Month 10 |
| 20 | Local Authority Grants — Winter Update | Local Auth | Month 10 |
| 21 | Heat Pump Market — Annual Review | Market News | Month 11 |
| 22 | SEAI Grants 2026 — What's Changed | SEAI Grants | Month 11 |
| 23 | Retrofit ROI — Payback Periods by Measure | How-To | Month 12 |
| 24 | Ireland's Retrofit Progress — Year in Review | Market News | Month 12 |
| 25 | Complete Retrofit Checklist for Irish Homeowners | How-To | Month 12 |

- [ ] Each article: minimum 800 words, verified facts, internal links to directory and related articles, schema markup, last-verified date visible to readers
- [ ] Spawn a **dedicated Claude Cowork project** for research and drafting — feed it the keyword targets and skyscraper briefs from Section 12

---

## 💡 17. Future Features (Post-Launch)

Not needed for launch, but worth planning for.

- [ ] **Grant calculator** — input house type/size/current BER, output estimated grant and cost
- [ ] **"Get quotes" contact form** per provider (Netlify Forms or Formspree work with static sites)
- [ ] **Provider self-service listings** — form for companies to submit their own details
- [ ] **Newsletter / email list** — capture homeowners who want grant updates (Mailchimp or ConvertKit)
- [ ] **Interactive county map** — visual map of Ireland linking to filtered directory results
- [ ] **Case studies** — before/after retrofit stories from real homeowners
- [ ] **Podcast or video embeds** — retrofit walkthroughs perform well on YouTube

---

*Last updated: May 2026*
