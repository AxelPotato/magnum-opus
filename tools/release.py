#!/usr/bin/env python3
"""Bump the essay version, rebuild the page, update the changelog, commit and tag.

    python tools/release.py {major|minor|fix} "what changed" [--push] [--trailer "Co-Authored-By: ..."]

Versions follow Major.minor.fix:
    major  a new part is added, or the argument is restructured
    minor  a new section, figure or substantive passage, or a changed claim
    fix    typos, wording, corrected facts, layout and bug fixes
"""
import datetime
import glob
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def run(*args, **kw):
    return subprocess.run(args, cwd=ROOT, check=True, **kw)


def sync_desk(version):
    """Copy the essay text to the project's shared folder so the Essay Desk can refresh from it.

    Best effort: only runs where /mnt/project-files exists, and never replaces a newer version.
    """
    dest = '/mnt/project-files/essay-latest'
    if not os.path.isdir('/mnt/project-files'):
        return
    try:
        os.makedirs(dest, exist_ok=True)
        vpath = os.path.join(dest, 'VERSION')
        key = lambda v: tuple(int(x) for x in v.split('.'))
        if os.path.exists(vpath) and key(open(vpath).read().strip()) > key(version):
            return
        for name in ('part-0-intro.md', 'part-1-rational.md', 'part-2-spiritual.md', 'part-3-practical.md'):
            shutil.copyfile(os.path.join(ROOT, 'essay', name), os.path.join(dest, name))
        open(vpath, 'w', newline='\n').write(version + '\n')
    except Exception as e:
        print(f'Desk sync skipped: {e}')


def main():
    argv = [a for a in sys.argv[1:]]
    push = '--push' in argv
    if push:
        argv.remove('--push')
    trailer = ''
    if '--trailer' in argv:
        i = argv.index('--trailer')
        trailer = argv[i + 1]
        del argv[i:i + 2]
    if len(argv) != 2 or argv[0] not in ('major', 'minor', 'fix'):
        sys.exit(__doc__)
    kind, msg = argv

    status = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    if not status:
        sys.exit('Nothing to release: the working tree has no changes.')

    vfile = os.path.join(ROOT, 'VERSION')
    major, minor, fix = (int(x) for x in open(vfile).read().strip().split('.'))
    if kind == 'major':
        major, minor, fix = major + 1, 0, 0
    elif kind == 'minor':
        minor, fix = minor + 1, 0
    else:
        fix += 1
    new = f'{major}.{minor}.{fix}'
    open(vfile, 'w', newline='\n').write(new + '\n')

    run(sys.executable, os.path.join('essay', 'build_html.py'))

    cl = os.path.join(ROOT, 'CHANGELOG.md')
    text = open(cl, encoding='utf-8').read()
    marker = '<!-- entries -->\n'
    assert marker in text, 'CHANGELOG.md lost its entries marker'
    entry = f'## {new} ({datetime.date.today().isoformat()})\n\n- {msg}\n\n'
    open(cl, 'w', encoding='utf-8', newline='\n').write(text.replace(marker, marker + '\n' + entry, 1))

    run('git', 'add', '-A')
    message = f'v{new}: {msg}'
    if trailer:
        message += '\n\n' + trailer
    run('git', 'commit', '-m', message)
    run('git', 'tag', '-a', f'v{new}', '-m', f'v{new}: {msg}')
    print(f'Released v{new}')
    sync_desk(new)

    if push:
        run('git', 'push', 'origin', 'HEAD', '--follow-tags')
        if shutil.which('gh'):
            pages = sorted(p for p in glob.glob(os.path.join(ROOT, 'essay', 'part-*-*.html')) + glob.glob(os.path.join(ROOT, 'essay', 'contact.html')) if '.fragment.' not in p)
            run('gh', 'release', 'create', f'v{new}', *pages, '--title', f'v{new}', '--notes', msg)


if __name__ == '__main__':
    main()
