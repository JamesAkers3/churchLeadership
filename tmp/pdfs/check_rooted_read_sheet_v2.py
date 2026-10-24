"""Verify the audience-neutral Rooted read-sheet revision."""

from hashlib import sha256
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
V1 = ROOT / "output/pdf/archive/rooted-flourishing-multiplying-life-read-sheet-v1.pdf"
V2 = ROOT / "output/pdf/archive/rooted-flourishing-multiplying-life-read-sheet-v2.pdf"

V1_SHA256 = "62725480bd84dc3addd76d0d790280931c248eca042adb57e0a712f957426d0c"
OLD_OPENING = (
    "Pastor, when you look at your church, what do you see first? The people God has "
    "placed there, or the things that still aren't working?"
)
NEW_OPENING = (
    "When you think about your church, what comes into view first: the people God has "
    "placed there, or everything that still isn't working?"
)
OLD_TRANSITION = (
    "Pastor, as we look for life in the church, your life belongs in this conversation, "
    "too. People may see your faithfulness without knowing what the work is costing you."
)
NEW_TRANSITION = (
    "As we look for life in the church, the people carrying its leadership belong in the "
    "conversation too. Their faithfulness may be visible while the cost remains hidden."
)
OLD_QUESTION = "Who has room to hear how you really are?"
NEW_QUESTION = "Who knows the soul beneath the role?"


def normalized(text: str) -> str:
    return " ".join(text.split())


def main() -> None:
    assert V2.exists(), f"Expected revised PDF does not exist: {V2.name}"
    assert sha256(V1.read_bytes()).hexdigest() == V1_SHA256, "v1 changed"

    old_reader = PdfReader(V1)
    new_reader = PdfReader(V2)
    assert len(new_reader.pages) == 3, "v2 must remain a three-page review copy"

    old_pages = [normalized(page.extract_text() or "") for page in old_reader.pages]
    new_pages = [normalized(page.extract_text() or "") for page in new_reader.pages]

    assert NEW_OPENING in new_pages[0]
    assert OLD_OPENING not in new_pages[0]
    assert NEW_TRANSITION in new_pages[1]
    assert NEW_QUESTION in new_pages[1]
    assert OLD_TRANSITION not in new_pages[1]
    assert OLD_QUESTION not in new_pages[1]

    restored_page_one = new_pages[0].replace(NEW_OPENING, OLD_OPENING)
    restored_page_two = (
        new_pages[1]
        .replace(NEW_TRANSITION, OLD_TRANSITION)
        .replace(NEW_QUESTION, OLD_QUESTION)
    )
    assert restored_page_one == old_pages[0], "page 1 changed beyond the approved opening"
    assert restored_page_two == old_pages[1], "page 2 changed beyond the approved transition"
    assert new_pages[2] == old_pages[2], "presenter notes changed"

    assert not any("/Annots" in page for page in new_reader.pages), "unexpected PDF annotations"
    print("PASS: v1 preserved; only the approved audience-language changes appear in v2.")


if __name__ == "__main__":
    main()
