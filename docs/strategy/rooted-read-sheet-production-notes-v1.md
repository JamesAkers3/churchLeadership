# Rooted Read Sheet: First PDF Review Copy

## Scope and status

September 17, 2026. James approved a three-page PDF: two reading pages and a distinct presenter-notes page, with embedded fonts, actual text, styling consistent with the visual, printed Scripture references and no visible version numbers or clickable links. New review copy: `output/pdf/rooted-flourishing-multiplying-life-read-sheet-v1.pdf`.

This completes the requested first PDF build, not James' resulting-page/wording selection, independent specialist approval or final publication readiness. Markdown master: `docs/strategy/rooted-read-sheet-v1.md`. No main reading or presenter-safeguard wording was rewritten for the PDF. Title/running headings, pagination and a NIV attribution were added as presentation material; internal drafting/status/source-link notes remain in the master, not on the recipient-facing pages.

The Rooted visual remains separate and unchanged. All 48 pre-existing current and archived PDF hashes were verified unchanged after production. The main PDF folder now has nine working PDFs and the archive still has 40, 49 total. When the Light Grows Dim remains paused; its files and reviews have not been continued. Saved locally; no GitHub backup performed.

## Layout

- Three U.S. Letter portrait pages, 46-point side margins, single-column text.
- Page one: conversational opening, Heartbeat/exact Scripture excerpt, Rooted and Awakening.
- Page two: remaining visual movements, questions, practical response and transition to pastoral support. The visual explanations continue at a paragraph boundary; none is cut mid-paragraph.
- Page three: complete presenter safeguards and contextual boundaries for all four visual reference passages, plus NIV attribution.
- Existing Rooted palette, not a new finalized brand: warm ivory `#FBF8EF`, forest `#173F36`, ink `#293630`, muted text `#59665E`, gold detail `#D5A13A` and darker gold text `#8A5C00`.
- Reading text 12 pt with 15.3 pt leading; presenter text 11 pt with 13.5 pt leading. Headers and important statements use Georgia Bold; body text uses Arial/Arial Bold. Small credits are 10 pt, running labels/pagination 9-9.2 pt.
- The first fit test rejected the last line below the 57-point safety boundary by 0.4 pt. Page-two paragraph gaps were adjusted from 6 to 5 pt without changing font sizes or words. Final content bottoms: page one 75.4 pt, page two 65.6 pt, page three 151.1 pt. Page two's final paragraph bottom remains 7.6 pt above the safety boundary, so future copy changes require a new fit check.

## Font compatibility and accessibility work

Used fonts are subset-embedded TrueType with Unicode maps. Their installed font embedding flags are 8 (editable embedding); original font files have not been copied into the project. Poppler confirmed all three used faces embedded/subset/Unicode. Final PDF header is PDF 1.4; no encryption, JavaScript, forms, images or page annotations.

Added tagged Document/Sect structure with H1/H2/H3, paragraphs and properly nested list/item/label/body elements; unique per-page marked-content identifiers and matching parent-tree mappings; English language metadata; document-title preference; and three outline entries. Decorative background/rules, repeated running labels and pagination are artifacts, not content in the reading sequence.

Checks verified all 65 tagged text blocks mapped in order, all 39 master reading/presenter paragraphs preserved in order, and all relevant fonts embedded. Normal-text contrast against ivory: forest 10.98:1, ink 11.88:1, muted 5.67:1 and darker gold 5.48:1.

These are basic structural and production checks. No screen-reader/user test, full WCAG/PDF-UA certification, universal old-reader guarantee or physical printer/copier proof is claimed. Existing visuals have not been retroactively certified by this work. Final book assembly needs to preserve/recheck tags, language, bookmarks and reading order rather than assume PDF merging will preserve them correctly.

## Scripture and publication boundaries

The excerpt is exactly John 15:4 NIV: “Remain in me, as I also remain in you.” It retains the published case and punctuation and is labeled as an excerpt. Context/source verification for John 15:1-17, John 7:37-39, Matthew 13:18-23 and Mark 4:26-32 is recorded in the master. Our tree illustration, seasons and systems statement are reflection/application, not rewritten biblical text or a five-stage biblical prescription.

A NIV copyright attribution is printed. Full publication/licensing review remains open for the mini-book's actual use. Biblica's current permissions page addresses quotation limits/acknowledgment, commercial print distribution and separately AI-related use; this production turn does not claim a negotiated license or settle applicability to the finished project. [Biblica permissions](https://www.biblica.com/permissions/), checked September 17, 2026. No paid service, account or permission request was changed/submitted.

## Production and verification

- Builder: `tmp/pdfs/build_rooted_read_sheet_v1.py`; reads the master and creates the new PDF only.
- Check script: `tmp/pdfs/check_rooted_read_sheet_v1.py`.
- Text/position map: `tmp/pdfs/rooted-read-sheet-v1-content-map.json`.
- Final complete color and grayscale renders: `tmp/pdfs/rooted-read-sheet-v1-color-1.png` through `-3.png`, and `tmp/pdfs/rooted-read-sheet-v1-gray-1.png` through `-3.png`.
- Root inspected all six final renders and checked margins, hierarchy, spacing, contrast, no clipping/overlaps, consistent typography and clean page transitions. Automated character/word/block bounds and overlap checks pass; no clickable links, visible version label or lowercase Pastor/Pastors in our writing.
- PDF SHA-256: `62725480bd84dc3addd76d0d790280931c248eca042adb57e0a712f957426d0c`.

## Next review

James reviews this first complete PDF for voice, comfort of reading, image-explanation page break and usefulness of the separate presenter page. Preserve any requested revisions as sibling versions. Any requested specialist QA and accessibility/user testing remain open. Next active chapter after Rooted review is A Pastor Can Be Known and Still Unsupported; Dim is not active. No other read sheet or combined mini-book was produced in this turn.
