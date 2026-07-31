"""גישה לנכסים המוטמעים, גם כשרצים מתוך EXE של PyInstaller."""

import os
import sys

ICON = "GH.ico"
NETFREE_LOGO = "Netfree_logo.svg.png"


def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
