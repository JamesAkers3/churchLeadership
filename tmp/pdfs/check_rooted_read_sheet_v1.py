"""Check the final text, layout, embedded fonts and basic tagged structure."""

import json
import re

import pdfplumber
from pypdf import PdfReader
from pypdf.generic import ContentStream

from build_rooted_read_sheet_v1 import ROOT, OUTPUT, MAP, load_sections


def plain(s):
    return " ".join(re.sub(r"\*\*(.*?)\*\*", r"\1", s).split())


reader = PdfReader(OUTPUT)
mapping = json.loads(MAP.read_text())
records = mapping["records"]
assert len(reader.pages) == 3
assert not reader.is_encrypted
assert reader.pdf_header == "%PDF-1.4"
assert reader.metadata.title.endswith("Read Sheet v1")
assert reader.trailer["/Root"]["/Lang"] == "en-US"
assert reader.trailer["/Root"]["/MarkInfo"]["/Marked"]
text = " ".join(" ".join(p.extract_text().split()) for p in reader.pages)
assert not re.search(r"\bv\d+\b|https?://|www\.", text, re.I)
assert not re.search(r"\bpastors?\b", text)
assert "“Remain in me, as I also remain in you.”" in text
assert "John 15:4, NIV, excerpt." in text

sections = load_sections()
expected = []
for heading in ["Opening the conversation", "The Heartbeat", "Walking through the image",
                "Questions worth sitting with", "Putting this into practice", "Moving into the next chapter"]:
    for block in sections[heading]:
        expected.extend(re.sub(r"^\d+\. ", "", s) for s in block.splitlines())
for block in sections["Notes for the presenter"]:
    expected.extend(re.sub(r"^- ", "", s) for s in block.splitlines())
expected.append(sections["Scripture and image boundaries"][0])
expected.extend(re.sub(r"^- ", "", s) for s in sections["Scripture and image boundaries"][1].splitlines())
position = 0
for paragraph in expected:
    position = text.index(plain(paragraph), position) + len(plain(paragraph))
assert all(r["box"][1] >= 57 and r["box"][0] >= 46 and r["box"][2] <= 566 for r in records)
for page_index in range(3):
    bodies = [r for r in records if r["page"] == page_index and r["role"] != "Lbl"]
    assert all(b["box"][3] <= a["box"][1] + 0.1 for a, b in zip(bodies, bodies[1:])), "Text blocks overlap"

root = reader.trailer["/Root"]["/StructTreeRoot"]
doc = root["/K"][0].get_object()
assert doc["/S"] == "/Document"
parent_nums = root["/ParentTree"]["/Nums"]
assert len(parent_nums) == 6
roles = set()


def leaves(node):
    node = node.get_object()
    roles.add(str(node["/S"]))
    children = node["/K"]
    if isinstance(children, int):
        return [(node, children)]
    return [leaf for child in children for leaf in leaves(child)]


for page_index, page in enumerate(reader.pages):
    assert tuple(page.mediabox) == (0, 0, 612, 792)
    assert not page.get("/Annots") and not page.images
    assert page["/StructParents"] == page_index and page["/Tabs"] == "/S"
    font_names = []
    for font in page["/Resources"]["/Font"].values():
        font = font.get_object()
        descriptor = font["/FontDescriptor"]
        assert descriptor.get("/FontFile2") or descriptor.get("/FontFile3")
        assert font.get("/ToUnicode")
        font_names.append(font["/BaseFont"])
    streams = ContentStream(page.get_contents(), reader)
    mcids = [int(args[1]["/MCID"]) for args, op in streams.operations
             if op == b"BDC" and "/MCID" in args[1]]
    assert mcids == list(range(len(mcids)))
    sect = doc["/K"][page_index].get_object()
    tagged = leaves(sect)
    assert [i for _, i in tagged] == mcids
    lookup = parent_nums[page_index * 2 + 1]
    for node, mcid in tagged:
        assert node["/Pg"].indirect_reference == page.indirect_reference
        assert lookup[mcid].get_object() == node
    expected_mcids = [r["mcid"] for r in records if r["page"] == page_index]
    assert expected_mcids == mcids
assert {"/H1", "/H2", "/H3", "/P", "/L", "/LI", "/Lbl", "/LBody"}.issubset(roles)
assert len(reader.outline) == 3

with pdfplumber.open(OUTPUT) as pdf:
    for page in pdf.pages:
        words = page.extract_words()
        assert all(w["x0"] >= 45 and w["x1"] <= 567 and w["top"] >= 25 and w["bottom"] <= 771 for w in words)
        for i, a in enumerate(words):
            for b in words[i + 1:]:
                horizontal = min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])
                vertical = min(a["bottom"], b["bottom"]) - max(a["top"], b["top"])
                assert horizontal < 0.4 or vertical < 0.4, f"Word overlap: {a['text']} / {b['text']}"


def luminance(hex_color):
    values = [int(hex_color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    values = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
    return sum(v * w for v, w in zip(values, (0.2126, 0.7152, 0.0722)))


ratios = {c: round((luminance("#FBF8EF") + 0.05) / (luminance(c) + 0.05), 2)
          for c in ["#173F36", "#293630", "#59665E", "#8A5C00"]}
assert all(r >= 4.5 for r in ratios.values())
print(f"PASS: 3 Letter pages; {len(expected)} source paragraphs preserved in order; {len(records)} tagged text blocks.")
print("PASS: embedded fonts/Unicode maps; structural MCID/parent mappings; headings/lists; language/bookmarks; no links/images/visible version.")
print("PASS: content bounds, block and word overlap checks; normal text contrast", ratios)
print("Accessibility scope: structural checks only; no screen-reader, PDF/UA or full WCAG conformance certification.")
