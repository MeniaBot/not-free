/* עזרים משותפים: ציור מסך, השהיות, טוסט, וגשר לפייתון. */
window.NF = window.NF || {};

NF.util = (function () {
  const root = () => document.getElementById("app");

  const sleep = (seconds) => new Promise((r) => setTimeout(r, seconds * 1000));

  /** מצייר מסך חדש במקום הקודם ומחזיר את האלמנט שלו.
   *  היוצא לא נמחק מיד — הוא יוצא מהזרימה ודוהה תוך כדי שהנכנס עולה, אחרת
   *  כל מעבר הוא חיתוך יבש. שים לב שבמהלך המעבר יש שני `.screen` ב-DOM,
   *  ולכן יש להשתמש בערך המוחזר ולא ב-$(".screen"). */
  function render(html, options) {
    const app = root();
    const dark = options && options.dark;
    const leaving = app.firstElementChild;

    if (leaving) {
      leaving.classList.add("leaving");
      // היוצא עדיין ב-DOM לרגע. בלי זה $("#fill") היה עלול לתפוס את שלו,
      // כי הוא מקדים את הנכנס בסדר המסמך.
      $$("[id]", leaving).forEach((node) => node.removeAttribute("id"));
      // .leaving חוסם עכבר, אבל לא מקלדת: כפתור שנשארה עליו הפוקוס עדיין
      // נענה ל-Enter, ולחיצה שנייה הייתה מפעילה את המסך הבא פעם נוספת.
      $$("button, select, input, textarea", leaving).forEach((node) => (node.disabled = true));
      // animationend מבעבע, ואנימציה של אלמנט־בן שמסתיימת באותו רגע הייתה
      // מוחקת את המסך לפני שהספיק לדהות. מסננים לפי היעד.
      leaving.addEventListener("animationend", function done(e) {
        if (e.target !== leaving) return;
        leaving.removeEventListener("animationend", done);
        leaving.remove();
      });
    }

    const el = document.createElement("div");
    el.className = "screen" + (dark ? " dark" : "");
    el.innerHTML = html;
    app.appendChild(el);
    app.scrollTop = 0;
    return el;
  }

  const $ = (selector, scope) => (scope || document).querySelector(selector);
  const $$ = (selector, scope) =>
    Array.prototype.slice.call((scope || document).querySelectorAll(selector));

  /** בריחה מ-HTML — טקסט שהמשתמש הזין לא אמור לשבור את הדף. */
  function esc(value) {
    return String(value === null || value === undefined ? "" : value).replace(
      /[&<>"']/g,
      (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );
  }

  let toastTimer = null;
  function toast(message) {
    const el = document.getElementById("toast");
    el.textContent = message;
    el.classList.add("on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove("on"), 4000);
  }

  /** חושף אלמנט שהמתין (.pending) — אותה דהייה לכל החשיפות בתוכנה. */
  function appear(el) {
    el.classList.remove("pending");
    el.classList.add("fade-in");
  }

  /** ממתין לסיום האנימציה של האלמנט עצמו.
   *  עדיף על sleep עם המספר שכתוב ב-CSS: אין שתי גרסאות של אותו תזמון. */
  function animationEnd(el) {
    return new Promise((resolve) => {
      el.addEventListener("animationend", function done(e) {
        if (e.target !== el) return; // animationend של אלמנט-בן מבעבע לכאן
        el.removeEventListener("animationend", done);
        resolve();
      });
    });
  }

  /** הקלדה תו-אחר-תו. */
  async function typewriter(el, text, secondsPerChar) {
    el.classList.add("caret");
    for (let i = 0; i <= text.length; i++) {
      el.textContent = text.slice(0, i);
      await sleep(secondsPerChar);
    }
    el.classList.remove("caret");
  }

  const api = () => (window.pywebview ? window.pywebview.api : null);

  async function closeApp() {
    const bridge = api();
    if (bridge) await bridge.close();
  }

  /** פותח קישור בדפדפן המערכת. window.open היה פותח חלון WebView בתוך התוכנה. */
  async function openUrl(url) {
    const bridge = api();
    if (bridge) {
      await bridge.open_url(url);
    } else {
      window.open(url, "_blank");
    }
  }

  /** {version, url} כשגיטהאב מדווח על גרסה חדשה, אחרת null.
   *  הבדיקה רצה בפייתון מאז ההפעלה; כאן רק שואלים אם כבר יש תשובה, ולכן
   *  צריך לשאול כמה פעמים. בדפדפן בלי המארח — תמיד null. */
  async function checkUpdate() {
    const bridge = api();
    if (!bridge) return null;
    try {
      return (await bridge.update_info()) || null;
    } catch (e) {
      return null;
    }
  }

  /** מחזיר {ok, text}. ok=false כשהלוח לא נגיש. */
  async function readClipboard() {
    const bridge = api();
    if (!bridge) return { ok: false, text: "" };
    try {
      return await bridge.read_clipboard();
    } catch (e) {
      return { ok: false, text: "" };
    }
  }

  /* המנוע הוא דפדפן, אבל למשתמש זו תוכנה. חוסמים את מה שמסגיר את זה. */
  function lockDownBrowserChrome() {
    document.addEventListener("contextmenu", (e) => e.preventDefault());

    // Ctrl+V/C/X/A נשארים פתוחים — בלעדיהם אי אפשר להדביק את הקישור
    const BLOCKED_WITH_CTRL = ["r", "p", "f", "g", "s", "u", "j", "o", "+", "-", "=", "0"];
    document.addEventListener("keydown", (e) => {
      const key = e.key.toLowerCase();
      const isFunctionKey = ["f3", "f5", "f7", "f12"].includes(key);
      const isBlockedCombo = (e.ctrlKey || e.metaKey) && BLOCKED_WITH_CTRL.includes(key);
      if (isFunctionKey || isBlockedCombo) e.preventDefault();
    });

    // Ctrl+גלגלת מזוויג את הממשק, והחלון לא ניתן לשינוי גודל
    document.addEventListener(
      "wheel",
      (e) => {
        if (e.ctrlKey) e.preventDefault();
      },
      { passive: false }
    );

    document.addEventListener("dragstart", (e) => e.preventDefault());
  }

  lockDownBrowserChrome();

  return {
    root,
    sleep,
    render,
    $,
    $$,
    esc,
    toast,
    appear,
    animationEnd,
    typewriter,
    closeApp,
    openUrl,
    checkUpdate,
    readClipboard,
  };
})();

/** נתוני המשתמש שנאספים לאורך הזרימה. */
NF.state = { url: "", reason: "", status: "", identity: "" };

NF.screens = {};
