#!/usr/bin/env python3
"""Builds the per-game legal pages (privacy, terms, support) from games/<slug>/content/*.html.

Each content file holds only the <main> body. This script wraps it in the site header/footer so
every game page matches the rest of mindkitelabs.com. Run: python3 games/build-game-legal-pages.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://mindkitelabs.com"

GAMES = {
    "midnight-inn": "The Midnight Inn",
}
PAGES = {
    "privacy": ("Privacy Policy", "How {game} collects, uses and protects player information."),
    "terms": ("Terms of Use", "The terms for playing {game}."),
    "support": ("Support", "Help, account, purchase and data requests for {game}."),
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {game} — MindKite Labs</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{site}/games/{slug}/{page}.html">
  <meta name="theme-color" content="#051c2c">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600&display=swap">
  <link rel="stylesheet" href="/assets/base.css">
</head>
<body>
<header class="site-header scrolled">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="/en/" aria-label="MindKite Labs, home">
      <svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="6" fill="#051c2c"/><path d="M16 4l8 9-8 15-8-15z" fill="#2251ff"/><path d="M16 4l8 9h-8z" fill="#00a9f4"/><path d="M16 4v24M8 13h16" stroke="#fff" stroke-width="1.2"/></svg>
      MindKite <span>Labs</span>
    </a>
    <a class="btn btn-primary" href="mailto:support@mindkitelabs.com">Contact</a>
  </nav>
</header>
<main class="wrap legal">
{body}
<p class="legal-nav"><a href="/games/{slug}/privacy.html">Privacy Policy</a> · <a href="/games/{slug}/terms.html">Terms of Use</a> · <a href="/games/{slug}/support.html">Support</a></p>
</main>
<footer class="site-footer">
  <div class="wrap">
    <p><a href="/en/">MindKite Labs</a> · <a href="/en/privacy.html">Website privacy policy</a> · <a href="/en/terms.html">Website terms of use</a></p>
    <p class="footer-note">© 2026 MindKite Labs. {game} is published on the App Store by An Tran (MindKite Labs).</p>
  </div>
</footer>
</body>
</html>
"""


def main() -> None:
    for slug, game in GAMES.items():
        for page, (title, description) in PAGES.items():
            body = (ROOT / slug / "content" / f"{page}.html").read_text(encoding="utf-8").strip()
            html = TEMPLATE.format(title=title, game=game, slug=slug, page=page, site=SITE,
                                   description=description.format(game=game), body=body)
            (ROOT / slug / f"{page}.html").write_text(html, encoding="utf-8")
            print(f"games/{slug}/{page}.html")


if __name__ == "__main__":
    main()
