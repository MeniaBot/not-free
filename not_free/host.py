"""החלון הנייטיב שמארח את הממשק.

פייתון כאן הוא רק מארח: הוא פותח חלון WebView2 על index.html וחושף שתי
פעולות שדפדפן לא יכול לעשות לבד — קריאת הלוח וסגירת התוכנה.
"""

import webview

from . import __version__, clipboard
from .resources import ui_entry

WINDOW_WIDTH = 560
WINDOW_HEIGHT = 700
TITLE = f"NetFree Unlocker V{__version__} - AI Engine"


class Api:
    """הגשר בין ה-JS לפייתון. נגיש מה-JS דרך pywebview.api."""

    def __init__(self):
        self._window = None

    def bind(self, window):
        self._window = window

    def read_clipboard(self):
        """מחזיר {ok, text}. ok=False כשהלוח לא נגיש."""
        try:
            return {"ok": True, "text": clipboard.read_text()}
        except OSError:
            return {"ok": False, "text": ""}

    def close(self):
        if self._window is not None:
            self._window.destroy()


def run():
    api = Api()
    window = webview.create_window(
        TITLE,
        url=ui_entry(),
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=False,
        background_color="#F1F5F9",
    )
    api.bind(window)
    webview.start()
