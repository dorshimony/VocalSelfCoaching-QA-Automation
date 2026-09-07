from pages.exercises_page import ExercisesPage
from pages.main_page import MainPage
from pages.progress_page import ProgressPage


def test_progress_page_shows_week_chart_and_empty_log(app):
    """
    בדיקה 8: עמוד ההתקדמות מציג גרף של שבעה ימים,
    ויומן ריק כשעוד לא בוצעה שום פעילות.
    """
    main_page = MainPage(app)
    progress_page = ProgressPage(app)

    main_page.open_tab("progress")

    assert progress_page.count(progress_page.chart_bars) == 7, \
        "ציפינו לשבע עמודות בגרף, התקבלו: " + str(progress_page.count(progress_page.chart_bars))

    assert progress_page.get_sessions_count() == 0
    assert progress_page.get_total_minutes() == 0
    assert progress_page.is_visible(progress_page.log_empty_message), "הודעת יומן ריק לא מוצגת"


def test_activity_is_logged_and_survives_reload(app):
    """
    בדיקה 8ב: פעילות באפליקציה נרשמת ביומן,
    והנתונים נשמרים גם אחרי רענון הדף.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)
    progress_page = ProgressPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")

    main_page.open_tab("progress")
    sessions_after_diagnosis = progress_page.get_sessions_count()
    assert sessions_after_diagnosis >= 1, "האבחנה לא נרשמה ביומן"

    log_texts = progress_page.get_log_texts()
    assert any("אבחנה" in text for text in log_texts), "רישום האבחנה לא מופיע ביומן"

    # רענון הדף: הנתונים אמורים להישמר
    progress_page.reload()
    app.wait_for_selector("nav.tabs button")
    main_page.open_tab("progress")

    assert progress_page.get_sessions_count() == sessions_after_diagnosis, \
        "מספר המפגשים השתנה אחרי רענון"

    main_page.open_tab("exercises")
    assert exercises_page.is_visible(exercises_page.program), \
        "התוכנית לא נשמרה אחרי רענון והמשתמש צריך לאבחן מחדש"
    assert exercises_page.get_verdict_text() == "יותר מדי אוויר", "האבחנה השמורה השתנתה"
