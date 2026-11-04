# Site analytics and short links

`app.py` runs next to the page server in the website's Portainer stack (`stack.yml`, stack 56 on gs-europe).
Python standard library only; the data is one SQLite file on the volume `bs-analytics`.
The allowed IPs and the API key are environment variables of the stack in Portainer, never in this repo.

## What it does

- **No 404.** Any address that is not a page or file goes to the service. A short link is counted and sent on;
  anything else is sent to `/intro`.
- **Short links.** `https://boringspirituality.com/<slug>` records the click (link previews by apps and bots are
  counted apart) and redirects to `/intro?utm_...&l=<slug>`. The page script saves the values in localStorage
  (`essay_utm` last, `essay_utm_first` first, `essay_ref` the first outside referrer) and takes them out of the
  address bar at once.
- **Page views.** Each page on the live site reports a view (path, outside referrer, UTM values when the address
  had them, device type, language, a random visitor id from localStorage and a session id), and when the reader
  leaves, how far down they scrolled and for how long. No cookie and no third party. The IP is never stored; it
  only marks visits from the allowed IPs as Alex's own, which the stats leave out by default.
- **Contact form.** Hidden fields carry the last and first UTM values, the short link and the referrer to the
  n8n webhook, and a sent form is counted as a lead.
- **`/analytics`.** The private page, only from `ALLOWED_IPS`; everyone else is sent to `/intro`.

## API

Authenticate with `Authorization: Bearer $API_KEY` (or call from an allowed IP). Anything unauthenticated gets a 404.

```
POST   /api/links        {"slug": "ig-reel1", "utm_source": "instagram", "utm_medium": "reel",
                          "utm_campaign": "launch", "utm_content": "...", "utm_term": "...", "note": "..."}
                          slug is optional (a random 6-character one is made); utm_source is required;
                          "target": "/faq" sends the link to another page (default /intro)
GET    /api/links        all links
DELETE /api/links/<slug>
GET    /api/stats?days=30[&own=1]   everything the analytics page shows, as JSON (days=0 for all time)
GET    /api/ip           the address the site sees for you, and whether it is allowed
```

Slugs are 1 to 40 characters, a to z, 0 to 9 and `-`. Page names and reserved words (intro, faq, api,
analytics, book and others) are refused.

## Local test

```
DB_PATH=/tmp/a.db ALLOWED_IPS=127.0.0.1 API_KEY=test PORT=8099 python site/app.py
```
