"""Build the prayer-centered pastoral-support companion revision."""

from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
import json

from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/strategy/pastoral-support-read-sheet-v6.md"
OUTPUT = ROOT / "output/pdf/a-pastor-can-be-known-and-still-unsupported-read-sheet-v6.pdf"
MAP = ROOT / "tmp/pdfs/pastoral-support-read-sheet-v6-content-map.json"

spec = spec_from_file_location("support_v5", ROOT / "tmp/pdfs/build_pastoral_support_read_sheet_v5.py")
v5 = module_from_spec(spec)
spec.loader.exec_module(v5)
v3 = v5.v3
v1 = v5.v1
base = v5.base


def build():
    v1.SOURCE = SOURCE
    base.SOURCE = SOURCE
    base.OUTPUT = OUTPUT
    base.MAP = MAP
    flags = base.register_fonts()
    sections = v1.load_sections()

    raw = BytesIO()
    c = canvas.Canvas(raw, pagesize=base.PAGE, pageCompression=1, pdfVersion=(1, 4), initialFontName="Arial")
    c.setTitle("A Pastor Can Be Known and Still Unsupported - Read Sheet v6")
    c.setAuthor("James Akers")
    c.setCreator("James Akers")
    c.setSubject("A Christ-centered conversation about pastoral support, shared prayer, and shared responsibility")
    sheet = v3.V3SupportSheet(c)

    opening = sections["Opening the conversation"]
    gethsemane = sections["Jesus named His sorrow"]
    bonhoeffer = sections["Bonhoeffer quotation"]
    weight = sections["The weight can be shared without diminishing the calling"]
    compassion = sections["Compassion takes different forms"]
    stanley = sections["Andy Stanley quotation"]

    sheet.page(1, opening[0])
    sheet.paragraph(opening[1], v1.BODY_COMPACT, gap=5)
    sheet.paragraph(opening[2], v1.BODY_COMPACT, gap=5)
    sheet.paragraph(opening[3], v1.EMPHASIS, gap=4)
    sheet.heading("Jesus named His sorrow")
    sheet.paragraph(gethsemane[0], v1.BODY_COMPACT, gap=4)
    sheet.paragraph(gethsemane[1], v1.BODY_COMPACT, gap=5)
    sheet.side_quote(gethsemane[2], bonhoeffer[0], bonhoeffer[1])
    for paragraph in gethsemane[3:]:
        sheet.paragraph(paragraph, v1.BODY_COMPACT, gap=5)
    sheet.heading("The weight can be shared without diminishing the calling")
    for paragraph in weight:
        paragraph_style = v1.EMPHASIS if paragraph.startswith("**The calling") else v1.BODY_COMPACT
        sheet.paragraph(paragraph, paragraph_style, gap=4)

    sheet.page(2, "Compassion takes different forms.")
    sheet.paragraph(compassion[0], v1.EMPHASIS, gap=5)
    sheet.paragraph(compassion[1], v1.BODY_COMPACT, gap=5)
    sheet.side_quote(compassion[2], stanley[0], stanley[1])
    sheet.paragraph(compassion[3], v1.EMPHASIS, gap=5)
    sheet.heading("Questions worth sitting with")
    sheet.list(sections["Questions worth sitting with"][0].splitlines(), numbered=True, text_style=v1.BODY_COMPACT, gap=3)
    sheet.heading("Putting this into practice")
    for paragraph in sections["Putting this into practice"]:
        paragraph_style = v1.EMPHASIS if paragraph.startswith("Caring for") else v1.BODY_COMPACT
        sheet.paragraph(paragraph, paragraph_style, gap=3)
    sheet.heading("Moving into the next chapter")
    for paragraph in sections["Moving into the next chapter"]:
        sheet.paragraph(paragraph, v1.EMPHASIS if paragraph.startswith("That brings") else v1.BODY_COMPACT, gap=2)

    sheet.page(3, "Presenter notes")
    sheet.list(sections["Notes for the presenter"][0].splitlines(), text_style=v1.NOTES, gap=3)
    sheet.heading("Scripture and content boundaries", notes=True)
    sheet.list(sections["Scripture and content boundaries"][0].splitlines(), text_style=v1.NOTES, gap=3)
    sheet.heading("Sources", notes=True)
    sheet.list(sections["Sources"][0].splitlines(), text_style=v1.SMALL, gap=2)

    c.save()
    raw.seek(0)
    base.add_structure(raw, sheet)
    MAP.write_text(json.dumps({"font_embedding_flags": flags, "records": sheet.records}, indent=2, ensure_ascii=False) + "\n")
    print(f"Created {OUTPUT.name}: 3 pages; embedding restriction flags {flags}")
    print("Lowest content bottom by page:", [round(min(record["box"][1] for record in sheet.records if record["page"] == page), 1) for page in range(3)])


if __name__ == "__main__":
    build()
