from pages.exercises_page import ExercisesPage
from pages.main_page import MainPage
from pages.vocal_test_page import VocalTestPage


def test_exercises_are_locked_before_any_diagnosis(app):
    """
    בדיקה 3: לפני שיש אבחנה, עמוד התרגילים נעול:
    מוצג מסך נעילה, והתוכנית עצמה מוסתרת.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")

    assert exercises_page.is_visible(exercises_page.gate), "מסך הנעילה לא מוצג"
    assert not exercises_page.is_visible(exercises_page.program), "התוכנית גלויה למרות שאין אבחנה"
    assert not exercises_page.is_visible(exercises_page.banner), "שורת האבחנה גלויה למרות שאין אבחנה"
    assert exercises_page.count(exercises_page.program_cards) == 0, "מוצגים תרגילים למרות שאין אבחנה"


def test_gate_button_sends_user_to_the_vocal_test(app):
    """
    בדיקה 3ב: הכפתור שבמסך הנעילה מעביר לעמוד המבחן הקולי.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)
    vocal_test_page = VocalTestPage(app)

    main_page.open_tab("exercises")
    exercises_page.click(exercises_page.go_to_test_button)

    assert main_page.is_visible(main_page.panel("test")), "לא עברנו לעמוד המבחן"
    assert vocal_test_page.is_visible(vocal_test_page.stage_intro), "מסך פתיחת המבחן לא מוצג"
