# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance by Northstar.
"""Verify the publication gate catches regressions on otherwise valid documents."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import check_docs


class DocumentationGateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "catalog"
        shutil.copytree(check_docs.ROOT, self.root)
        override = patch.object(check_docs, "ROOT", self.root)
        override.start()
        self.addCleanup(override.stop)

    def change(self, relative, before, after):
        page = self.root / relative
        text = page.read_text()
        self.assertIn(before, text)
        page.write_text(text.replace(before, after, 1))

    def test_missing_asset_blocks_publication(self):
        (self.root / "assets/design-system.css").unlink()
        with self.assertRaisesRegex(SystemExit, "missing local target"):
            check_docs.check()

    def test_broken_fragment_blocks_publication(self):
        self.change("examples/first-page.html", 'href="#overview"', 'href="#missing"')
        with self.assertRaisesRegex(SystemExit, "missing fragment"):
            check_docs.check()

    def test_stale_consumer_version_blocks_publication(self):
        self.change("templates/page.html", 'content="0.2.0"', 'content="0.1.0"')
        with self.assertRaisesRegex(SystemExit, "version differs"):
            check_docs.check()

    def test_duplicate_ids_block_publication(self):
        self.change("examples/first-page.html", 'id="steps"', 'id="overview"')
        with self.assertRaisesRegex(SystemExit, "duplicate IDs"):
            check_docs.check()

    def test_wrong_current_page_blocks_publication(self):
        self.change("index.html", 'href="index.html" aria-current="page">Index', 'href="index.html">Index')
        with self.assertRaisesRegex(SystemExit, "current-page marker"):
            check_docs.check()


if __name__ == "__main__":
    unittest.main()
