"""החשיפה — "עלינו עליך" ואחריה "עבדנו עליך"."""

import random
import time

import flet as ft

from ..resources import NETFREE_LOGO, get_resource_path

SHAKE_STEPS = 15

EXPOSURE_BODY = (
    'התוכנה מופצת במטרה לזהות משתמשים המנסים לעקוף את הסינון המצוין של "נטפרי".\n\n'
    "פרטי המשתמש שלך, כתובת ה-IP והמיקום הפיזי שלך \nהועברו באופן אוטומטי למחלקת הפיקוח.\n"
    "מהיום רמת הסינון שלכם תתוגבר וכל פעולותיכם יפוקחו."
)

TYPED_LINE = "אבל אל תנסו את זה באמת..."


def show(app):
    """רעידת המסך שפותחת את רצף החשיפה."""
    app.clean()
    app.page.bgcolor = ft.Colors.BLACK

    warning_msg = ft.Text(
        "זיהוי המשתמש הושלם", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.RED
    )
    container = ft.Container(
        content=ft.Column(
            [
                ft.Icon(name=ft.Icons.GPP_BAD_ROUNDED, color=ft.Colors.RED, size=120),
                warning_msg,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        animate=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT),
    )
    app.add(ft.Container(height=150), container)
    app.update()

    for step in range(SHAKE_STEPS):
        flash = step % 2 == 0
        container.margin = ft.margin.only(left=25 if flash else -25)
        warning_msg.color = ft.Colors.WHITE if flash else ft.Colors.RED
        app.update()
        time.sleep(0.06)

    time.sleep(0.8)
    app.page.bgcolor = ft.Colors.WHITE
    _show_report(app)


def _show_report(app):
    """הדו"ח המזויף לנטפרי — עם הנימוק שהמשתמש עצמו כתב."""
    app.clean()
    fake_ip = f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    report_text = (
        f"המשתמש בכתובת {fake_ip} ניסה לעקוף את הסינון ולגשת לכתובת:\n"
        f"{app.user_data['url']}\n\n"
        f"בנימוק שהוזן למערכת:\n"
        f"\"{app.user_data['reason']}\""
    )

    loading_icon = ft.ProgressRing(width=20, height=20, stroke_width=2)
    status_label = ft.Text('שולח דו"ח הפרה למוקד נטפרי...', size=12, italic=True)

    app.add(
        ft.Container(height=100),
        ft.Column(
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.REPORT_GMAILERRORRED_ROUNDED, color=ft.Colors.RED
                                    ),
                                    title=ft.Text(
                                        'נשלח אל- נטפרי מערכת פניות \nדו"ח פעילות חריגה',
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    subtitle=ft.Text("מערכת ניטור אוטומטית"),
                                ),
                                ft.Container(
                                    content=ft.Text(report_text, color=ft.Colors.BLACK, size=14),
                                    padding=20,
                                ),
                                ft.Row(
                                    [loading_icon, status_label],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Container(height=10),
                            ]
                        ),
                        width=450,
                        padding=10,
                    ),
                    color=ft.Colors.GREY_100,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    app.update()

    time.sleep(3.5)
    status_label.value = 'הדו"ח נשלח בהצלחה ונקלט במערכת.'
    loading_icon.visible = False
    app.update()
    time.sleep(1.5)

    _show_exposure(app)


def _show_exposure(app):
    app.clean()
    app.add(
        ft.Column(
            [
                ft.Image(src=get_resource_path(NETFREE_LOGO), width=400),
                ft.Text("עלינו עליך!", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                ft.Text(EXPOSURE_BODY, text_align=ft.TextAlign.CENTER, width=450),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "להגשת ערעור למחלקת הפניות",
                    on_click=lambda _: _reveal(app),
                    bgcolor=ft.Colors.ORANGE,
                    color=ft.Colors.BLACK,
                    width=350,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
    )


def _reveal(app):
    app.clean()

    title = ft.Text(
        "עבדנו עליך...",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE,
        scale=0.1,
        opacity=0,
        animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN),
    )
    punchline = ft.Text(
        "😂😂😂\nבאמת חשבת שאפשר לעקוף סינון כל כך בקלות?",
        size=20,
        text_align=ft.TextAlign.CENTER,
        width=450,
        opacity=0,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN),
    )

    typewriter_text = ft.Text(value="", size=20, italic=True, color=ft.Colors.BLUE_700)
    typing_row = ft.Row(
        [typewriter_text, ft.Text(value=" 😉", size=20, italic=False)],  # האימוג'י ללא הטיה
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
        visible=False,
    )

    exit_btn = ft.ElevatedButton(
        "סגור וחשב מסלול מחדש",
        on_click=app.close,
        opacity=0,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN),
    )

    app.add(
        ft.Column(
            [
                ft.Container(height=40),
                ft.Icon(name=ft.Icons.SENTIMENT_VERY_SATISFIED_ROUNDED, color=ft.Colors.BLUE, size=80),
                title,
                ft.Container(height=10),
                punchline,
                ft.Container(height=10),
                typing_row,
                ft.Container(height=30),
                exit_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    app.update()

    time.sleep(0.2)
    title.scale = 1.0
    title.opacity = 1
    app.update()
    time.sleep(0.6)

    punchline.opacity = 1
    app.update()
    time.sleep(1.0)

    typing_row.visible = True
    for i in range(len(TYPED_LINE) + 1):
        typewriter_text.value = TYPED_LINE[:i]
        app.update()
        time.sleep(0.05)  # מהירות הקלדה טבעית

    time.sleep(0.3)
    exit_btn.opacity = 1
    app.update()
