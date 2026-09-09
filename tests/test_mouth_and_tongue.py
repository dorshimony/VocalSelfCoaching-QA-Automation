from pages.main_page import MainPage
from pages.mouth_page import MouthPage


def test_mouth_tab_opens_and_requires_gender(app):
    """
    בדיקה 10: לשונית "חסימות לשון ופה משוחרר" נפתחת,
    וכפתור ההתחלה נעול עד שנבחר מין.
    """
    main_page = MainPage(app)
    mouth_page = MouthPage(app)

    main_page.open_tab("mouth")

    assert mouth_page.is_visible(mouth_page.stage_intro), "מסך הפתיחה של הבדיקה לא מוצג"
    assert "לשון" in mouth_page.get_text(mouth_page.heading), \
        "כותרת העמוד לא מתארת את הבדיקה: " + mouth_page.get_text(mouth_page.heading)

    assert not mouth_page.is_start_enabled(), "כפתור ההתחלה פעיל עוד לפני בחירת מין"

    mouth_page.choose_gender("male")
    assert mouth_page.is_start_enabled(), "כפתור ההתחלה נשאר חסום אחרי בחירת מין"


def test_camera_stage_opens_with_a_framing_step(app):
    """
    בדיקה 10ב: אחרי התחלה נפתח מסך ההרצה עם וידאו חי,
    מסגרת מיקום, ובקשה לאשר שהפה בתוך המסגרת.
    """
    main_page = MainPage(app)
    mouth_page = MouthPage(app)

    main_page.open_tab("mouth")
    mouth_page.choose_gender("female")
    mouth_page.start_check()

    app.wait_for_selector("#mouthRun:not([hidden])", timeout=15000)

    assert mouth_page.is_visible(mouth_page.video), "תצוגת המצלמה לא מוצגת"
    assert mouth_page.is_visible(mouth_page.guide_frame), "מסגרת המיקום לא מוצגת"
    assert mouth_page.is_visible(mouth_page.ready_button), "כפתור אישור המסגרת לא מוצג"
    assert "מסגרת" in mouth_page.get_phase_text(), \
        "שלב המיקום לא מוצג: " + mouth_page.get_phase_text()


def test_calibration_starts_after_confirming_the_frame(app):
    """
    בדיקה 10ג: אישור המסגרת מעביר לשלב מדידת הרקע,
    וכפתור האישור נעלם כדי שלא ילחצו עליו פעמיים.
    """
    main_page = MainPage(app)
    mouth_page = MouthPage(app)

    main_page.open_tab("mouth")
    mouth_page.choose_gender("male")
    mouth_page.start_check()

    app.wait_for_selector("#mouthRun:not([hidden])", timeout=15000)
    mouth_page.confirm_frame()

    assert not mouth_page.is_visible(mouth_page.ready_button), "כפתור האישור נשאר גלוי"
    app.wait_for_timeout(300)
    assert "רקע" in mouth_page.get_phase_text() or "סולם" in mouth_page.step_label.inner_text(), \
        "לא עברנו לשלב מדידת הרקע: " + mouth_page.get_phase_text()


def test_cancel_returns_to_the_intro_screen(app):
    """
    בדיקה 10ד: ביטול באמצע הבדיקה מחזיר למסך הפתיחה
    ומכבה את המצלמה.
    """
    main_page = MainPage(app)
    mouth_page = MouthPage(app)

    main_page.open_tab("mouth")
    mouth_page.choose_gender("male")
    mouth_page.start_check()

    app.wait_for_selector("#mouthRun:not([hidden])", timeout=15000)
    mouth_page.cancel_check()
    app.wait_for_timeout(500)

    assert mouth_page.is_visible(mouth_page.stage_intro), "לא חזרנו למסך הפתיחה"
    assert not mouth_page.is_visible(mouth_page.stage_run), "מסך ההרצה נשאר גלוי"

    camera_is_live = app.evaluate(
        "() => { const v = document.getElementById('mouthVideo'); return !!(v && v.srcObject); }"
    )
    assert not camera_is_live, "המצלמה נשארה דולקת אחרי ביטול"


def test_full_check_produces_three_measurements_and_a_verdict(app):
    """
    בדיקה 10ה: מסלול מלא — מיקום, כיול, שלושה סולמות,
    ואז שלושה מדדים בטווח 0-100 ואבחנה עם המלצות.
    """
    main_page = MainPage(app)
    mouth_page = MouthPage(app)

    main_page.open_tab("mouth")
    mouth_page.choose_gender("male")
    mouth_page.start_check()

    app.wait_for_selector("#mouthRun:not([hidden])", timeout=15000)
    mouth_page.confirm_frame()

    # שלושה סולמות עם חלון הקלטה מוארך בסולם הראשון
    app.wait_for_selector("#mouthResults:not([hidden])", timeout=60000)

    assert mouth_page.count(mouth_page.meters) == 3, "ציפינו לשלושה מדדים"

    for value in mouth_page.get_meter_values():
        assert 0 <= value <= 100, "מדד מחוץ לטווח: " + str(value)

    assert mouth_page.is_visible(mouth_page.verdict_title), "לא הוצגה אבחנה"
    assert mouth_page.count(mouth_page.tips) > 0, "לא הוצגו המלצות תרגול"
    assert mouth_page.is_visible(mouth_page.banner), "שורת הסיכום לא מוצגת"
