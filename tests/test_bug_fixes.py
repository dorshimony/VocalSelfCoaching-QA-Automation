from pages.exercises_page import ExercisesPage
from pages.main_page import MainPage
from pages.progress_page import ProgressPage
from pages.vocal_test_page import VocalTestPage


def test_bug01_playing_a_reference_tone_is_not_counted_as_practice(app):
    """
    רגרסיה ל־BUG-01: האזנה לטון ייחוס היא פעולת עזר,
    ולא אמורה להירשם כדקות אימון ביומן.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)
    progress_page = ProgressPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")

    main_page.open_tab("progress")
    minutes_before = progress_page.get_total_minutes()

    main_page.open_tab("exercises")
    for _ in range(5):
        exercises_page.play_first_reference_tone()
        exercises_page.wait(150)

    main_page.open_tab("progress")
    minutes_after = progress_page.get_total_minutes()

    assert minutes_after == minutes_before, \
        "השמעת טון ייחוס הוסיפה דקות אימון: לפני " + str(minutes_before) + " אחרי " + str(minutes_after)


def test_bug01_exercise_is_logged_once_when_marked_done(app):
    """
    רגרסיה ל־BUG-01: סימון תרגיל כבוצע נרשם פעם אחת בלבד ביום,
    גם אם לוחצים שוב.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)
    progress_page = ProgressPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")

    main_page.open_tab("progress")
    sessions_before = progress_page.get_sessions_count()

    main_page.open_tab("exercises")
    exercises_page.mark_first_exercise_done()
    exercises_page.wait(200)

    assert exercises_page.is_first_exercise_marked_done(), "הכפתור לא ננעל אחרי סימון התרגיל"

    main_page.open_tab("progress")
    sessions_after = progress_page.get_sessions_count()

    assert sessions_after == sessions_before + 1, \
        "ציפינו לרישום אחד בלבד, נוספו: " + str(sessions_after - sessions_before)


def test_bug02_exercises_page_restores_saved_diagnosis(app):
    """
    רגרסיה ל־BUG-02: לחיצה על "שינוי" ואז מעבר בין לשוניות
    לא משאירה את התרגילים נעולים כשיש אבחנה שמורה.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")
    assert exercises_page.is_visible(exercises_page.program)

    exercises_page.click(exercises_page.change_button)
    assert exercises_page.is_visible(exercises_page.gate), "מסך הבחירה לא נפתח"

    main_page.open_tab("progress")
    main_page.open_tab("exercises")

    assert exercises_page.is_visible(exercises_page.program), \
        "התרגילים נשארו נעולים למרות שיש אבחנה שמורה"
    assert exercises_page.get_verdict_text() == "יותר מדי אוויר"


def test_bug03_manual_diagnosis_is_not_labelled_as_a_test(app):
    """
    רגרסיה ל־BUG-03: אבחנה שנבחרה ידנית לא מוצגת כאילו בוצע מבחן קולי.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)
    vocal_test_page = VocalTestPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("pressure")

    main_page.open_tab("test")
    banner_text = vocal_test_page.get_text(app.locator("#rbDate"))

    assert "אבחנה ידנית" in banner_text, "האבחנה הידנית לא מסומנת ככזו: " + banner_text
    assert "מבחן אחרון" not in banner_text, "אבחנה ידנית מוצגת כמבחן: " + banner_text


def test_bug04_tabs_and_panels_are_linked_for_screen_readers(app):
    """
    רגרסיה ל־BUG-04: כל לשונית מקושרת לעמוד שלה,
    וכל עמוד מוגדר כלוח טאב.
    """
    tabs = app.locator('nav.tabs button[role="tab"]')
    panels = app.locator('[role="tabpanel"]')

    assert tabs.count() == 5, "ציפינו לחמש לשוניות מוגדרות"
    assert panels.count() == 5, "ציפינו לחמישה עמודים מוגדרים כלוח טאב"

    for index in range(tabs.count()):
        tab = tabs.nth(index)
        panel_id = tab.get_attribute("aria-controls")
        assert panel_id, "ללשונית אין קישור לעמוד שלה"

        panel = app.locator("#" + panel_id)
        assert panel.count() == 1, "העמוד " + panel_id + " לא נמצא"
        assert panel.get_attribute("aria-labelledby") == tab.get_attribute("id"), \
            "העמוד " + panel_id + " לא מקושר בחזרה ללשונית שלו"


def test_bug05_test_stops_when_no_voice_is_picked_up(page):
    """
    רגרסיה ל־BUG-05: כשהמיקרופון לא קולט כלום,
    המבדק נעצר מיד, מציג אזהרה, ולא ממציא תוצאה.

    כדי לבדוק את זה מחליפים את המיקרופון בזרם שקט לחלוטין.
    """
    from conftest import APP_URL

    # מיקרופון מדומה שלא מפיק שום צליל
    page.add_init_script(
        "navigator.mediaDevices.getUserMedia = async () => {"
        "  const ctx = new AudioContext();"
        "  return ctx.createMediaStreamDestination().stream;"
        "};"
    )

    page.goto(APP_URL)
    page.evaluate("localStorage.clear()")
    page.evaluate("localStorage.setItem('vsc_hero_seen_v1', '1')")
    page.reload()
    page.wait_for_selector("nav.tabs button")

    vocal_test_page = VocalTestPage(page)
    vocal_test_page.choose_gender("male")
    vocal_test_page.start_test()

    # מחכים מספיק זמן לסולם הראשון ולזיהוי השקט
    page.wait_for_timeout(14000)

    assert vocal_test_page.is_visible(vocal_test_page.stage_intro), \
        "המבדק לא חזר למסך הפתיחה למרות שלא נקלט קול"
    assert not vocal_test_page.is_visible(vocal_test_page.stage_results), \
        "הוצגו תוצאות למרות שלא נקלט שום קול"

    hint = vocal_test_page.get_hint_text()
    assert "לא נקלט" in hint, "לא הוצגה אזהרה על היעדר קליטה: " + hint
