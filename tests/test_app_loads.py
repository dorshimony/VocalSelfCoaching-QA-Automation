from pages.main_page import MainPage


def test_app_loads_with_name_and_five_tabs(app):
    """
    בדיקה 1: האפליקציה נטענת, מציגה את שמה ואת חמש הלשוניות,
    והלשונית הפעילה כברירת מחדל היא המבחן הקולי.
    """
    main_page = MainPage(app)

    assert main_page.is_visible(main_page.app_name), "שם האפליקציה לא מוצג"
    assert main_page.get_text(main_page.app_name) == "VocalSelfCoaching"

    tab_names = main_page.get_tab_names()
    assert len(tab_names) == 5, "ציפינו לחמש לשוניות, התקבלו: " + str(len(tab_names))
    assert "מבחן קולי" in tab_names
    assert "תרגילים" in tab_names
    assert "הגייה מיטבית" in tab_names
    assert "חסימות לשון ופה משוחרר" in tab_names
    assert "התקדמות" in tab_names

    assert main_page.get_active_tab_name() == "מבחן קולי"
    assert main_page.is_visible(main_page.panel("test"))
