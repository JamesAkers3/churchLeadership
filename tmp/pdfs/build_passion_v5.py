from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas

import build_passion_v4 as base


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output" / "pdf" / "from-passion-to-impact-v5.pdf"


def contact_dot(c, x, y):
    """Mark one collision point without turning it into a decorative starburst."""
    c.setFillColor(Color(1.0, 0.94, 0.72, alpha=0.96))
    c.circle(x, y, 1.8, fill=1, stroke=0)


def focused_journey(c):
    c.setFillColor(base.PALE_SAGE)
    c.roundRect(42, 410, 528, 213, 14, fill=1, stroke=0)
    base.panel_header(
        c,
        "LIFE-GIVING IMPACT",
        "PASSION + VISION × MISSION = LIFE-GIVING IMPACT",
        596,
        base.FOREST,
    )

    base.optical_window(c, 58, 463, 496, 111)
    source = (84, 529)
    lens = (195, 529)
    contact = (337, 529)
    target = (493, 468)

    base.draw_incident_light(c, *source, *lens, 78)
    base.draw_light_source(c, *source)
    base.draw_focused_light(c, *lens, 78, *contact)
    base.draw_lens(c, *lens, 78)
    base.draw_reflected_light(c, contact, target)
    outgoing_angle = base.line_angle(*contact, *target)
    base.draw_mirror(c, *contact, surface_angle=outgoing_angle / 2, length=61)
    base.draw_living_ground(c, *target, illuminated=True)

    base.stage(c, 55, 446, 78, "PASSION", "energy we bring")
    base.stage(c, 153, 446, 88, "VISION", "clarity that focuses")
    base.stage(c, 282, 446, 108, "MISSION", "direction we receive")
    base.stage(c, 443, 446, 112, "IMPACT", "faithful presence in a real place")


def scattered_journey(c):
    c.setFillColor(base.PALE_RUST)
    c.roundRect(42, 181, 528, 212, 14, fill=1, stroke=0)
    base.panel_header(
        c,
        "LIMITED IMPACT",
        "PASSION - VISION / MISSION = LIMITED IMPACT",
        366,
        base.RUST,
    )

    base.optical_window(c, 58, 233, 496, 111)
    source = (84, 299)
    lens = (195, 299)
    target = (501, 241)

    base.draw_incident_light(c, *source, *lens, 78)
    base.draw_light_source(c, *source)
    base.draw_lens(c, *lens, 78, cracked=True)

    lens_exit = (208, 299)
    contacts = [(323, 307), (337, 299), (323, 291)]
    endpoints = [(405, 340), (430, 272), (402, 239)]

    # Each incident ray ends at one precise point on its reflector.
    for contact in contacts:
        c.setStrokeColor(Color(0.85, 0.39, 0.22, alpha=0.66))
        c.setLineWidth(1.35)
        c.line(lens_exit[0], lens_exit[1], contact[0], contact[1])

    # The reflected paths leave those same points at visibly different angles.
    for contact, endpoint in zip(contacts, endpoints):
        base.draw_fading_ray(c, contact, endpoint)

    # The mirror face sits halfway between the incoming and outgoing ray angles.
    # Drawing the opaque mirror after both segments masks any apparent transmission.
    mirror_angles = []
    for contact, endpoint in zip(contacts, endpoints):
        incoming_angle = base.line_angle(*lens_exit, *contact)
        outgoing_angle = base.line_angle(*contact, *endpoint)
        mirror_angles.append((incoming_angle + outgoing_angle) / 2)

    for contact, angle in zip(contacts, mirror_angles):
        base.draw_mirror(
            c,
            *contact,
            surface_angle=angle,
            length=34,
            contact_glint=False,
        )
        contact_dot(c, *contact)

    base.draw_living_ground(c, *target, illuminated=False)

    base.stage(c, 55, 216, 78, "PASSION", "the energy is still there", base.RUST)
    base.stage(c, 145, 216, 105, "DISTORTED VISION", "sends it off course", base.RUST)
    base.stage(c, 278, 216, 115, "COMPETING MISSIONS", "divide the direction", base.RUST)
    base.stage(c, 439, 216, 116, "LIMITED IMPACT", "less reaches where it was meant to land", base.RUST)


def build():
    base.register_fonts()
    c = canvas.Canvas(
        str(OUTPUT),
        pagesize=LETTER,
        pageCompression=1,
        initialFontName="Arial",
    )
    c.setTitle("From Passion to Impact - V5")
    c.setSubject("How vision and mission turn passion into life-giving impact")
    c.setAuthor("James Akers")

    c.setFillColor(base.PAPER)
    c.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)

    base.kicker(c, "From Passion to Impact", 42, 751)
    c.setFillColor(base.DARK_FOREST)
    c.setFont("Georgia-Bold", 26)
    c.drawString(42, 707, "Passion is powerful.")
    opening = ParagraphStyle(
        "opening",
        fontName="Georgia",
        fontSize=12.2,
        leading=16.5,
        textColor=base.INK,
        alignment=TA_LEFT,
    )
    base.paragraph(
        c,
        "But without vision to focus it and mission to move it, passion becomes scattered energy.",
        43,
        682,
        520,
        opening,
    )

    focused_journey(c)
    scattered_journey(c)

    c.setFillColor(base.DARK_FOREST)
    c.roundRect(42, 53, 528, 103, 12, fill=1, stroke=0)
    c.setFillColor(base.GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawString(58, 134, "THE HEARTBEAT")
    c.setFillColor(base.WHITE)
    c.setFont("Georgia-Bold", 12.2)
    c.drawString(58, 108, "Passion creates the energy. Vision brings it into focus.")
    c.drawString(58, 88, "Mission points it somewhere that matters. Impact happens where it lands.")
    c.setFillColor(HexColor("#D8E1DB"))
    c.setFont("Arial", 8.4)
    c.drawString(58, 70, "Jesus knew why He came. He prayed, chose where to go next, and did not let the crowd choose His mission.")

    c.setFillColor(base.MUTED)
    c.setFont("Arial", 7.8)
    c.drawRightString(554, 32, "Mark 1:35-39")
    c.save()


if __name__ == "__main__":
    build()
