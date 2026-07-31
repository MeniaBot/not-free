"""מסך הדחייה, ומסך השריפה שאחריו."""

import time

import flet as ft

GENERIC_VERDICT = (
    "ניתוח ה-AI הסתיים:\n\nהמשתמש אינו עומד בקריטריונים הרוחניים.\n\n"
    "המערכת זיהתה רמת סיכון גבוהה עבור הפרופיל שהוזן.\n\n"
    "הגישה לכלי הפריצה נחסמה מטעמי הגנה."
)

BURNING_LINE = "ישרפו דברי תורה ואל ימסרו לנשים!!"
BURNING_SOURCE = "(ירושלמי סוטה, פרק ג' הלכה ד')"
FLICKER_STEPS = 15


def show(app, custom_msg=None):
    app.clean()

    icon = ft.Icon(
        name=ft.Icons.GPP_BAD,
        color=ft.Colors.RED_800,
        size=80,
        scale=0.1,
        opacity=0,
        animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN),
    )
    title = ft.Text(
        "בקשתך נדחתה!",
        size=25,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED_800,
        scale=0.1,
        opacity=0,
        animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN),
    )

    column = ft.Column(
        [ft.Container(height=50), icon, title],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    app.add(column)
    app.update()

    # אנימציית ההגדלה
    time.sleep(0.1)
    icon.scale = 1.0
    icon.opacity = 1
    title.scale = 1.0
    title.opacity = 1
    app.update()

    time.sleep(0.7)  # המתנה לסיום האנימציה לפני הוספת שאר הטקסט

    if custom_msg:
        column.controls.extend(_custom_verdict(app, custom_msg))
    else:
        column.controls.extend(_generic_verdict(app))
    app.update()


def _custom_verdict(app, custom_msg):
    return [
        ft.Container(height=20),
        ft.Text(
            f'"{custom_msg}"',
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
            font_family="serif",
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Text("(סוטה ג', ד')", size=12, color=ft.Colors.GREY_700),
        ft.Container(height=30),
        ft.ElevatedButton(
            "אולי בכל זאת?",
            on_click=lambda _: show_burning(app),
            bgcolor=ft.Colors.RED_700,
            color=ft.Colors.WHITE,
        ),
    ]


def _generic_verdict(app):
    return [
        ft.Text(GENERIC_VERDICT, text_align=ft.TextAlign.CENTER, width=450),
        ft.Container(height=30),
        ft.ElevatedButton(
            "יציאה מהתוכנה",
            on_click=app.close,
            bgcolor=ft.Colors.GREY_700,
            color=ft.Colors.WHITE,
        ),
    ]


def show_burning(app):
    app.clean()
    app.page.bgcolor = ft.Colors.BLACK

    text = ft.Text(
        BURNING_LINE,
        size=35,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.ORANGE_800,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_IN),
    )
    source = ft.Text(
        BURNING_SOURCE,
        size=16,
        color=ft.Colors.BLACK,
        weight=ft.FontWeight.BOLD,
        opacity=0,
        animate_opacity=ft.Animation(1500, ft.AnimationCurve.EASE_IN),
    )
    fire = ft.Icon(
        name=ft.Icons.WHATSHOT,
        color=ft.Colors.ORANGE,
        size=100,
        opacity=0,
        animate_opacity=ft.Animation(800, ft.AnimationCurve.BOUNCE_IN),
    )

    app.add(
        ft.Container(
            content=ft.Column(
                [ft.Container(height=100), fire, ft.Container(height=20), text, source],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )
    )
    app.update()

    time.sleep(0.5)
    text.opacity = 1
    fire.opacity = 1
    app.update()
    time.sleep(0.5)
    source.opacity = 1
    app.update()

    # אפקט "להבות" - שינוי צבעים מהיר
    for step in range(FLICKER_STEPS):
        flash = step % 2 == 0
        app.page.bgcolor = ft.Colors.RED_900 if flash else ft.Colors.BLACK
        fire.color = ft.Colors.YELLOW if flash else ft.Colors.ORANGE
        text.color = ft.Colors.YELLOW if flash else ft.Colors.RED
        app.update()
        time.sleep(0.15)

    time.sleep(3)
    app.close()
