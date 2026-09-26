"""Offline behavior checks for brand freshness detection; no live website mutations."""

import importlib.util
import json
from pathlib import Path
import unittest

SKILL = Path(__file__).resolve().parents[1] / 'plugins/wizlex-office/skills/wizlex-branding'
SPEC = importlib.util.spec_from_file_location('check_brand', SKILL / 'scripts/check_brand.py')
brand = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(brand)


class BrandCheckTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = json.loads((SKILL / 'assets/brand-source.json').read_text())
        self.logo_url = self.snapshot['logo']['source_url']
        self.css_url = self.snapshot['stylesheets'][0]['url']
        self.resources = {
            brand.SITE: (
                f'<img class="brand-navbar" src="{self.logo_url}">'
                f'<img class="brand-navbar" src="{self.logo_url}">'
                '<img class="marquee-logo" src="https://example.com/partner.svg">'
                f'<link rel="stylesheet" href="{self.css_url}">'
            ).encode(),
            self.logo_url: (SKILL / self.snapshot['logo']['file']).read_bytes(),
            self.css_url: b':root { --black: #151515; }',
        }
        self.snapshot['stylesheets'][0]['sha256'] = brand.sha(self.resources[self.css_url])

    def check(self):
        return brand.check(self.snapshot, SKILL, self.resources.__getitem__)

    def test_matching_assets_ignore_partner_logo_and_deduplicate(self):
        self.assertEqual(self.check()['status'], 'unchanged')

    def test_changed_logo_requires_review(self):
        self.resources[self.logo_url] += b'\n'
        self.assertIn('Official logo content changed', self.check()['reasons'])

    def test_changed_css_requires_review(self):
        self.resources[self.css_url] += b'body { color: red; }'
        self.assertEqual(self.check()['status'], 'review_required')

    def test_missing_brand_logo_does_not_fall_back_to_partner(self):
        self.resources[brand.SITE] = b'<img class="marquee-logo" src="https://example.com/partner.svg">'
        with self.assertRaises(ValueError):
            self.check()

    def test_non_svg_response_is_not_accepted(self):
        self.resources[self.logo_url] = b'<html>Not a logo</html>'
        with self.assertRaises(ValueError):
            self.check()

    def test_unknown_hosts_and_insecure_urls_are_rejected(self):
        for url in ['http://www.wizlex.com/', 'https://example.com/logo.svg', brand.SITE.replace('://', '://user:example@')]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                brand.allowed(url)


if __name__ == '__main__':
    unittest.main()
