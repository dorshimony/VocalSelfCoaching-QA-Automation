from urllib.parse import unquote

from pages.exercises_page import ExercisesPage
from pages.lead_page import LeadPage
from pages.main_page import MainPage


def decoded_message(link):
    """מחלץ את ההודעה המוכנה מתוך קישור הוואטסאפ."""
    return unquote(link.split("?text=", 1)[1])


def fresh_visitor(page, app_url):
    """מבקר חדש לגמרי: בלי שום נתון שמור."""
    page.goto(app_url)
    page.evaluate("localStorage.clear()")
    page.reload()
    page.wait_for_selector("#heroCard")
    return LeadPage(page)


def test_first_visitor_sees_one_screen_and_one_button(page):
    """
    בדיקה 12: מי שמגיע בפעם הראשונה רואה מסך פתיחה אחד —
    מה הוא מקבל, כפתור התחלה, ומי המורה. הלשוניות מוסתרות
    כדי שלא יתפזר.
    """
    from conftest import APP_URL

    lead_page = fresh_visitor(page, APP_URL)

    assert lead_page.is_visible(lead_page.hero), "מסך הפתיחה לא מוצג למבקר חדש"
    assert lead_page.is_visible(lead_page.hero_start_button), "כפתור ההתחלה לא מוצג"
    assert lead_page.get_text(lead_page.teacher_name) == "דור שמעוני"
    assert "פיתוח קול" in lead_page.get_text(lead_page.teacher_role)

    assert not lead_page.is_visible(page.locator("nav.tabs")), \
        "הלשוניות מוצגות כבר במסך הפתיחה"


def test_the_teacher_photo_is_shown(page):
    """
    בדיקה 12ב: במסך הפתיחה מופיעה תמונה של המורה, ולא ראשי תיבות.
    """
    from conftest import APP_URL

    lead_page = fresh_visitor(page, APP_URL)
    photo = page.locator("#heroCard img.dor-photo")

    assert lead_page.is_visible(photo), "תמונת המורה לא מוצגת"
    assert "דור שמעוני" in (photo.get_attribute("alt") or ""), "לתמונה אין תיאור נגיש"


def test_opening_screen_disappears_after_starting(page):
    """
    בדיקה 12ג: אחרי לחיצה על ההתחלה מסך הפתיחה נעלם,
    הלשוניות נחשפות, והמסך לא חוזר גם אחרי רענון.
    """
    from conftest import APP_URL

    lead_page = fresh_visitor(page, APP_URL)

    lead_page.start_from_hero()
    assert not lead_page.is_visible(lead_page.hero), "מסך הפתיחה נשאר אחרי ההתחלה"
    assert lead_page.is_visible(page.locator("nav.tabs")), "הלשוניות לא נחשפו אחרי ההתחלה"

    lead_page.reload()
    page.wait_for_selector("nav.tabs button")
    assert not lead_page.is_visible(lead_page.hero), "מסך הפתיחה חזר אחרי רענון"


def test_result_screen_offers_a_lesson_with_the_diagnosis_in_the_message(app):
    """
    בדיקה 12ג: מסך התוצאות מציג את האבחון בשפה פשוטה,
    וכפתור הוואטסאפ מכיל את האבחון עצמו ואת מקור הפנייה.
    """
    from pages.vocal_test_page import VocalTestPage

    lead_page = LeadPage(app)
    vocal_test_page = VocalTestPage(app)

    vocal_test_page.choose_gender("male")
    vocal_test_page.start_test()

    app.wait_for_selector("#stageRun:not([hidden])", timeout=15000)
    vocal_test_page.wait(16500)
    vocal_test_page.stop_test()
    app.wait_for_selector("#stageResults:not([hidden])", timeout=15000)

    assert lead_page.is_visible(lead_page.result_cta), "לא הוצגה קריאה לפעולה אחרי האבחון"
    assert lead_page.get_text(lead_page.result_title), "לא הוצגה כותרת אבחון בשפה פשוטה"
    assert lead_page.get_text(lead_page.result_next), "לא הוסבר מה הצעד הבא"

    gap = lead_page.get_text(app.locator("#resultCta .rc-gap"))
    assert "בשיעור" in gap, "לא נאמר מה אי אפשר לדעת מהקלטה: " + gap
    assert lead_page.is_visible(app.locator("#resultCta .first-lesson")), \
        "לא הוסבר מה קורה בשיעור ראשון"

    link = lead_page.get_result_link()
    assert link.startswith(LeadPage.WHATSAPP_PREFIX), "הקישור לא מפנה למספר הנכון: " + link

    message = decoded_message(link)
    assert "המבחן הקולי" in message, "ההודעה לא מזכירה את המבחן: " + message
    assert "אפליקציה" in message, "ההודעה לא מסמנת שהפנייה הגיעה מהאפליקציה: " + message
    assert "לקבוע שיעור" in message, "ההודעה לא מבקשת לקבוע שיעור: " + message

    # האבחון שנבחר חייב להופיע בהודעה עצמה
    verdict_labels = ["יותר מדי אוויר", "יותר מדי לחץ", "מאוזן"]
    assert any(label in message for label in verdict_labels), \
        "האבחון לא נכלל בהודעה: " + message


def test_the_message_follows_the_chosen_diagnosis(app):
    """
    בדיקה 12ד: אם המשתמש משנה את האבחנה, ההודעה המוכנה משתנה איתה.
    """
    from pages.vocal_test_page import VocalTestPage

    lead_page = LeadPage(app)
    vocal_test_page = VocalTestPage(app)

    vocal_test_page.choose_gender("male")
    vocal_test_page.start_test()

    app.wait_for_selector("#stageRun:not([hidden])", timeout=15000)
    vocal_test_page.wait(16500)
    vocal_test_page.stop_test()
    app.wait_for_selector("#stageResults:not([hidden])", timeout=15000)

    app.locator('#verdictRow .choice[data-verdict="pressure"]').click()
    message = decoded_message(lead_page.get_result_link())

    assert "יותר מדי לחץ" in message, "ההודעה לא עודכנה לאבחנה שנבחרה: " + message


def test_every_exercise_invites_to_a_lesson(app):
    """
    בדיקה 12ה: בתחתית כל תרגיל יש הזמנה עדינה לשיעור,
    וההודעה כוללת את שם התרגיל ואת מקור הפנייה.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)
    lead_page = LeadPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")

    invites = lead_page.count(lead_page.exercise_invites)
    cards = exercises_page.count(exercises_page.program_cards)
    assert invites == cards, \
        "לא בכל תרגיל יש הזמנה לשיעור: " + str(invites) + " מתוך " + str(cards)

    assert "בשיעור" in lead_page.get_text(lead_page.exercise_invites.first), \
        "הניסוח בתרגיל לא מזמין לשיעור"

    link = lead_page.get_first_exercise_link()
    assert link.startswith(LeadPage.WHATSAPP_PREFIX), "הקישור לא מפנה למספר הנכון"

    message = decoded_message(link)
    first_title = exercises_page.get_program_titles()[0]
    assert first_title in message, "שם התרגיל לא נכלל בהודעה: " + message
    assert "אפליקציה" in message, "ההודעה לא מסמנת את מקור הפנייה: " + message


def test_lead_form_rejects_empty_and_invalid_details(app):
    """
    בדיקה 12ו: טופס הפרטים לא נשלח בלי שם או עם טלפון לא תקין.
    """
    lead_page = LeadPage(app)

    lead_page.send_lead_form()
    assert "שם" in lead_page.get_error_text(), \
        "לא הוצגה שגיאה על שם חסר: " + lead_page.get_error_text()

    lead_page.fill_lead_form("דני", "123")
    lead_page.send_lead_form()
    assert "טלפון" in lead_page.get_error_text(), \
        "לא הוצגה שגיאה על טלפון לא תקין: " + lead_page.get_error_text()


def test_lead_form_opens_whatsapp_with_the_details(app):
    """
    בדיקה 12ז: טופס תקין פותח וואטסאפ עם השם, הטלפון ומקור הפנייה.
    """
    lead_page = LeadPage(app)

    lead_page.fill_lead_form("דני כהן", "0521234567")

    # תופסים את הכתובת שהאפליקציה מבקשת לפתוח, בלי לצאת באמת לוואטסאפ
    app.evaluate("() => { window.__opened = null; window.open = url => { window.__opened = url; return null; }; }")
    lead_page.send_lead_form()
    opened_url = app.evaluate("() => window.__opened")

    assert opened_url, "לא נפתח כלום אחרי שליחת הטופס"
    assert opened_url.startswith(LeadPage.WHATSAPP_PREFIX), \
        "לא נפתח וואטסאפ עם המספר הנכון: " + opened_url

    message = decoded_message(opened_url)
    assert "דני כהן" in message, "השם לא נכלל בהודעה: " + message
    assert "0521234567" in message, "הטלפון לא נכלל בהודעה: " + message
    assert "אפליקציה" in message, "ההודעה לא מסמנת את מקור הפנייה: " + message
