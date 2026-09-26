#!/usr/bin/env python3
"""Read-only check of the current official Wizlex logo and website CSS (Python 3.10+)."""

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from datetime import datetime, timezone
from xml.etree import ElementTree

SITE = 'https://www.wizlex.com/'
ALLOWED_HOSTS = {'www.wizlex.com', 'wizlex.com', 'cdn.prod.website-files.com'}
LIMIT = 8 * 1024 * 1024


def allowed(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname not in ALLOWED_HOSTS or parsed.username or parsed.password or parsed.port not in (None, 443):
        raise ValueError('Unrecognized asset source; inspect the official website manually.')


class Redirects(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        allowed(newurl)
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def fetch(url):
    allowed(url)
    request = Request(url, headers={'User-Agent': 'WizlexBrandCheck/1.0'})
    with build_opener(Redirects()).open(request, timeout=20) as response:
        allowed(response.url)
        data = response.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError('Asset exceeds the check size limit; review manually.')
        return data


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.logos = set()
        self.styles = set()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'img':
            url = urljoin(SITE, attrs.get('src', ''))
            label = unquote(url).lower()
            if 'brand-navbar' in attrs.get('class', '').split() and 'wizlex' in label and urlsplit(url).path.lower().endswith('.svg'):
                self.logos.add(url)
        if tag == 'link' and 'stylesheet' in attrs.get('rel', '').split() and attrs.get('href'):
            self.styles.add(urljoin(SITE, attrs['href']))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(snapshot, skill_dir, fetcher=fetch):
    page = Assets()
    page.feed(fetcher(SITE).decode('utf-8'))
    if len(page.logos) != 1:
        raise ValueError('The current brand SVG is missing or ambiguous; inspect the website manually.')
    url = next(iter(page.logos))
    logo = fetcher(url)
    if ElementTree.fromstring(logo).tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('The discovered logo is not an SVG document.')
    current = {source: sha(fetcher(source)) for source in sorted(page.styles)}
    expected = {item['url']: item['sha256'] for item in snapshot['stylesheets']}
    reasons = []
    if url != snapshot['logo']['source_url']:
        reasons.append('Official logo URL changed')
    if sha(logo) != snapshot['logo']['sha256']:
        reasons.append('Official logo content changed')
    if sha((skill_dir / snapshot['logo']['file']).read_bytes()) != snapshot['logo']['sha256']:
        reasons.append('Bundled SVG differs from the recorded source')
    if sha((skill_dir / snapshot['raster']['file']).read_bytes()) != snapshot['raster']['sha256']:
        reasons.append('Bundled PNG differs from the recorded derivative')
    if not current or current != expected:
        reasons.append('Website stylesheets changed or are missing')
    return {
        'status': 'review_required' if reasons else 'unchanged',
        'checked_at': datetime.now(timezone.utc).isoformat(),
        'website': SITE, 'current_logo_url': url, 'logo_sha256': sha(logo),
        'stylesheets': current, 'reasons': reasons,
        'next_step': 'Visually inspect the live website before creating the asset. This check does not prove all branding is unchanged.'
    }


def main():
    skill_dir = Path(__file__).resolve().parent.parent
    try:
        snapshot = json.loads((skill_dir / 'assets/brand-source.json').read_text(encoding='utf-8'))
        result = check(snapshot, skill_dir)
    except Exception as error:
        print(json.dumps({'status': 'unverified', 'reason': str(error), 'next_step': 'Inspect https://www.wizlex.com/ manually; do not claim the bundle is current.'}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'unchanged' else 1


if __name__ == '__main__':
    sys.exit(main())
