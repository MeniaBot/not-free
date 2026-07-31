"""מסך הפתיחה."""

import flet as ft

from . import survey

AUTHOR_URL = (
    "https://mitmachim.top/user/"
    "%D7%91%D7%A0%D7%99%D7%9E%D7%99%D7%9F-%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D"
)

PITCH = (
    'בס"ד עלה בידינו לפתח תוכנה עוצמתית ופשוטה לשימוש \n'
    'המסוגלת לאפשר גישה לתכנים שנחסמו ע"י נטפרי.\n\n'
    "כלי מתקדם מבוסס AI יסקור את בקשתך בכפוף לקריטריונים מחמירים.\n\n"
    "שימו לב! אין להעביר את התוכנה לאף גורם המקושר לנטפרי!!!"
)


def _credit(app):
    return ft.Text(
        spans=[
            ft.TextSpan(
                "©️",
                style=ft.TextStyle(color=ft.Colors.BLUE, size=18, weight=ft.FontWeight.BOLD),
            ),
            ft.TextSpan(" נוצר על ידי ", style=ft.TextStyle(color=ft.Colors.BLUE, size=14)),
            ft.TextSpan(
                "@בנימין-מחשבים",
                style=ft.TextStyle(
                    color=ft.Colors.BLUE,
                    size=14,
                    decoration=ft.TextDecoration.UNDERLINE,
                    decoration_thickness=1.5,
                    weight=ft.FontWeight.BOLD,
                ),
                on_click=lambda _: app.page.launch_url(AUTHOR_URL),
            ),
            ft.TextSpan(" באתר מתמחים טופ", style=ft.TextStyle(color=ft.Colors.BLUE, size=14)),
        ]
    )


def show(app):
    app.clean()
    app.add(
        ft.Column(
            [
                ft.Container(height=20),
                ft.Icon(name=ft.Icons.LOCK_OPEN_ROUNDED, color=ft.Colors.RED_700, size=60),
                ft.Text("בשורה למשתמשי נטפרי!", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                ft.Text("הסוף לרודנות - פתיחת תכנים שנחסמו ללא סיבה", size=16, italic=True),
                ft.Container(height=20),
                ft.Text(PITCH, text_align=ft.TextAlign.RIGHT, width=450),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "אני מסכים - המשך",
                    on_click=lambda _: survey.show(app),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, padding=20),
                ),
                _credit(app),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
