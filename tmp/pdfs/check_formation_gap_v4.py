"""Check exact approved changes, equal statistics and page geometry."""

from hashlib import sha256
from itertools import combinations
from pathlib import Path
import re

import pdfplumber
from pypdf import PdfReader

from build_formation_gap_v4 import OUTPUT, QUOTE, ROOT


def flattened(path):
    return " ".join(PdfReader(path).pages[0].extract_text().split())


def check():
    previous = ROOT / "output/pdf/the-formation-gap-v3.pdf"
    assert sha256(previous.read_bytes()).hexdigest() == "b1062725a0d198de66370f89b463ecd13544611c52020e659a74f9619f691ed2"
    before, after = flattened(previous), flattened(OUTPUT)
    replacements = (
        ("Pastors agree that", "Pastors agreed that"),
        ("Pastors say their church", "Pastors said their church"),
        ("Pastors strongly agree their team", "Pastors strongly agreed their team"),
        (
            "Jesus called the Twelve to be with Him before He sent them out. Jesus formed people through shared life before He trusted them to carry the work. MARK 3:14",
            QUOTE + " MARK 3:14 / NIV PUTTING THIS INTO PRACTICE",
        ),
        (
            "WITH HIM MARK 3:14 They stayed close enough to watch Jesus, ask questions, fail and learn.",
            "WITH HIM READ MARK 3:14 Invite someone to serve beside you. Explain what you're doing and why.",
        ),
        (
            "SENT TOGETHER MARK 6:7 Jesus gave authority and a clear assignment. On this mission, no one went alone.",
            "SENT TOGETHER READ MARK 6:7-13 Agree on a clear responsibility. Give them room to lead, with support.",
        ),
        (
            "BACK WITH HIM MARK 6:30-31 They told Him what happened. Jesus called them to rest.",
            "BACK WITH HIM READ MARK 6:30-31 Make time to listen afterward. Talk about what happened, and make room for rest.",
        ),
    )
    expected = before.split("Sources:", 1)[0].strip()
    for old, new in replacements:
        assert expected.count(old) == 1, old
        expected = expected.replace(old, new)
    actual = after.split("Historical research:", 1)[0].strip()
    assert actual == expected, "Unexpected wording change outside the source footer."
    assert after.count(QUOTE) == 1
    assert "July 25-August 13, 2019" in after and "508 U.S. Protestant senior Pastors" in after
    assert "2026" not in after and "trusted them" not in after
    assert not re.search(r"\bv\d+\b|https?://|PARAPHRASE", after, re.I)
    assert not re.search(r"\bpastors?\b", after)

    reader = PdfReader(OUTPUT)
    assert len(reader.pages) == 1
    assert tuple(map(float, reader.pages[0].mediabox)) == (0, 0, 612, 792)
    assert not reader.pages[0].get("/Annots")
    with pdfplumber.open(OUTPUT) as pdf:
        page = pdf.pages[0]
        assert not page.images
        numbers = [page.search(re.escape(number), regex=True)[0] for number in ("96%", "41%", "9%")]
        assert max(n["top"] for n in numbers) - min(n["top"] for n in numbers) < 0.01
        assert all(all(abs(c["size"] - 34) < 0.01 for c in n["chars"]) for n in numbers)
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
    print("PASS: exact Scripture/application revision; protected opening, question, action and closing unchanged.")
    print("PASS: three equal 34-point statistics; historical dates/population; one Letter page; no overlaps or divider collisions.")
    print("PASS: zero images/links/annotations; Pastor capitalization; no visible version; v3 hash unchanged.")
    print("SHA-256:", sha256(OUTPUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    check()
