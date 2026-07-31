/* עזרים משותפים: ציור מסך, השהיות, טוסט, וגשר לפייתון. */
window.NF = window.NF || {};

NF.util = (function () {
  const root = () => document.getElementById("app");

  const sleep = (seconds) => new Promise((r) => setTimeout(r, seconds * 1000));

  /** מצייר מסך חדש במקום הקודם ומחזיר את האלמנט שלו. */
  function render(html, options) {
    const dark = options && options.dark;
    root().innerHTML = '<div class="screen' + (dark ? " dark" : "") + '">' + html + "</div>";
    root().scrollTop = 0;
    return root().firstElementChild;
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
    typewriter,
    closeApp,
    openUrl,
    readClipboard,
  };
})();

/** נתוני המשתמש שנאספים לאורך הזרימה. */
NF.state = { url: "", reason: "", status: "", identity: "" };

NF.screens = {};
