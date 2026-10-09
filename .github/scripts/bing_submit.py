"""Tell Bing about new or changed pages after a push (Bing Webmaster URL submission API).

Reads the API key from the BING_API_KEY environment variable (a GitHub Actions
secret), never prints it, and never fails the workflow: problems are logged only.
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

MAX_URLS = 50
ENDPOINT = 'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey='

key = os.environ.get('BING_API_KEY', '').strip()
if not key:
    print('BING_API_KEY is not set as a repository secret; nothing submitted.')
    sys.exit(0)

site = 'https://' + open('CNAME', encoding='utf-8').read().strip()


def skip(path):
    name = os.path.basename(path)
    return name == '404.html' or name.startswith('google')


def url_for(path):
    if path.endswith('index.html'):
        return site + '/' + path[:-len('index.html')]
    return site + '/' + path


def sitemap_urls():
    xml = open('sitemap.xml', encoding='utf-8').read()
    return re.findall(r'<loc>([^<]+)</loc>', xml)


before = os.environ.get('BEFORE', '')
sha = os.environ.get('SHA', 'HEAD')
submit_all = os.environ.get('SUBMIT_ALL', '').lower() == 'true'

if submit_all or not before or set(before) == {'0'}:
    urls = sitemap_urls()
else:
    out = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=AM', before, sha, '--', '*.html'],
        capture_output=True, text=True)
    paths = [p for p in out.stdout.split() if p.endswith('.html') and not skip(p)]
    urls = [url_for(p) for p in paths]
    # only pages listed in the sitemap are meant to be indexed (skips legacy/duplicate pages)
    listed = set(sitemap_urls())
    for u in urls:
        if u not in listed:
            print('Skipped (not in sitemap.xml): ' + u)
    urls = [u for u in urls if u in listed]

urls = list(dict.fromkeys(urls))[:MAX_URLS]
if not urls:
    print('No changed pages to submit.')
    sys.exit(0)

print('Submitting %d URL(s) for %s:' % (len(urls), site))
for u in urls:
    print('  ' + u)

body = json.dumps({'siteUrl': site, 'urlList': urls}).encode('utf-8')
req = urllib.request.Request(ENDPOINT + key, data=body,
                             headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    resp = urllib.request.urlopen(req, timeout=60)
    print('Bing responded:', resp.status, resp.read().decode('utf-8')[:300])
except urllib.error.HTTPError as e:
    print('Bing returned an error (workflow continues):', e.code, e.read().decode('utf-8')[:300])
except Exception as e:  # network problems must not fail the workflow
    print('Could not reach Bing (workflow continues):', type(e).__name__)
