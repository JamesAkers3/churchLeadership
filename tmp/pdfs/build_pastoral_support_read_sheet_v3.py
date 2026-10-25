"""Vertically center the two support paragraphs beside their quote boxes."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output/pdf/a-pastor-can-be-known-and-still-unsupported-read-sheet-v3.pdf"
MAP = ROOT / "tmp/pdfs/pastoral-support-read-sheet-v3-content-map.json"

spec = spec_from_file_location("support_v2", ROOT / "tmp/pdfs/build_pastoral_support_read_sheet_v2.py")
v2 = module_from_spec(spec)
spec.loader.exec_module(v2)
v1 = v2.v1
base = v2.base


class V3SupportSheet(v2.V2SupportSheet):
    def side_quote(self, main_text, quote_text, author):
        top = self.y
        left_width = 310
        right_x = base.LEFT + 332
        right_width = base.WIDTH - 332

        main_para = v1.Paragraph(base.markup(main_text), v1.BODY)
        _, main_h = main_para.wrap(left_width, 1000)
        quote_para = v1.Paragraph(base.markup(quote_text), v1.QUOTE)
        _, quote_h = quote_para.wrap(right_width - 26, 1000)
        author_para = v1.Paragraph(base.markup(author), v1.QUOTE_AUTHOR)
        _, author_h = author_para.wrap(right_width - 26, 1000)
        box_h = quote_h + author_h + 34
        box_bottom = top - box_h
        if box_bottom < 57:
            raise ValueError("Side quotation overflows the page")

        self.c.addLiteral("/Artifact BMC")
        self.c.setFillColor(v1.PAPER_LIGHT)
        self.c.roundRect(right_x, box_bottom, right_width, box_h, 10, fill=1, stroke=0)
        self.c.setFillColor(v1.GOLD)
        self.c.rect(right_x, box_bottom, 3.2, box_h, fill=1, stroke=0)
        self.c.addLiteral("EMC")

        main_top = top - max(0, (box_h - main_h) / 2)
        self.draw(main_text, main_top, v1.BODY, "P", x=base.LEFT, width=left_width)

        quote_top = top - 14
        quote_h_drawn = self.draw(quote_text, quote_top, v1.QUOTE, "BlockQuote", x=right_x + 14, width=right_width - 26)
        author_top = quote_top - quote_h_drawn - 8
        self.draw(author, author_top, v1.QUOTE_AUTHOR, "P", x=right_x + 14, width=right_width - 26)
        self.y = box_bottom - 8


v2.OUTPUT = OUTPUT
v2.MAP = MAP
v2.VERSION = "v3"
v2.V2SupportSheet = V3SupportSheet


if __name__ == "__main__":
    v2.build()
