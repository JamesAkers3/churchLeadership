from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas

import build_passion_v4 as optics
import build_passion_v5 as prior


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output" / "pdf" / "from-passion-to-impact-v6.pdf"


def draw_clouded_lens(c, x, y, height=78):
    """An intact lens whose softened center cannot gather light to one point."""
    optics.draw_lens(c, x, y, height, cracked=False)

    # Restrained, nested haze stays inside the glass boundary.
    haze = [
        (16, 54, 0.09),
        (13, 43, 0.13),
        (9, 31, 0.18),
    ]
    for width, h, alpha in haze:
        c.setFillColor(Color(0.94, 0.94, 0.87, alpha=alpha))
        c.ellipse(x - width, y - h / 2, x + width, y + h / 2, fill=1, stroke=0)

    # A soft offset highlight suggests haze, not breakage.
    c.setStrokeColor(Color(1, 1, 1, alpha=0.30))
    c.setLineWidth(1.0)
    c.line(x - 5, y - 23, x - 5, y + 22)


def draw_unfocused_field(c, lens_x, lens_y):
    """Show energy remaining broad after the lens rather than converging."""
    optics.polygon(
        c,
        [
            (lens_x + 13, lens_y - 28),
            (423, lens_y - 40),
            (423, lens_y + 40),
            (lens_x + 13, lens_y + 28),
        ],
        Color(0.80, 0.38, 0.20, alpha=0.055),
    )


def scattered_journey(c):
    c.setFillColor(optics.PALE_RUST)
    c.roundRect(42, 181, 528, 212, 14, fill=1, stroke=0)
    optics.panel_header(
        c,
        "LIMITED IMPACT",
        "PASSION - VISION / MISSION = LIMITED IMPACT",
        366,
        optics.RUST,
    )

    optics.optical_window(c, 58, 233, 496, 111)
    source = (84, 299)
    lens = (195, 299)
    target = (501, 241)

    optics.draw_incident_light(c, *source, *lens, 78)
    optics.draw_light_source(c, *source)
    draw_clouded_lens(c, *lens, 78)

    # The intact but clouded lens leaves the light broad. Each ray begins from
    # a different part of the lens instead of converging at one shared focus.
    lens_exits = [(208, 315), (208, 299), (208, 283)]
    contacts = [(303, 321), (357, 299), (411, 279)]
    endpoints = [(360, 341), (438, 273), (461, 238)]

    for lens_exit, contact in zip(lens_exits, contacts):
        c.setStrokeColor(Color(0.85, 0.39, 0.22, alpha=0.64))
        c.setLineWidth(1.35)
        c.line(lens_exit[0], lens_exit[1], contact[0], contact[1])

    for contact, endpoint in zip(contacts, endpoints):
        optics.draw_fading_ray(c, contact, endpoint)

    for lens_exit, contact, endpoint in zip(lens_exits, contacts, endpoints):
        incoming_angle = optics.line_angle(*lens_exit, *contact)
        outgoing_angle = optics.line_angle(*contact, *endpoint)
        surface_angle = (incoming_angle + outgoing_angle) / 2
        optics.draw_mirror(
            c,
            *contact,
            surface_angle=surface_angle,
            length=34,
            contact_glint=False,
        )
        prior.contact_dot(c, *contact)

    optics.draw_living_ground(c, *target, illuminated=False)

    optics.stage(c, 55, 216, 78, "PASSION", "the energy is still there", optics.RUST)
    optics.stage(c, 145, 216, 105, "UNCLEAR VISION", "leaves the energy spread wide", optics.RUST)
    optics.stage(c, 278, 216, 115, "COMPETING MISSIONS", "pull it in different directions", optics.RUST)
    optics.stage(c, 439, 216, 116, "LIMITED IMPACT", "less reaches where it was meant to land", optics.RUST)


def build():
    optics.register_fonts()
    c = canvas.Canvas(
        str(OUTPUT),
        pagesize=LETTER,
        pageCompression=1,
        initialFontName="Arial",
    )
    c.setTitle("From Passion to Impact - V6")
    c.setSubject("How vision and mission turn passion into life-giving impact")
    c.setAuthor("James Akers")

    c.setFillColor(optics.PAPER)
    c.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)

    optics.kicker(c, "From Passion to Impact", 42, 751)
    c.setFillColor(optics.DARK_FOREST)
    c.setFont("Georgia-Bold", 26)
    c.drawString(42, 707, "Passion is powerful.")
    opening = ParagraphStyle(
        "opening",
        fontName="Georgia",
        fontSize=12.2,
        leading=16.5,
        textColor=optics.INK,
        alignment=TA_LEFT,
    )
    optics.paragraph(
        c,
        "But without vision to focus it and mission to move it, passion becomes scattered energy.",
        43,
        682,
        520,
        opening,
    )

    prior.focused_journey(c)
    scattered_journey(c)

    c.setFillColor(optics.DARK_FOREST)
    c.roundRect(42, 53, 528, 103, 12, fill=1, stroke=0)
    c.setFillColor(optics.GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawString(58, 134, "THE HEARTBEAT")
    c.setFillColor(optics.WHITE)
    c.setFont("Georgia-Bold", 12.2)
    c.drawString(58, 108, "Passion creates the energy. Vision brings it into focus.")
    c.drawString(58, 88, "Mission points it somewhere that matters. Impact happens where it lands.")
    c.setFillColor(HexColor("#D8E1DB"))
    c.setFont("Arial", 8.4)
    c.drawString(58, 70, "Jesus knew why He came. He prayed, chose where to go next, and did not let the crowd choose His mission.")

    c.setFillColor(optics.MUTED)
    c.setFont("Arial", 7.8)
    c.drawRightString(554, 32, "Mark 1:35-39")
    c.save()


if __name__ == "__main__":
    build()
