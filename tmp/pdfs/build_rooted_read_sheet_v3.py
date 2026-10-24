"""Build the seed-and-soil revision of the Rooted companion."""

from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
import json

from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/strategy/rooted-read-sheet-v3.md"
OUTPUT = ROOT / "output/pdf/rooted-flourishing-multiplying-life-read-sheet-v3.pdf"
MAP = ROOT / "tmp/pdfs/rooted-read-sheet-v3-content-map.json"

spec = spec_from_file_location("rooted_v2", ROOT / "tmp/pdfs/build_rooted_read_sheet_v2.py")
base = module_from_spec(spec)
spec.loader.exec_module(base)


class V3Sheet(base.Sheet):
    def page(self, number, title):
        if self.pages:
            self.c.showPage()
        self.nodes = []
        self.pages.append(self.nodes)
        self.mcid = 0
        self.c.addLiteral("/Artifact BMC")
        self.c.setFillColor(base.PAPER)
        self.c.rect(0, 0, *base.PAGE, fill=1, stroke=0)
        self.c.setStrokeColor(base.GOLD)
        self.c.setLineWidth(1.3)
        self.c.line(base.LEFT, 728, base.LEFT + 48, 728)
        self.c.setFillColor(base.MUTED)
        self.c.setFont("Arial", 9)
        self.c.drawString(base.LEFT, 29, "ROOTED  |  READ SHEET" if number < 3 else "ROOTED  |  PRESENTER NOTES")
        self.c.drawRightString(base.PAGE[0] - base.LEFT, 29, f"{number} / 3")
        self.c.addLiteral("EMC")
        if number == 1:
            self.draw("ROOTED. FLOURISHING. MULTIPLYING LIFE.", 755,
                      base.style("eyebrow", 9.2, 12, "Arial-Bold", base.TEXT_GOLD), "P")
        else:
            self.c.addLiteral("/Artifact BMC")
            self.c.setFillColor(base.TEXT_GOLD)
            self.c.setFont("Arial-Bold", 9.2)
            self.c.drawString(base.LEFT, 745.69, "ROOTED. FLOURISHING. MULTIPLYING LIFE.")
            self.c.addLiteral("EMC")
        self.y = 711
        title_size = 23 if number == 1 else 22
        self.draw(title, self.y, base.style("title", title_size, 27 if number == 1 else 29,
                                           "Georgia-Bold", base.FOREST),
                  "H1" if number == 1 else "H2")
        self.y -= self.last_height + 16


def build():
    base.SOURCE = SOURCE
    base.OUTPUT = OUTPUT
    base.MAP = MAP
    flags = base.register_fonts()
    sections = base.load_sections()
    raw = BytesIO()
    c = canvas.Canvas(raw, pagesize=base.PAGE, pageCompression=1,
                      pdfVersion=(1, 4), initialFontName="Arial")
    c.setTitle("Rooted. Flourishing. Multiplying Life. - Read Sheet v3")
    c.setAuthor("James Akers")
    c.setCreator("James Akers")
    c.setSubject("A Christ-centered seed-and-soil conversation about recognizing and tending life")
    sheet = V3Sheet(c)

    sheet.page(1, "Life often begins where no one can see it.")
    for paragraph in sections["Opening the conversation"]:
        paragraph_style = base.EMPHASIS if paragraph.startswith("**Faithful leadership") else base.SMALL if paragraph.startswith("**Scripture for reflection") else base.BODY
        sheet.paragraph(paragraph, paragraph_style, gap=5)
    sheet.heading("The Heartbeat")
    for paragraph in sections["The Heartbeat"]:
        paragraph_style = base.QUOTE if paragraph.startswith("Jesus says") else base.EMPHASIS if paragraph.startswith("**Systems") else base.SMALL if paragraph.startswith("John 15:4") else base.BODY
        sheet.paragraph(paragraph, paragraph_style, gap=5)

    sheet.page(2, "Walking through the image")
    for paragraph in sections["Walking through the image"]:
        sheet.paragraph(paragraph, gap=4)
    sheet.heading("Questions worth sitting with")
    sheet.list(sections["Questions worth sitting with"][0].splitlines(), numbered=True, gap=4)
    sheet.heading("Putting this into practice")
    for paragraph in sections["Putting this into practice"]:
        sheet.paragraph(paragraph, gap=4)
    sheet.heading("Moving into the next chapter")
    for paragraph in sections["Moving into the next chapter"]:
        sheet.paragraph(paragraph, base.EMPHASIS if paragraph.startswith("Who knows") else base.BODY, gap=4)

    sheet.page(3, "Presenter notes")
    sheet.list(sections["Notes for the presenter"][0].splitlines(), text_style=base.NOTES, gap=4)
    sheet.heading("Scripture and image boundaries", notes=True)
    sheet.paragraph(sections["Scripture and image boundaries"][0], base.NOTES)
    sheet.list(sections["Scripture and image boundaries"][1].splitlines(), text_style=base.NOTES, gap=4)
    sheet.y -= 4
    sheet.paragraph("NIV quotation: Holy Bible, New International Version®, NIV®. Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.® All rights reserved worldwide.", base.SMALL)

    c.save()
    raw.seek(0)
    base.add_structure(raw, sheet)
    MAP.write_text(json.dumps({"font_embedding_flags": flags, "records": sheet.records}, indent=2, ensure_ascii=False) + "\n")
    print(f"Created {OUTPUT.name}: 3 pages; embedding restriction flags {flags}")
    print("Lowest content bottom by page:", [round(min(record["box"][1] for record in sheet.records if record["page"] == page), 1) for page in range(3)])


if __name__ == "__main__":
    build()
