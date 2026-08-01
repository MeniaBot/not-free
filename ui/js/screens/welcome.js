/* מסך הפתיחה. */
NF.screens.welcome = (function () {
  const { render, $, sleep, esc, appear, checkUpdate, openUrl } = NF.util;
  const { icon } = NF.icons;

  const AUTHOR_URL = "https://github.com/BeniaBot";

  const PITCH =
    'בס"ד עלה בידינו לפתח תוכנה עוצמתית ופשוטה לשימוש \n' +
    'המסוגלת לאפשר גישה לתכנים שנחסמו ע"י נטפרי.\n\n' +
    "כלי מתקדם מבוסס AI יסקור את בקשתך בכפוף לקריטריונים מחמירים.";

  const WARNING_LINE = "שימו לב! אין להעביר את התוכנה לאף גורם המקושר לנטפרי!!!";

  // הבדיקה בפייתון עשויה לרוץ אחרי שהמסך כבר עלה, ולכן שואלים כמה פעמים
  const UPDATE_TRIES = 12;
  const UPDATE_GAP = 0.7;

  /** מחכה שהבדיקה ברקע תסתיים, ואם יש גרסה חדשה — מציג את הפס.
   *  לא ממתין לכלום: המסך פעיל כרגיל גם אם אין תשובה לעולם. */
  async function watchForUpdate(slot) {
    for (let i = 0; i < UPDATE_TRIES; i++) {
      const info = await checkUpdate();
      if (info) {
        slot.innerHTML =
          '<div class="strip update pending" id="update-strip">' +
          "<span>גרסה חדשה זמינה — " +
          esc(info.version) +
          "</span>" +
          '<span class="link" id="update-link">להורדה</span>' +
          "</div>";
        appear($("#update-strip"));
        $("#update-link").onclick = () => openUrl(info.url);
        return;
      }
      await sleep(UPDATE_GAP);
    }
  }

  async function show() {
    render(
      '<div class="badge-circle pop-in">' +
        icon("lockOpen", 52) +
        "</div>" +
        '<h1 class="danger rise-in">בשורה למשתמשי נטפרי!</h1>' +
        '<p class="muted italic rise-in">הסוף לרודנות - פתיחת תכנים שנחסמו ללא סיבה</p>' +
        // בלי כרטיס וכלי כרצועה כתומה. הטקסט נושם על הרקע, והאזהרה מודגשת
        // בצבע ובמשקל במקום בקופסה משלה.
        '<div class="body-text pre rise-in">' +
        PITCH +
        "</div>" +
        '<p class="warn-line rise-in">' +
        WARNING_LINE +
        "</p>" +
        '<button class="btn success rise-in" id="agree" style="min-width:260px;margin-top:6px">אני מסכים - המשך</button>' +
        '<p class="caption credit rise-in"><span>©️</span><span>פותח על ידי</span>' +
        '<span class="link" id="credit">@בני-הבוט</span></p>' +
        '<p class="caption terms rise-in">התוכנה מסופקת כמות שהיא, ללא אחריות מכל סוג</p>' +
        '<div id="update-slot"></div>'
    );

    $("#agree").onclick = () => NF.screens.survey.show();
    $("#credit").onclick = () => openUrl(AUTHOR_URL);
    watchForUpdate($("#update-slot"));
  }

  return { show };
})();
