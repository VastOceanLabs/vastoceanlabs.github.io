"""Write the Vast Ocean Labs logo SVGs into assets/img/ (decision D-03).

The mark comes from the user's artwork, traced by trace_mark.py; the wordmark
is Nunito ExtraBold (D-04), converted to outlines so the logo files need no
font. Also writes _includes/logo-mark.svg, the inline copy the header uses,
coloured by CSS classes so it follows the colour scheme.

    pip install fonttools brotli uharfbuzz
    python3 scripts/brand/make_logo.py
"""
import json
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
IMG = os.path.join(ROOT, 'assets', 'img')
FONT = os.path.join(ROOT, 'assets', 'fonts', 'nunito-latin-wght-normal.woff2')

# Palette (D-12). Keep in step with the --mark-* tokens in assets/css/site.css.
SKY, SEA, CREAM = '#8EBFD6', '#0B3A52', '#FAF6F0'
DARK_SEA, DARK_INK = '#24597A', '#D3E6EF'   # sea + text on dark backgrounds

# Sky and sea shapes traced from the user's artwork by trace_mark.py.
PATHS = json.load(open(os.path.join(os.path.dirname(__file__), 'source', 'mark-paths.json')))


def mark(sky=SKY, sea=SEA, gap=CREAM):
    """Sun setting over the sea, in a 64x64 disc. The sun, horizon and wave
    lines are gaps between the shapes, filled by a disc of `gap` behind them."""
    return (f'<circle cx="32" cy="32" r="31.6" fill="{gap}"/>'
            f'<path fill="{sky}" d="{PATHS["sky"]}"/><path fill="{sea}" d="{PATHS["sea"]}"/>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img">'
            f'<title>{title}</title>{body}</svg>\n')


def wordmark(text, size, x0, baseline, weight=800):
    """Shape `text` with HarfBuzz (so kerning applies) and return one SVG path."""
    font = TTFont(FONT)
    font = instantiateVariableFont(font, {'wght': weight})
    upem = font['head'].unitsPerEm
    hbfont = hb.Font(hb.Face(hb.Blob(font_bytes(font))))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {'kern': True, 'liga': True})
    glyphs = font.getGlyphSet(); order = font.getGlyphOrder()
    pen = SVGPathPen(glyphs, ntos=lambda v: f'{v:.1f}'.rstrip('0').rstrip('.'))
    s = size / upem; x = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        g = order[info.codepoint]
        glyphs[g].draw(TransformPen(pen, (s, 0, 0, -s, x0 + (x + pos.x_offset) * s, baseline)))
        x += pos.x_advance
    return pen.getCommands(), x * s, font['OS/2'].sCapHeight * s


def font_bytes(font):
    import io
    b = io.BytesIO(); font.flavor = None; font.save(b); return b.getvalue()


def main():
    name = 'Vast Ocean Labs'
    # Mark, alone (also the favicon).
    open(f'{IMG}/logo-mark.svg', 'w').write(svg(64, 64, mark(), name))
    open(f'{IMG}/favicon.svg', 'w').write(svg(64, 64, mark(), name))
    inline = (mark(sky='SKY', sea='SEA', gap='GAP').replace('fill="GAP"', 'class="mark-gap"')
              .replace('fill="SKY"', 'class="mark-sky"').replace('fill="SEA"', 'class="mark-sea"'))
    open(os.path.join(ROOT, '_includes', 'logo-mark.svg'), 'w').write(
        f'<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false">{inline}</svg>\n')
    # Horizontal lockup: 64-unit mark, 18-unit gap, wordmark cap height ~28.
    size = 40
    d, width, cap = wordmark(name, size, 82, 0)
    baseline = 32 + cap / 2
    d, width, cap = wordmark(name, size, 82, baseline)
    w = 82 + width + 2
    for suffix, sea, ink in (('', SEA, SEA), ('-dark', DARK_SEA, DARK_INK)):
        body = mark(sea=sea) + f'<path fill="{ink}" d="{d}"/>'
        open(f'{IMG}/logo{suffix}.svg', 'w').write(svg(w, 64, body, name))
    print(f'logo lockup {w:.0f}x64')


if __name__ == '__main__':
    main()
