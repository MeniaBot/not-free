"""שאלון הכשירות."""

import time

import flet as ft

from ..scoring import EDA_SCORES, GOAL_SCORES, IDENTITY_SCORES, OTHER, STATUS_SCORES
from . import analysis, rejection

SEMINAR_STATUS = "תלמידת סמינר"
TORAH_GOAL = "לימוד תורה"
SEMINAR_VERDICT = "כל המלמד בתו תורה כאילו מלמדה תיפלות"

DECLARE_KEY = "declare_cb_container"


def _dropdown(label, scores):
    return ft.Dropdown(
        label=label,
        width=400,
        label_style=ft.TextStyle(weight=ft.FontWeight.W_300),
        options=[ft.dropdown.Option(text) for text in scores],
    )


def _seminar_stall(app):
    """המתנה מבוימת לפני הפסילה של תלמידת סמינר שגולשת ללימוד תורה."""
    app.clean()
    app.add(
        ft.Container(height=200),
        ft.Column(
            [
                ft.Text("מנתח שילוב סטטוס וצורך...", size=18),
                ft.ProgressBar(width=400, color=ft.Colors.RED_700),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    app.update()
    time.sleep(3)


def show(app):
    app.clean()

    status_dd = _dropdown("סטטוס", STATUS_SCORES)
    identity_dd = _dropdown("מגדיר/ה את עצמך", IDENTITY_SCORES)
    goal_dd = _dropdown("גולש/ת לצורך", GOAL_SCORES)
    eda_dd = _dropdown("עדה", EDA_SCORES)

    extra_status = ft.TextField(label="נא לפרט סטטוס...", visible=False, width=400)
    extra_goal = ft.TextField(label="נא לפרט צורך...", visible=False, width=400)

    declare_cb = ft.Checkbox(
        label="אני מצהיר כי הגישה לתכנים הינה לצורך לימודי/תורני בלבד\nואינה סותרת את דעת רבותיי.",
        label_style=ft.TextStyle(size=13),
        value=False,
    )

    fields = ft.Column(
        [
            status_dd,
            extra_status,
            identity_dd,
            goal_dd,
            extra_goal,
            eda_dd,
            ft.Container(content=declare_cb, padding=ft.padding.only(right=20), key=DECLARE_KEY),
        ],
        height=338,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def check_extra(e):
        extra_status.visible = status_dd.value == OTHER
        extra_goal.visible = goal_dd.value == OTHER
        app.update()

    status_dd.on_change = check_extra
    goal_dd.on_change = check_extra

    def validate(e):
        if not status_dd.value or not goal_dd.value or not eda_dd.value or not identity_dd.value:
            app.show_error("חובה למלא את כל השדות בשאלון כדי להמשיך!")
            return

        if not declare_cb.value:
            app.show_error("עליך לאשר את ההצהרה כדי להמשיך!")
            fields.scroll_to(key=DECLARE_KEY, duration=1000)
            return

        if (status_dd.value == OTHER and not extra_status.value) or (
            goal_dd.value == OTHER and not extra_goal.value
        ):
            app.show_error('בבחירה ב"אחר" - חובה לפרט!')
            return

        if status_dd.value == SEMINAR_STATUS and goal_dd.value == TORAH_GOAL:
            _seminar_stall(app)
            rejection.show(app, custom_msg=SEMINAR_VERDICT)
            return

        app.user_data["status"] = status_dd.value
        app.user_data["identity"] = identity_dd.value
        analysis.show(app, status_dd.value, identity_dd.value, goal_dd.value, eda_dd.value)

    app.add(
        ft.Column(
            [
                ft.Text("הבוט שלנו רוצה לדעת עליך יותר!", size=22, weight=ft.FontWeight.BOLD),
                fields,
                ft.Container(height=20),
                ft.ElevatedButton(
                    "שלח לאבחון רובוטי",
                    on_click=validate,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    width=200,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
