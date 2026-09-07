from pages.exercises_page import ExercisesPage
from pages.main_page import MainPage


def test_changing_diagnosis_replaces_the_program(app):
    """
    בדיקה 5: שינוי האבחנה מחליף את רשימת התרגילים,
    ולא מוסיף אותם על גבי הקודמים.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")

    exercises_page.choose_manual_verdict("air")
    air_titles = exercises_page.get_program_titles()
    air_count = exercises_page.count(exercises_page.program_cards)

    exercises_page.click(exercises_page.change_button)
    assert exercises_page.is_visible(exercises_page.gate), "מסך הבחירה לא חזר אחרי לחיצה על שינוי"
    assert not exercises_page.is_visible(exercises_page.program), "התוכנית נשארה גלויה בזמן שינוי האבחנה"

    exercises_page.choose_manual_verdict("balanced")
    balanced_titles = exercises_page.get_program_titles()
    balanced_count = exercises_page.count(exercises_page.program_cards)

    assert exercises_page.get_verdict_text() == "מאוזן"
    assert balanced_count > 0, "לא הוצגו תרגילים אחרי שינוי האבחנה"
    assert balanced_count <= air_count + 6, "נראה שהתרגילים הצטברו במקום להתחלף"
    assert balanced_titles != air_titles, "רשימת התרגילים לא השתנתה למרות שהאבחנה שונתה"
