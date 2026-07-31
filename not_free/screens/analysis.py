"""מסך הניתוח — פרוגרס-בר וחישוב הציון."""

import time

import flet as ft

from ..scoring import is_approved
from . import rejection, request

STEPS = {
    0: "מנתח נתונים אישיים...",
    40: "בודק התאמה לקריטריונים...",
    70: "מחשב רמת סיכון רוחנית...",
}


def show(app, status, identity, goal, eda):
    app.clean()
    bar = ft.ProgressBar(width=400, color=ft.Colors.BLUE_700)
    label = ft.Text(STEPS[0], size=18)
    app.add(
        ft.Container(height=200),
        ft.Column([label, bar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    )

    for percent in range(101):
        bar.value = percent * 0.01
        if percent in STEPS:
            label.value = STEPS[percent]
        app.update()
        time.sleep(0.03)

    if is_approved(status, identity, goal, eda):
        request.show_flash_scan(app)
    else:
        rejection.show(app)
