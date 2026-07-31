/* אייקוני SVG מוטמעים — בלי גופן אייקונים ובלי קובץ חיצוני. */
NF.icons = (function () {
  const PATHS = {
    lockOpen: '<rect x="3" y="11" width="14" height="10" rx="2.5"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>',
    warning: '<path d="M12 3 2.5 20h19L12 3Z"/><path d="M12 9.5v4.5"/><path d="M12 17.4v.01"/>',
    shieldBad:
      '<path d="M12 2.5 20 6v5.6c0 4.9-3.3 8.8-8 10.4-4.7-1.6-8-5.5-8-10.4V6l8-3.5Z"/><path d="m9.4 9.4 5.2 5.2"/><path d="m14.6 9.4-5.2 5.2"/>',
    flame:
      '<path d="M12 2.5c3 3.6 5.5 6.1 5.5 9.6a5.5 5.5 0 1 1-11 0c0-3.5 2.5-6 5.5-9.6Z"/><path d="M12 20.2a3 3 0 0 1-3-3c0-1.6 1.2-2.7 3-5.1 1.8 2.4 3 3.5 3 5.1a3 3 0 0 1-3 3Z"/>',
    verified: '<circle cx="12" cy="12" r="9"/><path d="m8.4 12.3 2.5 2.5 4.7-5"/>',
    errorCircle: '<circle cx="12" cy="12" r="9"/><path d="M12 7.3v5.4"/><path d="M12 16.4v.01"/>',
    celebration:
      '<path d="M3 21 9.4 8.6l6 6L3 21Z"/><path d="M14.5 3v3"/><path d="m20 4.6-2.1 2.1"/><path d="M21.5 10.2h-3"/><path d="m17 9.7 2.1 2.1"/>',
    report:
      '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Z"/><path d="M14 3v5h5"/><path d="M12 11.4v3.4"/><path d="M12 17.6v.01"/>',
    smiley:
      '<circle cx="12" cy="12" r="9"/><path d="M8.3 14.3a4.6 4.6 0 0 0 7.4 0"/><path d="M9 9.4v.01"/><path d="M15 9.4v.01"/>',
    paste:
      '<rect x="8" y="3" width="8" height="4" rx="1.2"/><path d="M9.5 5H6.5A2 2 0 0 0 4.5 7v12a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-3"/>',
  };

  /** מחזיר SVG כמחרוזת. הצבע נלקח מ-currentColor. */
  function icon(name, size, className) {
    return (
      '<svg viewBox="0 0 24 24" width="' +
      size +
      '" height="' +
      size +
      '" fill="none" stroke="currentColor" stroke-width="1.7" ' +
      'stroke-linecap="round" stroke-linejoin="round"' +
      (className ? ' class="' + className + '"' : "") +
      ">" +
      PATHS[name] +
      "</svg>"
    );
  }

  /** גלי מכ"ם — אנימציה טהורה ב-CSS. */
  function radar() {
    return '<div class="radar"><span></span><span></span><span></span></div>';
  }

  return { icon, radar };
})();
