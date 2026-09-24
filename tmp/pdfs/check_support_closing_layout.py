"""Check the two layout defects James marked in the support-page screenshot."""

from pathlib import Path
import sys

import pdfplumber


with pdfplumber.open(Path(sys.argv[1])) as document:
    page = document.pages[0]
    words = page.extract_words(extra_attrs=["size", "fontname"])
    failures = []
    if len(page.lines) != 1:
        failures.append("Expected one accent line, confined to the question box.")
    closing = [word for word in words if word["top"] > 590 and word["top"] < 640]
    if not closing or any(abs(word["size"] - 10.5) > 0.01 for word in closing):
        failures.append("Both closing lines must use the same 10.5-point size.")
    starts = [word for word in closing if word["text"] in ("Begin", "You")]
    if len(starts) != 2 or any(abs(word["x0"] - 70) > 0.1 for word in starts):
        failures.append("Closing lines must share the question text's left edge.")
    if len(starts) == 2 and abs(starts[1]["top"] - starts[0]["top"] - 14) > 0.1:
        failures.append("Closing lines must have a consistent 14-point rhythm.")
    if failures:
        raise AssertionError("\n".join(failures))
    print("PASS: one accent; equal closing-text size; aligned left edges; 14-point rhythm.")
