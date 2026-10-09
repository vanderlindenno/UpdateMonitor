# UpdateMonitor – website

Source of **[updatemonitor.app](https://updatemonitor.app/)**, the website of **UpdateMonitor**, a privacy-first Android app that keeps a history of every app update, install and removal on your phone.

## About the app

- History of app updates, installs and removals, with a calendar view
- Overview of which apps can use sensitive permissions such as camera, microphone and location
- Warnings about newly granted permissions and apps installed from outside the Play Store
- Export for IT support
- Free, no ads, no account, no internet permission. All data stays on the device.
- Available in English and Norwegian

The Android app is on its way to Google Play. Made by Nordic Appworks, who also make [RebootMonitor](https://rebootmonitor.com/).

## Pages

| Page | Topic |
|------|-------|
| [Home](https://updatemonitor.app/) | Overview, screenshots, FAQ |
| [Norsk](https://updatemonitor.app/no/) | Norwegian homepage |
| [Guides](https://updatemonitor.app/guides/) | How-to guides |
| [Android app permissions](https://updatemonitor.app/guides/android-app-permissions.html) | See which apps can use what |
| [Android app update history](https://updatemonitor.app/guides/android-app-update-history.html) | Find when an app was last updated |
| [Apps outside the Play Store](https://updatemonitor.app/guides/find-apps-outside-play-store.html) | Spot sideloaded apps |
| [Privacy policy](https://updatemonitor.app/privacy.html) | What the app and the website do with data |

## About this repository

A plain static website hosted on GitHub Pages, without analytics or tracking. After a push that changes pages, two GitHub Actions update `lastmod` in `sitemap.xml` and notify Bing about the changed pages.

Found an error on the site? Please [open an issue](https://github.com/vanderlindenno/UpdateMonitor/issues).

© 2026 Nordic Appworks. All rights reserved.

---

## Maintainer notes (Dutch)

Website voor de Android-app UpdateMonitor (Nordic Appworks), gehost op GitHub Pages met eigen domein `updatemonitor.app`. Zelfde opzet als rebootmonitor.com.

- `index.html` — homepagina (functies, screenshots, privacy, contactformulier via Formspree)
- `privacy.html` — privacybeleid (de URL voor de Play Console: `https://updatemonitor.app/privacy.html`)
- `404.html`, `robots.txt`, `sitemap.xml`, `.nojekyll`
- `img/` — banner, screenshots, iconen; gemaakt vanuit de app-repo (`Android-Apps/UpdateMonitor`)

## Live zetten

1. **Repo aanmaken** op GitHub, bijvoorbeeld `vanderlindenno/UpdateMonitor` (publiek, zonder README), en deze map pushen:

   ```bash
   git remote add origin https://github.com/vanderlindenno/UpdateMonitor.git
   git push -u origin main
   ```

2. **GitHub Pages aanzetten**: Settings → Pages → *Deploy from a branch* → `main` / `/ (root)`.
3. **Eigen domein**: het bestand `CNAME` bevat `updatemonitor.app` (sinds 7 oktober 2026, toen de DNS bij Porkbun klaarstond). Settings → Pages → *Enforce HTTPS* aanzetten zodra GitHub het certificaat heeft; `.app` werkt alleen via HTTPS.
4. **DNS bij de registrar** (bijvoorbeeld Porkbun, zoals rebootmonitor.com):

   | Type | Host | Waarde |
   |------|------|--------|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | AAAA | `@` | `2606:50c0:8000::153` |
   | AAAA | `@` | `2606:50c0:8001::153` |
   | AAAA | `@` | `2606:50c0:8002::153` |
   | AAAA | `@` | `2606:50c0:8003::153` |
   | CNAME | `www` | `vanderlindenno.github.io` |

   Verwijder eventuele standaard parkeerrecords van de registrar (ALIAS/URL-forward naar `@`).
5. **HTTPS afdwingen**: zodra GitHub het certificaat heeft uitgegeven (kan tot een uur duren), *Enforce HTTPS* aanvinken. `.app`-domeinen werken alleen via HTTPS; de site is pas bereikbaar als het certificaat er is.
6. **Domein verifiëren** (aanbevolen): GitHub → profiel-Settings → Pages → *Add a domain*, en het TXT-record toevoegen dat GitHub geeft. Dat voorkomt dat iemand anders het domein aan een eigen repo koppelt.

## Na de lancering op Google Play

In `index.html` het blok "Available on Google Play" aanpassen: de badges "Coming soon" weghalen en de knop een link geven naar
`https://play.google.com/store/apps/details?id=app.updatemonitor.mobile`.
