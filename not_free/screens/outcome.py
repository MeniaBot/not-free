"""מסך הכישלון והבחירה שאחריו."""

import time

import flet as ft

from . import exposure

FAILURE_BODY = (
    "\n\nהמערכת לא הצליחה לשלוף בשבילך את התוכן המבוקש.\n\n"
    "עדיין יש באפשרותך להמשיך לגלוש ללא סינון כלל\n\n\n      יש לבחור באחת האפשרויות:"
)


def show(app):
    app.clean()
    app.add(
        ft.Column(
            [
                ft.Text(
                    "\n\n- - - הפריצה נכשלה - - -",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED,
                ),
                ft.Text(FAILURE_BODY, text_align=ft.TextAlign.RIGHT),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "חזרה לסינון נטפרי (סגור תוכנה)",
                    on_click=lambda _: _show_praise(app),
                    width=400,
                ),
                ft.ElevatedButton(
                    "אני לוקח/ת סיכון! - המשך גלישה ללא סינון כלל",
                    on_click=lambda _: exposure.show(app),
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    width=400,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


def _show_praise(app):
    """מי שבחר לחזור לסינון — מקבל מחמאה והתוכנה נסגרת."""
    app.clean()

    icon = ft.Icon(
        name=ft.Icons.CELEBRATION_ROUNDED,
        color=ft.Colors.BLUE_700,
        size=120,
        scale=0.1,
        opacity=0,
        animate_scale=ft.Animation(800, ft.AnimationCurve.ELASTIC_OUT),
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN),
    )
    msg = ft.Text(
        "עשית את הבחירה הנכונה!",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
        opacity=0,
        animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_IN),
    )
    sub_msg = ft.Text("התוכנה נסגרת כעת...", size=16, color=ft.Colors.GREY_700, visible=False)

    app.add(
        ft.Column(
            [
                ft.Container(height=80),
                icon,
                ft.Container(height=20),
                msg,
                ft.Container(height=15),
                sub_msg,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    app.update()

    time.sleep(0.1)
    icon.scale = 1.0
    icon.opacity = 1
    msg.opacity = 1
    app.update()

    time.sleep(1.0)
    sub_msg.visible = True
    app.update()

    time.sleep(3.0)
    app.close()
