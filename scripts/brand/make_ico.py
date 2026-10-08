"""Pack the rendered 16/32/48 favicon PNGs into /favicon.ico.
Usage: python3 scripts/brand/make_ico.py <tmp-dir>"""
import os, sys
from PIL import Image
tmp = sys.argv[1]
root = os.path.join(os.path.dirname(__file__), '..', '..')
imgs = [Image.open(os.path.join(tmp, f'favicon-{px}.png')).convert('RGBA') for px in (48, 32, 16)]
imgs[0].save(os.path.join(root, 'favicon.ico'), sizes=[(48, 48), (32, 32), (16, 16)], append_images=imgs[1:])
