#!/usr/bin/env python3
"""Generate /en/ and /th/ pages from the Vietnamese source pages.

Vietnamese HTML at the site root is the single source of truth. This script
applies i18n/translations.json and rewrites paths/metadata for each locale.
It fails if any Vietnamese text is left untranslated, so a missing string
can never ship silently.

Usage: python3 i18n/build-localized-pages.py   (run from the site root)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://mindkitelabs.com"
# source page -> locales to generate (Thai links to the English legal pages)
PAGES = {"index.html": ["en", "th"], "privacy.html": ["en"], "terms.html": ["en"]}
THAI_FONT = "family=Be+Vietnam+Pro:wght@400;600&family=Noto+Sans+Thai:wght@400;600"
# characters that exist in Vietnamese but never in English or Thai output
VIETNAMESE = re.compile(r"[ăâđêôơưàảãáạằẳẵắặầẩẫấậèẻẽéẹềểễếệìỉĩíịòỏõóọồổỗốộờởỡớợùủũúụừửữứựỳỷỹýỵ]", re.I)
ATTRS = re.compile(r'\b(content|aria-label|title|alt)="([^"]*)"')
TEXT = re.compile(r">([^<]+)<")


def load_dictionary():
    data = json.loads((ROOT / "i18n" / "translations.json").read_text(encoding="utf-8"))
    return data["raw"], data["text"]


def translate_text(html, table):
    def node(m):
        raw = m.group(1)
        key = raw.strip()
        if key not in table:
            return m.group(0)
        lead = raw[: len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        return f">{lead}{table[key]}{trail}<"

    def attr(m):
        value = m.group(2)
        return f'{m.group(1)}="{table.get(value, value)}"'

    return ATTRS.sub(attr, TEXT.sub(node, html))


def rewrite_paths(html, page, lang):
    url = f"{SITE}/{lang}/" + ("" if page == "index.html" else page)
    html = html.replace('<html lang="vi"', f'<html lang="{lang}"')
    html = re.sub(r'(<link rel="canonical" href=")[^"]*(")', rf"\g<1>{url}\g<2>", html)
    html = re.sub(r'(<meta property="og:url" content=")[^"]*(")', rf"\g<1>{url}\g<2>", html)
    # relative asset paths break one directory down
    html = re.sub(r'(href|src)="(assets/|favicon\.svg)', r'\1="/\2', html)
    legal = "/en/"
    # skip switcher links (they carry hreflang) so the VI option keeps pointing at the VI page
    html = re.sub(r'href="/?(privacy|terms)\.html"(?! hreflang)', rf'href="{legal}\1.html"', html)
    html = html.replace('class="brand" href="/"', f'class="brand" href="/{lang}/"')
    html = html.replace('href="/#lien-he"', f'href="/{lang}/#lien-he"')
    html = html.replace('<a href="/">', f'<a href="/{lang}/">')
    # language switcher: mark the current locale (switcher hrefs are absolute and untouched above)
    html = html.replace(' lang="vi" aria-current="page">', ' lang="vi">')
    html = re.sub(rf'(hreflang="{lang}" lang="{lang}")>', r'\1 aria-current="page">', html)
    html = html.replace('<span class="lang-code">VI</span>', f'<span class="lang-code">{lang.upper()}</span>')
    if lang == "th":
        html = html.replace("family=Be+Vietnam+Pro:wght@400;600", THAI_FONT)
        html = html.replace('font-family="Be Vietnam Pro, sans-serif"', 'font-family="Be Vietnam Pro, Noto Sans Thai, sans-serif"')
    return html


def leftovers(html):
    body = re.sub(r"<(script|style)[\s\S]*?</\1>", "", html)
    # the language menu names each language in its own script on purpose
    body = re.sub(r'<a [^>]*lang="vi"[^>]*>[^<]*</a>', "", body)
    found = [t.strip() for t in TEXT.findall(body) if VIETNAMESE.search(t)]
    found += [v for _, v in ATTRS.findall(body) if VIETNAMESE.search(v)]
    return found


def main():
    raw_pairs, text_pairs = load_dictionary()
    failed = False
    for page, locales in PAGES.items():
        source = (ROOT / page).read_text(encoding="utf-8")
        for lang in locales:
            html = source
            for pair in raw_pairs:
                if pair["vi"] in html and lang in pair:
                    html = html.replace(pair["vi"], pair[lang])
            table = {p["vi"]: p[lang] for p in text_pairs if lang in p}
            html = rewrite_paths(translate_text(html, table), page, lang)
            missing = leftovers(html)
            if missing:
                failed = True
                print(f"[{lang}/{page}] untranslated:", *missing, sep="\n  - ")
            out = ROOT / lang / page
            out.parent.mkdir(exist_ok=True)
            out.write_text(html, encoding="utf-8")
            print(f"wrote {out.relative_to(ROOT)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
