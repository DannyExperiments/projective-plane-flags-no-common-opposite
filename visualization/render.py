"""Render the PG(2,3) incidence diagram with a 3D camera sweep."""

import argparse
from itertools import combinations
from math import cos, hypot, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 620, 800
PANEL_BOX = (23, 169, 597, 549)
SWEEP = .30
N_FRAMES, DELAY_MS = 64, 100
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
SELECTED_EDGES = tuple((index, index + 4) for index in range(4))
EDGES = SELECTED_EDGES + ((8, 9), (0, 9))


def incident(point, line):
    return sum(p * l for p, l in zip(point, line)) % 3 == 0


def fonts():
    def load(name, size):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            return ImageFont.load_default(size=size)

    return {
        "title": load("Arial Bold.ttf", 44),
        "callout": load("Arial Bold.ttf", 35),
        "body": load("Arial.ttf", 28),
        "label": load("Arial Bold.ttf", 28),
        "legend": load("Arial.ttf", 25),
    }


def project(position, angle):
    x, y, z = position
    side = x * cos(angle) - y * sin(angle)
    depth = x * sin(angle) + y * cos(angle)
    vertical = z * cos(.30) - depth * sin(.30)
    camera_depth = depth * cos(.30) + z * sin(.30)
    zoom = 8 / (8 - camera_depth)
    return (WIDTH / 2 + side * 111 * zoom, 351 - vertical * 86 * zoom), camera_depth, zoom


def padded(box, amount):
    left, top, right, bottom = box
    return left - amount, top - amount, right + amount, bottom + amount


def marker_box(center, radius):
    x, y = center
    return x - radius, y - radius, x + radius, y + radius


def layout(angle, label_font):
    markers, labels = [], []
    for index, (name, color, position) in enumerate(NODES):
        center, depth, zoom = project(position, angle)
        x, y = center
        radius = (11 if index < 8 else 12) * zoom
        markers.append((center, depth, radius))
        if index < 4:
            location, anchor = (x - radius - 9, y), "rm"
        elif index < 8:
            location, anchor = (x + radius + 9, y), "lm"
        elif index == 8:
            location, anchor = (x, y - radius - 9), "mb"
        else:
            location, anchor = (x + radius + 9, y - 10), "lm"
        left, top, right, bottom = label_font.getbbox(name, anchor=anchor)
        u, v = location
        box = padded((u + left, v + top, u + right, v + bottom), 3)
        labels.append((name, color, location, anchor, box))
    return markers, labels


def box_gap(a, b):
    return max(b[0] - a[2], a[0] - b[2], b[1] - a[3], a[1] - b[3])


def layout_clearance(markers, labels):
    boxes = [marker_box(center, radius) for center, _, radius in markers]
    boxes.extend(box for _, _, _, _, box in labels)
    panel = min(
        min(a[0] - PANEL_BOX[0], a[1] - PANEL_BOX[1], PANEL_BOX[2] - a[2], PANEL_BOX[3] - a[3])
        for a in boxes
    )
    separation = min(box_gap(a, b) for a, b in combinations(boxes, 2))
    return min(panel, separation)


def crosses(box, start, end):
    low, high = 0, 1
    for axis in range(2):
        delta = end[axis] - start[axis]
        if delta == 0:
            if not box[axis] <= start[axis] <= box[axis + 2]:
                return False
        else:
            bounds = sorted((box[index] - start[axis]) / delta for index in (axis, axis + 2))
            low, high = max(low, bounds[0]), min(high, bounds[1])
            if low > high:
                return False
    return True


def distance_to_segment(point, start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    x, y = point[0] - start[0], point[1] - start[1]
    t = min(1, max(0, (x*dx + y*dy) / (dx*dx + dy*dy)))
    return hypot(x - t*dx, y - t*dy)


def draw_marker(draw, center, radius, color):
    x, y = center
    if color == POINT:
        draw.ellipse(marker_box(center, radius), fill=color, outline=BG, width=2)
    else:
        diamond = ((x, y-radius), (x+radius, y), (x, y+radius), (x-radius, y))
        draw.polygon(diamond, fill=color, outline=BG, width=2)


def draw_dashes(draw, start, end):
    for step in range(0, 20, 2):
        segment = [tuple(a + (b-a)*t/20 for a, b in zip(start, end)) for t in (step, step+1)]
        draw.line(segment, fill=MUTED, width=3)


def draw_legend(draw, font):
    draw.line((30, 708, 590, 708), fill=PANEL, width=3)
    for x, label, color in ((44, "Point", POINT), (324, "Line", LINE)):
        draw_marker(draw, (x, 732), 10, color)
        draw.text((x + 22, 732), label, font=font, fill=MUTED, anchor="lm")
    for x, label, color in ((32, "Selected flag", FLAG), (311, "Blocking incidence", HIT)):
        draw.line((x, 769, x + 24, 769), fill=color, width=5)
        draw.text((x + 33, 769), label, font=font, fill=MUTED, anchor="lm")


def render(angle, font):
    im = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(im)
    draw.text((31, 20), "Four flags with", font=font["title"], fill=FOREGROUND, anchor="lt")
    draw.text((31, 70), "no common opposite", font=font["title"], fill=FOREGROUND, anchor="lt")
    draw.text((32, 129), "PG(2,3)  ·  Trial flag (y, n)", font=font["body"], fill=MUTED, anchor="lt")
    draw.rounded_rectangle(PANEL_BOX, radius=16, fill=PANEL)
    markers, labels = layout(angle, font["label"])
    assert layout_clearance(markers, labels) >= 3, f"Overlapping marks at angle {angle}"
    for first, second in SELECTED_EDGES:
        draw.line((markers[first][0], markers[second][0]), fill=FLAG, width=5)
    start, end = markers[8][0], markers[9][0]
    draw_dashes(draw, start, end)
    draw.line((markers[0][0], end), fill=HIT, width=7)
    for index in sorted(range(len(NODES)), key=lambda i: markers[i][1]):
        center, _, radius = markers[index]
        draw_marker(draw, center, radius, NODES[index][1])
    for name, color, location, anchor, box in labels:
        draw.rounded_rectangle(box, radius=4, fill=PANEL)
        draw.text(location, name, fill=color, font=font["label"], anchor=anchor)
    draw.text((32, 569), "n contains P1.", font=font["callout"], fill=HIT, anchor="lt")
    draw.text((32, 615), "That rules out the trial flag.", font=font["body"], fill=FOREGROUND, anchor="lt")
    draw.text((32, 657), "y lies off the four selected lines.", font=font["legend"], fill=MUTED, anchor="lt")
    draw_legend(draw, font["legend"])
    return im


def check_geometry(font):
    assert all(incident(point, line) for point, line in zip(POINTS, LINES))
    assert incident(Y, N) and all(not incident(Y, line) for line in LINES)
    assert [i for i, point in enumerate(POINTS) if incident(point, N)] == [0]
    # Check angles more finely than the GIF samples. Each box edge moves less
    # than 400 px/radian, from the perspective denominator > 5.8 and the
    # position bounds in NODES. Between samples the two-box gap loses < 1 px.
    angles = [-SWEEP + 2 * SWEEP * i / 1000 for i in range(1001)]
    minimum_box, minimum_edge = float("inf"), float("inf")
    for angle in angles:
        markers, labels = layout(angle, font["label"])
        minimum_box = min(minimum_box, layout_clearance(markers, labels))
        for first, second in EDGES:
            start, end = markers[first][0], markers[second][0]
            assert all(not crosses(padded(box, 6), start, end) for _, _, _, _, box in labels)
            for index, (point, _, radius) in enumerate(markers):
                if index not in (first, second):
                    minimum_edge = min(minimum_edge, distance_to_segment(point, start, end) - radius - 3.5)
    assert minimum_box >= 4 and minimum_edge >= 2, (minimum_box, minimum_edge)
    print(f"PG(2,3) incidences pass. 1,001 angles, {minimum_box:.2f} px mark/label clearance, "
          f"{minimum_edge:.2f} px clearance between edges and other marks.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("four-flags.gif"))
    args = parser.parse_args()
    font = fonts()
    check_geometry(font)
    frames = [render(-SWEEP * cos(tau * index / N_FRAMES), font) for index in range(N_FRAMES)]
    palette = frames[0].quantize(colors=64, dither=Image.Dither.NONE)
    frames = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    frames[0].save(args.output, save_all=True, append_images=frames[1:],
                   duration=DELAY_MS, loop=0, disposal=1, optimize=True)


if __name__ == "__main__":
    main()
