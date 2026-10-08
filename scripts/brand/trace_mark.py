"""Trace the logo mark (D-03) from the user-supplied artwork into vector paths.

The source (source/mark-source.webp) is a flat three-colour image: a cream
background, a pale sky half with the sun cut out, and a dark sea half with two
wave lines cut out. This writes the sky and sea shapes, scaled to a 64x64 box
with the disc filling it, to source/mark-paths.json. make_logo.py recolours
them; the cut-outs become a cream disc drawn behind.

    pip install potracer pillow numpy
    python3 scripts/brand/trace_mark.py
"""
import json, os
import numpy as np, potrace
from PIL import Image

HERE = os.path.dirname(__file__)
im = np.array(Image.open(os.path.join(HERE, 'source', 'mark-source.webp')).convert('RGB')).astype(float)
cols = np.array([(250, 245, 239), (178, 206, 200), (20, 82, 90)])  # cream, sky, sea
label = np.argmin(((im[:, :, None, :] - cols) ** 2).sum(-1), -1)
sky, sea = label == 1, label == 2
ys, xs = np.where(sky | sea)
cx, cy = (xs.min() + xs.max() + 1) / 2, (ys.min() + ys.max() + 1) / 2
r = max(xs.max() + 1 - xs.min(), ys.max() + 1 - ys.min()) / 2
s = 32 / r


def trace(mask):
    out = []
    for c in potrace.Bitmap(~mask).trace(turdsize=60, alphamax=1.0, opticurve=True, opttolerance=0.2):
        p = lambda pt: f'{(pt.x - cx) * s + 32:.2f},{(pt.y - cy) * s + 32:.2f}'
        out.append('M' + p(c.start_point))
        for g in c.segments:
            out.append(f'L{p(g.c)}L{p(g.end_point)}' if g.is_corner
                       else f'C{p(g.c1)} {p(g.c2)} {p(g.end_point)}')
        out.append('Z')
    return ''.join(out)


json.dump({'sky': trace(sky), 'sea': trace(sea)}, open(os.path.join(HERE, 'source', 'mark-paths.json'), 'w'), indent=0)
print(f'disc centre {cx:.0f},{cy:.0f} radius {r:.0f}px')
