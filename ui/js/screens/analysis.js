/* מסך הניתוח — פרוגרס-בר וחישוב הציון. */
NF.screens.analysis = (function () {
  const { render, $, sleep } = NF.util;

  const STEPS = {
    0: "מנתח נתונים אישיים...",
    40: "בודק התאמה לקריטריונים...",
    70: "מחשב רמת סיכון רוחנית...",
  };

  async function show(status, identity, goal, eda) {
    render(
      '<div class="spinner"></div>' +
        '<h3 id="label" style="margin-top:22px">' +
        STEPS[0] +
        "</h3>" +
        '<div class="bar" style="margin-top:12px"><i id="fill"></i></div>' +
        '<p class="caption" id="percent">0%</p>'
    );

    const label = $("#label");
    const fill = $("#fill");
    const percent = $("#percent");

    for (let step = 0; step <= 100; step++) {
      fill.style.width = step + "%";
      percent.textContent = step + "%";
      if (STEPS[step]) label.textContent = STEPS[step];
      await sleep(0.03);
    }

    if (NF.scoring.isApproved(status, identity, goal, eda)) {
      await NF.screens.request.flashScan();
    } else {
      await NF.screens.rejection.show();
    }
  }

  return { show };
})();
