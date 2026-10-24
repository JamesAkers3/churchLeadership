"""Verify the requested practical-language changes and preservation of v3."""

from hashlib import sha256
import json
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
V3 = ROOT / "output/pdf/archive/rooted-flourishing-multiplying-life-read-sheet-v3.pdf"
V4 = ROOT / "output/pdf/rooted-flourishing-multiplying-life-read-sheet-v4.pdf"
MAP = ROOT / "tmp/pdfs/rooted-read-sheet-v4-content-map.json"
V3_SHA256 = "8050d182d5d902ffa8e07f76607cb3375993d559e0ffe4450673d1d6f0b70b34"


def normalized(text):
    return " ".join(text.split())


def main():
    assert V4.exists(), "Expected v4 review PDF"
    assert sha256(V3.read_bytes()).hexdigest() == V3_SHA256, "v3 changed"
    reader = PdfReader(V4)
    assert len(reader.pages) == 3, "review copy must remain two reading pages plus notes"
    pages = [normalized(page.extract_text() or "") for page in reader.pages]
    joined = " ".join(pages)
    required = [
        "protect what is working, share responsibility, simplify a process, or stop something harmful.",
        "It does not have to mean starting over or having to start another ministry.",
        "Not every conversation needs to produce a new assignment.",
        "Sometimes the faithful response is to protect what is already life-giving.",
    ]
    removed = [
        "No extra assignment is required to prove that the conversation mattered.",
        "No Barna statistic has been added.",
        "The tree landscape is our illustration",
    ]
    for phrase in required:
        assert phrase in joined, f"Missing requested text: {phrase}"
    for phrase in removed:
        assert phrase not in joined, f"Removed text remains: {phrase}"
    assert not any("/Annots" in page for page in reader.pages), "unexpected PDF annotations"
    records = json.loads(MAP.read_text())["records"]
    for record in records:
        x1, y1, x2, y2 = record["box"]
        assert x1 >= 0 and y1 >= 0 and x2 <= 612 and y2 <= 792, f"Out-of-bounds record: {record}"
    print("PASS: v3 preserved; requested wording, removals, page count, bounds, and link checks pass.")


if __name__ == "__main__":
    main()
