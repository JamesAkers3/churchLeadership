"""Verify the narrow hybrid change and preserved surrounding layout/text."""

from hashlib import sha256
from itertools import combinations
import re

import pdfplumber
from pypdf import PdfReader

from build_formation_gap_v5 import OUTPUT, ROOT, QUOTE, LEAD


def check():
    old_path = ROOT / "output/pdf/archive/the-formation-gap-v4.pdf"
    assert sha256(old_path.read_bytes()).hexdigest() == "80f8b46de795a28fd73ee368ee7940bd1e84c2fd42ce05436e5c14209cf249e2"
    old = " ".join(PdfReader(old_path).pages[0].extract_text().split())
    reader = PdfReader(OUTPUT)
    assert len(reader.pages) == 1
    page = reader.pages[0]
    assert tuple(map(float, page.mediabox)) == (0, 0, 612, 792)
    new = " ".join(page.extract_text().split())
    assert old.count(QUOTE) == 1
    assert new == old.replace(QUOTE, LEAD + " " + QUOTE), "Unexpected wording change."
    assert new.count(QUOTE) == 1 and new.count(LEAD) == 1
    assert "trusted them" not in new
    assert not page.get("/Annots")
    assert not re.search(r"\bv\d+\b|https?://|PARAPHRASE", new, re.I)
    assert not re.search(r"\bpastors?\b", new)

    with pdfplumber.open(OUTPUT) as pdf, pdfplumber.open(old_path) as original:
        page = pdf.pages[0]
        assert not page.images
        numbers = [page.search(re.escape(n), regex=True)[0] for n in ("96%", "41%", "9%")]
        assert max(n["top"] for n in numbers) - min(n["top"] for n in numbers) < 0.01
        assert all(all(abs(c["size"] - 34) < 0.01 for c in n["chars"]) for n in numbers)
        lead_pattern = r"\s+".join(re.escape(word) for word in LEAD.split())
        lead_chars = page.search(lead_pattern, regex=True)[0]["chars"]
        assert all(abs(c["size"] - 16.5) < 0.01 and "Georgia-Bold" in c["fontname"] for c in lead_chars)
        quote_chars = page.search(re.escape(QUOTE), regex=True)[0]["chars"]
        assert all(abs(c["size"] - 9) < 0.01 for c in quote_chars)
        assert min(c["top"] for c in lead_chars) >= 248
        assert max(c["bottom"] for c in quote_chars) <= 309
        # Outside the green section, each character retains its exact layout.
        def surrounding_chars(p):
            return [(c["text"], round(c["x0"], 3), round(c["top"], 3),
                     round(c["size"], 3), c["fontname"].split("+", 1)[-1])
                    for c in p.chars if c["top"] < 237 or c["top"] > 317]
        assert surrounding_chars(page) == surrounding_chars(original.pages[0])
        words = page.extract_words()
        for word in words:
            assert 24 <= word["x0"] < word["x1"] <= 588, word
            assert 25 <= word["top"] < word["bottom"] <= 750, word
        for a, b in combinations(words, 2):
            ox = min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])
            oy = min(a["bottom"], b["bottom"]) - max(a["top"], b["top"])
            assert not (ox > 0.5 and oy > 0.5), (a, b)
        for edge in page.edges:
            if edge["orientation"] != "v" or abs(edge["x0"] - edge["x1"]) > 0.1:
                continue
            for word in words:
                assert not (word["x0"] < edge["x0"] < word["x1"] and
                            min(word["bottom"], edge["bottom"]) > max(word["top"], edge["top"])), word
    print("PASS: v3 lead restored; exact NIV retained beneath it; all v4 words/layout outside the green section unchanged.")
    print("PASS: equal 34-point statistics, 16.5-point lead, panel fit, one Letter page, no word/divider collisions.")
    print("PASS: zero images/links/annotations; Pastor capitalization; no visible version; v4 hash unchanged.")
    print("SHA-256:", sha256(OUTPUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    check()
