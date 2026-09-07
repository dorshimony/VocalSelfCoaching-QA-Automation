from pages.exercises_page import ExercisesPage
from pages.main_page import MainPage


def test_manual_air_diagnosis_opens_closure_program(app):
    """
    בדיקה 4: בחירה ידנית של "יותר מדי אוויר" פותחת את התוכנית,
    ומציגה תרגילי סגירת מיתרים.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")

    assert exercises_page.is_visible(exercises_page.program), "התוכנית לא נפתחה"
    assert not exercises_page.is_visible(exercises_page.gate), "מסך הנעילה נשאר גלוי"
    assert exercises_page.get_verdict_text() == "יותר מדי אוויר"

    assert exercises_page.count(exercises_page.program_cards) > 0, "לא הוצגו תרגילים"

    subtitle = exercises_page.get_text(exercises_page.program_subtitle)
    assert "סגירת מיתרים" in subtitle, "כותרת המשנה לא מתאימה לאבחנה: " + subtitle


def test_manual_pressure_diagnosis_opens_airflow_program(app):
    """
    בדיקה 4ב: בחירה ידנית של "יותר מדי לחץ" מציגה תוכנית אחרת לגמרי.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("pressure")

    assert exercises_page.get_verdict_text() == "יותר מדי לחץ"

    subtitle = exercises_page.get_text(exercises_page.program_subtitle)
    assert "אוויר" in subtitle, "כותרת המשנה לא מתאימה לאבחנה: " + subtitle

    titles = exercises_page.get_program_titles()
    assert len(titles) > 0, "לא הוצגו תרגילים"
    assert "לחיצות שפתיים" in " ".join(titles), "תרגיל מפתח חסר בתוכנית"
