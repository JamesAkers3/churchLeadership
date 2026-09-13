from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas

import build_passion_v4 as optics
import build_passion_v5 as prior


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output" / "pdf" / "from-passion-to-impact-v7.pdf"


def panel_header(c, title, equation, y, color):
    c.setFillColor(color)
    c.setFont("Arial-Bold", 9.2)
    c.drawString(59, y, title)
    c.setFont("Arial-Bold", 7.4)
    c.drawRightString(553, y + 0.5, equation)


def draw_clouded_lens(c, x, y, height=78):
    """An intact lens with a quiet, slightly off-center haze."""
    optics.draw_lens(c, x, y, height, cracked=False)
    for dx, dy, width, h, alpha in (
        (-2, 2, 15, 51, 0.08),
        (-1, 0, 12, 39, 0.12),
        (1, -2, 8, 27, 0.17),
    ):
        c.setFillColor(Color(0.94, 0.94, 0.87, alpha=alpha))
        c.ellipse(x + dx - width, y + dy - h / 2, x + dx + width, y + dy + h / 2, fill=1, stroke=0)

    c.setStrokeColor(Color(1, 1, 1, alpha=0.26))
    c.setLineWidth(0.9)
    c.line(x - 5, y - 22, x - 5, y + 21)


def strong_fading_ray(c, contact, endpoint):
    """Keep the redirected path legible in print before it loses strength."""
    x1, y1 = contact
    x2, y2 = endpoint
    for i, alpha in enumerate((0.90, 0.76, 0.56, 0.30)):
        t0 = i / 4
        t1 = (i + 1) / 4
        sx = x1 + (x2 - x1) * t0
        sy = y1 + (y2 - y1) * t0
        ex = x1 + (x2 - x1) * t1
        ey = y1 + (y2 - y1) * t1
        c.setStrokeColor(Color(optics.RUST.red, optics.RUST.green, optics.RUST.blue, alpha=alpha))
        c.setLineWidth(max(1.0, 1.8 - i * 0.16))
        c.line(sx, sy, ex, ey)


def stage(c, x, y_top, width, title, body, title_color=optics.FOREST, body_size=8.2):
    style = ParagraphStyle(
        f"stage-{title}",
        fontName="Arial",
        fontSize=body_size,
        leading=10.2,
        textColor=optics.INK,
        alignment=TA_CENTER,
    )
    html = (
        f'<font name="Arial-Bold" color="{title_color.hexval()}" size="8.6">'
        f"{title}</font><br/>{body}"
    )
    optics.paragraph(c, html, x, y_top, width, style)


def focused_journey(c):
    c.setFillColor(optics.PALE_SAGE)
    c.roundRect(42, 410, 528, 213, 14, fill=1, stroke=0)
    panel_header(c, "LIFE-GIVING IMPACT", "PASSION + VISION × MISSION = LIFE-GIVING IMPACT", 596, optics.FOREST)

    optics.optical_window(c, 58, 463, 496, 111)
    source = (84, 529)
    lens = (195, 529)
    contact = (337, 529)
    target = (493, 468)

    optics.draw_incident_light(c, *source, *lens, 78)
    optics.draw_light_source(c, *source)
    optics.draw_focused_light(c, *lens, 78, *contact)
    optics.draw_lens(c, *lens, 78)
    optics.draw_reflected_light(c, contact, target)
    outgoing_angle = optics.line_angle(*contact, *target)
    optics.draw_mirror(c, *contact, surface_angle=outgoing_angle / 2, length=61)
    optics.draw_living_ground(c, *target, illuminated=True)

    stage(c, 55, 446, 78, "PASSION", "energy we bring")
    stage(c, 153, 446, 88, "VISION", "clarity that focuses")
    stage(c, 282, 446, 108, "MISSION", "direction we receive")
    stage(c, 430, 446, 132, "IMPACT", "faithful presence where God has called us", body_size=8.0)


def limited_journey(c):
    c.setFillColor(optics.PALE_RUST)
    c.roundRect(42, 181, 528, 212, 14, fill=1, stroke=0)
    panel_header(c, "LIMITED IMPACT", "PASSION - VISION / MISSION = LIMITED IMPACT", 366, optics.RUST)

    optics.optical_window(c, 58, 233, 496, 111)
    source = (84, 299)
    lens = (195, 299)
    target = (501, 241)

    optics.draw_incident_light(c, *source, *lens, 78)
    optics.draw_light_source(c, *source)
    draw_clouded_lens(c, *lens, 78)

    lens_exits = [(208, 315), (208, 299), (208, 283)]
    contacts = [(303, 321), (357, 299), (411, 279)]
    endpoints = [(366, 344), (446, 270), (470, 236)]

    for lens_exit, contact in zip(lens_exits, contacts):
        c.setStrokeColor(Color(0.85, 0.39, 0.22, alpha=0.72))
        c.setLineWidth(1.45)
        c.line(lens_exit[0], lens_exit[1], contact[0], contact[1])

    for contact, endpoint in zip(contacts, endpoints):
        strong_fading_ray(c, contact, endpoint)

    for lens_exit, contact, endpoint in zip(lens_exits, contacts, endpoints):
        incoming_angle = optics.line_angle(*lens_exit, *contact)
        outgoing_angle = optics.line_angle(*contact, *endpoint)
        optics.draw_mirror(c, *contact, surface_angle=(incoming_angle + outgoing_angle) / 2, length=34, contact_glint=False)
        prior.contact_dot(c, *contact)

    optics.draw_living_ground(c, *target, illuminated=False)

    stage(c, 55, 216, 78, "PASSION", "the energy is still there", optics.RUST)
    stage(c, 145, 216, 105, "UNCLEAR VISION", "leaves the energy spread wide", optics.RUST)
    stage(c, 276, 216, 120, "DIVIDED DIRECTION", "pulls the work in different directions", optics.RUST, body_size=7.9)
    stage(c, 439, 216, 116, "LIMITED IMPACT", "less reaches where it was meant to land", optics.RUST)


def build():
    optics.register_fonts()
    c = canvas.Canvas(str(OUTPUT), pagesize=LETTER, pageCompression=1, initialFontName="Arial")
    c.setTitle("From Passion to Impact - V7")
    c.setSubject("How vision and mission help direct passion toward life-giving impact")
    c.setAuthor("James Akers")

    c.setFillColor(optics.PAPER)
    c.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)

    optics.kicker(c, "From Passion to Impact", 42, 751)
    c.setFillColor(optics.DARK_FOREST)
    c.setFont("Georgia-Bold", 26)
    c.drawString(42, 707, "Passion is powerful.")
    opening = ParagraphStyle("opening", fontName="Georgia", fontSize=12.2, leading=16.5, textColor=optics.INK, alignment=TA_LEFT)
    optics.paragraph(c, "But without vision to focus it and mission to move it, passion becomes scattered energy.", 43, 682, 520, opening)

    focused_journey(c)
    limited_journey(c)

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
    c.setFont("Arial", 7.8)
    c.drawString(58, 70, "Jesus knew why He came and stayed faithful to the Father's purpose. We align what we carry with where He is leading.")
    c.setFont("Arial-Bold", 7.8)
    c.drawString(58, 58, "Only Jesus gives life.")
    c.setFont("Arial", 7.8)
    c.drawRightString(554, 58, "Mark 1:35-39")
    c.save()


if __name__ == "__main__":
    build()
