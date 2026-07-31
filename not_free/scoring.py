"""משקלי הניקוד של השאלון.

זה מקור האמת היחיד גם לאפשרויות וגם לציונים: הדרופדאונים במסך השאלון
נבנים מהמפתחות כאן, כך שאי אפשר להוסיף אפשרות בלי לקבוע לה ציון.
מקביל ל-docs/תרחישים.xlsx.
"""

OTHER = "אחר (נא לפרט)"

STATUS_SCORES = {
    "אברך": 20,
    "בחור ישיבה": 10,
    "תלמידת סמינר": 8,
    'תלמיד ת"ת': 0,
    "נושר": -40,
    OTHER: 0,
}

IDENTITY_SCORES = {
    'צו"ל': 15,
    "ליטאי קלאס": 10,
    "חסידישע'ר": 12,
    "חזונישנ'יק": 15,
    "בעל תשובה": 15,
    "חרדי מודרני": -20,
}

GOAL_SCORES = {
    "פרנסה": 15,
    "לימוד תורה": 25,
    "לימודים כלליים": 10,
    "חדשות": -20,
    "בידור ופנאי": -50,
    OTHER: 0,
}

EDA_SCORES = {
    "אשכנזי": 10,
    "ספרדי": 0,
    "תימני": -5,
    "מעורב": 0,
    "ספרדי אבל לומד בסורוצקין😉": 5,
}

PASS_THRESHOLD = 35


def compute_score(status, identity, goal, eda):
    return (
        STATUS_SCORES.get(status, 0)
        + IDENTITY_SCORES.get(identity, 0)
        + GOAL_SCORES.get(goal, 0)
        + EDA_SCORES.get(eda, 0)
    )


def is_approved(status, identity, goal, eda):
    return compute_score(status, identity, goal, eda) >= PASS_THRESHOLD
