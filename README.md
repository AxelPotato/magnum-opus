# Magnum opus

An essay in three parts by Alex Satya: **Rational**, **Spiritual**, **Practical**.

Part one, "Rational", is written. It explains personal growth as two directions, **DO** (making things happen) and **BE** (letting go, and being here), the four rooms you can live in, why the top right is worth the trouble, and why almost nobody stays there. Parts two and three are not started.

The essay began as a talk, "Why letting go is a high-agency skill", given on 2026-09-25. Everything that came out of that talk is archived here too.

## Read it

Open `essay/part-1-rational.html` in a browser. It is one self-contained file: the charts are inline SVG, the pictures are inside it, and it follows your light or dark setting. Each release on the [Releases](../../releases) page carries the file for that version.

The text lives in `essay/part-1-rational.md`.

## Versions

The page follows **Major.minor.fix**, starting at 0.1.0. Every change to it is a new version.

| bump | when |
|---|---|
| major | a new part is added, or the argument is restructured |
| minor | a new section, figure or substantive passage, or a changed claim |
| fix | typos, wording, corrected facts, layout and bug fixes |

The current version is in `VERSION`, shown in the page footer and in `<meta name="version">`. `CHANGELOG.md` lists every version.

To make a change:

```bash
# 1. edit essay/part-1-rational.md (or build_html.py, figs2.py, img/)
# 2. release it:
python tools/release.py fix "Corrected the Grant 2007 numbers"
python tools/release.py minor "Added a section on ..." --push
```

`tools/release.py` bumps `VERSION`, rebuilds the page, adds a changelog entry, commits and tags `vX.Y.Z`. With `--push` it also pushes and creates a GitHub release with the page attached.

A git hook refuses a commit that changes the essay without a version bump. Turn it on once per clone:

```bash
git config core.hooksPath .githooks
```

## Build

Needs Python 3 and Pillow.

```bash
python essay/prep_images.py   # square portraits from essay/img/raw and the talk deck
python essay/build_html.py    # writes essay/part-1-rational.html
```

## What is here

| path | what |
|---|---|
| `essay/` | the essay: text, page builder, charts (`figs2.py`), pictures, sources, notes |
| `talk-2026-09-25/structure/` | the talk as given: structure, presenter notes, prep sheet, the life-goal notes |
| `talk-2026-09-25/recording/` | transcript with timings (the audio itself is not in this repo) |
| `talk-2026-09-25/deck/` | the 44-slide deck (PPTX, PDF, PNGs) and the scripts that build it |
| `talk-2026-09-25/source-dictation/` | the voice dictation the talk grew from |
| `related/` | earlier pitch drafts and the ADHD talk |
| `CLAUDE.md` | the briefing for AI sessions that work on this folder |

## What is not here, and why

- `history/`, the full log of the session that designed the talk. It holds tokens, email addresses, a private group invite and full names of people who have not agreed to be named.
- `talk-2026-09-25/recording/*.ogg`, the audio of the talk. It has audience voices and a first name that is not published.
- Two friends who appear in the talk are called "friend A" and "friend B" throughout.

## Pictures and rights

The portraits and character stills (TV shows, films, sports, photos) are used as illustration in a personal draft. Free-licensed portraits come from Wikimedia Commons and are credited in the page footer. Check image rights before reusing the page elsewhere.

## License

None chosen yet. Until one is added, all rights are reserved.
