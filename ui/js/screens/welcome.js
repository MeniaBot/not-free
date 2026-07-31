/* מסך הפתיחה. */
NF.screens.welcome = (function () {
  const { render, $ } = NF.util;
  const { icon } = NF.icons;

  const AUTHOR_URL =
    "https://mitmachim.top/user/" +
    "%D7%91%D7%A0%D7%99%D7%9E%D7%99%D7%9F-%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D";

  const PITCH =
    'בס"ד עלה בידינו לפתח תוכנה עוצמתית ופשוטה לשימוש \n' +
    'המסוגלת לאפשר גישה לתכנים שנחסמו ע"י נטפרי.\n\n' +
    "כלי מתקדם מבוסס AI יסקור את בקשתך בכפוף לקריטריונים מחמירים.";

  const WARNING_LINE = "שימו לב! אין להעביר את התוכנה לאף גורם המקושר לנטפרי!!!";

  async function show() {
    render(
      '<div class="badge-circle pop-in">' +
        icon("lockOpen", 44) +
        "</div>" +
        '<h1 class="danger rise-in">בשורה למשתמשי נטפרי!</h1>' +
        '<p class="muted italic rise-in">הסוף לרודנות - פתיחת תכנים שנחסמו ללא סיבה</p>' +
        '<div class="card right rise-in">' +
        '<p class="pre">' +
        PITCH +
        "</p>" +
        '<div class="strip warning" style="margin-top:16px">' +
        icon("warning", 18) +
        "<span>" +
        WARNING_LINE +
        "</span>" +
        "</div>" +
        "</div>" +
        '<button class="btn success rise-in" id="agree" style="min-width:260px;margin-top:6px">אני מסכים - המשך</button>' +
        '<p class="caption credit rise-in"><span>©️</span><span>נוצר על ידי</span>' +
        '<span class="link" id="credit">@בנימין-מחשבים</span><span>באתר מתמחים טופ</span></p>'
    );

    $("#agree").onclick = () => NF.screens.survey.show();
    $("#credit").onclick = () => NF.util.openUrl(AUTHOR_URL);
  }

  return { show };
})();
