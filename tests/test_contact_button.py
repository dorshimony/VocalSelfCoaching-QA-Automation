from pages.main_page import MainPage


def test_contact_button_opens_whatsapp_in_a_new_tab(app):
    """
    בדיקה 11: כפתור יצירת הקשר מוצג, מפנה לוואטסאפ של המורה
    עם הודעה מוכנה מראש, ונפתח בלשונית חדשה.
    """
    main_page = MainPage(app)
    contact_button = app.locator("#contactBtn")

    assert main_page.is_visible(contact_button), "כפתור יצירת הקשר לא מוצג"
    assert "צרו קשר" in main_page.get_text(contact_button), \
        "הכיתוב על הכפתור לא מזמין ליצירת קשר: " + main_page.get_text(contact_button)

    link = contact_button.get_attribute("href")
    assert link.startswith("https://wa.me/972544837553"), "הקישור לא מפנה למספר הנכון: " + link
    assert "?text=" in link, "לא צורפה הודעה מוכנה מראש לקישור"

    assert contact_button.get_attribute("target") == "_blank", "הקישור לא נפתח בלשונית חדשה"
    assert "noopener" in (contact_button.get_attribute("rel") or ""), \
        "חסר noopener בקישור שנפתח בלשונית חדשה"


def test_contact_button_is_available_on_every_tab(app):
    """
    בדיקה 11ב: הכפתור זמין מכל הלשוניות, לא רק מהראשונה.
    """
    main_page = MainPage(app)
    contact_button = app.locator("#contactBtn")

    for tab_name in ["test", "exercises", "vowels", "mouth", "progress"]:
        main_page.open_tab(tab_name)
        assert main_page.is_visible(contact_button), \
            "כפתור יצירת הקשר נעלם בלשונית " + tab_name
