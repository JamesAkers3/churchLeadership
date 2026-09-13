from math import atan2, cos, degrees, radians, sin
from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from build_v2_visuals import (
    DARK_FOREST,
    FOREST,
    GOLD,
    INK,
    MUTED,
    PAPER,
    TEXT_GOLD,
    WHITE,
    kicker,
    register_fonts,
)


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output" / "pdf" / "from-passion-to-impact-v4.pdf"

PALE_SAGE = HexColor("#E7EDDF")
PALE_RUST = HexColor("#F1E3D8")
RUST = HexColor("#B85F3D")
OPTICAL_FIELD = HexColor("#142E29")
OPTICAL_EDGE = HexColor("#355148")
GLASS = HexColor("#B9D9D1")
GLASS_EDGE = HexColor("#A9DDD5")
MIRROR_FACE = HexColor("#F2D68B")
MIRROR_EDGE = HexColor("#8B6726")
SOIL = HexColor("#9B7654")
MOSS = HexColor("#88A96F")
DIM = HexColor("#62766E")


def paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - height)
    return height


def panel_header(c, title, equation, y, color):
    c.setFillColor(color)
    c.setFont("Arial-Bold", 9.2)
    c.drawString(59, y, title)
    c.setFont("Arial-Bold", 8.9)
    c.drawRightString(553, y, equation)


def stage(c, x, y_top, width, title, body, title_color=FOREST):
    style = ParagraphStyle(
        "stage",
        fontName="Arial",
        fontSize=8.2,
        leading=10.2,
        textColor=INK,
        alignment=TA_CENTER,
    )
    html = (
        f'<font name="Arial-Bold" color="{title_color.hexval()}" size="8.6">'
        f"{title}</font><br/>{body}"
    )
    paragraph(c, html, x, y_top, width, style)


def optical_window(c, x, y, width, height):
    c.setFillColor(OPTICAL_FIELD)
    c.setStrokeColor(OPTICAL_EDGE)
    c.setLineWidth(0.8)
    c.roundRect(x, y, width, height, 10, fill=1, stroke=1)

    # A restrained inner haze gives the light room to feel dimensional.
    c.setFillColor(Color(0.34, 0.43, 0.36, alpha=0.10))
    c.ellipse(x + 20, y + height * 0.20, x + width - 20, y + height * 0.88, fill=1, stroke=0)


def polygon(c, points, fill):
    p = c.beginPath()
    p.moveTo(*points[0])
    for point in points[1:]:
        p.lineTo(*point)
    p.close()
    c.setFillColor(fill)
    c.drawPath(p, fill=1, stroke=0)


def draw_light_source(c, x, y, scale=1.0):
    # Concentric, soft-edged light replaces the literal sun symbol.
    rings = [
        (34, 0.025),
        (28, 0.045),
        (22, 0.075),
        (17, 0.13),
        (12, 0.22),
    ]
    for radius, alpha in rings:
        c.setFillColor(Color(0.96, 0.70, 0.26, alpha=alpha))
        c.circle(x, y, radius * scale, fill=1, stroke=0)
    c.setFillColor(Color(1.0, 0.91, 0.63, alpha=0.88))
    c.circle(x, y, 8.5 * scale, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.circle(x, y, 4.6 * scale, fill=1, stroke=0)


def draw_incident_light(c, source_x, source_y, lens_x, lens_y, lens_height):
    # A broad field of energy reaches the lens; three rays make the optics readable.
    polygon(
        c,
        [
            (source_x + 7, source_y - 4),
            (lens_x - 12, lens_y - lens_height * 0.40),
            (lens_x - 12, lens_y + lens_height * 0.40),
            (source_x + 7, source_y + 4),
        ],
        Color(0.93, 0.68, 0.25, alpha=0.13),
    )
    c.setStrokeColor(Color(0.98, 0.80, 0.41, alpha=0.48))
    c.setLineWidth(1.15)
    for offset in (-18, 0, 18):
        c.line(source_x + 7, source_y, lens_x - 12, lens_y + offset)


def draw_lens(c, x, y, height=78, cracked=False):
    width = 22

    # Soft shadow and glass body.
    shadow = c.beginPath()
    shadow.moveTo(x + 3, y - height / 2 - 2)
    shadow.curveTo(x + width + 5, y - height / 3, x + width + 5, y + height / 3, x + 3, y + height / 2 + 2)
    shadow.curveTo(x - width + 3, y + height / 3, x - width + 3, y - height / 3, x + 3, y - height / 2 - 2)
    shadow.close()
    c.setFillColor(Color(0, 0, 0, alpha=0.18))
    c.drawPath(shadow, fill=1, stroke=0)

    lens = c.beginPath()
    lens.moveTo(x, y - height / 2)
    lens.curveTo(x + width, y - height / 3, x + width, y + height / 3, x, y + height / 2)
    lens.curveTo(x - width, y + height / 3, x - width, y - height / 3, x, y - height / 2)
    lens.close()
    c.setFillColor(Color(0.72, 0.85, 0.82, alpha=0.36))
    c.setStrokeColor(GLASS_EDGE)
    c.setLineWidth(1.8)
    c.drawPath(lens, fill=1, stroke=1)

    # Edge highlights make the form read as glass rather than a flat icon.
    c.setStrokeColor(Color(1, 1, 1, alpha=0.55))
    c.setLineWidth(0.75)
    c.line(x - 2, y - height * 0.42, x - 2, y + height * 0.42)
    c.setStrokeColor(Color(0.45, 0.77, 0.73, alpha=0.60))
    c.line(x + 3, y - height * 0.38, x + 3, y + height * 0.38)

    if cracked:
        c.setStrokeColor(HexColor("#E58A67"))
        c.setLineWidth(1.25)
        c.line(x - 1, y + 27, x + 6, y + 10)
        c.line(x + 6, y + 10, x - 7, y - 3)
        c.line(x - 7, y - 3, x + 7, y - 24)
        c.line(x + 6, y + 10, x + 13, y + 4)


def draw_focused_light(c, lens_x, lens_y, lens_height, contact_x, contact_y):
    # The broad light visibly narrows to a single point on the mirror face.
    polygon(
        c,
        [
            (lens_x + 13, lens_y - lens_height * 0.40),
            (contact_x, contact_y),
            (lens_x + 13, lens_y + lens_height * 0.40),
        ],
        Color(0.96, 0.75, 0.30, alpha=0.18),
    )
    c.setStrokeColor(Color(1.0, 0.84, 0.49, alpha=0.82))
    c.setLineWidth(1.6)
    c.line(lens_x + 13, lens_y, contact_x, contact_y)


def line_angle(x1, y1, x2, y2):
    return degrees(atan2(y2 - y1, x2 - x1))


def draw_reflected_light(c, contact, target, color=GOLD, wide=True):
    x1, y1 = contact
    x2, y2 = target
    angle = radians(line_angle(x1, y1, x2, y2))
    nx, ny = -sin(angle), cos(angle)
    start_half = 2.0 if wide else 1.0
    end_half = 10.0 if wide else 3.5
    polygon(
        c,
        [
            (x1 + nx * start_half, y1 + ny * start_half),
            (x2 + nx * end_half, y2 + ny * end_half),
            (x2 - nx * end_half, y2 - ny * end_half),
            (x1 - nx * start_half, y1 - ny * start_half),
        ],
        Color(0.96, 0.71, 0.25, alpha=0.16 if wide else 0.08),
    )
    c.setStrokeColor(Color(color.red, color.green, color.blue, alpha=0.86 if wide else 0.46))
    c.setLineWidth(1.8 if wide else 1.15)
    c.line(x1, y1, x2, y2)


def draw_fading_ray(c, contact, endpoint, color=RUST):
    x1, y1 = contact
    x2, y2 = endpoint
    for i, alpha in enumerate((0.58, 0.40, 0.23, 0.10)):
        t0 = i / 4
        t1 = (i + 1) / 4
        sx = x1 + (x2 - x1) * t0
        sy = y1 + (y2 - y1) * t0
        ex = x1 + (x2 - x1) * t1
        ey = y1 + (y2 - y1) * t1
        c.setStrokeColor(Color(color.red, color.green, color.blue, alpha=alpha))
        c.setLineWidth(max(0.8, 1.55 - i * 0.18))
        c.line(sx, sy, ex, ey)


def draw_mirror(c, contact_x, contact_y, surface_angle, length=58, contact_glint=True):
    # The beam is drawn first. This opaque plate is drawn over it so no light can
    # appear to continue through the reflective surface.
    angle = radians(surface_angle)
    ux, uy = cos(angle), sin(angle)
    nx, ny = -uy, ux
    half = length / 2
    thickness = 5.5

    a = (contact_x - ux * half, contact_y - uy * half)
    b = (contact_x + ux * half, contact_y + uy * half)
    back_a = (a[0] - nx * thickness, a[1] - ny * thickness)
    back_b = (b[0] - nx * thickness, b[1] - ny * thickness)
    polygon(c, [a, b, back_b, back_a], HexColor("#0B1D19"))

    c.setStrokeColor(MIRROR_EDGE)
    c.setLineWidth(4.8)
    c.line(a[0], a[1], b[0], b[1])
    c.setStrokeColor(MIRROR_FACE)
    c.setLineWidth(2.2)
    c.line(a[0], a[1] + 0.5, b[0], b[1] + 0.5)

    if contact_glint:
        c.setFillColor(WHITE)
        c.circle(contact_x, contact_y, 2.7, fill=1, stroke=0)
        c.setStrokeColor(Color(1, 0.85, 0.46, alpha=0.72))
        c.setLineWidth(0.7)
        c.line(contact_x - 6, contact_y, contact_x + 6, contact_y)
        c.line(contact_x, contact_y - 6, contact_x, contact_y + 6)


def draw_living_ground(c, x, y, illuminated=True):
    if illuminated:
        c.setFillColor(Color(0.97, 0.76, 0.31, alpha=0.10))
        c.ellipse(x - 47, y - 12, x + 47, y + 18, fill=1, stroke=0)
        c.setFillColor(Color(1.0, 0.87, 0.50, alpha=0.18))
        c.ellipse(x - 30, y - 7, x + 30, y + 11, fill=1, stroke=0)
        ground_color = SOIL
        growth_color = MOSS
    else:
        ground_color = DIM
        growth_color = DIM

    ground = c.beginPath()
    ground.moveTo(x - 31, y - 2)
    ground.curveTo(x - 13, y + 5, x + 13, y + 5, x + 31, y - 2)
    c.setStrokeColor(ground_color)
    c.setLineWidth(2.3)
    c.drawPath(ground, fill=0, stroke=1)

    c.setStrokeColor(growth_color)
    c.setLineWidth(2.2)
    stem = c.beginPath()
    stem.moveTo(x, y)
    stem.curveTo(x - 1, y + 8, x + 1, y + 15, x, y + 23)
    c.drawPath(stem, fill=0, stroke=1)

    c.setFillColor(growth_color)
    left = c.beginPath()
    left.moveTo(x, y + 12)
    left.curveTo(x - 5, y + 17, x - 12, y + 18, x - 14, y + 13)
    left.curveTo(x - 8, y + 9, x - 3, y + 9, x, y + 12)
    left.close()
    c.drawPath(left, fill=1, stroke=0)
    right = c.beginPath()
    right.moveTo(x, y + 17)
    right.curveTo(x + 5, y + 23, x + 13, y + 23, x + 15, y + 18)
    right.curveTo(x + 9, y + 14, x + 4, y + 14, x, y + 17)
    right.close()
    c.drawPath(right, fill=1, stroke=0)


def focused_journey(c):
    c.setFillColor(PALE_SAGE)
    c.roundRect(42, 410, 528, 213, 14, fill=1, stroke=0)
    panel_header(c, "FOCUSED IMPACT", "PASSION + VISION × MISSION = FOCUSED IMPACT", 596, FOREST)

    optical_window(c, 58, 463, 496, 111)
    source = (84, 529)
    lens = (195, 529)
    contact = (337, 529)
    target = (493, 468)

    draw_incident_light(c, *source, *lens, 78)
    draw_light_source(c, *source)
    draw_focused_light(c, *lens, 78, *contact)
    draw_lens(c, *lens, 78)

    # The reflected beam starts where the incoming beam stops.
    draw_reflected_light(c, contact, target)
    outgoing_angle = line_angle(*contact, *target)
    draw_mirror(c, *contact, surface_angle=outgoing_angle / 2, length=61)
    draw_living_ground(c, *target, illuminated=True)

    stage(c, 55, 446, 78, "PASSION", "energy we bring")
    stage(c, 153, 446, 88, "VISION", "clarity that focuses")
    stage(c, 282, 446, 108, "MISSION", "direction we receive")
    stage(c, 443, 446, 112, "IMPACT", "faithful presence in a real place")


def scattered_journey(c):
    c.setFillColor(PALE_RUST)
    c.roundRect(42, 181, 528, 212, 14, fill=1, stroke=0)
    panel_header(c, "SCATTERED ENERGY", "PASSION - VISION / MISSION = SCATTERED ENERGY", 366, RUST)

    optical_window(c, 58, 233, 496, 111)
    source = (84, 299)
    lens = (195, 299)
    target = (501, 241)

    draw_incident_light(c, *source, *lens, 78)
    draw_light_source(c, *source)
    draw_lens(c, *lens, 78, cracked=True)

    contacts = [(323, 323), (336, 299), (323, 275)]
    endpoints = [(464, 338), (472, 310), (454, 244)]
    mirror_angles = [22, -5, -21]

    # Distorted vision sends the same energy toward several competing directions.
    for contact in contacts:
        c.setStrokeColor(Color(0.85, 0.39, 0.22, alpha=0.62))
        c.setLineWidth(1.35)
        c.line(lens[0] + 13, lens[1], contact[0], contact[1])

    # Each path visibly terminates at its own reflector and begins again there.
    for contact, endpoint in zip(contacts, endpoints):
        draw_fading_ray(c, contact, endpoint)
    for contact, angle in zip(contacts, mirror_angles):
        draw_mirror(c, *contact, surface_angle=angle, length=35, contact_glint=False)

    draw_living_ground(c, *target, illuminated=False)

    stage(c, 55, 216, 78, "PASSION", "the energy is still there", RUST)
    stage(c, 145, 216, 105, "DISTORTED VISION", "sends it off course", RUST)
    stage(c, 278, 216, 115, "COMPETING MISSIONS", "divide the direction", RUST)
    stage(c, 439, 216, 116, "SCATTERED ENERGY", "loses strength before it lands", RUST)


def build():
    register_fonts()
    c = canvas.Canvas(
        str(OUTPUT),
        pagesize=LETTER,
        pageCompression=1,
        initialFontName="Arial",
    )
    c.setTitle("From Passion to Impact - V4")
    c.setSubject("Focused and scattered journeys through passion, vision, mission, and impact")
    c.setAuthor("James Akers")

    c.setFillColor(PAPER)
    c.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)

    kicker(c, "From Passion to Impact", 42, 751)
    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 26)
    c.drawString(42, 707, "Passion is powerful.")
    opening = ParagraphStyle(
        "opening",
        fontName="Georgia",
        fontSize=12.2,
        leading=16.5,
        textColor=INK,
        alignment=TA_LEFT,
    )
    paragraph(
        c,
        "But without vision to focus it and mission to move it, passion becomes scattered energy.",
        43,
        682,
        520,
        opening,
    )

    focused_journey(c)
    scattered_journey(c)

    c.setFillColor(DARK_FOREST)
    c.roundRect(42, 53, 528, 103, 12, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawString(58, 134, "THE HEARTBEAT")
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 12.2)
    c.drawString(58, 108, "Passion creates the energy. Vision brings it into focus.")
    c.drawString(58, 88, "Mission points it somewhere that matters. Impact happens where it lands.")
    c.setFillColor(HexColor("#D8E1DB"))
    c.setFont("Arial", 8.4)
    c.drawString(58, 70, "Jesus knew why He came. He prayed, chose where to go next, and did not let the crowd choose His mission.")

    c.setFillColor(MUTED)
    c.setFont("Arial", 7.8)
    c.drawRightString(554, 32, "Mark 1:35-39")
    c.save()


if __name__ == "__main__":
    build()
