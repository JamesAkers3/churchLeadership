"""Build the practical-language revision of the Rooted companion."""

from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
import json

from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/strategy/rooted-read-sheet-v4.md"
OUTPUT = ROOT / "output/pdf/rooted-flourishing-multiplying-life-read-sheet-v4.pdf"
MAP = ROOT / "tmp/pdfs/rooted-read-sheet-v4-content-map.json"
VERSION = "v4"

spec = spec_from_file_location("rooted_v3", ROOT / "tmp/pdfs/build_rooted_read_sheet_v3.py")
v3 = module_from_spec(spec)
spec.loader.exec_module(v3)
base = v3.base


def build():
    base.SOURCE = SOURCE
    base.OUTPUT = OUTPUT
    base.MAP = MAP
    flags = base.register_fonts()
    sections = base.load_sections()
    raw = BytesIO()
    c = canvas.Canvas(raw, pagesize=base.PAGE, pageCompression=1,
                      pdfVersion=(1, 4), initialFontName="Arial")
    c.setTitle(f"Rooted. Flourishing. Multiplying Life. - Read Sheet {VERSION}")
    c.setAuthor("James Akers")
    c.setCreator("James Akers")
    c.setSubject("A Christ-centered seed-and-soil conversation about recognizing and tending life")
    sheet = v3.V3Sheet(c)

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
    sheet.list(sections["Scripture and image boundaries"][0].splitlines(), text_style=base.NOTES, gap=4)
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
