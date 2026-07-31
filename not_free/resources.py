"""גישה לקבצי הממשק, גם כשרצים מתוך EXE של PyInstaller."""

import os
import sys


def resource_path(*parts):
    base = getattr(sys, "_MEIPASS", None) or os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base, *parts)


def ui_entry():
    """הנתיב ל-index.html שנטען לחלון."""
    return resource_path("ui", "index.html")
