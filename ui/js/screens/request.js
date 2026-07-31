/* סריקת חומות האש וטופס הבקשה. */
NF.screens.request = (function () {
  const { render, $, sleep, toast, readClipboard } = NF.util;
  const { icon, radar } = NF.icons;

  const APPROVED_HEADER = "אישור המערכת התקבל!";

  const LITVAK_STATUS = "אברך";
  const LITVAK_IDENTITY = "ליטאי קלאס";
  const LITVAK_MIN_WORDS = 20;

  const REASON_HINT =
    "יש לפרט בהרחבה לצורך ניתוח מעמיק של האלגוריתם. " +
    "תיאור קצר מדי עלול להוביל לדחיית הבקשה.";

  const approvedBadge =
    '<div class="strip success">' + icon("verified", 20) + "<span>" + APPROVED_HEADER + "</span></div>";

  async function flashScan() {
    render(
      approvedBadge +
        '<div style="margin-top:48px">' +
        radar() +
        "</div>" +
        '<h3 class="scan-blink" style="margin-top:18px">מתכונן לפריצה - סורק חומות אש</h3>'
    );
    await sleep(2.8);
    await show();
  }

  async function show() {
    render(
      approvedBadge +
        '<div class="field" style="margin-top:10px">' +
        '<label for="url">כאן מדביקים קישור לתוכן החסום</label>' +
        '<div class="row" style="gap:4px">' +
        '<input id="url" type="text" placeholder="ניתן להשתמש ב-Ctrl+V להדבקה" />' +
        '<button class="icon-btn" id="paste" title="נסה להדביק מהלוח">' +
        icon("paste", 22) +
        "</button>" +
        "</div></div>" +
        '<div class="field w-text" style="max-width:430px">' +
        '<label for="reason">נא לנמק מדוע התוכן צריך להיפתח (לניתוח ה-AI)</label>' +
        '<textarea id="reason" rows="8" maxlength="1000" placeholder="' +
        REASON_HINT +
        '"></textarea></div>' +
        '<button class="btn warning wide" id="go" style="margin-top:6px">בצע פריצה באמצעות בינה מלאכותית</button>'
    );

    const url = $("#url");
    const reason = $("#reason");
    url.focus();

    $("#paste").onclick = async () => {
      const result = await readClipboard();
      if (!result.ok) {
        toast("חסימת מערכת: השתמש ב-Ctrl+V להדבקה ידנית");
        return;
      }
      if (result.text) {
        url.value = result.text;
      } else {
        toast("הלוח ריק. אין מה להדביק");
      }
      url.focus();
    };

    $("#go").onclick = async () => {
      if (!url.value || !reason.value) {
        toast("חובה למלא את הקישור והסיבה כדי להמשיך!");
        return;
      }

      // מאברך ליטאי מצפים לפלפול
      if (
        NF.state.status === LITVAK_STATUS &&
        NF.state.identity === LITVAK_IDENTITY &&
        reason.value.split(/\s+/).filter(Boolean).length < LITVAK_MIN_WORDS
      ) {
        toast("מאברך ליטאי מצופה לכתוב פלפול למדני מנומק היטב! נסח שוב...");
        return;
      }

      NF.state.url = url.value;
      NF.state.reason = reason.value;
      await NF.screens.hacking.show();
    };
  }

  return { show, flashScan };
})();
