"""מצב האפליקציה, הגדרות החלון והעזרים המשותפים לכל המסכים."""

import flet as ft

from . import __version__
from .resources import ICON, get_resource_path

WINDOW_SIZE = 550


class App:
    """נושא את ה-page ואת נתוני המשתמש. כל מסך מקבל אותו ומחזיר אותו לבא אחריו."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.user_data = {"url": "", "reason": "", "status": "", "identity": ""}
        self._snack_bar = None
        self._setup_window()

    def _setup_window(self):
        page = self.page
        page.title = f"NetFree Unlocker V{__version__} - AI Engine"
        page.window.icon = get_resource_path(ICON)
        page.window.width = WINDOW_SIZE
        page.window.height = WINDOW_SIZE
        page.window.resizable = False
        page.window.center()

        page.theme_mode = ft.ThemeMode.LIGHT
        page.rtl = True
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding = 20

    def add(self, *controls):
        self.page.add(*controls)

    def clean(self):
        self.page.clean()

    def update(self):
        self.page.update()

    def show_error(self, message):
        """מציג הודעת שגיאה ממורכזת, ומשאיר SnackBar אחד ב-overlay במקום לצבור."""
        if self._snack_bar is not None and self._snack_bar in self.page.overlay:
            self.page.overlay.remove(self._snack_bar)
        self._snack_bar = ft.SnackBar(
            content=ft.Row(
                [ft.Text(message)], alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.RED_700,
        )
        self.page.overlay.append(self._snack_bar)
        self._snack_bar.open = True
        self.page.update()

    def close(self, _=None):
        """סוגר את התוכנה. מתאים ישירות כ-on_click."""
        self.page.window.destroy()


def main(page: ft.Page):
    from .screens import welcome

    welcome.show(App(page))


def run():
    ft.app(target=main)
