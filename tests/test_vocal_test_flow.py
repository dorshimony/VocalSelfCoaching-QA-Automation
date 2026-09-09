from pages.exercises_page import ExercisesPage
from pages.main_page import MainPage
from pages.vocal_test_page import VocalTestPage


def test_start_button_requires_gender_selection(app):
    """
    בדיקה 7: לא ניתן להתחיל מבדק לפני בחירת מין,
    ולאחר הבחירה הכפתור נפתח.
    """
    vocal_test_page = VocalTestPage(app)

    assert not vocal_test_page.is_start_enabled(), "כפתור ההתחלה פעיל עוד לפני בחירת מין"

    vocal_test_page.choose_gender("male")
    assert vocal_test_page.is_start_enabled(), "כפתור ההתחלה נשאר חסום אחרי בחירת מין"


def test_full_vocal_test_produces_results_and_opens_program(app):
    """
    בדיקה 7ב: מסלול מלא של המבחן הקולי:
    התחלה, סולם ראשון, עצירה מוקדמת, תוצאות, בחירת אבחנה,
    ומעבר אוטומטי לעמוד התרגילים.
    """
    main_page = MainPage(app)
    vocal_test_page = VocalTestPage(app)
    exercises_page = ExercisesPage(app)

    vocal_test_page.choose_gender("female")
    vocal_test_page.start_test()

    app.wait_for_selector("#stageRun:not([hidden])", timeout=15000)
    assert vocal_test_page.is_visible(vocal_test_page.stage_run), "מסך ההרצה לא נפתח"
    assert "סולם" in vocal_test_page.get_step_text(), \
        "מונה הסולמות לא מוצג: " + vocal_test_page.get_step_text()

    # נותנים לסולם הראשון להיקלט, ואז עוצרים.
    # חלון ההקלטה של הסולם הראשון הוארך (זמן חסד למי שמתחיל לשיר לאט),
    # ולכן ההמתנה כאן ארוכה בהתאם.
    vocal_test_page.wait(16500)
    vocal_test_page.stop_test()

    app.wait_for_selector("#stageResults:not([hidden])", timeout=15000)
    assert vocal_test_page.is_visible(vocal_test_page.stage_results), "מסך התוצאות לא נפתח"

    air = int(vocal_test_page.get_text(vocal_test_page.air_value))
    pressure = int(vocal_test_page.get_text(vocal_test_page.pressure_value))
    assert 0 <= air <= 100, "מדד האוויר מחוץ לטווח: " + str(air)
    assert 0 <= pressure <= 100, "מדד הלחץ מחוץ לטווח: " + str(pressure)

    assert vocal_test_page.count(vocal_test_page.results_table_rows) > 1, "טבלת התוצאות ריקה"

    vocal_test_page.choose_verdict("air")
    app.wait_for_timeout(500)

    assert main_page.is_visible(main_page.panel("exercises")), "לא עברנו אוטומטית לעמוד התרגילים"
    assert exercises_page.count(exercises_page.program_cards) > 0, "לא נבנתה תוכנית אחרי המבחן"


def test_cancel_returns_to_the_intro_screen(app):
    """
    בדיקה 7ג: ביטול באמצע המבדק מחזיר למסך הפתיחה.
    """
    vocal_test_page = VocalTestPage(app)

    vocal_test_page.choose_gender("male")
    vocal_test_page.start_test()

    app.wait_for_selector("#stageRun:not([hidden])", timeout=15000)
    vocal_test_page.cancel_test()
    app.wait_for_timeout(500)

    assert vocal_test_page.is_visible(vocal_test_page.stage_intro), "לא חזרנו למסך הפתיחה"
    assert not vocal_test_page.is_visible(vocal_test_page.stage_run), "מסך ההרצה נשאר גלוי"
