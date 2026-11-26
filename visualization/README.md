# The four-flag example

The image renders a full 3D camera orbit around an incidence diagram for a fixed trial flag in PG(2,3). Node coordinates are layout coordinates. Circular nodes represent points, diamond nodes represent lines, and edges represent incidences specified in the legend. The trial uses the point (1:1:2) and the line [0,1,1]. Its point lies outside all four selected lines. Its line contains exactly one selected point, P1 = (1:0:0).

Open `index.html` in a browser without network access or extract it from the companion ZIP. The controls cover all 52 incident candidates. Drag, use the canvas arrow keys, or press Rotate to change the perspective. The point and line choices and the text report are available independently of the graphic.

Run `python3 visualization/render.py` from the repository root with Pillow 13.0 to render the 80-frame loop. The renderer uses Arial when present and Pillow's bundled font otherwise.
