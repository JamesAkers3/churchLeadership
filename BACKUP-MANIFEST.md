# Backup Manifest

**Prepared:** September 15, 2026
**Purpose:** Preserve enough context, source material, working history, and production files for another session or collaborator to continue without starting over.

## Orientation

- `README.md` — brief project introduction.
- `PROJECT-CHECKPOINT.md` — authoritative continuation point and current-state narrative.
- `OPEN-WORK-AND-NEXT-STEPS.md` — living roadmap from diagnosis to practical systems, tools, and implementation rhythms.
- `docs/superpowers/specs/2026-09-12-project-voice-and-heartbeat-design.md` — voice, theology, and editorial standard.
- `docs/superpowers/plans/2026-09-12-project-voice-and-heartbeat-plan.md` — working plan behind the project-wide voice pass.

## Strategy and frameworks

- `docs/strategy/business-discovery-notes.md` — calling, intended churches, James' background, protected language, and evolving frameworks.
- `docs/strategy/calling-vision-mission-systems-discovery-draft.md` — first working guide connecting calling, vision, mission, systems, and the Life-Giving Reach Test.
- `docs/strategy/scriptural-foundation.md` — primary and supporting Scriptures, their relationship to the work, and the pastoral guardrail around 2 Timothy 1:6–7.
- `docs/strategy/posture-of-the-work.md` — approved engagement posture, biblical anchors, guardrails, and questions for entering a church without claiming to hold all the answers.
- `docs/strategy/when-the-light-grows-dim-framework.md` — separate pastoral burnout and shared-weight framework.
- `docs/strategy/assets/` — working HTML concepts and source visual assets.
- `docs/strategy/assets/rooted-botanical-panorama-v1.png` — source illustration for the current Rooted PDF.

## Research

- `docs/research/jesus-three-twelve-leadership-research.md` — study of Jesus with the Three and the Twelve, their sending, and the pattern carried into Acts.
- `docs/research/barna-research-and-resource-map.md` — research map and Barna source notes, with Jesus retained as the standard.
- `docs/research/scripture-translation-comparison.md` — working recommendations for how the NKJV, NIV, Amplified Bible, and The Message should serve the Scriptural foundation.

## Current deliverables

- `output/pdf/rooted-flourishing-multiplying-life-v8.pdf`
- `output/pdf/from-passion-to-impact-v8.pdf`
- `output/pdf/a-pastor-can-be-known-and-still-unsupported.pdf`
- `output/pdf/christ-at-the-center-1-3-12.pdf`
- `output/pdf/the-formation-gap-v2.pdf`

## Preserved history

- `output/pdf/archive/` — every superseded PDF version and an index explaining the progression.
- `.superpowers/brainstorm/*/content/` — early interactive visual concepts.
- `tmp/` — PDF builders, intermediate exports, review renders, and QA working files. Although the folder is named `tmp`, it is intentionally backed up because it contains the build history needed to reproduce and refine the work.

## Current production sources

- `tmp/pdfs/build_rooted_v8.py` — current Rooted. Flourishing. Multiplying Life. PDF builder.
- `tmp/pdfs/build_passion_v8.py` — current Passion PDF builder.
- `tmp/pdfs/build_christ_center_pdf.py` — current builder for the separate pastoral-support and Christ at the Center / 1–3–12 PDFs.
- `tmp/pdfs/build_christ_center_pdf_v1.py` — preserved builder for the superseded combined page.
- `tmp/pdfs/build_formation_gap_v2.py` — current Formation Gap builder.

Earlier builders remain alongside them so previous visual decisions can be recovered.

## Voice continuity

The project-specific voice is fully recorded in the checkpoint, discovery notes, and voice-and-heartbeat specification. It should remain warm, charismatic, pastoral, familiar, encouraging, direct, and free of corporate or canned language. It should sound like a trusted big brother or mentor without superiority.

The separate personal `my-voice` skill used during drafting is an external user-level skill rather than a project-created artifact. It contains private work-context information and is intentionally not copied into this public repository. The project files contain the ministry-specific voice guidance needed to continue this work faithfully.

## Files intentionally excluded from version control

- macOS `.DS_Store` files.
- Python bytecode and `__pycache__` directories.
- Local preview-server process IDs, ports, and session tokens under `.superpowers/**/state/`.

These are machine-specific runtime debris, not project content.
