#!/usr/bin/env python3
"""Assemble the Hope Plastics site: wraps each page fragment in the shared layout
and copies assets into dist/. No dependencies beyond the standard library."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"

NAV = [
    ("design.html", "Design"),
    ("prototypes.html", "Prototypes"),
    ("mold-making.html", "Mold making"),
    ("molding.html", "Molding"),
    ("materials.html", "Materials"),
    ("gallery.html", "Gallery"),
    ("contact.html", "Contact"),
]

LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/k3kQo8UDI-1M0wlSfdnoLg.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/css/site.css">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="assets/img/mold-cavity.jpg">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Hope Plastics, Inc.",
  "description": "Family-owned injection molding, over-molding, mold making and product design in North Hollywood, California, since 1964.",
  "telephone": "+1-818-769-5560",
  "faxNumber": "+1-818-769-5140",
  "email": "info@hopeplastics.com",
  "foundingDate": "1964",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "5353 Strohm Avenue",
    "addressLocality": "North Hollywood",
    "addressRegion": "CA",
    "postalCode": "91601",
    "addressCountry": "US"
  }}
}}
</script>
</head>
<body class="page-{slug}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <a class="wordmark" href="index.html" aria-label="Hope Plastics home">
    <span class="wordmark-name">Hope Plastics</span>
    <span class="wordmark-place">North Hollywood, since 1964</span>
  </a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">
    <span class="nav-toggle-bars" aria-hidden="true"></span>Menu
  </button>
  <nav id="site-nav" class="site-nav">
    <ul>
{nav_items}
    </ul>
    <a class="masthead-phone" href="tel:+18187695560">818-769-5560</a>
  </nav>
</header>
<main id="main">
{content}
</main>
<footer class="colophon">
  <div class="colophon-grid">
    <div>
      <p class="colophon-name">Hope Plastics, Inc.</p>
      <p>5353 Strohm Avenue<br>North Hollywood, CA 91601</p>
    </div>
    <div>
      <p><a href="tel:+18187695560">818-769-5560</a><br>Fax 818-769-5140</p>
      <p><a href="mailto:info@hopeplastics.com">info@hopeplastics.com</a></p>
    </div>
    <div>
      <p>Bill Borden, design and mold making<br>Steve Borden, molding operations</p>
    </div>
    <div class="colophon-note">
      <p>Family owned and operated since 1964. This is our only website; hopeplastics.com is the only address we use.</p>
    </div>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def nav_html(current: str) -> str:
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'      <li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(out)


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(SRC / "assets", DIST / "assets")
    for extra in ("CNAME", ".nojekyll", "robots.txt"):
        if (SRC / extra).exists():
            shutil.copy(SRC / extra, DIST / extra)
    for page in sorted((SRC / "pages").glob("*.html")):
        text = page.read_text(encoding="utf-8")
        m = re.match(r"<!--\s*title:(.*?)\n\s*description:(.*?)\n-->\n", text, re.S)
        if not m:
            raise SystemExit(f"{page.name}: missing title/description header")
        title, desc = m.group(1).strip(), m.group(2).strip()
        body = text[m.end():]
        html = LAYOUT.format(
            title=title,
            description=desc,
            slug=page.stem,
            nav_items=nav_html(page.name),
            content=body,
        )
        (DIST / page.name).write_text(html, encoding="utf-8")
        print("built", page.name)
    pages = sorted(p.name for p in (SRC / "pages").glob("*.html"))
    urls = "".join(
        f"  <url><loc>https://hopeplastics.com/{'' if n == 'index.html' else n}</loc></url>\n"
        for n in pages
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
