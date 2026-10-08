# essay/research: the research behind Part two (perennial philosophy, Theosophy, the traditions)

Not part of the essay, and not part of the essay build. Kept for reference. Everything here was produced on 2026-10-07 and 2026-10-08 in cloud sessions by Claude and its sub-agents, on Alex's briefs.

## Read this first: nothing here is checked against a source

- The web search tool in these sessions allows about 200 searches per turn, shared by every agent running in that turn. The big run (94 agents, one turn) spent that allowance in its first hour. Only the first pass of three topics (history of the idea, Guénon, Coomaraswamy) had working search. Every fact-check pass after that had no search and no page fetch (WebFetch, curl and Crossref are blocked in the cloud environment).
- So almost every date, title, locator, attribution and wording in these files comes from model memory, cross-read between files. The checking passes corrected about 400 items by comparing files. They confirmed almost nothing against a page or a book.
- Tiers used in the files: [V] a search result in that session showed the wording or fact; [C] carried: a first-pass agent reported a search result that nobody re-saw; [S] a search supports the gist, wording from memory; [M] memory, confident; [U] memory, unsure: keep out of the essay until checked. The older reports (`earlier-rounds/`) use their own tags: VERIFIED, PLAUSIBLE, WRONG.
- No quotation in these files is cleared for printing. Quotations in the essay itself should be copied from the book with edition and page.
- Two topics (P15 veil and the way, P17 ethic of unity) were never checked at all: the checkers were blocked by a content filter.
- Lesson for the next run: the search allowance is per turn, so verify in a fresh turn with a few agents and a list of specific items, not in a long run with dozens of agents.

## Where to start

1. `perennial-theosophy-digest.md`: about 3,000 words, the reading. How the perennial philosophy movement and Theosophy look at the axiom, how they compare religions, and what it would change in Part two.
2. `CHECKLIST.md`: the claim-by-claim check of Part two (2026-10-08, 521 claims): what is wrong and needs fixing, what is still unconfirmed and what to open, and the confirmed items with the pages they were seen on.
3. `synthesis/S2-alignment.md`: Alex's axiom restated in the perennialists' and Theosophists' vocabulary, a correspondence table, and fifteen proposed replacement passages for Part two in his voice (none applied).

## What is where

| path | what it is |
|---|---|
| `perennial-theosophy-digest.md` | the short reading (above) |
| `CHECKLIST.md` | what is wrong, what is unconfirmed and what to open, what was confirmed and where (521 claims) |
| `translation-check-2026-10-08.md` | the check of every foreign-word gloss and quoted rendering in Part two (four agents with search, a skeptic per finding, a completeness critic): what was wrong, what was applied in v3.2.7, what was left on purpose |
| `synthesis/S1-matrix.md` | nine ideas (the one, the veil, why separation, lives, karma, return, letting go, stages, cosmic scale) across the perennial authors and the Theosophists |
| `synthesis/S2-alignment.md` | the axiom in their words, correspondence table, proposed changes to Part two, claims in the draft that are loose |
| `synthesis/S3-methods.md` | how they compare religions: anthology, parallel passages, glossaries, outer and inner, levels, descent from one source, stage maps, claimed revelation, experience |
| `synthesis/S4-traditions.md` | tradition by tradition: which texts and terms the comparers use for Hinduism, Buddhism, Jainism, Judaism, Christianity, Islam, Daoism, the Greeks and others |
| `synthesis/S5-differences.md` | ten families of answer to "why do religions differ if they say the same thing", with what scholars say, four ways Alex could phrase it, and what not to say |
| `dossiers/dossier-1-perennial-philosophy.md` | long (70,000 words): the movement, the Traditionalists, the anthologies, Smith, Wilber, the comparers of experience, the scholarly debate, traps, open checks |
| `dossiers/dossier-2-theosophy-and-blavatsky.md` | long (33,000 words): Blavatsky and the Society, her books, her teaching, later Theosophists, the Mahatma Letters, lineage, assessment, traps, open checks |
| `dossiers/dossier-3-what-it-means-for-part-two.md` | long (48,000 words): the synthesis for Part two, with a list of changes to the draft and open checks |
| `topics/` | the 27 topic files and 15 gap files, in their fact-checked form (`.verified.md`, with a corrections log at the top). P15 and P17 are `.unchecked.md` |
| `first-pass/` | the same topics before checking, kept for audit (the checked file's corrections log lists what changed) |
| `earlier-rounds/` | seven agent reports from the first rounds of Part two variant B: Buddhism and Jainism, Christianity, Judaism and Islam against the axiom, and four fact-check reports on the draft; their prompts are in `prompts/` |
| `method/` | the workflow script that ran the big study (`perennial-theosophy-research.workflow.js`, with all topic prompts) and two checker logs |

Topic ids: P01 history of the idea · P02 Guénon · P03 Coomaraswamy · P04 Schuon I (method) · P05 Schuon II (metaphysics) · P06 the wider Traditionalist circle · P07 the thematic anthologies (Perry, Huxley, Novak, Wilson) · P08 Huxley · P09 Huston Smith · P10 Wilber, Jung, Eliade, Campbell · P11 comparers of mysticism (James, Underhill, Otto, Stace, Zaehner) · P12 the academic debate · P13 non-Western reconcilers · P14 the One and why it becomes many · P15 the veil and the way out · P16 lives, the soul and karma · P17 ethic of unity and the golden rule · P18 stage maps and ladders · T01 Blavatsky and the Society · T02 Isis Unveiled and The Secret Doctrine · T03 The Key, The Voice of the Silence, the Glossary · T04 Theosophy on lives, karma and after-death states · T05 Theosophical cosmology and the Path · T06 scholarly assessment · T07 lineage of the word and relation to the perennial philosophy · T08 Theosophists after Blavatsky · T09 the Mahatma Letters, Subba Row, Sinnett.

Gap files added by a completeness critic: G1-1 how independent the witnesses are (contact, transmission, convergence) · G1-2 Theosophical primary texts (wording, edition, page) · G1-3 Traditionalist primary sentences · G1-4 perennial and experience classics beyond the Traditionalists · G1-5 Indic, Buddhist, Jain, Greek and Chinese passages in named translations · G1-6 Abrahamic and Christian inner-layer passages · G1-7 Kashmir Shaivism and other Indian systems that state the three clauses · G1-8 survival, filter theory and the Western case for plural lives · G1-9 thin traditions (Chinese, Iranian, Gnostic, Sikh, Jain, primal and African) · G1-10 teachers of the movement and the marks of a person further along · G2-1 action and stillness together (the DO half) · G2-2 the academic home of the axiom (cosmopsychism, priority monism, analytic idealism) with an audit of the opening's science claims · G2-3 the traditions' technical theories of illusion · G2-4 the Absolute's self-estrangement and return in German and Russian philosophy · G2-5 what you can check: the empirical record on loosening the wall.

## Rules for using this material

- It is a store of leads. Nothing goes into the essay from here without opening the source.
- Some files carry reported scandals or allegations about named historical people (for example Schuon's later circle, Leadbeater in 1906) and criticism of living scholars. Keep these out of the essay. The research notes say "cite the books, not the man".
- Rights: Blavatsky, James (1902), Underhill (1911), Emerson, Schopenhauer in old translations and the Sacred Books of the East are public domain. Huxley, Schuon, Guénon (English translations), Coomaraswamy, Smith, Wilber and modern translations are in copyright: paraphrase, or quote a sentence or two copied from the book.
- Alex's rules still apply: Part two is not an attempt to prove anything, no section on where specialists object, never claim a tradition says something it does not (see `CLAUDE.md`).
