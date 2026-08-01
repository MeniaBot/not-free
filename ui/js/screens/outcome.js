/* מסך הכישלון והבחירה שאחריו. */
NF.screens.outcome = (function () {
  const { render, $, sleep, closeApp, appear } = NF.util;
  const { icon } = NF.icons;

  const FAILURE_BODY =
    "המערכת לא הצליחה לשלוף בשבילך את התוכן המבוקש.\n\n" +
    "עדיין יש באפשרותך להמשיך לגלוש ללא סינון כלל.";

  async function show() {
    render(
      '<div class="danger pop-in">' +
        icon("errorCircle", 64) +
        "</div>" +
        '<h2 class="danger">- - - הפריצה נכשלה - - -</h2>' +
        '<div class="body-text pre">' +
        FAILURE_BODY +
        "</div>" +
        '<p class="caption" style="margin-top:8px">יש לבחור באחת האפשרויות:</p>' +
        '<button class="btn neutral wide" id="safe">חזרה לסינון נטפרי (סגור תוכנה)</button>' +
        '<button class="btn danger wide" id="risk">אני לוקח/ת סיכון! - המשך גלישה ללא סינון כלל</button>'
    );

    $("#safe").onclick = () => praise();
    $("#risk").onclick = () => NF.screens.exposure.show();
  }

  /** מי שבחר לחזור לסינון — מקבל מחמאה והתוכנה נסגרת. */
  async function praise() {
    render(
      '<div class="brand pop-elastic">' +
        icon("celebration", 120) +
        "</div>" +
        '<h1 class="brand fade-in" style="margin-top:20px">עשית את הבחירה הנכונה!</h1>' +
        // היה visibility:hidden שקפץ ל-visible בלי מעבר, ליד כותרת שדוהה
        '<p class="muted pending" id="sub">התוכנה נסגרת כעת...</p>'
    );

    await sleep(1.1);
    appear($("#sub"));
    await sleep(3);
    await closeApp();
  }

  return { show };
})();
