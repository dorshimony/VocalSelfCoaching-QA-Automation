from urllib.parse import unquote

from pages.exercises_page import ExercisesPage
from pages.main_page import MainPage


def test_only_two_exercises_are_open(app):
    """
    בדיקה 6: התוכנית החינמית מכילה שני תרגילים בלבד.
    השאר נשמר לשיעור.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")

    open_count = exercises_page.count(exercises_page.program_cards)
    assert open_count == 2, "ציפינו לשני תרגילים פתוחים, יש " + str(open_count)


def test_the_rest_is_shown_as_names_only(app):
    """
    בדיקה 6ב: שאר התרגילים מוצגים כרשימת שמות בלבד,
    בלי הסברים, בלי שלבים ובלי כפתורי ניגון.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("air")

    assert exercises_page.is_visible(exercises_page.peek_section), "לא מוצגת ההצצה לשאר התרגילים"

    titles = exercises_page.get_peek_titles()
    assert len(titles) > 0, "רשימת ההצצה ריקה"

    # שום תרגיל ברשימה לא מופיע גם כתרגיל פתוח
    open_titles = exercises_page.get_program_titles()
    for title in titles:
        assert title not in open_titles, "התרגיל " + title + " מופיע גם פתוח וגם נעול"

    # אין בהצצה שום תוכן מעבר לשמות
    assert exercises_page.count(app.locator("#peekSection .ex-steps")) == 0, "ההצצה חושפת שלבי תרגול"
    assert exercises_page.count(app.locator("#peekSection .ex-play")) == 0, "ההצצה כוללת כפתורי ניגון"


def test_the_peek_invites_to_a_lesson_with_the_diagnosis(app):
    """
    בדיקה 6ג: כפתור ההצצה פותח וואטסאפ עם האבחון ועם מקור הפנייה.
    """
    main_page = MainPage(app)
    exercises_page = ExercisesPage(app)

    main_page.open_tab("exercises")
    exercises_page.choose_manual_verdict("pressure")

    link = exercises_page.peek_whatsapp.get_attribute("href")
    assert link.startswith("https://wa.me/972544837553"), "הקישור לא מפנה למספר הנכון: " + link

    message = unquote(link.split("?text=", 1)[1])
    assert "יותר מדי לחץ" in message, "האבחון לא נכלל בהודעה: " + message
    assert "אפליקציה" in message, "ההודעה לא מסמנת את מקור הפנייה: " + message
    assert "לקבוע שיעור" in message, "ההודעה לא מבקשת לקבוע שיעור: " + message


def test_reference_note_can_be_changed(app):
    """
    בדיקה 6ד: אפשר לשנות את תו ההתחלה של התרגילים,
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
