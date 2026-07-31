/* מסך הדחייה, ומסך השריפה שאחריו. */
NF.screens.rejection = (function () {
  const { render, $, sleep, closeApp } = NF.util;
  const { icon } = NF.icons;

  const GENERIC_VERDICT =
    "ניתוח ה-AI הסתיים:\n\nהמשתמש אינו עומד בקריטריונים הרוחניים.\n\n" +
    "המערכת זיהתה רמת סיכון גבוהה עבור הפרופיל שהוזן.\n\n" +
    "הגישה לכלי הפריצה נחסמה מטעמי הגנה.";

  const BURNING_LINE = "ישרפו דברי תורה ואל ימסרו לנשים!!";
  const BURNING_SOURCE = "(ירושלמי סוטה, פרק ג' הלכה ד')";

  async function show(customMsg) {
    render(
      '<div class="danger-deep pop-in">' +
        icon("shieldBad", 80) +
        "</div>" +
        '<h2 class="danger-deep pop-in">בקשתך נדחתה!</h2>' +
        '<div id="verdict" style="width:100%;display:flex;flex-direction:column;align-items:center;gap:var(--gap-lg)"></div>'
    );

    // המתנה לסיום אנימציית הכניסה לפני הוספת שאר הטקסט
    await sleep(0.8);

    const slot = $("#verdict");
    slot.style.marginTop = "10px";

    if (customMsg) {
      slot.innerHTML =
        '<div class="card fade-in">' +
        '<p class="serif" style="font-size:26px;font-weight:700;line-height:1.4">"' +
        customMsg +
        '"</p>' +
        '<p class="caption" style="margin-top:8px">(סוטה ג\', ד\')</p>' +
        "</div>" +
        '<button class="btn danger fade-in" id="anyway" style="min-width:260px">אולי בכל זאת?</button>';
      $("#anyway").onclick = () => burning();
    } else {
      slot.innerHTML =
        '<div class="card fade-in"><p class="pre">' +
        GENERIC_VERDICT +
        "</p></div>" +
        '<button class="btn neutral fade-in" id="quit" style="min-width:260px">יציאה מהתוכנה</button>';
      $("#quit").onclick = () => closeApp();
    }
  }

  async function burning() {
    render(
      '<div id="fire" style="color:var(--fire)">' +
        icon("flame", 100) +
        "</div>" +
        '<h1 id="burn" style="color:var(--fire);max-width:460px;margin-top:20px">' +
        BURNING_LINE +
        "</h1>" +
        '<p id="src" style="color:#000;font-weight:700;font-size:15px;opacity:0">' +
        BURNING_SOURCE +
        "</p>",
      { dark: true }
    );

    const screen = $(".screen");
    const fire = $("#fire");
    const burn = $("#burn");
    const src = $("#src");

    fire.style.opacity = "0";
    burn.style.opacity = "0";
    fire.style.transition = "opacity .8s ease-in";
    burn.style.transition = "opacity 1s ease-in";
    src.style.transition = "opacity 1.5s ease-in";

    await sleep(0.5);
    fire.style.opacity = "1";
    burn.style.opacity = "1";
    await sleep(0.5);
    src.style.opacity = "1";

    // אפקט "להבות" — הבהוב מהיר של הרקע, האש והכיתוב
    screen.classList.add("burning");
    fire.classList.add("burning-icon");
    burn.classList.add("burning-text");
    await sleep(2.4);

    await sleep(3);
    await closeApp();
  }

  return { show, burning };
})();
