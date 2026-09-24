# Pastor Capitalization Review

James requested a review of all five current PDFs and consistent capitalization of Pastor/Pastors as a sign of respect. Direct quotations and published source titles retain their original form. Archived versions remain unchanged.

## Reviewed and revised

- `output/pdf/a-pastor-can-be-known-and-still-unsupported-v2.pdf` — headline, bridge, and source sample description capitalized.
- `output/pdf/christ-at-the-center-1-3-12-v2.pdf` — Pastor's trusted-support description capitalized.
- `output/pdf/the-formation-gap-v3.pdf` — headline, statistical explanations, closing reminder, and source sample descriptions capitalized.

## Reviewed without changes

- `output/pdf/from-passion-to-impact-v8.pdf` — no references requiring capitalization.
- `output/pdf/rooted-flourishing-multiplying-life-v8.pdf` — no references requiring capitalization.

## Preservation and checks

The three earlier PDFs remain in `output/pdf/archive/`. Their original builders remain intact. The revised builders are `tmp/pdfs/build_christ_center_pdf_v2.py` and `tmp/pdfs/build_formation_gap_v3.py`.

Extracted text comparison confirmed that only capitalization changed. Each revised PDF remains one page. All three revised pages were rendered and visually inspected for wrapping, spacing, and clipping. No version labels were added to the artwork. Review renders are in `tmp/pdfs/pastor-capitalization-review/`.

## Pending separate correction

James also requested that 80%, 22%, and 65% on the pastoral-support page occupy equal-width columns with equal-sized percentages, three across. That layout correction remains the next visual task; it was not bundled into this capitalization-only revision.

## Subsequent approved layout revision

James subsequently approved that correction together with enlarging "Who knows the soul beneath your role?" from 17-point to 22-point bold. The rebuilt page is `output/pdf/a-pastor-can-be-known-and-still-unsupported-v3.pdf`; v2 remains in the archive. The percentages share the same 36-point bold font, baseline, and 180-point column allocation. The source, sample size, and separate-survey-measures qualifier remain present. All other page content is unchanged, except the added label "LONELY OR ISOLATED" above the third statistic. The final page was rendered and inspected for spacing, wrapping, and clipping.

Production source: `tmp/pdfs/build_christ_center_pdf_v3.py`. This builder's command-line entry point builds the support page only; the current circles page remains v2 and was not rebuilt.
