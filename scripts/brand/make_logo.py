"""Write the Vast Ocean Labs logo SVGs into assets/img/ (decision D-03).

The mark is drawn here as plain SVG; the wordmark is Nunito ExtraBold (D-04),
converted to outlines so the logo files need no font.

    pip install fonttools brotli uharfbuzz
    python3 scripts/brand/make_logo.py
"""
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
IMG = os.path.join(ROOT, 'assets', 'img')
FONT = os.path.join(ROOT, 'assets', 'fonts', 'nunito-latin-wght-normal.woff2')

# Palette (D-09, revised in S3). Keep in step with the tokens in assets/css/site.css.
DEEP, SKY, CREAM = '#0B3A52', '#8EBFD6', '#FAF6F0'
DARK_DEEP, DARK_INK = '#24597A', '#D3E6EF'   # mark disc + text on dark backgrounds


def mark(stroke=4.4, disc=DEEP, accent=SKY, line=CREAM):
    """Sun on the horizon over one wave, in a 64x64 disc."""
    return (f'<circle cx="32" cy="32" r="32" fill="{disc}"/>'
            f'<path d="M21,31a11,11 0 0 1 22,0z" fill="{accent}"/>'
            f'<path d="M10,31h44" stroke="{line}" stroke-width="{stroke}" stroke-linecap="round"/>'
            f'<path d="M14,44q4.5,-4.6 9,0t9,0t9,0t9,0" fill="none" stroke="{accent}" '
            f'stroke-width="{stroke}" stroke-linecap="round"/>')


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
    # Mark, alone (also the header logo and the basis for the favicons).
    open(f'{IMG}/logo-mark.svg', 'w').write(svg(64, 64, mark(), name))
    # Favicon: heavier strokes so it survives 16px.
    open(f'{IMG}/favicon.svg', 'w').write(svg(64, 64, mark(stroke=5.6), name))
    # Horizontal lockup: 64-unit mark, 18-unit gap, wordmark cap height ~28.
    size = 40
    d, width, cap = wordmark(name, size, 82, 0)
    baseline = 32 + cap / 2
    d, width, cap = wordmark(name, size, 82, baseline)
    w = 82 + width + 2
    for suffix, disc, ink in (('', DEEP, DEEP), ('-dark', DARK_DEEP, DARK_INK)):
        body = mark(disc=disc) + f'<path fill="{ink}" d="{d}"/>'
        open(f'{IMG}/logo{suffix}.svg', 'w').write(svg(w, 64, body, name))
    print(f'logo lockup {w:.0f}x64')


if __name__ == '__main__':
    main()
