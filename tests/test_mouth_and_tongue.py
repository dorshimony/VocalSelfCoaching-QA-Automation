from pages.main_page import MainPage
from pages.mouth_page import MouthPage

# מזהה פנים מדומה שמוזרק לאפליקציה במקום המודל האמיתי.
# הוא מחזיר נקודות פנים מלאכותיות שאפשר לשלוט בהן מהבדיקה,
# וכך אפשר לבדוק את חישוב הציונים בלי מצלמה אמיתית ובלי פנים אמיתיות.
FAKE_LANDMARKER = """
window.__fakeMouth = { open: 0.30, width: 0.42 };

window.VSC_TEST_LANDMARKER = {
  detectForVideo: function () {
    var points = [];
    for (var i = 0; i < 478; i++) points.push({ x: 0.5, y: 0.5, z: 0 });

    // גובה הפנים: מצח וסנטר
    points[10]  = { x: 0.5, y: 0.20, z: 0 };
    points[152] = { x: 0.5, y: 0.80, z: 0 };

    // פתח הפה: שפה עליונה ותחתונה
    var half = window.__fakeMouth.open / 2;
    points[13] = { x: 0.5, y: 0.60 - half, z: 0 };
    points[14] = { x: 0.5, y: 0.60 + half, z: 0 };

    // רוחב הפה: שתי הזוויות
    var side = window.__fakeMouth.width / 2;
    points[61]  = { x: 0.5 - side, y: 0.60, z: 0 };
    points[291] = { x: 0.5 + side, y: 0.60, z: 0 };

    return { faceLandmarks: [points] };
  }
};
"""


def open_mouth_page(page, app_url, mouth_open=0.30, mouth_width=0.42):
    """
    פותח את האפליקציה עם מזהה הפנים המדומה מוזרק מראש,
    ועובר ללשונית של חסימות לשון ופה משוחרר.
    """
    page.add_init_script(FAKE_LANDMARKER)
    page.goto(app_url)
    page.evaluate("localStorage.clear()")
    page.evaluate("localStorage.setItem('vsc_hero_seen_v1', '1')")
    page.reload()
    page.wait_for_selector("nav.tabs button")
    page.evaluate(
        "size => { window.__fakeMouth.open = size.open; window.__fakeMouth.width = size.width; }",
        {"open": mouth_open, "width": mouth_width},
    )
    MainPage(page).open_tab("mouth")
    return MouthPage(page)


def test_mouth_tab_opens_and_requires_gender(app):
    """
    בדיקה 10: הלשונית נפתחת, וכפתור ההתחלה נעול עד שנבחר מין.
    """
    main_page = MainPage(app)
    mouth_page = MouthPage(app)

    main_page.open_tab("mouth")

    assert mouth_page.is_visible(mouth_page.stage_intro), "מסך הפתיחה לא מוצג"
    assert "לשון" in mouth_page.get_text(mouth_page.heading), \
        "כותרת העמוד לא מתארת את הבדיקה: " + mouth_page.get_text(mouth_page.heading)

    assert not mouth_page.is_start_enabled(), "כפתור ההתחלה פעיל עוד לפני בחירת מין"

    mouth_page.choose_gender("male")
    assert mouth_page.is_start_enabled(), "כפתור ההתחלה נשאר חסום אחרי בחירת מין"


def test_start_is_blocked_until_a_face_is_detected(page):
    """
    בדיקה 10ב: אי אפשר להתחיל את הכיול לפני שזוהו פנים.
    זו ההגנה שמונעת כיול על רקע במקום על הפנים.
    """
    from conftest import APP_URL

    mouth_page = open_mouth_page(page, APP_URL)
    mouth_page.choose_gender("male")
    mouth_page.start_check()

    page.wait_for_selector("#mouthRun:not([hidden])", timeout=15000)

    assert mouth_page.is_visible(mouth_page.ready_button), "כפתור ההתחלה לא מוצג בשלב המיקום"
    page.wait_for_function(
        "() => !document.getElementById('mouthReadyBtn').disabled", timeout=10000
    )
    assert "זוהו" in mouth_page.get_text(mouth_page.heard_badge), \
        "לא הוצגה הודעה על זיהוי פנים: " + mouth_page.get_text(mouth_page.heard_badge)


def test_calibration_fails_when_the_mouth_never_opens(page):
    """
    בדיקה 10ג: אם בכיול לא נמדד הבדל בין פה סגור לפה פתוח,
    הבדיקה נעצרת עם הסבר ולא ממציאה תוצאה.

    זה בדיוק הבאג שהיה בגרסה הראשונה: פה סגור שהתקבל כפתוח.
    """
    from conftest import APP_URL

    mouth_page = open_mouth_page(page, APP_URL, mouth_open=0.03)
    mouth_page.choose_gender("male")
    mouth_page.start_check()

    page.wait_for_selector("#mouthRun:not([hidden])", timeout=15000)
    page.wait_for_function(
        "() => !document.getElementById('mouthReadyBtn').disabled", timeout=10000
    )
    mouth_page.confirm_frame()

    # שלושת שלבי הכיול ואז ההודעה
    page.wait_for_selector("#mouthIntro:not([hidden])", timeout=20000)

    assert not mouth_page.is_visible(mouth_page.stage_results), \
        "הוצגו תוצאות למרות שהכיול נכשל"
    assert "הכיול לא הצליח" in mouth_page.get_hint_text(), \
        "לא הוצגה הודעת כשל כיול: " + mouth_page.get_hint_text()


def test_cancel_returns_to_the_intro_screen_and_stops_the_camera(page):
    """
    בדיקה 10ד: ביטול מחזיר למסך הפתיחה ומכבה את המצלמה.
    """
    from conftest import APP_URL

    mouth_page = open_mouth_page(page, APP_URL)
    mouth_page.choose_gender("male")
    mouth_page.start_check()

    page.wait_for_selector("#mouthRun:not([hidden])", timeout=15000)
    mouth_page.cancel_check()
    page.wait_for_timeout(500)

    assert mouth_page.is_visible(mouth_page.stage_intro), "לא חזרנו למסך הפתיחה"
    assert not mouth_page.is_visible(mouth_page.stage_run), "מסך ההרצה נשאר גלוי"

    camera_is_live = page.evaluate(
        "() => { const v = document.getElementById('mouthVideo'); return !!(v && v.srcObject); }"
    )
    assert not camera_is_live, "המצלמה נשארה דולקת אחרי ביטול"


def run_full_check(page, app_url, calibration_open, singing_open):
    """
    מריץ מסלול מלא: כיול עם פה פתוח בגודל אחד, ושירה בגודל אחר.
    מחזיר את שלושת הציונים.
    """
    mouth_page = open_mouth_page(page, app_url, mouth_open=0.05)
    mouth_page.choose_gender("male")
    mouth_page.start_check()

    page.wait_for_selector("#mouthRun:not([hidden])", timeout=15000)
    page.wait_for_function(
        "() => !document.getElementById('mouthReadyBtn').disabled", timeout=10000
    )
    mouth_page.confirm_frame()

    # כיול 1 — פה סגור. כיול 2 — פה פתוח לרווחה.
    page.wait_for_function(
        "() => document.getElementById('mouthPhase').textContent.indexOf('2 מתוך 3') > -1",
        timeout=15000,
    )
    page.evaluate("v => { window.__fakeMouth.open = v; }", calibration_open)

    # כיול 3 ואילך — הגודל שבו 'שרים'
    page.wait_for_function(
        "() => document.getElementById('mouthPhase').textContent.indexOf('3 מתוך 3') > -1",
        timeout=15000,
    )
    page.evaluate("v => { window.__fakeMouth.open = v; }", singing_open)

    page.wait_for_selector("#mouthResults:not([hidden])", timeout=90000)
    return mouth_page


def test_a_mouth_that_stays_shut_while_singing_scores_low(page):
    """
    בדיקה 10ה: מי שפתח את הפה בכיול אבל שר עם פה כמעט סגור
    מקבל ציון פתיחה נמוך ואבחנה שמצביעה על כך.
    """
    from conftest import APP_URL

    mouth_page = run_full_check(page, APP_URL, calibration_open=0.40, singing_open=0.07)

    values = mouth_page.get_meter_values()
    assert len(values) == 3, "ציפינו לשלושה מדדים"
    assert values[0] < 45, "פה סגור בזמן שירה קיבל ציון פתיחה גבוה: " + str(values[0])
    assert "הפה כמעט לא נפתח" in mouth_page.get_text(mouth_page.verdict_title), \
        "האבחנה לא הצביעה על פה סגור: " + mouth_page.get_text(mouth_page.verdict_title)


def test_a_mouth_that_opens_while_singing_scores_high(page):
    """
    בדיקה 10ו: מי ששר בפתיחה דומה לכיול מקבל ציון פתיחה גבוה.
    יחד עם הבדיקה הקודמת זה מוכיח שהמדד באמת מגיב לפתיחת הפה.
    """
    from conftest import APP_URL

    mouth_page = run_full_check(page, APP_URL, calibration_open=0.40, singing_open=0.38)

    values = mouth_page.get_meter_values()
    assert values[0] > 60, "פה פתוח בזמן שירה קיבל ציון פתיחה נמוך: " + str(values[0])

    for value in values:
        assert 0 <= value <= 100, "מדד מחוץ לטווח: " + str(value)

    assert mouth_page.count(mouth_page.tips) > 0, "לא הוצגו המלצות תרגול"
    assert mouth_page.is_visible(mouth_page.banner), "שורת הסיכום לא מוצגת"


def test_the_log_entry_matches_the_verdict_on_screen(page):
    """
    בדיקה 10ז: מה שנרשם ביומן האימונים זהה לאבחנה שהוצגה במסך התוצאות.
    """
    from conftest import APP_URL
    from pages.main_page import MainPage

    mouth_page = run_full_check(page, APP_URL, calibration_open=0.40, singing_open=0.07)
    verdict_on_screen = mouth_page.get_text(mouth_page.banner_main)

    MainPage(page).open_tab("progress")
    log_text = page.locator(".log-list li").first.inner_text()

    assert verdict_on_screen in log_text, \
        "היומן רושם משהו אחר מהאבחנה: ביומן '" + log_text + "' במסך '" + verdict_on_screen + "'"
