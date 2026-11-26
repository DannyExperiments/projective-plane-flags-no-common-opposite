# Reproducibility

The proof in [the manuscript](paper/manuscript.pdf) is mathematical. Run the illustrative replay with Python 3.11 or later and no third-party libraries.

```sh
python3 -I verification/src/replay.py
```

The script reconstructs projective coordinates and their incidence tables, checks the construction at each stated finite order and exhausts the sets at orders 2 or 3. At order 4 it exhausts the sets that contain one fixed flag. Every flag belongs to the same number of admissible families by projective collineation transitivity. Multiplying the fixed-flag count by the number of flags, then dividing by five, yields the total. The [transcript](verification/results/replay.txt) gives the denominators and counts. The order-11 construction check holds over two million flag-set tuples in memory.

Open `visualization/index.html` directly in a browser to run the explorer offline. The GIF renderer uses Python and Pillow. See [visualization notes](visualization/README.md) and [PDF build instructions](paper/BUILD.md).
