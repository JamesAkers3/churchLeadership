# Formation Gap: Approved Hybrid

September 17, 2026. James prefers v3's dark green section and v4's Putting This Into Practice section. He separately approved keeping v4's historical statistics wording, READ references and corrected source footer. He then authorized completing the hybrid PDF: "ok, go ahead and finish that PDF change, unless you have any open questions."

Latest working PDF: `output/pdf/the-formation-gap-v5.pdf`. The requested implementation is complete; James has not yet reviewed the resulting v5 page. Prior selections/candidates and archived versions remain preserved without overwriting or moving them.

## The green section

Restored the v3 lead, in its original 16.5-point Georgia Bold, color, position and two-line treatment:

> Jesus called the Twelve to be with Him before He sent them out.

This is our unquoted narrative reflection on the appointment in Mark 3 and sending in Mark 6, not the literal wording of Mark 3:14. It does not claim Jesus had to wait until He could trust them. Beneath it, replacing the old unsupported trust inference, is the exact NIV verse text, in quotation marks with **MARK 3:14 / NIV** beside it:

> “He appointed twelve that they might be with him and that he might send them out to preach”

The Scripture is 9-point Helvetica with 11.5-point leading; its reference is bold gold. Both fit on one support line inside the original 80-point-high panel. As in v3, the lead is dominant and its supporting text smaller. NIV's lowercase pronouns and absence of an ending period are retained. This is verse 14 within a sentence that continues into verse 15, not Jesus' direct speech. Verification source/context: [Mark 3:14 NIV](https://www.biblegateway.com/passage/?search=Mark%203%3A14&version=NIV), [Mark 3](https://www.biblegateway.com/passage/?search=Mark%203&version=NIV) and [Mark 6](https://www.biblegateway.com/passage/?search=Mark%206&version=NIV), checked during the v4 revision. The unsupported "before He trusted them to carry the work" line stays removed.

## Everything retained from v4

Putting This Into Practice, all three prompts/READ references, historical statistics copy, equal 34-point percentages, source footer and research limits remain exactly unchanged. Opening, large reflection question, action invitation, exhaustion reminder and James' protected Holy Spirit statement also remain unchanged. The green section is the only layout/content difference from v4. No visible version, link, illustration or extra assignment was added. Detailed research provenance and interpretive safeguards remain in `docs/strategy/formation-gap-production-notes-v4.md`; all three numbers come from the 2019 survey of 508 U.S. Protestant senior Pastors published in 2020, not the 2026 burnout article.

## Verification and continuation

Root inspected the complete final color and grayscale pages. Automated checks confirm the restored lead is the only added word sequence, every other v4 word is retained, every character outside the green section retains its position/font/size, the exact NIV quotation remains, percentages are equally sized/aligned, panel text fits, one Letter page, no word overlaps or vertical-divider collisions, no images/links/annotations, Pastor capitalization and no visible version. All 52 baseline PDFs and earlier Formation builders remain byte-for-byte unchanged.

An initial check could not match the restored headline across its line break. Diagnostics confirmed literal-space matching was the cause, not missing PDF content; allowing whitespace in that search yielded exactly one match. The check was corrected and the complete checks passed. No PDF change was made to address that test issue.

These are root production checks, not a new independent specialist approval or print-rights clearance. James' review of the resulting page, any requested specialist recheck, translation-credit/publication-rights review and the future talking sheet remain open. Other PDFs and earlier builders are untouched. Saved locally; no commit or GitHub backup performed.

Reproduction: `tmp/pdfs/build_formation_gap_v5.py`, importing preserved original helpers, v3 statistics and the v4 quote constant; `tmp/pdfs/check_formation_gap_v5.py`. Color/grayscale renders: `tmp/pdfs/the-formation-gap-v5-preview.png` and `tmp/pdfs/the-formation-gap-v5-grayscale.png`. Embedded system-font subsets only; do not redistribute font files.

V5 SHA-256: `63477b48317da6ca321a333653ed9f585d9fa4a20cd1f7b300e73de6724b95d4`.

Preserved v4 SHA-256: `80f8b46de795a28fd73ee368ee7940bd1e84c2fd42ce05436e5c14209cf249e2`.
