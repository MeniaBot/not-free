/* שאלון הכשירות. */
NF.screens.survey = (function () {
  const { render, $, sleep, toast, esc } = NF.util;
  const S = NF.scoring;

  const SEMINAR_STATUS = "תלמידת סמינר";
  const TORAH_GOAL = "לימוד תורה";
  const SEMINAR_VERDICT = "כל המלמד בתו תורה כאילו מלמדה תיפלות";

  const DECLARATION =
    "אני מצהיר כי הגישה לתכנים הינה לצורך לימודי/תורני בלבד\nואינה סותרת את דעת רבותיי.";

  function select(id, label, table) {
    // חובה לברוח — למשל 'תלמיד ת"ת' ו-'צו"ל' מכילים מרכאות שישברו את ה-value
    const options = Object.keys(table)
      .map((key) => '<option value="' + esc(key) + '">' + esc(key) + "</option>")
      .join("");
    return (
      '<div class="field"><label for="' +
      id +
      '">' +
      label +
      "</label>" +
      '<select id="' +
      id +
      '"><option value="" selected></option>' +
      options +
      "</select></div>"
    );
  }

  function detail(id, label) {
    return (
      '<div class="field hidden" id="' +
      id +
      '-wrap"><label for="' +
      id +
      '">' +
      label +
      '</label><input id="' +
      id +
      '" type="text" /></div>'
    );
  }

  /** המתנה מבוימת לפני הפסילה של תלמידת סמינר שגולשת ללימוד תורה. */
  async function seminarStall() {
    render(
      "<h3>מנתח שילוב סטטוס וצורך...</h3>" +
        '<div class="bar danger" style="margin-top:14px"><i id="fill"></i></div>'
    );
    // מד ההתקדמות רץ לאורך שלוש השניות
    const fill = $("#fill");
    fill.style.transition = "width 3s linear";
    requestAnimationFrame(() => (fill.style.width = "100%"));
    await sleep(3);
  }

  async function show() {
    render(
      "<h3>הבוט שלנו רוצה לדעת עליך יותר!</h3>" +
        '<div class="stack" style="width:100%;margin-top:6px">' +
        select("status", "סטטוס", S.STATUS) +
        detail("status-extra", "נא לפרט סטטוס...") +
        select("identity", "מגדיר/ה את עצמך", S.IDENTITY) +
        select("goal", "גולש/ת לצורך", S.GOAL) +
        detail("goal-extra", "נא לפרט צורך...") +
        select("eda", "עדה", S.EDA) +
        '<label class="check" id="declare-row"><input type="checkbox" id="declare" />' +
        '<span class="pre">' +
        DECLARATION +
        "</span></label>" +
        "</div>" +
        '<button class="btn" id="submit" style="min-width:260px;margin-top:10px">שלח לאבחון רובוטי</button>'
    );

    const status = $("#status");
    const identity = $("#identity");
    const goal = $("#goal");
    const eda = $("#eda");
    const statusExtra = $("#status-extra");
    const goalExtra = $("#goal-extra");
    const declare = $("#declare");

    function toggleExtras() {
      $("#status-extra-wrap").classList.toggle("hidden", status.value !== S.OTHER);
      $("#goal-extra-wrap").classList.toggle("hidden", goal.value !== S.OTHER);
    }
    status.onchange = toggleExtras;
    goal.onchange = toggleExtras;

    $("#submit").onclick = async () => {
      if (!status.value || !goal.value || !eda.value || !identity.value) {
        toast("חובה למלא את כל השדות בשאלון כדי להמשיך!");
        return;
      }

      if (!declare.checked) {
        toast("עליך לאשר את ההצהרה כדי להמשיך!");
        $("#declare-row").scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }

      if (
        (status.value === S.OTHER && !statusExtra.value) ||
        (goal.value === S.OTHER && !goalExtra.value)
      ) {
        toast('בבחירה ב"אחר" - חובה לפרט!');
        return;
      }

      if (status.value === SEMINAR_STATUS && goal.value === TORAH_GOAL) {
        await seminarStall();
        await NF.screens.rejection.show(SEMINAR_VERDICT);
        return;
      }

      NF.state.status = status.value;
      NF.state.identity = identity.value;
      await NF.screens.analysis.show(status.value, identity.value, goal.value, eda.value);
    };
  }

  return { show };
})();
