"""Keep sitemap.xml current after a push.

For every HTML page added or modified in the push:
  - set its <lastmod> to the date of the head commit, or
  - add it to the sitemap when it is a new indexable page
    (not 404 / google verification files, not noindex, canonical must point to itself).
Prints what changed; writes sitemap.xml only when something changed.
"""
import os
import re
import subprocess
import sys

site = 'https://' + open('CNAME', encoding='utf-8').read().strip()
before = os.environ.get('BEFORE', '')
sha = os.environ.get('SHA', 'HEAD')


def run(*args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def skip(path):
    name = os.path.basename(path)
    return name == '404.html' or name.startswith('google')


def url_for(path):
    if path.endswith('index.html'):
        return site + '/' + path[:-len('index.html')]
    return site + '/' + path


def indexable(path, url):
    html = open(path, encoding='utf-8', errors='replace').read()
    if re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', html, re.I):
        return False
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html, re.I)
    return not m or m.group(1) == url


if not before or set(before) == {'0'}:
    print('No previous commit to compare with; sitemap left untouched.')
    sys.exit(0)

date = run('git', 'log', '-1', '--format=%cs', sha).strip()
diff = run('git', 'diff', '--name-status', '--diff-filter=AM', before, sha, '--', '*.html')
changes = []
for line in diff.splitlines():
    status, _, path = line.partition('\t')
    if path and not skip(path):
        changes.append((status, path))

sitemap = open('sitemap.xml', encoding='utf-8', newline='').read()
original = sitemap
newline = '\r\n' if '\r\n' in sitemap else '\n'

for status, path in changes:
    url = url_for(path)
    loc = re.escape(url)
    if re.search(r'<loc>%s</loc>' % loc, sitemap):
        # existing entry: set or add <lastmod>
        pat = r'(<loc>%s</loc>\s*<lastmod>)[^<]*(</lastmod>)' % loc
        if re.search(pat, sitemap):
            sitemap = re.sub(pat, lambda m: m.group(1) + date + m.group(2), sitemap)
        else:
            sitemap = re.sub(r'(<loc>%s</loc>)' % loc,
                             lambda m: m.group(1) + '<lastmod>' + date + '</lastmod>', sitemap)
        print('lastmod -> %s  %s' % (date, url))
    elif status == 'A' and indexable(path, url):
        entry = '  <url><loc>%s</loc><lastmod>%s</lastmod></url>%s' % (url, date, newline)
        sitemap = sitemap.replace('</urlset>', entry + '</urlset>')
        print('added      %s  %s' % (date, url))
    else:
        print('not in sitemap, left alone: ' + url)

if sitemap != original:
    with open('sitemap.xml', 'w', encoding='utf-8', newline='') as f:
        f.write(sitemap)
    print('sitemap.xml updated.')
else:
    print('sitemap.xml already up to date.')
