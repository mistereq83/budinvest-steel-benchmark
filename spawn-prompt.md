# Task

Build a cinematic, production-grade homepage for **Bud Invest Steel** — an industrial company specializing in steel construction, metalworking, pipelines, pressure vessels, and concrete prefabrication. 15+ years experience, operating in Poland and Germany.

## Requirements
1. Output: A SINGLE `index.html` file with ALL CSS and JS inline (no external files except Google Fonts and GSAP CDN)
2. Use GSAP 3 + ScrollTrigger for animations (CDN: https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js and ScrollTrigger)
3. Use Google Fonts (specified in the variant brief below)
4. Mobile-responsive (mobile-first, works on 375px iPhone SE)
5. Include the company logo as inline SVG in the navbar and footer
6. Language: Polish
7. DO NOT use React/Vue/framework — pure HTML + CSS + vanilla JS + GSAP
8. All images: use Unsplash URLs matching the mood. Include onError fallback.
9. The file must be self-contained and viewable by opening in a browser

## Company Info
- **Name:** Bud Invest Steel
- **Tagline:** Stabilna i doświadczona marka
- **Description:** Międzynarodowa firma z 15+ letnim doświadczeniem. Kompleksowa realizacja projektów konstrukcji stalowych, obróbka metali, prefabrykacja elementów betonowych.
- **Certyfikaty:** EN ISO 3834, EN 1090, Świadectwo spawalnicze
- **Services:** Obróbka metali | Konstrukcje stalowe | Rurociągi przemysłowe | Zbiorniki ciśnieniowe | Prefabrykacja betonu | Zbrojenia budowlane
- **Industries:** Chemiczny, petrochemiczny, energetyczny, papierniczy, farmaceutyczny, spożywczy, stoczniowy, offshore
- **Stats:** 15+ lat doświadczenia | Rynki: Polska & Niemcy | Certyfikaty EN 1090 & ISO 3834
- **CTA:** "Zapytaj o wycenę"
- **Address:** ul. Dworcowa 12, 83-100 Tczew | tel. +48 511 641 580 | kontakt@bud-invest.com
- **Social proof:** Certyfikaty EN ISO 3834, EN 1090; 15+ lat; rynki PL/DE

## Homepage Sections (in order)
1. **Hero (100dvh)** — Full-screen with powerful headline, subtext, CTA button "Zapytaj o wycenę"
2. **O firmie** — Short about section with key stats (15+ lat, certyfikaty, rynki PL/DE)
3. **Usługi** — 5-6 service cards: Obróbka metali, Konstrukcje stalowe, Rurociągi przemysłowe, Zbiorniki ciśnieniowe, Prefabrykacja betonu, Zbrojenia budowlane
4. **Certyfikaty** — Highlighted section showing EN ISO 3834, EN 1090, Świadectwo spawalnicze
5. **Realizacje** — Project gallery section (use Unsplash industrial/steel images)
6. **CTA Section** — "Zapytaj o wycenę" with contact form or prominent button
7. **Footer** — Company info, address, phone, email, links

## Logo SVG (use inline)
Use this SVG for the logo in navbar (white version on dark backgrounds):
```svg
<svg width="150" height="47" viewBox="0 0 150 47" fill="none" xmlns="http://www.w3.org/2000/svg"><text x="0" y="35" font-family="Arial Black, sans-serif" font-size="16" font-weight="900" fill="currentColor" letter-spacing="2">BUD INVEST</text><text x="0" y="47" font-family="Arial, sans-serif" font-size="10" fill="currentColor" letter-spacing="4">STEEL</text></svg>
```
(Use color="white" on dark backgrounds, color="#1A1A1A" on light backgrounds)

## Design Rules (Cinematic Quality)
- Global CSS noise overlay (feTurbulence filter, 0.03 opacity) — depth, not flat
- Rounded containers (border-radius: 1.5rem-2rem)
- Magnetic buttons: scale(1.03) on hover with smooth easing
- GSAP scroll animations: staggered reveals, parallax effects
- Section transitions: gradient fades between sections
- Typography: strong hierarchy, heading vs drama font contrast
- All interactive elements: translateY(-1px) lift on hover
- Stagger: 0.08 for text, 0.15 for cards

IMPORTANT: Make this feel like a premium industrial website, NOT a generic template. Every detail matters. The design should feel heavy, solid, and powerful — like steel itself.
