/* רצף ה"פריצה" — מסך הניתוח ואחריו הטרמינל. */
NF.screens.hacking = (function () {
  const { render, $, sleep, esc } = NF.util;

  const PROMPT = "> ";
  const URL_LINE = "> Requesting content: ";

  /** שורת לוג אחת.
   *  ה-">" נשאר מחוץ לבידוד כדי שיישאר בשמאל כמו בטרמינל אמיתי, והתוכן
   *  נעטף ב-bdi כדי שעברית מעורבת באנגלית תקרא בסדר הנכון. */
  function lineHtml(text, tailHtml) {
    const rest = text.startsWith(PROMPT) ? text.slice(PROMPT.length) : text;
    return (
      '<span class="ln"><span class="p">&gt; </span><bdi>' +
      esc(rest) +
      (tailHtml || "") +
      "</bdi>\n</span>"
    );
  }

  const LOG_LINES = [
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
  ];

  async function analyzing() {
    render(
      '<div class="spinner"></div>' +
        '<h3 class="brand" id="status" style="margin-top:22px">מנוע AI מנתח את בקשת הפריצה...</h3>' +
        '<div class="bar" style="margin-top:12px"><i id="fill"></i></div>'
    );

    const fill = $("#fill");
    fill.style.transition = "width 5s linear";
    requestAnimationFrame(() => (fill.style.width = "100%"));

    await sleep(3);
    const status = $("#status");
    status.textContent = "ניתוח הושלם. הטיעונים אושרו. מתחבר לשרתי הליבה...";
    status.classList.remove("brand");
    status.classList.add("success");
    await sleep(2);
  }

  async function terminal() {
    render(
      '<h3 style="font-size:17px">הפריצה מתבצעת כעת - יש להמתין לסיום</h3>' +
        '<div class="terminal" style="margin-top:12px">' +
        '<div class="chrome">' +
        '<div class="dots"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></div>' +
        '<span class="title">netfree-slayer — bypass</span>' +
        '<span style="width:44px"></span>' +
        "</div>" +
        '<div class="out" id="out"></div>' +
        "</div>"
    );

    const out = $("#out");
    for (const line of LOG_LINES) {
      if (line === URL_LINE) {
        const url = '<span class="url">' + esc(NF.state.url) + "</span>";
        out.insertAdjacentHTML("beforeend", lineHtml(line, url));
        out.scrollTop = out.scrollHeight;
        await sleep(2.5); // עיכוב ארוך יותר לקישור
      } else {
        out.insertAdjacentHTML("beforeend", lineHtml(line));
        out.scrollTop = out.scrollHeight;
        await sleep(0.2 + Math.random() * 1.6); // קצב הופעה לא אחיד
      }
    }
  }

  async function show() {
    await analyzing();
    await terminal();
    await sleep(1.5);
    await NF.screens.outcome.show();
  }

  return { show };
})();
