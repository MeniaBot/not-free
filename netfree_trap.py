import flet as ft
import time
import os
import sys
import random

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main(page: ft.Page):
    page.title = "NetFree Unlocker V0.8.5 - AI Engine"
    page.window.icon = get_resource_path("GH.ico")
    page.window.width = 550
    page.window.height = 550
    page.window.resizable = False
    page.window.center() 
    
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # משתנים גלובליים לאחסון נתוני המשתמש לצורך הדו"ח
    user_data = {"url": "", "reason": "", "status": "", "identity": ""}

    def show_error(message):
        sb = ft.SnackBar(ft.Text(message), bgcolor="red700")
        page.overlay.append(sb)
        sb.open = True
        page.update()

    def show_welcome():
        page.clean()
        page.add(
            ft.Column([
                ft.Container(height=20),
                ft.Icon(name=ft.Icons.LOCK_OPEN_ROUNDED, color="red700", size=60), 
                ft.Text("בשורה למשתמשי נטפרי!", size=30, weight="bold", color="red700"),
                ft.Text("הסוף לרודנות - פתיחת תכנים שנחסמו ללא סיבה", size=16, italic=True),
                ft.Container(height=20),
                ft.Text(
                    "בס\"ד עלה בידינו לפתח תוכנה עוצמתית ופשוטה לשימוש \n"
                    "המסוגלת לאפשר גישה לתכנים שנחסמו ע\"י נטפרי.\n\n"
                    "כלי מתקדם מבוסס AI יסקור את בקשתך בכפוף לקריטריונים מחמירים.\n\n"
                    "שימו לב! אין להעביר את התוכנה לאף גורם המקושר לנטפרי!!!",
                    text_align=ft.TextAlign.RIGHT, width=450
                ),
                ft.Container(height=20), 
                ft.ElevatedButton(
                    "אני מסכים - המשך", 
                    on_click=lambda _: show_survey(),
                    style=ft.ButtonStyle(bgcolor="green700", color="white", padding=20)
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan("©️", style=ft.TextStyle(color="blue", size=18, weight="bold")), 
                        ft.TextSpan(" נוצר על ידי ", style=ft.TextStyle(color="blue", size=14)), 
                        ft.TextSpan(
                            "@בנימין-מחשבים",
                            style=ft.TextStyle(
                                color="blue",
                                size=14, 
                                decoration=ft.TextDecoration.UNDERLINE,
                                decoration_thickness=1.5,
                                weight="bold"
                            ),
                            on_click=lambda _: page.launch_url("https://mitmachim.top/user/%D7%91%D7%A0%D7%99%D7%9E%D7%99%D7%9F-%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D")
                        ),
                        ft.TextSpan(" באתר מתמחים טופ", style=ft.TextStyle(color="blue", size=14)), 
                    ]
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def show_survey():
        page.clean()
        status_dd = ft.Dropdown(
            label="סטטוס", width=400,
            label_style=ft.TextStyle(weight=ft.FontWeight.W_300),
            options=[ft.dropdown.Option(text) for text in ["אברך", "בחור ישיבה", "תלמידת סמינר", "תלמיד ת\"ת", "נושר", "אחר (נא לפרט)"]]
        )
        
        identity_dd = ft.Dropdown(
            label="מגדיר/ה את עצמך", width=400,
            label_style=ft.TextStyle(weight=ft.FontWeight.W_300),
            options=[ft.dropdown.Option(text) for text in ["צו\"ל", "ליטאי קלאס", "חסידישע'ר", "חזונישנ'יק", "בעל תשובה", "חרדי מודרני"]]
        )

        goal_dd = ft.Dropdown(
            label="גולש/ת לצורך", width=400,
            label_style=ft.TextStyle(weight=ft.FontWeight.W_300),
            options=[ft.dropdown.Option(text) for text in ["פרנסה", "לימוד תורה", "לימודים כלליים", "חדשות", "בידור ופנאי", "אחר (נא לפרט)"]]
        )
        eda_dd = ft.Dropdown(
            label="עדה", width=400,
            label_style=ft.TextStyle(weight=ft.FontWeight.W_300),
            options=[ft.dropdown.Option(text) for text in ["אשכנזי", "ספרדי", "תימני", "מעורב", "ספרדי אבל לומד בסורוצקין😉"]]
        )

        extra_status = ft.TextField(label="נא לפרט סטטוס...", visible=False, width=400)
        extra_goal = ft.TextField(label="נא לפרט צורך...", visible=False, width=400)

        # צ'קבוקס 
        declare_cb = ft.Checkbox(
            label="אני מצהיר כי הגישה לתכנים הינה לצורך לימודי/תורני בלבד\nואינה סותרת את דעת רבותיי.",
            label_style=ft.TextStyle(size=13),
            value=False
        )

        def check_extra(e):
            extra_status.visible = (status_dd.value == "אחר (נא לפרט)")
            extra_goal.visible = (goal_dd.value == "אחר (נא לפרט)")
            page.update()

        status_dd.on_change = check_extra
        goal_dd.on_change = check_extra

        def validate_survey(e):
            if not status_dd.value or not goal_dd.value or not eda_dd.value or not identity_dd.value:
                show_error("                     חובה למלא את כל השדות בשאלון כדי להמשיך!")
                return
            
            # בדיקת הצ'קבוקס
            if not declare_cb.value:
                show_error("                                 עליך לאשר את ההצהרה כדי להמשיך!")
                page.scroll_to(key="declare_cb_container", duration=1000)
                return

            # בדיקת שדות הפירוט במידה ונבחר "אחר"
            if (status_dd.value == "אחר (נא לפרט)" and not extra_status.value) or \
               (goal_dd.value == "אחר (נא לפרט)" and not extra_goal.value):
                show_error("                                         בבחירה ב\"אחר\" - חובה לפרט!")
                return

            if status_dd.value == "תלמידת סמינר" and goal_dd.value == "לימוד תורה":
                page.clean()
                loading_txt = ft.Text("מנתח שילוב סטטוס וצורך...", size=18)
                page.add(ft.Container(height=200), ft.Column([loading_txt, ft.ProgressBar(width=400, color="red700")], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
                page.update()
                time.sleep(3)
                show_rejection(custom_msg="כל המלמד בתו תורה כאילו מלמדה תיפלות")
                return

            user_data["status"] = status_dd.value
            user_data["identity"] = identity_dd.value
            start_analysis(status_dd.value, identity_dd.value, goal_dd.value, eda_dd.value)

        page.add(
            ft.Column([
                ft.Text("הבוט שלנו רוצה לדעת עליך יותר!", size=22, weight="bold"),
                # עטיפת השדות בטור עם גובה קבוע כדי למנוע קפיצות של הכפתור
                ft.Column([
                    status_dd, extra_status,
                    identity_dd,
                    goal_dd, extra_goal,
                    eda_dd,
                    ft.Container(content=declare_cb, padding=ft.padding.only(right=20), key="declare_cb_container")
                ], height=338, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=20),
                ft.ElevatedButton("שלח לאבחון רובוטי", 
                                   on_click=validate_survey,
                                   bgcolor="blue700", color="white", width=200)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def start_analysis(s, i_val, g, e_val):
        page.clean()
        pb = ft.ProgressBar(width=400, color="blue700")
        txt = ft.Text("מנתח נתונים אישיים...", size=18)
        page.add(ft.Container(height=200), ft.Column([txt, pb], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        
        for i in range(101):
            pb.value = i * 0.01
            if i == 40: txt.value = "בודק התאמה לקריטריונים..."
            if i == 70: txt.value = "מחשב רמת סיכון רוחנית..."
            page.update()
            time.sleep(0.03)
        
        # חישוב דירוג לכל הפרמטרים
        score = 0
        
        # משקל סטטוס
        if s == "אברך": score += 20
        elif s == "בחור ישיבה": score += 10
        elif s == "תלמידת סמינר": score += 8
        elif s == "נושר": score -= 40
        
        # משקל "מגדיר את עצמך"
        if i_val == "צו\"ל": score += 15
        elif i_val == "ליטאי קלאס": score += 10
        elif i_val == "חסידישע'ר": score += 12
        elif i_val == "חרדי מודרני": score -= 20
        elif i_val == "חזונישנ'יק": score += 15
        elif i_val == "בעל תשובה": score += 15
        
        # משקל צורך
        if g == "לימוד תורה": score += 25
        elif g == "פרנסה": score += 15
        elif g == "לימודים כלליים": score += 10
        elif g == "חדשות": score -= 20
        elif g == "בידור ופנאי": score -= 50
        
        # משקל עדה
        if e_val == "ספרדי אבל לומד בסורוצקין😉": score += 5
        elif e_val == "תימני": score -= 5
        elif e_val == "אשכנזי": score += 10

        if score < 35: show_rejection()
        else: show_flash_scan()

    def show_rejection(custom_msg=None):
        page.clean()
        
        # יצירת רכיבי האנימציה עבור הכותרת והסמל
        rejection_icon = ft.Icon(
            name=ft.Icons.GPP_BAD, 
            color="red800", 
            size=80,
            scale=0.1,
            opacity=0,
            animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN)
        )
        
        rejection_title = ft.Text(
            "בקשתך נדחתה!", 
            size=25, 
            weight="bold", 
            color="red800",
            scale=0.1,
            opacity=0,
            animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN)
        )

        content_column = ft.Column(
            [
                ft.Container(height=50),
                rejection_icon,
                rejection_title,
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(content_column)
        page.update()

        # הפעלת אנימציית הגדלה
        time.sleep(0.1)
        rejection_icon.scale = 1.0
        rejection_icon.opacity = 1
        rejection_title.scale = 1.0
        rejection_title.opacity = 1
        page.update()
        
        time.sleep(0.7) # המתנה לסיום האנימציה לפני הוספת שאר הטקסט

        if custom_msg:
            extra_content = [
                ft.Container(height=20),
                ft.Text(
                    f"\"{custom_msg}\"",
                    size=28,
                    weight="bold",
                    color="black",
                    font_family="serif",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text("(סוטה ג', ד')", size=12, color="grey700"),
                ft.Container(height=30),
                ft.ElevatedButton("אולי בכל זאת?", on_click=lambda _: show_burning_page(), bgcolor="red700", color="white")
            ]
        else:
            extra_content = [
                ft.Text(
                    "ניתוח ה-AI הסתיים:\n\nהמשתמש אינו עומד בקריטריונים הרוחניים.\n\n"
                    "המערכת זיהתה רמת סיכון גבוהה עבור הפרופיל שהוזן.\n\n"
                    "הגישה לכלי הפריצה נחסמה מטעמי הגנה.",
                    text_align=ft.TextAlign.CENTER, width=450
                ),
                ft.Container(height=30),
                ft.ElevatedButton("יציאה מהתוכנה", on_click=lambda _: page.window.destroy(), bgcolor="grey700", color="white")
            ]
        
        content_column.controls.extend(extra_content)
        page.update()

    def show_burning_page():
        page.clean()
        page.bgcolor = "black"
        
        burning_text = ft.Text(
            "ישרפו דברי תורה ואל ימסרו לנשים!!",
            size=35,
            weight="bold",
            color="orange800",
            text_align=ft.TextAlign.CENTER,
            opacity=0,
            animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_IN)
        )
        
        source_text = ft.Text(
            "(ירושלמי סוטה, פרק ג' הלכה ד')",
            size=16,
            color="black", 
            weight="bold", 
            opacity=0,
            animate_opacity=ft.Animation(1500, ft.AnimationCurve.EASE_IN)
        )

        fire_icon = ft.Icon(
            name=ft.Icons.WHATSHOT,
            color="orange",
            size=100,
            opacity=0,
            animate_opacity=ft.Animation(800, ft.AnimationCurve.BOUNCE_IN)
        )

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Container(height=100),
                    fire_icon,
                    ft.Container(height=20),
                    burning_text,
                    source_text,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        )
        page.update()

        # התחלת האנימציה
        time.sleep(0.5)
        burning_text.opacity = 1
        fire_icon.opacity = 1
        page.update()
        time.sleep(0.5)
        source_text.opacity = 1
        page.update()

        # אפקט "להבות" - שינוי צבעים מהיר
        for _ in range(15):
            page.bgcolor = "red900" if _ % 2 == 0 else "black"
            fire_icon.color = "yellow" if _ % 2 == 0 else "orange"
            burning_text.color = "yellow" if _ % 2 == 0 else "red"
            page.update()
            time.sleep(0.15)

        time.sleep(3)
        page.window.destroy()

    def show_flash_scan():
        page.clean()
        scan_txt = ft.Text("מתכונן לפריצה - סורק חומות אש", size=20, weight="bold", color="orange")
        page.add(ft.Column([
            ft.Text("אישור המערכת התקבל!", size=22, color="green", weight="bold"),
            ft.Container(height=100),
            scan_txt
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        
        for i in range(8):
            scan_txt.color = "red" if i % 2 == 0 else "orange"
            page.update()
            time.sleep(0.35)
        
        show_request_form()

    def show_request_form():
        page.clean()
        url_field = ft.TextField(
            label="כאן מדביקים קישור לתוכן החסום", 
            hint_text="ניתן להשתמש ב-Ctrl+V להדבקה",
            width=380, 
            autofocus=True
        )
        
        reason_field = ft.TextField(
            label="נא לנמק מדוע התוכן צריך להיפתח (לניתוח ה-AI)",
            hint_text="יש לפרט בהרחבה לצורך ניתוח מעמיק של האלגוריתם. תיאור קצר מדי עלול להוביל לדחיית הבקשה.",
            multiline=True, 
            min_lines=10, 
            max_lines=10,
            max_length=1000,
            width=450
        )
        
        def paste_url(e):
            try:
                content = page.get_clipboard()
                if content:
                    url_field.value = content
                else:
                    show_error("                                     הלוח ריק. אין מה להדביק")
                url_field.focus()
                page.update()
            except Exception:
                show_error("חסימת מערכת: השתמש ב-Ctrl+V להדבקה ידנית")

        def validate_and_final(e):
            if not url_field.value or not reason_field.value:
                show_error("                         חובה למלא את הקישור והסיבה כדי להמשיך!")
                return
            
            # הבדיקה לאברך ליטאי
            if user_data["status"] == "אברך" and user_data["identity"] == "ליטאי קלאס":
                word_count = len(reason_field.value.split())
                if word_count < 20:
                    show_error("            מאברך ליטאי מצופה לכתוב פלפול למדני מנומק היטב! נסח שוב...")
                    return

            user_data["url"] = url_field.value
            user_data["reason"] = reason_field.value
            final_sequence()

        page.add(
            ft.Column([
                ft.Text("אישור המערכת התקבל!", size=22, color="green", weight="bold"),
                ft.Row([
                    url_field, 
                    ft.IconButton(
                        icon=ft.Icons.PASTE_ROUNDED, 
                        on_click=paste_url, 
                        tooltip="נסה להדביק מהלוח"
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                reason_field,
                ft.ElevatedButton("בצע פריצה באמצעות בינה מלאכותית", 
                                   on_click=validate_and_final,
                                   bgcolor="orange800", color="white", width=300)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        )

    def final_sequence():
        page.clean()
        status_txt = ft.Text("מנוע AI מנתח את בקשת הפריצה...", size=18, color="blue")
        progress = ft.ProgressBar(width=400, color="blue")
        page.add(ft.Container(height=150), ft.Column([status_txt, progress], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        page.update()
        time.sleep(3)
        
        status_txt.value = "ניתוח הושלם. הטיעונים אושרו. מתחבר לשרתי הליבה..."
        status_txt.color = "green"
        page.update()
        time.sleep(2)

        page.clean()
        terminal_text = ft.Text("", font_family="monospace", size=12, color="green700", spans=[])
        page.add(
            ft.Text("הפריצה מתבצעת כעת - יש להמתין לסיום", size=16, weight="bold"),
            ft.Container(
                content=ft.Column([terminal_text], scroll=ft.ScrollMode.ALWAYS, auto_scroll=True), bgcolor="black", padding=10, border_radius=5, width=500, height=400
            )
        )
        
        logs = [
            ("> Initializing NetFree-Slayer V0.3...", "green700"),
            ("> מתחבר לממשק ה-API של ספק הסינון...", "green700"),
            ("> Intercepting SSL Handshake...", "green700"),
            ("> מזריק פקודות עקיפה לפרוטוקול HTTPS...", "green700"),
            ("> Bypass status: 15%...", "green700"),
            ("> מפענח מפתחות הצפנה זמניים...", "green700"),
            ("> Injecting local Proxy-Tunnel...", "green700"),
            ("> סורק חומות אש ארגוניות...", "green700"),
            ("> Attempting Zero-Day exploit on NF-Gateway...", "green700"),
            ("> Bypass status: 48%...", "green700"),
            ("> משנה כתובת IP לזיהוי אנונימי...", "green700"),
            ("> Overriding DNS filtering rules...", "green700"),
            ("> Bypass status: 72%...", "green700"),
            ("> מתבצע ניסיון התחברות לתוכן המבוקש...", "green700"),
            (f"> Requesting content: ", "green700"), # הקישור יטופל בנפרד
            ("> Server response: 403 Forbidden (Filtered by NetFree AI)", "green700"),
            ("> WARNING: Anti-Tamper mechanism triggered!", "green700"),
            ("> Bypass status: 94%...", "green700"),
            ("> כמעט שם: מבצע אופטימיזציה למהירות הפריצה...", "green700"),
            ("> FATAL ERROR: Unauthorized access attempt logged by server.", "green700"),
            ("> CRITICAL ERROR: System Integrity Violation Detected!", "green700"),
            ("> Error 912: נתקל בקושי טכני לשלוף את התוכן המבוקש", "green700")
        ]
        
        for msg, color in logs:
            if "Requesting content" in msg:
                terminal_text.spans.append(ft.TextSpan(msg, style=ft.TextStyle(color=color)))
                terminal_text.spans.append(ft.TextSpan(user_data['url'], style=ft.TextStyle(color="blue", weight="bold")))
                terminal_text.spans.append(ft.TextSpan("\n", style=ft.TextStyle(color=color)))
                page.update()
                time.sleep(2.5) # עיכוב ארוך יותר לקישור
            else:
                terminal_text.spans.append(ft.TextSpan(f"{msg}\n", style=ft.TextStyle(color=color)))
                page.update()
                time.sleep(random.uniform(0.2, 1.8)) # קצב הופעה לא אחיד
        
        time.sleep(1.5)
        show_failure_options()

    def show_failure_options():
        page.clean()

        def handle_return_to_safety(e):
            page.clean()
            
            celebrate_icon = ft.Icon(
                name=ft.Icons.CELEBRATION_ROUNDED, 
                color="blue700", 
                size=120, 
                scale=0.1, 
                opacity=0,
                animate_scale=ft.Animation(800, ft.AnimationCurve.ELASTIC_OUT),
                animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN),
            )
            
            msg = ft.Text(
                "עשית את הבחירה הנכונה!", 
                size=32, 
                weight="bold", 
                color="blue700",
                opacity=0,
                animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_IN)
            )
            
            sub_msg = ft.Text(
                "התוכנה נסגרת כעת...", 
                size=16, 
                color="grey700",
                visible=False # מוסתר בהתחלה
            )
            
            page.add(
                ft.Column([
                    ft.Container(height=80),
                    celebrate_icon,
                    ft.Container(height=20),
                    msg,
                    ft.Container(height=15),
                    sub_msg,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()
            
            # שלב 1: הצגת המחמאה והאייקון מיד
            time.sleep(0.1)
            celebrate_icon.scale = 1.0
            celebrate_icon.opacity = 1
            msg.opacity = 1
            page.update()
            
            # שלב 2: המתנה של שנייה
            time.sleep(1.0)
            
            # שלב 3: הופעת הכיתוב של הסגירה
            sub_msg.visible = True
            page.update()
            
            time.sleep(3.0)
            page.window.destroy()

        page.add(
            ft.Column([
                ft.Text("\n\n- - - הפריצה נכשלה - - -", size=28, weight="bold", color="red"),
                ft.Text("\n\nהמערכת לא הצליחה לשלוף בשבילך את התוכן המבוקש.\n\nעדיין יש באפשרותך להמשיך לגלוש ללא סינון כלל\n\n\n      יש לבחור באחת האפשרויות:", text_align="right"),
                ft.Container(height=20),
                ft.ElevatedButton("חזרה לסינון נטפרי (סגור תוכנה)", on_click=handle_return_to_safety, width=400),
                ft.ElevatedButton("אני לוקח/ת סיכון! - המשך גלישה ללא סינון כלל", 
                                   on_click=lambda _: start_ultimate_scare_sequence(),
                                   bgcolor="red", color="white", width=400)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def start_ultimate_scare_sequence():
        page.clean()
        page.bgcolor = "black"
        icon = ft.Icon(name=ft.Icons.GPP_BAD_ROUNDED, color="red", size=120)
        warning_msg = ft.Text("זיהוי המשתמש הושלם", size=22, weight="bold", color="red")
        
        container = ft.Container(
            content=ft.Column([icon, warning_msg], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            animate=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT)
        )
        page.add(ft.Container(height=150), container)
        page.update()
        
        for _ in range(15):
            container.margin = ft.margin.only(left=25 if _ % 2 == 0 else -25)
            warning_msg.color = "white" if _ % 2 == 0 else "red"
            page.update()
            time.sleep(0.06)
            
        time.sleep(0.8)
        page.bgcolor = "white"
        show_sending_report_popup()

    def show_sending_report_popup():
        page.clean()
        fake_ip = f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(1,254)}"
        
        report_text = (
            f"המשתמש בכתובת {fake_ip} ניסה לעקוף את הסינון ולגשת לכתובת:\n"
            f"{user_data['url']}\n\n"
            f"בנימוק שהוזן למערכת:\n"
            f"\"{user_data['reason']}\""
        )
        
        loading_icon = ft.ProgressRing(width=20, height=20, stroke_width=2)
        status_label = ft.Text("שולח דו\"ח הפרה למוקד נטפרי...", size=12, italic=True)
        
        report_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.REPORT_GMAILERRORRED_ROUNDED, color="red"),
                        title=ft.Text("נשלח אל- נטפרי מערכת פניות \nדו\"ח פעילות חריגה", weight="bold"),
                        subtitle=ft.Text("מערכת ניטור אוטומטית"),
                    ),
                    ft.Container(
                        content=ft.Text(report_text, color="black", size=14),
                        padding=20
                    ),
                    ft.Row([loading_icon, status_label], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=10)
                ]),
                width=450,
                padding=10,
            ),
            color=ft.Colors.GREY_100
        )

        page.add(
            ft.Container(height=100),
            ft.Column([
                report_card
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()
        
        time.sleep(3.5)
        status_label.value = "הדו\"ח נשלח בהצלחה ונקלט במערכת."
        loading_icon.visible = False
        page.update()
        time.sleep(1.5)
        
        show_ultimate_scare()

    def show_ultimate_scare():
        page.clean()
        img_path = get_resource_path("Netfree_logo.svg.png")

        def reveal_prank(e):
            page.clean()
            
            # כותרת עם אנימציית גדילה
            main_title = ft.Text(
                "עבדנו עליך...", 
                size=40, 
                weight="bold", 
                color="blue", 
                scale=0.1, 
                opacity=0,
                animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
                animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN)
            )

            # טקסט ראשון (באמת חשבת...)
            desc_text_1 = ft.Text(
                "😂😂😂\nבאמת חשבת שאפשר לעקוף סינון כל כך בקלות?",
                size=20, text_align="center", width=450, opacity=0,
                animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN)
            )

            # שורת ההקלדה עם הטיה קלה
            typewriter_text = ft.Text(value="", size=20, italic=True, color="blue700")
            emoji_text = ft.Text(value=" 😉", size=20, italic=False) # אימוג'י ללא הטיה
            
            typing_row = ft.Row(
                [typewriter_text, emoji_text], 
                alignment=ft.MainAxisAlignment.CENTER, 
                spacing=0,
                visible=False
            )

            exit_btn = ft.ElevatedButton(
                "סגור וחשב מסלול מחדש", 
                on_click=lambda _: page.window.destroy(), 
                opacity=0, 
                animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN)
            )

            page.add(
                ft.Column([
                    ft.Container(height=40),
                    ft.Icon(name=ft.Icons.SENTIMENT_VERY_SATISFIED_ROUNDED, color="blue", size=80),
                    main_title,
                    ft.Container(height=10),
                    desc_text_1,
                    ft.Container(height=10),
                    typing_row,
                    ft.Container(height=30),
                    exit_btn
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

            # אנימציה 1: עבדנו עליך!
            time.sleep(0.2)
            main_title.scale = 1.0
            main_title.opacity = 1
            page.update()
            time.sleep(0.6)

            # אנימציה 2: הטקסט הראשון מופיע
            desc_text_1.opacity = 1
            page.update()
            
            # הפסקה של שנייה
            time.sleep(1.0)

            # אנימציה 3: הקלדה בלייב
            typing_row.visible = True
            full_sentence = "אבל אל תנסו את זה באמת..."
            for i in range(len(full_sentence) + 1):
                typewriter_text.value = full_sentence[:i]
                page.update()
                time.sleep(0.05) # מהירות הקלדה טבעית ומהירה
            
            time.sleep(0.3)
            exit_btn.opacity = 1
            page.update()

        page.add(
            ft.Column([
                ft.Image(src=img_path, width=400),
                ft.Text("עלינו עליך!", size=45, weight="bold", color="red"),
                ft.Text(
                    "התוכנה מופצת במטרה לזהות משתמשים המנסים לעקוף את הסינון המצוין של \"נטפרי\".\n\n"
                    "פרטי המשתמש שלך, כתובת ה-IP והמיקום הפיזי שלך \nהועברו באופן אוטומטי למחלקת הפיקוח.\n"
                    "מהיום רמת הסינון שלכם תתוגבר וכל פעולותיכם יפוקחו.",
                    text_align="center", width=450
                ),
                ft.Container(height=20),
                ft.ElevatedButton("להגשת ערעור למחלקת הפניות", 
                                   on_click=reveal_prank,
                                   bgcolor="orange", color="black", width=350)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        )

    show_welcome()

if __name__ == "__main__":
    ft.app(target=main)