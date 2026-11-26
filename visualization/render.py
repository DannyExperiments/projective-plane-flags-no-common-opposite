"""Render a loop of the PG(2,3) incidence diagram with an actual 3D camera orbit."""
from math import cos, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 800, 444
BG, PANEL = "#0e1829", "#16243a"
FOREGROUND, MUTED = "#edf2fa", "#abbad1"
POINT, LINE, FLAG, HIT = "#69ddc7", "#ffc582", "#728fd7", "#eade73"
Z = (1.45, .49, -.49, -1.45)
NODES = (
    [(f"P{i + 1}", POINT, (-1.75, -.45, z)) for i, z in enumerate(Z)]
    + [(f"L{i + 1}", LINE, (1.75, .45, z)) for i, z in enumerate(Z)]
    + [("y", POINT, (-.43, -1.38, .46)), ("n", LINE, (.43, 1.38, -.46))]
)
POINTS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1)]
LINES = [(0, 1, 0), (0, 0, 1), (1, 0, 0), (1, 0, 2)]
Y, N = (1, 1, 2), (0, 1, 1)


def incident(point, line):
    return sum(p * l for p, l in zip(point, line)) % 3 == 0


def fonts():
    def load(name, size):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            return ImageFont.load_default(size=size)
    return {
        "title": load("Arial Bold.ttf", 36), "body": load("Arial.ttf", 19),
        "small": load("Arial.ttf", 16), "label": load("Arial Bold.ttf", 17),
    }


def project(position, angle):
    x, y, z = position
    side = x * cos(angle) - y * sin(angle)
    depth = x * sin(angle) + y * cos(angle)
    vertical = z * cos(.30) - depth * sin(.30)
    camera_depth = depth * cos(.30) + z * sin(.30)
    zoom = 8 / (8 - camera_depth)
    return (WIDTH / 2 + side * 122 * zoom, 242 - vertical * 73 * zoom), camera_depth, zoom


def render(angle, font):
    im = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(im)
    draw.text((30, 24), "Four flags with no common opposite", font=font["title"], fill=FOREGROUND)
    draw.text((32, 77), "PG(2,3)  •  Candidate y lies outside every selected line", font=font["body"], fill=MUTED)
    draw.rounded_rectangle((28, 113, 772, 365), radius=13, fill=PANEL)
    projected = [project(position, angle) for _, _, position in NODES]
    for i in range(4):
        draw.line((projected[i][0], projected[i+4][0]), fill=FLAG, width=3)
    start, end = projected[8][0], projected[9][0]
    for step in range(0, 16, 2):
        path = [tuple(start[j] + (end[j]-start[j])*t/16 for j in range(2)) for t in (step, step+1)]
        draw.line(path, fill=MUTED, width=2)
    assert incident(Y, N) and all(not incident(Y, line) for line in LINES)
    hits = [i for i, point in enumerate(POINTS) if incident(point, N)]
    assert hits == [0]
    draw.line((projected[hits[0]][0], end), fill=HIT, width=5)
    for index in sorted(range(len(NODES)), key=lambda i: projected[i][1]):
        name, color, _ = NODES[index]
        (x, y), _, zoom = projected[index]
        r = (9 if index >= 8 else 7) * zoom
        if color == POINT:
            draw.ellipse((x-r, y-r, x+r, y+r), fill=color, outline=BG, width=2)
        else:
            draw.polygon(((x,y-r),(x+r,y),(x,y+r),(x-r,y)), fill=color, outline=BG, width=2)
        draw.text((x, y-r-3), name, fill=color, font=font["label"], anchor="ms", stroke_width=2, stroke_fill=PANEL)
    draw.text((32, 380), "The candidate line n contains P1, so its flag is ruled out.", font=font["body"], fill=HIT)
    draw.text((32, 412), "Circle: point    Diamond: line    Blue: selected pair    Gold: blocking incidence", font=font["small"], fill=MUTED)
    return im


def main():
    font = fonts()
    frames = [render(-.15 + tau * i / 80, font) for i in range(80)]
    frames[0].save(Path(__file__).with_name("four-flags.gif"), save_all=True,
                   append_images=frames[1:], duration=85, loop=0, optimize=False)


if __name__ == "__main__":
    main()
