# 🚀 Viral Launch Playbook

A step-by-step plan to take this repo from 0 → trending, modeled on what made the viral Turkish fitness-exercise dataset work: **a genuinely useful, ready-to-use dataset + a clean README + a relatable "I made this so you don't have to" story.**

---

## 0. The 5 things that actually drive stars

1. **A clear "starter pack" promise** — "everything you need to build X." Yours: *build a skincare app without scraping data.*
2. **A README that sells in 5 seconds** — badges, a preview table, one screenshot/GIF. ✅ done.
3. **One unique hook nobody else has** — yours is the **compatibility engine** ("can I mix retinol + vitamin C?"). Lead with it.
4. **A live demo** — people share things they can *click*. ✅ `demo/index.html` → host on GitHub Pages.
5. **A founder story posted by a real human**, not a faceless repo. The fitness dataset went viral because a developer said *"I built this, eline sağlık, use it."*

---

## 1. Before you post (the 30-minute prep)

- [ ] Replace `bsyilmaz` / `Bayram Selim Yılmaz` in `README.md`, `LICENSE`, `demo/_template.html`, then re-run `python3 scripts/build.py`.
- [ ] Push to GitHub. Repo name suggestion: **`skincare-ingredients-dataset`** (exact, searchable).
- [ ] Add GitHub **topics**: `dataset`, `skincare`, `cosmetics`, `beauty`, `ingredients`, `json`, `open-data`, `inci`, `api`.
- [ ] Enable **GitHub Pages** (Settings → Pages → deploy from `main` / root). Your demo will be at
      `https://bsyilmaz.github.io/skincare-ingredients-dataset/demo/`.
- [ ] Set the repo's **Website** field to that Pages URL.
- [ ] Upload `assets/social-banner.svg` (or a PNG export) as the **social preview** (Settings → General → Social preview). This is the image that shows when the link is shared — it massively affects click-through.
- [ ] Record a 10–15s screen capture of the Mix Checker in action → drop it in the README as a GIF.
- [ ] Pin one "good first issue" (e.g. "Add 5 ingredients") so newcomers can contribute instantly.

---

## 2. Where to post (in priority order)

| Platform | What works | Best time (UTC) |
|---|---|---|
| **X / Twitter** | Short founder story + demo GIF + repo link. Tag dev + indie-hacker accounts. | Tue–Thu, 14:00–17:00 |
| **Reddit** | r/SideProject, r/webdev, r/opensource, r/coolgithubprojects, r/SkincareAddiction (frame as a free tool, read each sub's self-promo rules) | Tue–Thu, 13:00–15:00 |
| **Hacker News** | "Show HN: Open skincare ingredients dataset with a mixing-compatibility engine" | Tue–Thu, 13:00–16:00 |
| **LinkedIn** | The professional founder-story version. Great for reach if you have a network. | Tue–Thu, 08:00–10:00 |
| **Dev.to / Hashnode** | A short article: "I open-sourced a skincare ingredients dataset — here's the schema." | Any weekday AM |
| **Turkish dev communities** | Same story in Turkish (see §4). Local pride drove the fitness repo's first 1K stars. | Evenings |
| **Product Hunt** | Optional, once you have the demo + GIF polished. | 00:01 PST launch |

> **Don't post everywhere at once.** Start with X + one subreddit + your Turkish community on day 1. If it gets traction, do Hacker News "Show HN" on day 2–3 while there's momentum.

---

## 3. Copy you can paste

**X / Twitter (English):**
> I kept hitting the same wall building a skincare app: there's no clean ingredient dataset. So I open-sourced one.
>
> 🧴 128 ingredients — function, benefits, skin-type fit, comedogenic rating, pregnancy safety
> ⚗️ + a compatibility engine: "can I mix retinol & vitamin C?" → structured answer
>
> Free, MIT. Live demo 👇 ⭐ if useful

**Hacker News (Show HN):**
> **Show HN: Open skincare ingredients dataset with a mixing-compatibility engine**
> I couldn't find a structured, app-ready dataset of skincare ingredients — existing ones are raw INCI/CAS identifiers or locked in commercial DBs. This has 128 ingredients with plain-language profiles (benefits, skin types, comedogenic rating, pregnancy safety, evidence level) plus a machine-readable rules file for ingredient compatibility (retinol + AHA = caution, etc.). JSON/CSV, zero-dependency tooling, MIT. Feedback welcome — especially on accuracy.

**Reddit (r/SideProject):**
> **I open-sourced a skincare ingredients dataset (128 ingredients + a "what can I mix" engine)**
> Built for anyone making a skincare app, AI routine-builder, or ingredient scanner. Plain-language data, every format, live demo, MIT-licensed. Trying to grow it to 1,000+ with the community — PRs for a single ingredient are welcome. Link + demo inside.

---

## 4. The Turkish angle (high-leverage)

The fitness dataset's first wave came from Turkish developers rallying behind a local builder. Do the same:

> Skincare uygulaması ya da yapay zeka cilt bakım asistanı yapmak isteyenler için açık kaynak bir veri seti hazırladım: **128 içerik** — fonksiyon, fayda, cilt tipi uyumu, komedojeniklik, gebelik güvenliği, kanıt düzeyi. Üstüne bir de **"hangi içerikleri birlikte kullanabilirim?"** uyumluluk motoru (retinol + C vitamini = dikkat, vb.).
>
> Tamamen ücretsiz, MIT lisanslı. Canlı demo aşağıda. Faydalı bulursanız ⭐ atın, kullanın, paylaşın. 🧴

Post it in Turkish dev Discord/Telegram groups, Twitter with Turkish dev hashtags, and tag people who shared the fitness dataset.

---

## 5. Sustaining momentum (week 1–4)

- **Reply to every comment and issue fast.** Early responsiveness = trust = stars.
- **Ship visible updates:** "Added 20 ingredients 🎉", "Now 200 ingredients thanks to contributors." Each is a fresh post.
- **Turn contributors into co-owners** — thank them by name, add a Contributors section. People star repos they're part of.
- **Cross-pollinate:** if a skincare app uses your data, ask them to link back; add a "Used by" list.
- **Add a `good first issue` label** to 5–10 small tasks. Hacktoberfest-style energy works year-round for datasets.
- **Post a "how it's going" update** at 500 and 1,000 stars — milestone posts get their own bump.

---

## 6. Metrics to watch

- ⭐ Stars per day (is it accelerating?)
- Traffic sources (GitHub Insights → Traffic) — double down on whatever's sending visitors
- Demo page visits (add a privacy-friendly counter if you like)
- Issues/PRs opened — the real signal that it's becoming a *project*, not just a post

---

**North star:** don't optimize for one viral spike. Optimize for becoming *the* dataset people link to when they say "where do I get skincare ingredient data?" That reputation compounds far longer than a day on the front page.
