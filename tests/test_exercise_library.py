from pages.exercises_page import ExercisesPage
from pages.main_page import MainPage


def test_show_all_exercises_toggle(app):
    """
    בדיקה 6: הכפתור שפותח את מאגר כל התרגילים עובד בשני הכיוונים,
    והמאגר המלא גדול מהתוכנית האישית.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")

    program_count = exercises_page.count(exercises_page.program_cards)
    assert not exercises_page.is_visible(exercises_page.all_grid), "מאגר התרגילים פתוח לפני שנלחץ"

    exercises_page.toggle_all_exercises()
    assert exercises_page.is_visible(exercises_page.all_grid), "המאגר לא נפתח"

    all_count = exercises_page.count(exercises_page.all_cards)
    assert all_count > program_count, \
        "המאגר המלא (" + str(all_count) + ") לא גדול מהתוכנית (" + str(program_count) + ")"

    exercises_page.toggle_all_exercises()
    assert not exercises_page.is_visible(exercises_page.all_grid), "המאגר לא נסגר בלחיצה שנייה"


def test_reference_note_can_be_changed(app):
    """
    בדיקה 6ב: אפשר לשנות את תו ההתחלה של התרגילים,
    ולנגן טון ייחוס בלי שהאפליקציה תיפול.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("balanced")

    exercises_page.select_reference_note("67")
    assert exercises_page.get_selected_reference_note() == "67"

    exercises_page.play_first_reference_tone()
    exercises_page.wait(500)

    assert exercises_page.is_visible(exercises_page.program), "העמוד נשבר אחרי השמעת טון"
