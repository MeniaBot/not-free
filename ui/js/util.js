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

  return { root, sleep, render, $, $$, esc, toast, typewriter, closeApp, readClipboard };
})();

/** נתוני המשתמש שנאספים לאורך הזרימה. */
NF.state = { url: "", reason: "", status: "", identity: "" };

NF.screens = {};
