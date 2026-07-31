/* החשיפה — "עלינו עליך" ואחריה "עבדנו עליך". */
NF.screens.exposure = (function () {
  const { render, $, sleep, esc, typewriter, closeApp } = NF.util;
  const { icon } = NF.icons;

  const EXPOSURE_BODY =
    'התוכנה מופצת במטרה לזהות משתמשים המנסים לעקוף את הסינון המצוין של "נטפרי".\n\n' +
    "פרטי המשתמש שלך, כתובת ה-IP והמיקום הפיזי שלך \nהועברו באופן אוטומטי למחלקת הפיקוח.\n" +
    "מהיום רמת הסינון שלכם תתוגבר וכל פעולותיכם יפוקחו.";

  const TYPED_LINE = "אבל אל תנסו את זה באמת...";

  const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

  /** רעידת המסך שפותחת את רצף החשיפה. */
  async function show() {
    render(
      '<div class="shake" style="display:flex;flex-direction:column;align-items:center;gap:8px">' +
        '<div class="danger">' +
        icon("shieldBad", 120) +
        "</div>" +
        '<h3 class="danger" id="warn">זיהוי המשתמש הושלם</h3>' +
        "</div>",
      { dark: true }
    );

    // הכיתוב מהבהב בקצב הרעידה
    const warn = $("#warn");
    for (let step = 0; step < 15; step++) {
      warn.style.color = step % 2 === 0 ? "#fff" : "var(--danger)";
      await sleep(0.06);
    }

    await sleep(0.8);
    await report();
  }

  /** הדו"ח המזויף לנטפרי — עם הנימוק שהמשתמש עצמו כתב. */
  async function report() {
    const fakeIp = "172." + rand(16, 31) + "." + rand(0, 255) + "." + rand(1, 254);
    // הכתובת מבודדת כ-LTR — אחרת היא נשברת בסדר לא צפוי בתוך פסקה עברית
    const reportText =
      "המשתמש בכתובת " +
      fakeIp +
      " ניסה לעקוף את הסינון ולגשת לכתובת:\n" +
      '<span class="ltr">' +
      esc(NF.state.url) +
      "</span>\n" +
      "בנימוק שהוזן למערכת:\n" +
      '"' +
      esc(NF.state.reason) +
      '"';

    render(
      '<div class="card right rise-in">' +
        '<div class="report-head">' +
        '<span class="danger">' +
        icon("report", 32) +
        "</span>" +
        '<div><div class="t">נשלח אל- נטפרי מערכת פניות \nדו"ח פעילות חריגה</div>' +
        '<div class="caption">מערכת ניטור אוטומטית</div></div>' +
        "</div>" +
        '<hr class="sep" />' +
        '<div class="report-body">' +
        reportText +
        "</div>" +
        '<div class="row" style="margin-top:22px">' +
        '<span class="spinner sm" id="ring"></span>' +
        '<span class="caption italic" id="status">שולח דו"ח הפרה למוקד נטפרי...</span>' +
        "</div></div>"
    );

    await sleep(3.5);
    $("#ring").style.display = "none";
    const status = $("#status");
    status.textContent = 'הדו"ח נשלח בהצלחה ונקלט במערכת.';
    status.classList.remove("caption");
    status.classList.add("success", "caption");
    await sleep(1.5);
    await exposure();
  }

  async function exposure() {
    render(
      '<img src="assets/netfree-logo.png" alt="" style="width:330px;max-width:100%" />' +
        '<h1 class="danger">עלינו עליך!</h1>' +
        '<p class="pre w-text">' +
        EXPOSURE_BODY +
        "</p>" +
        '<button class="btn warning wide" id="appeal" style="margin-top:10px">להגשת ערעור למחלקת הפניות</button>'
    );
    $("#appeal").onclick = () => reveal();
  }

  async function reveal() {
    render(
      '<div class="brand">' +
        icon("smiley", 80) +
        "</div>" +
        '<h1 class="brand pop-in">עבדנו עליך...</h1>' +
        '<p class="w-text pre" id="punch" style="font-size:19px;opacity:0">😂😂😂\nבאמת חשבת שאפשר לעקוף סינון כל כך בקלות?</p>' +
        '<div class="row" style="gap:0;visibility:hidden" id="typing">' +
        '<span class="italic" id="typed" style="font-size:19px;color:var(--brand-soft)"></span>' +
        '<span style="font-size:19px"> 😉</span>' +
        "</div>" +
        '<button class="btn" id="exit" style="min-width:280px;margin-top:16px;opacity:0;transition:opacity .5s ease-in">סגור וחשב מסלול מחדש</button>'
    );

    const punch = $("#punch");
    punch.style.transition = "opacity .5s ease-in";

    await sleep(0.8);
    punch.style.opacity = "1";
    await sleep(1);

    $("#typing").style.visibility = "visible";
    await typewriter($("#typed"), TYPED_LINE, 0.05);

    await sleep(0.3);
    const exit = $("#exit");
    exit.style.opacity = "1";
    exit.onclick = () => closeApp();
  }

  return { show };
})();
