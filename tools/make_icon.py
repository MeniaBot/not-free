"""מחולל האייקון: מגן נטפרי מנופץ.

הרעיון — הצללית של נטפרי נשארת מזוהה, וסדק ברק חוצה אותה לשני חצאים שזזו.
כל גודל מצויר מחדש עם עובי סדק והיסט משלו: אייקון של 16 פיקסל לא יכול לשאת
את אותם פרטים כמו 256, ולכן ההיסט קטן והסדק עבה יותר יחסית ככל שקטנים.

    py tools/make_icon.py        → כותב GH.ico בשורש

תלוי ב-Pillow, שלא נחוץ להרצת התוכנה עצמה. מריצים רק כשמשנים את האייקון.
"""

import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

S = 1024   # מרחב עבודה לוגי — כל הקואורדינטות כאן
SS = 4     # דגימת-על, לקצוות חלקים

GREY = (163, 170, 178, 255)   # גוף המגן — אמצע הדרך, נקרא גם על סרגל כהה וגם על לבן
TEAL = (82, 162, 140, 255)    # ה"וי" של נטפרי

# סדק ברק — מעט פניות, כל אחת חדה. יותר פניות נמרחות בגדלים קטנים.
CRACK = [(556, 150), (470, 402), (566, 516), (464, 692), (518, 960)]

# גודל -> (פיזור החצאים, עובי הסדק)
PLAN = [(256, 0.40, 22), (128, 0.40, 24), (64, 0.35, 30), (48, 0.30, 34),
        (32, 0.25, 38), (24, 0.20, 42), (16, 0.15, 46)]


def quad(p0, p1, p2, n=72):
    """נקודות על עקומת בזייה ריבועית."""
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return out


def shield():
    """קו עליון מוטה כמו במקור, צדדים תפוחים, תחתית מחודדת."""
    a, b, tip = (206, 286), (822, 200), (510, 908)
    return [a, b] + quad(b, (884, 636), tip)[1:] + quad(tip, (136, 636), a)[1:]


def swoosh():
    """ה\"וי\" — צולל במרכז ומטפס לשני הצדדים."""
    return quad((114, 306), (480, 636), (892, 282)) + quad((152, 442), (484, 752), (906, 420))[::-1]


def scaled(pts, k):
    return [(x * k, y * k) for x, y in pts]


def art(size):
    """המגן השלם, לפני הניפוץ."""
    k = size / S
    body = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.polygon(scaled(shield(), k), fill=GREY)
    bd.polygon(scaled(swoosh(), k), fill=TEAL)

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).polygon(scaled(shield(), k), fill=255)   # ה"וי" נגזר לפי המגן
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    img.paste(body, (0, 0), mask)
    return img


def carve(img, width, k):
    """מנקב את הסדק דרך הציור."""
    cut = Image.new("L", img.size, 255)
    ImageDraw.Draw(cut).line(scaled(CRACK, k), fill=0, width=int(width * k), joint="curve")
    img.putalpha(Image.composite(img.getchannel("A"), Image.new("L", img.size, 0), cut))
    return img


def half(src, side, angle, dx, dy, k):
    """חצי מגן — נחתך לאורך הסדק, מסובב ומוזז."""
    pad = 300
    edge = -pad if side == "left" else S + pad
    plane = [(CRACK[0][0], -pad)] + CRACK[1:-1] + [(512, S + pad), (edge, S + pad), (edge, -pad)]

    m = Image.new("L", src.size, 0)
    ImageDraw.Draw(m).polygon(scaled(plane, k), fill=255)
    p = Image.new("RGBA", src.size, (0, 0, 0, 0))
    p.paste(src, (0, 0), m)
    p = p.rotate(angle, resample=Image.BICUBIC, center=(src.size[0] / 2, src.size[1] * 0.58))
    return p, (int(dx * k), int(dy * k))


def render(size, spread, crack):
    big = size * SS
    k = big / S
    a = carve(art(big), crack, k)

    canvas = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    left, ol = half(a, "left", 3.2 * spread, -20 * spread, 10 * spread, k)
    right, orr = half(a, "right", -3.8 * spread, 22 * spread, 14 * spread, k)
    canvas.alpha_composite(left, ol)
    canvas.alpha_composite(right, orr)
    return canvas.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    imgs = [render(s, sp, cr) for s, sp, cr in PLAN]
    target = os.path.join(ROOT, "GH.ico")
    imgs[0].save(target, format="ICO",
                 sizes=[(i.size[0], i.size[0]) for i in imgs], append_images=imgs[1:])
    print("wrote %s (%d bytes, %d sizes)" % (target, os.path.getsize(target), len(imgs)))
