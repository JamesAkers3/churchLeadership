"""Create the approved three-page Rooted companion with tagged, embedded text."""

from html import escape
from io import BytesIO
from pathlib import Path
import json
import re
import struct

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject, BooleanObject, DictionaryObject, NameObject, NumberObject,
    TextStringObject,
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/strategy/rooted-read-sheet-v1.md"
OUTPUT = ROOT / "output/pdf/rooted-flourishing-multiplying-life-read-sheet-v1.pdf"
MAP = ROOT / "tmp/pdfs/rooted-read-sheet-v1-content-map.json"
PAGE = (612, 792)
LEFT, WIDTH = 46, 520
PAPER = HexColor("#FBF8EF")
FOREST = HexColor("#173F36")
INK = HexColor("#293630")
MUTED = HexColor("#59665E")
GOLD = HexColor("#D5A13A")
TEXT_GOLD = HexColor("#8A5C00")


def load_sections():
    sections = {}
    for part in re.split(r"(?m)^## ", SOURCE.read_text())[1:]:
        heading, body = part.split("\n", 1)
        sections[heading] = [p.strip() for p in body.strip().split("\n\n") if p.strip() != "---"]
    return sections


def register_fonts():
    flags = {}
    for name, filename in (
        ("Arial", "Arial.ttf"), ("Arial-Bold", "Arial Bold.ttf"),
        ("Georgia", "Georgia.ttf"), ("Georgia-Bold", "Georgia Bold.ttf"),
    ):
        path = Path("/System/Library/Fonts/Supplemental") / filename
        data = path.read_bytes()
        count = struct.unpack_from(">H", data, 4)[0]
        for i in range(count):
            tag, _, offset, _ = struct.unpack_from(">4sIII", data, 12 + i * 16)
            if tag == b"OS/2":
                flags[name] = struct.unpack_from(">H", data, offset + 8)[0]
                break
        if flags.get(name, 2) & (2 | 256 | 512):
            raise ValueError(f"Font not eligible for this outline-subset embedding: {name}")
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")
    pdfmetrics.registerFontFamily("Georgia", normal="Georgia", bold="Georgia-Bold")
    return flags


def markup(text):
    return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", escape(text))


def style(name, size=12, leading=15.3, font="Arial", color=INK):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading,
                          textColor=color, allowWidows=0, allowOrphans=0)


BODY = style("body")
NOTES = style("notes", 11, 13.5)
HEADING = style("heading", 16, 19, "Georgia-Bold", FOREST)
NOTE_HEADING = style("note-heading", 15, 18, "Georgia-Bold", FOREST)
QUOTE = style("quote", 16, 20, "Georgia-Bold", FOREST)
EMPHASIS = style("emphasis", 12.4, 16, "Georgia-Bold", FOREST)
SMALL = style("small", 10, 12.7, "Arial", MUTED)


class Sheet:
    def __init__(self, c):
        self.c, self.pages, self.records = c, [], []

    def page(self, number, title):
        if self.pages:
            self.c.showPage()
        self.nodes = []
        self.pages.append(self.nodes)
        self.mcid = 0
        self.c.addLiteral("/Artifact BMC")
        self.c.setFillColor(PAPER)
        self.c.rect(0, 0, *PAGE, fill=1, stroke=0)
        self.c.setStrokeColor(GOLD)
        self.c.setLineWidth(1.3)
        self.c.line(LEFT, 728, LEFT + 48, 728)
        self.c.setFillColor(MUTED)
        self.c.setFont("Arial", 9)
        self.c.drawString(LEFT, 29, "ROOTED  |  READ SHEET" if number < 3 else "ROOTED  |  PRESENTER NOTES")
        self.c.drawRightString(PAGE[0] - LEFT, 29, f"{number} / 3")
        self.c.addLiteral("EMC")
        if number == 1:
            self.draw("ROOTED. FLOURISHING. MULTIPLYING LIFE.", 755,
                      style("eyebrow", 9.2, 12, "Arial-Bold", TEXT_GOLD), "P")
        else:
            self.c.addLiteral("/Artifact BMC")
            self.c.setFillColor(TEXT_GOLD)
            self.c.setFont("Arial-Bold", 9.2)
            self.c.drawString(LEFT, 745.69, "ROOTED. FLOURISHING. MULTIPLYING LIFE.")
            self.c.addLiteral("EMC")
        self.y = 711
        self.draw(title, self.y, style("title", 25 if number == 1 else 22, 29,
                                     "Georgia-Bold", FOREST), "H1" if number == 1 else "H2")
        self.y -= self.last_height + 16

    def draw(self, text, top, text_style=BODY, role="P", parent=None, x=LEFT, width=WIDTH):
        p = Paragraph(markup(text), text_style)
        _, height = p.wrap(width, 1000)
        bottom = top - height
        if bottom < 57:
            raise ValueError(f"Page {len(self.pages)} overflows at {text[:65]!r}: {bottom:.1f}")
        node = {"role": role, "mcid": self.mcid, "page": len(self.pages) - 1, "children": []}
        (self.nodes if parent is None else parent["children"]).append(node)
        self.c.addLiteral(f"/{role} << /MCID {self.mcid} >> BDC")
        p.drawOn(self.c, x, bottom)
        self.c.addLiteral("EMC")
        self.records.append({"page": len(self.pages) - 1, "mcid": self.mcid,
                             "role": role, "text": re.sub(r"\*\*(.*?)\*\*", r"\1", text),
                             "box": [x, bottom, x + width, top], "font_size": text_style.fontSize})
        self.mcid += 1
        self.last_height = height
        return height

    def paragraph(self, text, text_style=BODY, role="P", gap=6):
        self.y -= self.draw(text, self.y, text_style, role) + gap

    def heading(self, text, notes=False):
        self.y -= 7
        self.paragraph(text, NOTE_HEADING if notes else HEADING,
                       "H3" if notes else "H2", gap=6)

    def list(self, lines, numbered=False, text_style=BODY, gap=5):
        group = {"role": "L", "children": []}
        self.nodes.append(group)
        for i, line in enumerate(lines, 1):
            text = re.sub(r"^(?:- |\d+\. )", "", line)
            item = {"role": "LI", "children": []}
            group["children"].append(item)
            self.draw(f"{i}." if numbered else "•", self.y, text_style, "Lbl",
                      parent=item, width=17)
            self.y -= self.draw(text, self.y, text_style, "LBody", parent=item,
                                x=LEFT + 20, width=WIDTH - 20) + gap


def add_structure(raw, sheet):
    writer = PdfWriter()
    writer.clone_document_from_reader(PdfReader(raw))
    writer.pdf_header = "%PDF-1.4"
    root = DictionaryObject({NameObject("/Type"): NameObject("/StructTreeRoot")})
    root_ref = writer._add_object(root)
    document = DictionaryObject({NameObject("/Type"): NameObject("/StructElem"),
                                 NameObject("/S"): NameObject("/Document"),
                                 NameObject("/P"): root_ref})
    doc_ref = writer._add_object(document)
    root[NameObject("/K")] = ArrayObject([doc_ref])
    document[NameObject("/K")] = ArrayObject()
    parent_nums = ArrayObject()
    for index, nodes in enumerate(sheet.pages):
        page_ref = writer.pages[index].indirect_reference
        sect = DictionaryObject({NameObject("/Type"): NameObject("/StructElem"),
                                 NameObject("/S"): NameObject("/Sect"),
                                 NameObject("/P"): doc_ref, NameObject("/Pg"): page_ref,
                                 NameObject("/K"): ArrayObject()})
        sect_ref = writer._add_object(sect)
        document[NameObject("/K")].append(sect_ref)
        lookup = {}

        def append_node(node, parent_ref):
            elem = DictionaryObject({NameObject("/Type"): NameObject("/StructElem"),
                                     NameObject("/S"): NameObject("/" + node["role"]),
                                     NameObject("/P"): parent_ref, NameObject("/Pg"): page_ref})
            ref = writer._add_object(elem)
            if "mcid" in node:
                elem[NameObject("/K")] = NumberObject(node["mcid"])
                lookup[node["mcid"]] = ref
            else:
                elem[NameObject("/K")] = ArrayObject([append_node(child, ref) for child in node["children"]])
            return ref

        sect[NameObject("/K")].extend(append_node(n, sect_ref) for n in nodes)
        parent_nums.extend([NumberObject(index), ArrayObject([lookup[i] for i in range(len(lookup))])])
        writer.pages[index][NameObject("/StructParents")] = NumberObject(index)
        writer.pages[index][NameObject("/Tabs")] = NameObject("/S")
    root[NameObject("/ParentTree")] = writer._add_object(DictionaryObject({NameObject("/Nums"): parent_nums}))
    root[NameObject("/ParentTreeNextKey")] = NumberObject(len(sheet.pages))
    writer._root_object[NameObject("/StructTreeRoot")] = root_ref
    writer._root_object[NameObject("/MarkInfo")] = DictionaryObject({NameObject("/Marked"): BooleanObject(True)})
    writer._root_object[NameObject("/Lang")] = TextStringObject("en-US")
    writer._root_object[NameObject("/ViewerPreferences")] = DictionaryObject({NameObject("/DisplayDocTitle"): BooleanObject(True)})
    writer.add_outline_item("Rooted. Flourishing. Multiplying Life.", 0)
    writer.add_outline_item("Discussion and practice", 1)
    writer.add_outline_item("Presenter notes", 2)
    with OUTPUT.open("wb") as stream:
        writer.write(stream)


def build():
    flags = register_fonts()
    sections = load_sections()
    raw = BytesIO()
    c = canvas.Canvas(raw, pagesize=PAGE, pageCompression=1, pdfVersion=(1, 4), initialFontName="Arial")
    c.setTitle("Rooted. Flourishing. Multiplying Life. - Read Sheet v1")
    c.setAuthor("James Akers")
    c.setCreator("James Akers")
    c.setSubject("Two reading pages and separate presenter notes for a Christ-centered church advisory mini-book")
    sheet = Sheet(c)
    sheet.page(1, "Bare is not the same as dead.")
    sheet.heading("Opening the conversation")
    for p in sections["Opening the conversation"]:
        sheet.paragraph(p)
    sheet.heading("The Heartbeat")
    for p in sections["The Heartbeat"]:
        text_style = QUOTE if p.startswith("Jesus says") else EMPHASIS if p.startswith("**Systems") else SMALL if p.startswith("John 15:4") else BODY
        sheet.paragraph(p, text_style)
    sheet.heading("Walking through the image")
    for p in sections["Walking through the image"][:2]:
        sheet.paragraph(p)

    sheet.page(2, "Walking through the image")
    for p in sections["Walking through the image"][2:]:
        sheet.paragraph(p, gap=5)
    sheet.heading("Questions worth sitting with")
    sheet.list(sections["Questions worth sitting with"][0].splitlines(), numbered=True)
    sheet.heading("Putting this into practice")
    for p in sections["Putting this into practice"]:
        sheet.paragraph(p, gap=5)
    sheet.heading("Moving into the next chapter")
    for p in sections["Moving into the next chapter"]:
        sheet.paragraph(p, EMPHASIS if p.startswith("Who has room") else BODY, gap=5)

    sheet.page(3, "Presenter notes")
    sheet.list(sections["Notes for the presenter"][0].splitlines(), text_style=NOTES, gap=5)
    sheet.heading("Scripture and image boundaries", notes=True)
    sheet.paragraph(sections["Scripture and image boundaries"][0], NOTES)
    sheet.list(sections["Scripture and image boundaries"][1].splitlines(), text_style=NOTES, gap=5)
    sheet.y -= 6
    sheet.paragraph("NIV quotation: Holy Bible, New International Version®, NIV®. Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.® All rights reserved worldwide.", SMALL)
    c.save()
    raw.seek(0)
    add_structure(raw, sheet)
    MAP.write_text(json.dumps({"font_embedding_flags": flags, "records": sheet.records}, indent=2, ensure_ascii=False) + "\n")
    print(f"Created {OUTPUT.name}: 3 pages; embedding restriction flags {flags}")
    print("Lowest content bottom by page:", [round(min(r["box"][1] for r in sheet.records if r["page"] == i), 1) for i in range(3)])


if __name__ == "__main__":
    build()
