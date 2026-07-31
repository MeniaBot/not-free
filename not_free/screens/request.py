"""סריקת חומות האש וטופס הבקשה."""

import time

import flet as ft

from . import hacking

APPROVED_HEADER = "אישור המערכת התקבל!"
SCAN_BLINKS = 8

LITVAK_STATUS = "אברך"
LITVAK_IDENTITY = "ליטאי קלאס"
LITVAK_MIN_WORDS = 20

REASON_HINT = (
    "יש לפרט בהרחבה לצורך ניתוח מעמיק של האלגוריתם. "
    "תיאור קצר מדי עלול להוביל לדחיית הבקשה."
)


def show_flash_scan(app):
    app.clean()
    scan_txt = ft.Text(
        "מתכונן לפריצה - סורק חומות אש", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE
    )
    app.add(
        ft.Column(
            [
                ft.Text(APPROVED_HEADER, size=22, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
                ft.Container(height=100),
                scan_txt,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    for blink in range(SCAN_BLINKS):
        scan_txt.color = ft.Colors.RED if blink % 2 == 0 else ft.Colors.ORANGE
        app.update()
        time.sleep(0.35)

    show(app)


def show(app):
    app.clean()

    url_field = ft.TextField(
        label="כאן מדביקים קישור לתוכן החסום",
        hint_text="ניתן להשתמש ב-Ctrl+V להדבקה",
        width=380,
        autofocus=True,
    )
    reason_field = ft.TextField(
        label="נא לנמק מדוע התוכן צריך להיפתח (לניתוח ה-AI)",
        hint_text=REASON_HINT,
        multiline=True,
        min_lines=10,
        max_lines=10,
        max_length=1000,
        width=450,
    )

    def paste_url(e):
        try:
            content = app.page.get_clipboard()
        except Exception:
            app.show_error("חסימת מערכת: השתמש ב-Ctrl+V להדבקה ידנית")
            return

        if content:
            url_field.value = content
        else:
            app.show_error("הלוח ריק. אין מה להדביק")
        url_field.focus()
        app.update()

    def submit(e):
        if not url_field.value or not reason_field.value:
            app.show_error("חובה למלא את הקישור והסיבה כדי להמשיך!")
            return

        # מאברך ליטאי מצפים לפלפול
        if (
            app.user_data["status"] == LITVAK_STATUS
            and app.user_data["identity"] == LITVAK_IDENTITY
            and len(reason_field.value.split()) < LITVAK_MIN_WORDS
        ):
            app.show_error("מאברך ליטאי מצופה לכתוב פלפול למדני מנומק היטב! נסח שוב...")
            return

        app.user_data["url"] = url_field.value
        app.user_data["reason"] = reason_field.value
        hacking.show(app)

    app.add(
        ft.Column(
            [
                ft.Text(APPROVED_HEADER, size=22, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        url_field,
                        ft.IconButton(
                            icon=ft.Icons.PASTE_ROUNDED,
                            on_click=paste_url,
                            tooltip="נסה להדביק מהלוח",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                reason_field,
                ft.ElevatedButton(
                    "בצע פריצה באמצעות בינה מלאכותית",
                    on_click=submit,
                    bgcolor=ft.Colors.ORANGE_800,
                    color=ft.Colors.WHITE,
                    width=300,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
    )
