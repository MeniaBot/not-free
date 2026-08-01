"""בדיקת עדכון מול גיטהאב.

זו הפעולה היחידה בתוכנה שיוצאת לרשת. היא שואלת מה מספר הגרסה האחרונה
ותו לא — לא מורידה קובץ, לא כותבת לדיסק ולא נוגעת בהגדרות. כשיש גרסה
חדשה מוצג פס במסך הפתיחה, והלחיצה עליו פותחת את דף המהדורה בדפדפן המערכת.

רצה בחוט רקע כדי שהפתיחה תישאר בחצי שנייה, ונכשלת בשקט: בלי אינטרנט,
מאחורי סינון, או בתשובה חריגה — פשוט אין הודעה.

הבדיקה נשארת בפייתון בכוונה. ה-CSP ב-index.html חוסם כל יציאה לרשת מצד
הממשק, וכך הוא נשאר.
"""

import json
import re
import threading
import urllib.request

from . import __version__

REPO = "BeniaBot/not-free"
API = "https://api.github.com/repos/%s/releases/latest" % REPO
RELEASES = "https://github.com/%s/releases/latest" % REPO
SAFE_PREFIX = "https://github.com/%s/" % REPO

TIMEOUT = 5      # שניות
MAX_BYTES = 1 << 16

_result = None


def _parse(tag):
    """'v0.9.2.1' -> (0, 9, 2, 1). כל מה שאינו ספרה מושמט."""
    return tuple(int(p) for p in re.findall(r"\d+", tag or ""))


def _safe_url(url):
    """רק דף מהדורה במאגר הזה. הכתובת מגיעה מתשובת רשת, ולא נעביר לדפדפן
    כל מה שהצד השני החזיר."""
    return url if isinstance(url, str) and url.startswith(SAFE_PREFIX) else RELEASES


def _check():
    global _result
    try:
        request = urllib.request.Request(API, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "not-free/%s" % __version__,
        })
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            data = json.loads(response.read(MAX_BYTES).decode("utf-8"))

        tag = data.get("tag_name") or ""
        if _parse(tag) > _parse(__version__):
            _result = {"version": tag.lstrip("vV"), "url": _safe_url(data.get("html_url"))}
    except Exception:  # noqa: BLE001 — כל תקלה כאן היא "אין הודעה", לא שגיאה
        pass


def start():
    """מפעיל את הבדיקה ברקע. הפתיחה לא ממתינה לה."""
    threading.Thread(target=_check, daemon=True).start()


def result():
    """{version, url} כשיש גרסה חדשה יותר, אחרת None."""
    return _result
