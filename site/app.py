#!/usr/bin/env python3
"""Analytics and short links for boringspirituality.com.

A small service that sits next to the static page server (nginx) in the same Portainer stack.
Python standard library only, data in one SQLite file.

nginx sends it:
  /api/...        the beacon from the pages, the stats and the short-link API
  /analytics      the private analytics page (only from ALLOWED_IPS, everyone else goes to /intro)
  anything else   that is not a page: a short link (count the click, go to /intro with the UTM values)
                  or an unknown address (go to /intro, so the site never shows a 404)

Settings come from the environment, never from this public repo:
  ALLOWED_IPS     comma separated IPs or CIDR ranges that may open /analytics
  API_KEY         bearer key for the short-link API and the stats (for Claude and scripts)
  DB_PATH         default /data/analytics.db
  PUBLIC_BASE     default https://boringspirituality.com
  PORT            default 8080

The visitor's IP is used only to tell Alex's own visits apart and is never stored.
"""
import hmac
import ipaddress
import json
import os
import re
import secrets
import sqlite3
import threading
import time
import urllib.parse
from collections import Counter, defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('DB_PATH', '/data/analytics.db')
API_KEY = os.environ.get('API_KEY', '').strip()
PUBLIC_BASE = os.environ.get('PUBLIC_BASE', 'https://boringspirituality.com').rstrip('/')
PORT = int(os.environ.get('PORT', '8080'))
HOME = '/intro'
UTM = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term')
OWN_HOSTS = ('boringspirituality.com', 'rationalspiritualpractical.com')
# Pages, files and routes a short link may never take.
RESERVED = {'intro', 'rational', 'spiritual', 'practical', 'contact', 'faq', 'next', 'book', 'api',
            'analytics', 'healthz', 'index', 'admin', 'static', 'assets', 'robots', 'favicon', 'sitemap'}
SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9-]{0,39}$')
BOT_RE = re.compile(r'bot|crawl|spider|slurp|preview|facebookexternalhit|whatsapp|telegram|twitter|discord|'
                    r'slack|linkedin|skype|vkshare|embedly|pinterest|curl|wget|python|go-http|headless|lighthouse|'
                    r'monitor|uptime|scan|fetch|http-client|okhttp|axios|node', re.I)
FIELD_MAX = 300


def parse_nets(raw):
    nets = []
    for part in (raw or '').replace(';', ',').split(','):
        part = part.strip()
        if part:
            try:
                nets.append(ipaddress.ip_network(part, strict=False))
            except ValueError:
                print(f'ALLOWED_IPS: ignoring {part!r}', flush=True)
    return nets


ALLOWED = parse_nets(os.environ.get('ALLOWED_IPS', ''))


def is_allowed(ip):
    try:
        a = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(a in n for n in ALLOWED)


SCHEMA = """
CREATE TABLE IF NOT EXISTS links (
  slug TEXT PRIMARY KEY, utm_source TEXT, utm_medium TEXT, utm_campaign TEXT, utm_content TEXT, utm_term TEXT,
  target TEXT NOT NULL DEFAULT '/intro', note TEXT, created REAL NOT NULL);
CREATE TABLE IF NOT EXISTS views (
  pv TEXT PRIMARY KEY, ts REAL NOT NULL, vid TEXT, sid TEXT, path TEXT, ref TEXT, ref_host TEXT,
  utm_source TEXT, utm_medium TEXT, utm_campaign TEXT, utm_content TEXT, utm_term TEXT, link TEXT,
  device TEXT, lang TEXT, own INTEGER NOT NULL DEFAULT 0, depth INTEGER, secs INTEGER);
CREATE INDEX IF NOT EXISTS views_ts ON views(ts);
CREATE TABLE IF NOT EXISTS clicks (
  id INTEGER PRIMARY KEY, ts REAL NOT NULL, slug TEXT, ref_host TEXT, bot INTEGER NOT NULL, own INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS clicks_ts ON clicks(ts);
CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY, ts REAL NOT NULL, vid TEXT, sid TEXT, path TEXT, own INTEGER NOT NULL);
"""

_lock = threading.Lock()


def db():
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    d = os.path.dirname(DB_PATH)
    if d:
        os.makedirs(d, exist_ok=True)
    with _lock, db() as con:
        con.execute('PRAGMA journal_mode=WAL')
        con.executescript(SCHEMA)


def clip(v, n=FIELD_MAX):
    if v is None:
        return None
    v = str(v).strip()
    return v[:n] or None


def host_of(url):
    try:
        h = (urllib.parse.urlsplit(url).hostname or '').lower()
    except ValueError:
        return None
    if h.startswith('www.'):
        h = h[4:]
    return h or None


def external_ref(url):
    """The referring address when it is another site, else None."""
    h = host_of(url or '')
    if not h or any(h == o or h.endswith('.' + o) for o in OWN_HOSTS):
        return None, None
    return clip(url, 500), h


def device_of(ua):
    ua = ua or ''
    if re.search(r'iPad|Tablet', ua):
        return 'tablet'
    if re.search(r'Mobi|Android|iPhone', ua):
        return 'mobile'
    return 'desktop'


# ---------------------------------------------------------------- short links

def link_dict(r):
    d = {k: r[k] for k in r.keys()}
    d['url'] = f"{PUBLIC_BASE}/{r['slug']}"
    d['created'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(r['created']))
    return d


def create_link(body):
    slug = (body.get('slug') or '').strip().lower()
    if not slug:
        with db() as con:
            while True:
                slug = ''.join(secrets.choice('abcdefghjkmnpqrstuvwxyz23456789') for _ in range(6))
                if not con.execute('SELECT 1 FROM links WHERE slug=?', (slug,)).fetchone():
                    break
    if not SLUG_RE.match(slug):
        return 400, {'error': 'slug: 1 to 40 characters, a to z, 0 to 9 and -, starting with a letter or digit'}
    if slug in RESERVED or os.path.exists(f'/srv/site/{slug}.html') or os.path.exists(f'/srv/site/{slug}'):
        return 409, {'error': f'"{slug}" is a page or reserved word on the site'}
    vals = {k: clip(body.get(k) or body.get(k.replace('utm_', ''))) for k in UTM}
    if not vals['utm_source']:
        return 400, {'error': 'utm_source is required (where the link will be posted, like instagram)'}
    target = (body.get('target') or HOME).strip()
    if not re.match(r'^/[a-z0-9/-]*$', target):
        return 400, {'error': 'target must be a path on the site, like /intro'}
    try:
        with _lock, db() as con:
            con.execute('INSERT INTO links (slug, utm_source, utm_medium, utm_campaign, utm_content, utm_term, target, note, created)'
                        ' VALUES (?,?,?,?,?,?,?,?,?)',
                        (slug, *[vals[k] for k in UTM], target, clip(body.get('note'), 500), time.time()))
            r = con.execute('SELECT * FROM links WHERE slug=?', (slug,)).fetchone()
    except sqlite3.IntegrityError:
        return 409, {'error': f'"{slug}" already exists'}
    return 201, link_dict(r)


def list_links():
    with db() as con:
        return [link_dict(r) for r in con.execute('SELECT * FROM links ORDER BY created DESC')]


def delete_link(slug):
    with _lock, db() as con:
        n = con.execute('DELETE FROM links WHERE slug=?', (slug.lower(),)).rowcount
    return (200, {'deleted': slug}) if n else (404, {'error': 'no such link'})


# ---------------------------------------------------------------- beacon

def record_hit(b, own):
    t = b.get('t')
    now = time.time()
    if t == 'view':
        pv = clip(b.get('pv'), 40)
        if not pv:
            return
        ref, ref_host = external_ref(b.get('ref'))
        u = b.get('utm') if isinstance(b.get('utm'), dict) else {}
        with _lock, db() as con:
            con.execute('INSERT OR IGNORE INTO views (pv, ts, vid, sid, path, ref, ref_host, utm_source, utm_medium, utm_campaign,'
                        ' utm_content, utm_term, link, device, lang, own) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        (pv, now, clip(b.get('vid'), 40), clip(b.get('sid'), 40), clip(b.get('path'), 100), ref, ref_host,
                         *[clip(u.get(k)) for k in UTM], clip(b.get('link'), 40), clip(b.get('device'), 10),
                         clip(b.get('lang'), 20), int(own)))
    elif t == 'leave':
        try:
            depth = max(0, min(100, int(b.get('depth') or 0)))
            secs = max(0, min(6 * 3600, int(b.get('secs') or 0)))
        except (TypeError, ValueError):
            return
        with _lock, db() as con:
            con.execute('UPDATE views SET depth=MAX(COALESCE(depth,0),?), secs=MAX(COALESCE(secs,0),?) WHERE pv=?',
                        (depth, secs, clip(b.get('pv'), 40)))
    elif t == 'lead':
        with _lock, db() as con:
            con.execute('INSERT INTO leads (ts, vid, sid, path, own) VALUES (?,?,?,?,?)',
                        (now, clip(b.get('vid'), 40), clip(b.get('sid'), 40), clip(b.get('path'), 100), int(own)))


# ---------------------------------------------------------------- stats

def stats(days, include_own=False):
    since = time.time() - days * 86400 if days else 0
    own = '' if include_own else ' AND own=0'
    with db() as con:
        views = [dict(r) for r in con.execute(f'SELECT * FROM views WHERE ts>=?{own} ORDER BY ts', (since,))]
        leads = [dict(r) for r in con.execute(f'SELECT * FROM leads WHERE ts>=?{own} ORDER BY ts', (since,))]
        clicks = [dict(r) for r in con.execute(f'SELECT * FROM clicks WHERE ts>=?{own}', (since,))]
        links = [dict(r) for r in con.execute('SELECT * FROM links ORDER BY created DESC')]
        first_seen = {r['vid']: r['f'] for r in con.execute('SELECT vid, MIN(ts) f FROM views GROUP BY vid')}

    # One session = one visit. Its source is the first view that carried UTM values, else the first outside referrer.
    sess = {}
    for v in views:
        s = sess.setdefault(v['sid'] or v['pv'], {'sid': v['sid'], 'vid': v['vid'], 'start': v['ts'], 'end': v['ts'],
                                                   'pages': [], 'utm': None, 'ref': None, 'link': None,
                                                   'device': v['device'], 'lang': v['lang'], 'lead': False, 'depth': {}})
        s['end'] = v['ts']
        if not s['pages'] or s['pages'][-1] != v['path']:
            s['pages'].append(v['path'])
        if v['utm_source'] and not s['utm']:
            s['utm'] = {k: v[k] for k in UTM}
            s['link'] = v['link']
        if v['ref_host'] and not s['ref']:
            s['ref'] = v['ref_host']
        if v['depth'] is not None:
            s['depth'][v['path']] = max(s['depth'].get(v['path'], 0), v['depth'])
    lead_sids = {l['sid'] for l in leads}
    for k, s in sess.items():
        s['lead'] = s['sid'] in lead_sids
        if s['utm']:
            s['source'] = s['utm']['utm_source'] + (' / ' + s['utm']['utm_medium'] if s['utm']['utm_medium'] else '')
        elif s['ref']:
            s['source'] = s['ref']
        else:
            s['source'] = '(direct)'
        s['new'] = first_seen.get(s['vid'], 0) >= s['start'] - 1

    def group(keyfn):
        g = defaultdict(lambda: {'visits': 0, 'visitors': set(), 'pages': 0, 'contact': 0, 'leads': 0})
        for s in sess.values():
            key = keyfn(s)
            if key is None:
                continue
            r = g[key]
            r['visits'] += 1
            r['visitors'].add(s['vid'])
            r['pages'] += len(s['pages'])
            r['contact'] += '/contact' in s['pages']
            r['leads'] += s['lead']
        out = []
        for key, r in g.items():
            out.append({'key': key, 'visits': r['visits'], 'visitors': len(r['visitors']),
                        'pages_per_visit': round(r['pages'] / r['visits'], 1), 'reached_contact': r['contact'], 'leads': r['leads']})
        return sorted(out, key=lambda x: -x['visits'])

    daily = defaultdict(lambda: {'visitors': set(), 'views': 0, 'leads': 0})
    for v in views:
        d = daily[time.strftime('%Y-%m-%d', time.gmtime(v['ts']))]
        d['visitors'].add(v['vid'])
        d['views'] += 1
    for l in leads:
        daily[time.strftime('%Y-%m-%d', time.gmtime(l['ts']))]['leads'] += 1

    if days and days <= 366:
        for i in range(days):
            daily[time.strftime('%Y-%m-%d', time.gmtime(time.time() - i * 86400))]
    pages = defaultdict(lambda: {'views': 0, 'visitors': set(), 'depth': [], 'secs': []})
    for v in views:
        p = pages[v['path']]
        p['views'] += 1
        p['visitors'].add(v['vid'])
        if v['depth'] is not None:
            p['depth'].append(v['depth'])
        if v['secs']:
            p['secs'].append(v['secs'])
    med = lambda xs: sorted(xs)[len(xs) // 2] if xs else None

    link_rows = []
    by_link = defaultdict(list)
    for s in sess.values():
        if s['link']:
            by_link[s['link']].append(s)
    for l in links:
        c = [x for x in clicks if x['slug'] == l['slug']]
        ss = by_link.get(l['slug'], [])
        link_rows.append({'slug': l['slug'], 'url': f"{PUBLIC_BASE}/{l['slug']}", 'note': l['note'],
                          **{k: l[k] for k in UTM},
                          'clicks': sum(1 for x in c if not x['bot']), 'previews': sum(1 for x in c if x['bot']),
                          'visits': len(ss), 'visitors': len({s['vid'] for s in ss}),
                          'reached_contact': sum('/contact' in s['pages'] for s in ss), 'leads': sum(s['lead'] for s in ss),
                          'created': time.strftime('%Y-%m-%d', time.gmtime(l['created']))})

    recent = sorted(sess.values(), key=lambda s: -s['start'])[:60]
    return {
        'days': days, 'include_own': include_own, 'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'totals': {'visitors': len({v['vid'] for v in views}), 'visits': len(sess), 'views': len(views), 'leads': len(leads),
                   'new_visitors': sum(1 for s in sess.values() if s['new']),
                   'link_clicks': sum(1 for c in clicks if not c['bot']), 'link_previews': sum(1 for c in clicks if c['bot'])},
        'daily': [{'date': d, 'visitors': len(r['visitors']), 'views': r['views'], 'leads': r['leads']} for d, r in sorted(daily.items())],
        'sources': group(lambda s: s['source']),
        'campaigns': group(lambda s: ' · '.join(x for x in (s['utm'][k] or '' for k in UTM) if x) if s['utm'] else None),
        'referrers': group(lambda s: s['ref']),
        'links': link_rows,
        'pages': sorted([{'path': k, 'views': p['views'], 'visitors': len(p['visitors']), 'median_depth': med(p['depth']),
                          'median_secs': med(p['secs'])} for k, p in pages.items()], key=lambda x: -x['views']),
        'devices': Counter(s['device'] or '?' for s in sess.values()).most_common(),
        'languages': Counter((s['lang'] or '?').split('-')[0] for s in sess.values()).most_common(12),
        'recent': [{'start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(s['start'])), 'minutes': round((s['end'] - s['start']) / 60),
                    'source': s['source'], 'campaign': (s['utm'] or {}).get('utm_campaign'), 'link': s['link'], 'pages': s['pages'],
                    'depth': s['depth'], 'device': s['device'], 'new': s['new'], 'lead': s['lead']} for s in recent],
    }


# ---------------------------------------------------------------- HTTP

class Handler(BaseHTTPRequestHandler):
    server_version = 'bs'
    sys_version = ''

    def log_message(self, fmt, *args):
        pass

    @property
    def ip(self):
        return (self.headers.get('X-Client-IP') or self.client_address[0]).split(',')[0].strip()

    def keyed(self):
        a = self.headers.get('Authorization', '')
        return bool(API_KEY) and a.startswith('Bearer ') and hmac.compare_digest(a[7:].strip(), API_KEY)

    def send(self, code, body=b'', ctype='application/json; charset=utf-8', headers=None):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False, indent=1).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Robots-Tag', 'noindex')
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def go(self, where):
        self.send(302, b'', 'text/plain', {'Location': where})

    def body_json(self):
        n = int(self.headers.get('Content-Length') or 0)
        if n > 8192:
            return None
        try:
            return json.loads(self.rfile.read(n) or b'{}')
        except ValueError:
            return None

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        u = urllib.parse.urlsplit(self.path)
        path = u.path
        q = dict(urllib.parse.parse_qsl(u.query))
        if path == '/healthz':
            return self.send(200, 'ok', 'text/plain')
        if path == '/api/ip':
            return self.send(200, {'ip': self.ip, 'allowed': is_allowed(self.ip)})
        if path == '/analytics':
            if not is_allowed(self.ip):
                return self.go(HOME)
            return self.send(200, open(os.path.join(HERE, 'analytics.html'), 'rb').read(), 'text/html; charset=utf-8')
        if path == '/api/stats':
            if not (is_allowed(self.ip) or self.keyed()):
                return self.send(404, {'error': 'not found'})
            try:
                days = max(0, min(3650, int(q.get('days', '30'))))
            except ValueError:
                days = 30
            return self.send(200, stats(days, q.get('own') == '1'))
        if path == '/api/links':
            if not (is_allowed(self.ip) or self.keyed()):
                return self.send(404, {'error': 'not found'})
            return self.send(200, list_links())
        if path.startswith('/api/'):
            return self.send(404, {'error': 'not found'})
        return self.short_link(path)

    def short_link(self, path):
        slug = path.strip('/').lower()
        if SLUG_RE.match(slug):
            with db() as con:
                r = con.execute('SELECT * FROM links WHERE slug=?', (slug,)).fetchone()
            if r:
                bot = bool(BOT_RE.search(self.headers.get('User-Agent', ''))) or self.command == 'HEAD'
                with _lock, db() as con:
                    con.execute('INSERT INTO clicks (ts, slug, ref_host, bot, own) VALUES (?,?,?,?,?)',
                                (time.time(), slug, external_ref(self.headers.get('Referer'))[1], int(bot), int(is_allowed(self.ip))))
                params = [(k, r[k]) for k in UTM if r[k]] + [('l', slug)]
                return self.go(r['target'] + '?' + urllib.parse.urlencode(params))
        self.go(HOME)

    def do_POST(self):
        path = urllib.parse.urlsplit(self.path).path
        if path == '/api/hit':
            b = self.body_json()
            if isinstance(b, dict) and not BOT_RE.search(self.headers.get('User-Agent', '')):
                try:
                    record_hit(b, is_allowed(self.ip))
                except sqlite3.Error as e:
                    print('hit failed:', e, flush=True)
            return self.send(204)
        if path == '/api/links':
            if not (is_allowed(self.ip) or self.keyed()):
                return self.send(404, {'error': 'not found'})
            b = self.body_json()
            if not isinstance(b, dict):
                return self.send(400, {'error': 'send a JSON object'})
            return self.send(*create_link(b))
        self.send(404, {'error': 'not found'})

    def do_DELETE(self):
        path = urllib.parse.urlsplit(self.path).path
        if path.startswith('/api/links/') and (is_allowed(self.ip) or self.keyed()):
            return self.send(*delete_link(path.rsplit('/', 1)[1]))
        self.send(404, {'error': 'not found'})


if __name__ == '__main__':
    init_db()
    print(f'analytics on :{PORT}, {len(ALLOWED)} allowed IP ranges, API key {"set" if API_KEY else "NOT set"}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
