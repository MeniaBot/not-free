"""רצף ה"פריצה" — מסך הניתוח ואחריו הטרמינל."""

import random
import time

import flet as ft

from . import outcome

LOG_COLOR = ft.Colors.GREEN_700
URL_LINE = "> Requesting content: "

LOG_LINES = [
    "> Initializing NetFree-Slayer V0.3...",
    "> מתחבר לממשק ה-API של ספק הסינון...",
    "> Intercepting SSL Handshake...",
    "> מזריק פקודות עקיפה לפרוטוקול HTTPS...",
    "> Bypass status: 15%...",
    "> מפענח מפתחות הצפנה זמניים...",
    "> Injecting local Proxy-Tunnel...",
    "> סורק חומות אש ארגוניות...",
    "> Attempting Zero-Day exploit on NF-Gateway...",
    "> Bypass status: 48%...",
    "> משנה כתובת IP לזיהוי אנונימי...",
    "> Overriding DNS filtering rules...",
    "> Bypass status: 72%...",
    "> מתבצע ניסיון התחברות לתוכן המבוקש...",
    URL_LINE,
    "> Server response: 403 Forbidden (Filtered by NetFree AI)",
    "> WARNING: Anti-Tamper mechanism triggered!",
    "> Bypass status: 94%...",
    "> כמעט שם: מבצע אופטימיזציה למהירות הפריצה...",
    "> FATAL ERROR: Unauthorized access attempt logged by server.",
    "> CRITICAL ERROR: System Integrity Violation Detected!",
    "> Error 912: נתקל בקושי טכני לשלוף את התוכן המבוקש",
]


def show(app):
    _analyzing(app)
    _terminal(app)
    time.sleep(1.5)
    outcome.show(app)


def _analyzing(app):
    app.clean()
    status_txt = ft.Text("מנוע AI מנתח את בקשת הפריצה...", size=18, color=ft.Colors.BLUE)
    app.add(
        ft.Container(height=150),
        ft.Column(
            [status_txt, ft.ProgressBar(width=400, color=ft.Colors.BLUE)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    app.update()
    time.sleep(3)

    status_txt.value = "ניתוח הושלם. הטיעונים אושרו. מתחבר לשרתי הליבה..."
    status_txt.color = ft.Colors.GREEN
    app.update()
    time.sleep(2)


def _terminal(app):
    app.clean()
    terminal_text = ft.Text("", font_family="monospace", size=12, color=LOG_COLOR, spans=[])
    app.add(
        ft.Text("הפריצה מתבצעת כעת - יש להמתין לסיום", size=16, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=ft.Column([terminal_text], scroll=ft.ScrollMode.ALWAYS, auto_scroll=True),
            bgcolor=ft.Colors.BLACK,
            padding=10,
            border_radius=5,
            width=500,
            height=400,
        ),
    )

    style = ft.TextStyle(color=LOG_COLOR)
    for line in LOG_LINES:
        if line == URL_LINE:
            terminal_text.spans.append(ft.TextSpan(line, style=style))
            terminal_text.spans.append(
                ft.TextSpan(
                    app.user_data["url"],
                    style=ft.TextStyle(color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD),
                )
            )
            terminal_text.spans.append(ft.TextSpan("\n", style=style))
            app.update()
            time.sleep(2.5)  # עיכוב ארוך יותר לקישור
        else:
            terminal_text.spans.append(ft.TextSpan(f"{line}\n", style=style))
            app.update()
            time.sleep(random.uniform(0.2, 1.8))  # קצב הופעה לא אחיד
