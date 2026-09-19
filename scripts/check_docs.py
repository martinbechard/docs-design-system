#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance by Northstar.
"""Check deterministic documentation contracts, without claiming rendered conformance."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "docs/design-system"


class Page(HTMLParser):
    """Collect authored references and identity markers, not text inside code specimens."""

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = []
        self.links = []
        self.versions = []
        self.footer_versions = []
        self.navigation = []
        self.in_suite = False
        self.in_version = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for attribute in ("href", "src"):
            if attrs.get(attribute):
                self.links.append(attrs[attribute])
        if attrs.get("name") == "design-system-version":
            self.versions.append(attrs.get("content"))
        if tag == "nav":
            self.in_suite = "suite-nav" in attrs.get("class", "").split() and "suite-nav--specimen" not in attrs.get("class", "").split()
        if tag == "a" and self.in_suite:
            self.navigation.append((attrs.get("href"), attrs.get("aria-current")))
        if tag == "span" and "ds-version" in attrs.get("class", "").split():
            self.in_version = True

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_suite = False
        if tag == "span":
            self.in_version = False

    def handle_data(self, data):
        if self.in_version:
            self.footer_versions.append(data.strip())


def check():
    """Keep broken links or stale contract markers out of the published artifact."""
    root = ROOT.resolve()
    pages = {p.resolve(): Page(p) for p in root.rglob("*.html")}
    version = (ROOT / "VERSION").read_text().strip()
    expected_nav = ["index.html", "getting-started.html", "foundations.html", "page-shell.html", "content.html", "data-display.html", "forms-and-actions.html", "diagrams.html", "accessibility.html", "variations.html", "source-inventory.html"]
    errors = []
    for path, page in pages.items():
        def fail(message):
            errors.append(f"{path.relative_to(root)}: {message}")
        duplicates = [name for name, count in Counter(page.ids).items() if count > 1]
        if duplicates:
            fail(f"duplicate IDs: {duplicates}")
        if page.versions != [version] or not page.footer_versions or any(value != f"Design system v{version}" for value in page.footer_versions):
            fail("metadata/footer version differs from VERSION")
        if path.parent == root:
            if [href for href, _ in page.navigation] != expected_nav:
                fail("catalog navigation destinations or order differ")
            if [href for href, current in page.navigation if current == "page"] != [path.name]:
                fail("catalog current-page marker differs")
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                fail(f"missing local target: {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                fail(f"missing fragment: {link}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(pages)} HTML pages: local links, fragments, IDs, versions, and catalog navigation pass.")


if __name__ == "__main__":
    check()
