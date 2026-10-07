# Tiny markdown -> readable HTML (headings, bullets, bold, code, tables). Usage: python md2read.py TALK.md talk-read.html
import re, sys, html
src, out = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().split("\n")

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s

body = []; i = 0; in_ul = 0
def close_ul():
    global in_ul
    while in_ul: body.append("</ul>"); in_ul -= 1
while i < len(lines):
    l = lines[i]
    m = re.match(r"^(#{1,4}) (.*)", l)
    if m: close_ul(); body.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>")
    elif l.strip() == "---": close_ul(); body.append("<hr>")
    elif l.startswith("> "): close_ul(); body.append('<div class="cue">' + inline(l[2:]) + "</div>")
    elif l.startswith("|"):
        close_ul(); rows = []
        while i < len(lines) and lines[i].startswith("|"): rows.append(lines[i]); i += 1
        i -= 1
        cells = [[inline(c.strip()) for c in r.strip().strip("|").split("|")] for r in rows if not re.match(r"^\|[\s:-]+\|", r.strip()) or not set(r.replace("|", "").strip()) <= set(":- ")]
        body.append("<table>" + "".join("<tr>" + "".join(("<th>" if k == 0 else "<td>") + c + ("</th>" if k == 0 else "</td>") for c in row) + "</tr>" for k, row in enumerate(cells)) + "</table>")
    elif re.match(r"^\s*[-*] ", l) or re.match(r"^\s*\d+\. ", l):
        depth = (len(l) - len(l.lstrip())) // 2 + 1
        while in_ul < depth: body.append("<ul>"); in_ul += 1
        while in_ul > depth: body.append("</ul>"); in_ul -= 1
        body.append("<li>" + inline(re.sub(r"^\s*([-*]|\d+\.) ", "", l)) + "</li>")
    elif l.strip() == "": close_ul()
    else: close_ul(); body.append("<p>" + inline(l) + "</p>")
    i += 1
close_ul()
css = """body{font:19px/1.5 Georgia,serif;max-width:720px;margin:24px auto;padding:0 18px;color:#2f2f2f;background:#eae2d4}
h1{font-size:30px;line-height:1.2}h2{font-size:24px;margin-top:40px;border-top:2px solid #2f2f2f;padding-top:14px}h3{font-size:20px;margin-top:26px}
li{margin:8px 0}.cue{background:#2f2f2f;color:#eae2d4;padding:6px 12px;margin:18px 0 6px;font:700 15px/1.3 Arial,sans-serif;letter-spacing:.02em}code{font-size:16px;background:#e0d7c6;padding:1px 4px}table{border-collapse:collapse;font-size:15px;width:100%}td,th{border:1px solid #bbb;padding:5px 7px;text-align:left;vertical-align:top}
@media(prefers-color-scheme:dark){body{background:#1e1c19;color:#e8e2d6}code{background:#3a352d}td,th{border-color:#555}h2{border-color:#e8e2d6}.cue{background:#e8e2d6;color:#1e1c19}}"""
open(out, "w", encoding="utf-8").write(f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(src)}</title><style>{css}</style>' + "\n".join(body))
print(out, len(body), "blocks")
