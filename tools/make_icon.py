"""מחולל האייקון: חותמת "מחשב נקי" של נטפרי, מנופצת.

הגרסה הזו **מנפצת את הסמל המקורי**, לא מציירת חיקוי שלו. ניסיון קודם שרטט
טבעת וסרט מחדש, והתוצאה הייתה דומה-בערך אבל לא מזוהה: בלי הכיתוב העברי,
בלי המגן הקטן ובלי הפרופורציות המדויקות, המוח לא קורא את זה כנטפרי.

המקור `tools/netfree-seal.png` הוא הסמל על רקע נייבט כהה. בהירות הרקע ~17
ובהירות הסמל ~53, ולכן החילוץ הוא סף בהירות פשוט. אחריו מגדילים, חוצים
בסדק ומזיזים את שני החצאים.

    py tools/make_icon.py        → כותב GH.ico בשורש

תלוי ב-Pillow, שלא נחוץ להרצת התוכנה. מריצים רק כשמשנים את האייקון.
"""

import os

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SOURCE = os.path.join(HERE, "netfree-seal.png")

S = 1024   # מרחב עבודה לוגי
SS = 2     # דגימת-על. המקור קטן, ולכן אין טעם ב-4

INK = (142, 155, 176)   # גוון ביניים — נקרא גם על סרגל כהה וגם על רקע לבן

LUM_BG, LUM_MARK = 19.0, 52.0   # נמדדו מהמקור

# סדק ברק. עובר ליד מרכז החותמת ולא דרך אמצע המילה, כדי ש-NETFREE יישאר קריא.
CRACK = [(556, 20), (452, 330), (574, 470), (446, 690), (528, 1010)]

# גודל -> (פיזור החצאים, עובי הסדק, עיבוי הקווים)
# הקווים הדקים של החותמת נעלמים בהקטנה, ולכן בגדלים הקטנים מעבים אותם
# לפני ההקטנה. בלי זה 16 ו-24 יוצאים כתם אפור חסר צורה.
PLAN = [(256, 0.5, 16, 0), (128, 0.5, 18, 0), (64, 0.4, 24, 1),
        (48, 0.34, 30, 1), (32, 0.26, 38, 2), (24, 0.2, 46, 2), (16, 0.15, 54, 3)]


def seal_mask():
    """מחלץ את הסמל מהרקע ומחזיר מסכת אלפא מרובעת וממורכזת."""
    im = Image.open(SOURCE).convert("RGB")
    w, h = im.size
    px = im.load()
    m = Image.new("L", (w, h), 0)
    mp = m.load()
    span = LUM_MARK - LUM_BG
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            v = (lum - LUM_BG) / span
            mp[x, y] = 0 if v <= 0 else (255 if v >= 1 else int(v * 255))

    box = m.getbbox()
    m = m.crop(box)
    side = max(m.size)
    sq = Image.new("L", (side, side), 0)
    sq.paste(m, ((side - m.width) // 2, (side - m.height) // 2))
    return sq


_MASK = None


def art(size, fatten=0):
    """הסמל בצבע ובגודל המבוקש, עם שוליים. fatten מעבה קווים דקים."""
    global _MASK
    if _MASK is None:
        _MASK = seal_mask()
    pad = int(size * 0.045)
    inner = size - pad * 2
    # מעבים אחרי ההגדלה ולא לפני: המקור הוא 169 פיקסל, ודילטציה עליו
    # סותמת את החורים של האותיות והכל הופך לכתם מלא
    m = _MASK.resize((inner, inner), Image.LANCZOS)
    if fatten:
        m = m.filter(ImageFilter.MaxFilter(2 * fatten + 1))
    full = Image.new("L", (size, size), 0)
    full.paste(m, (pad, pad))
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    img.paste(Image.new("RGBA", (size, size), INK), (0, 0), full)
    return img


def scaled(pts, k):
    return [(x * k, y * k) for x, y in pts]


def carve(img, width, k):
    """מנקב את הסדק דרך הציור."""
    cut = Image.new("L", img.size, 255)
    ImageDraw.Draw(cut).line(scaled(CRACK, k), fill=0, width=max(1, int(width * k)), joint="curve")
    img.putalpha(Image.composite(img.getchannel("A"), Image.new("L", img.size, 0), cut))
    return img


def half(src, side, angle, dx, dy, k):
    """חצי חותמת — נחתך לאורך הסדק, מסובב ומוזז."""
    pad = 300
    edge = -pad if side == "left" else S + pad
    plane = [(CRACK[0][0], -pad)] + CRACK[1:-1] + [(CRACK[-1][0], S + pad), (edge, S + pad), (edge, -pad)]
    m = Image.new("L", src.size, 0)
    ImageDraw.Draw(m).polygon(scaled(plane, k), fill=255)
    p = Image.new("RGBA", src.size, (0, 0, 0, 0))
    p.paste(src, (0, 0), m)
    p = p.rotate(angle, resample=Image.BICUBIC, center=(src.size[0] / 2, src.size[1] / 2))
    return p, (int(dx * k), int(dy * k))


def render(size, spread, crack, fatten=0):
    big = size * SS
    k = big / S
    a = carve(art(big, fatten), crack, k)
    canvas = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    left, ol = half(a, "left", 2.6 * spread, -20 * spread, 8 * spread, k)
    right, orr = half(a, "right", -3.2 * spread, 22 * spread, 11 * spread, k)
    canvas.alpha_composite(left, ol)
    canvas.alpha_composite(right, orr)
    return canvas.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    imgs = [render(s, sp, cr, ft) for s, sp, cr, ft in PLAN]
    target = os.path.join(ROOT, "GH.ico")
    imgs[0].save(target, format="ICO",
                 sizes=[(i.size[0], i.size[0]) for i in imgs], append_images=imgs[1:])
    print("wrote %s (%d bytes, %d sizes)" % (target, os.path.getsize(target), len(imgs)))
