# Onderhoudsnotities – updatemonitor.app

> Interne notities van de beheerder (Nederlands). De publieke uitleg staat in [README.md](README.md).

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

## Automatisch bij elke push (GitHub Actions)

Bij een push die HTML-pagina's wijzigt, draaien twee workflows (`.github/workflows/`):

- **Update sitemap lastmod**: zet `lastmod` in `sitemap.xml` voor de gewijzigde pagina's en voegt nieuwe indexeerbare pagina's toe (commit door `github-actions[bot]`; daarna eerst `git pull`).
- **Submit changed pages to Bing**: meldt de gewijzigde pagina's aan bij de Bing Webmaster API. Vereist het repository-secret `BING_API_KEY` (Settings → Secrets and variables → Actions).
