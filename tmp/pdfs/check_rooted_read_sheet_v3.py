"""Verify the Rooted seed-and-soil review copy and preservation of v2."""

from hashlib import sha256
import json
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "output/pdf/archive/rooted-flourishing-multiplying-life-read-sheet-v2.pdf"
V3 = ROOT / "output/pdf/archive/rooted-flourishing-multiplying-life-read-sheet-v3.pdf"
MAP = ROOT / "tmp/pdfs/rooted-read-sheet-v3-content-map.json"
V2_SHA256 = "ddc76c68b48d6ce63d73724fb7589eaa9d7ecc43efb4efef10d5d1c1b8208364"


def normalized(text):
    return " ".join(text.split())


def main():
    assert V3.exists(), "Expected v3 review PDF"
    assert sha256(V2.read_bytes()).hexdigest() == V2_SHA256, "v2 changed"
    reader = PdfReader(V3)
    assert len(reader.pages) == 3, "review copy must remain two reading pages plus notes"
    pages = [normalized(page.extract_text() or "") for page in reader.pages]
    expected = [
        "Life often begins where no one can see it.",
        "Faithful leadership pays attention to both the seed and the soil.",
        "Listen for Jesus through His Word",
        "The Holy Spirit is leading you",
        "Walking through the image",
        "Who knows the soul beneath the role?",
        "The parable of the sower sharpens discernment",
    ]
    joined = " ".join(pages)
    for phrase in expected:
        assert phrase in joined, f"Missing approved text: {phrase}"
    assert "Bare is not the same as dead" not in joined
    assert "Pray together with Scripture open" not in joined
    assert not any("/Annots" in page for page in reader.pages), "unexpected PDF annotations"
    records = json.loads(MAP.read_text())["records"]
    for record in records:
        x1, y1, x2, y2 = record["box"]
        assert x1 >= 0 and y1 >= 0 and x2 <= 612 and y2 <= 792, f"Out-of-bounds record: {record}"
    print("PASS: v2 preserved; approved seed-and-soil language is present; page count, bounds, and link checks pass.")


if __name__ == "__main__":
    main()
