/* משקלי הניקוד של השאלון.
   מקור אמת יחיד גם לאפשרויות וגם לציונים — הדרופדאונים נבנים מהמפתחות כאן.
   מקביל ל-docs/תרחישים.xlsx. */
NF.scoring = (function () {
  const OTHER = "אחר (נא לפרט)";

  const STATUS = {
    אברך: 20,
    "בחור ישיבה": 10,
    "תלמידת סמינר": 8,
    'תלמיד ת"ת': 0,
    נושר: -40,
    [OTHER]: 0,
  };

  const IDENTITY = {
    'צו"ל': 15,
    "ליטאי קלאס": 10,
    "חסידישע'ר": 12,
    "חזונישנ'יק": 15,
    "בעל תשובה": 15,
    "חרדי מודרני": -20,
  };

  const GOAL = {
    פרנסה: 15,
    "לימוד תורה": 25,
    "לימודים כלליים": 10,
    חדשות: -20,
    "בידור ופנאי": -50,
    [OTHER]: 0,
  };

  const EDA = {
    אשכנזי: 10,
    ספרדי: 0,
    תימני: -5,
    מעורב: 0,
    "ספרדי אבל לומד בסורוצקין😉": 5,
  };

  const PASS_THRESHOLD = 35;

  function score(status, identity, goal, eda) {
    return (
      (STATUS[status] || 0) +
      (IDENTITY[identity] || 0) +
      (GOAL[goal] || 0) +
      (EDA[eda] || 0)
    );
  }

  function isApproved(status, identity, goal, eda) {
    return score(status, identity, goal, eda) >= PASS_THRESHOLD;
  }

  return { OTHER, STATUS, IDENTITY, GOAL, EDA, PASS_THRESHOLD, score, isApproved };
})();
