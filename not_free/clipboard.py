"""קריאת הלוח דרך Win32.

ה-Clipboard API של הדפדפן חסום תחת file://, ולכן ההדבקה עוברת דרך פייתון.
ctypes מגיע עם פייתון — בלי תלות נוספת ובלי להגדיל את ה-EXE.
"""

import ctypes
from ctypes import wintypes

CF_UNICODETEXT = 13

_user32 = ctypes.WinDLL("user32", use_last_error=True)
_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

# בלי ההצהרות האלה ctypes מניח שכל פונקציה מחזירה int של 32 ביט,
# ומקצץ מצביעים ו-handles ב-64 ביט.
_user32.OpenClipboard.argtypes = [wintypes.HWND]
_user32.OpenClipboard.restype = wintypes.BOOL
_user32.CloseClipboard.argtypes = []
_user32.CloseClipboard.restype = wintypes.BOOL
_user32.GetClipboardData.argtypes = [wintypes.UINT]
_user32.GetClipboardData.restype = wintypes.HANDLE
_kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
_kernel32.GlobalLock.restype = wintypes.LPVOID
_kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
_kernel32.GlobalUnlock.restype = wintypes.BOOL


def read_text():
    """מחזיר את הטקסט שבלוח, או מחרוזת ריקה. זורק OSError אם הלוח נעול."""
    if not _user32.OpenClipboard(None):
        raise OSError("clipboard is locked by another process")
    try:
        handle = _user32.GetClipboardData(CF_UNICODETEXT)
        if not handle:
            return ""
        pointer = _kernel32.GlobalLock(handle)
        if not pointer:
            return ""
        try:
            return ctypes.c_wchar_p(pointer).value or ""
        finally:
            _kernel32.GlobalUnlock(handle)
    finally:
        _user32.CloseClipboard()
