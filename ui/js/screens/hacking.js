/* רצף ה"פריצה" — מסך הניתוח ואחריו הטרמינל. */
NF.screens.hacking = (function () {
  const { render, $, sleep, esc } = NF.util;

  const PROMPT = "> ";
  const URL_LINE = "> Requesting content: ";

  /** שורת לוג אחת.
   *  ה-">" נשאר מחוץ לבידוד כדי שיישאר בשמאל כמו בטרמינל אמיתי, והתוכן
   *  נעטף ב-bdi כדי שעברית מעורבת באנגלית תקרא בסדר הנכון. */
  /** חותמת זמן אמיתית, כמו בלוג של תוכנה שרצה עכשיו. */
  function stamp() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    return "[" + pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds()) + "]";
  }

  function lineHtml(text, tailHtml) {
    const rest = text.startsWith(PROMPT) ? text.slice(PROMPT.length) : text;
    return (
      '<span class="ln"><span class="ts">' +
      stamp() +
      '</span> <span class="p">&gt;</span> <bdi>' +
      esc(rest) +
      (tailHtml || "") +
      "</bdi>\n</span>"
    );
  }

  const hex = () =>
    Array.from({ length: 4 }, () =>
      Math.floor(Math.random() * 256).toString(16).toUpperCase().padStart(2, "0")
    ).join(" ");

  /** שורת רעש טכני. אין לה משמעות — היא שם כדי שהמסך ייראה עסוק. */
  function noiseHtml() {
    return (
      '<span class="ln noise">    MEM_ADDR: 0x' +
      (Math.floor(Math.random() * 9000) + 1000) +
      " | DATA: " +
      hex() +
      "\n</span>"
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

  const MAX_NODES = 260; // לוג רץ, לא היסטוריה. בלי זה ה-DOM תופח לאורך הרצף.

  function push(out, html) {
    out.insertAdjacentHTML("beforeend", html);
    while (out.childElementCount > MAX_NODES) out.firstElementChild.remove();
    out.scrollTop = out.scrollHeight;
  }

  /** ממלא את ההפסקה שאחרי שורה אמיתית בשורות רעש, במקום באוויר מת.
   *  ה-n שורות נפרשות על פני כל אורך ההפסקה, ולכן משך הרצף לא משתנה. */
  async function fillGap(out, seconds, lines) {
    const n = Math.max(1, lines);
    const step = seconds / n;
    for (let i = 0; i < n; i++) {
      push(out, noiseHtml());
      await sleep(step);
    }
  }

  async function terminal() {
    render(
      '<h3 style="font-size:17px">הפריצה מתבצעת כעת - יש להמתין לסיום</h3>' +
        '<div class="terminal" style="margin-top:12px"><div class="out" id="out"></div></div>'
    );

    const out = $("#out");
    for (const line of LOG_LINES) {
      if (line === URL_LINE) {
        const url = '<span class="url">' + esc(NF.state.url) + "</span>";
        push(out, lineHtml(line, url));
        // הקישור הוא רגע השיא — רעש דליל, כדי שיישאר קריא
        await fillGap(out, 2.5, 6);
      } else {
        push(out, lineHtml(line));
        // אותה הפסקה של 0.2–1.8 שנ' כמו קודם, רק שעכשיו היא מלאה
        await fillGap(out, 0.2 + Math.random() * 1.6, 8 + Math.floor(Math.random() * 7));
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
