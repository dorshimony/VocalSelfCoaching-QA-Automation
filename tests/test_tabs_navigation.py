from pages.main_page import MainPage


def test_each_tab_opens_its_own_panel(app):
    """
    בדיקה 2: לחיצה על כל לשונית פותחת את העמוד שלה
    ומסתירה את כל השאר.
    """
    main_page = MainPage(app)
    tab_names = ["test", "exercises", "vowels", "mouth", "progress"]

    for opened_tab in tab_names:
        main_page.open_tab(opened_tab)

        assert main_page.is_visible(main_page.panel(opened_tab)), \
            "העמוד " + opened_tab + " לא נפתח"

        for other_tab in tab_names:
            if other_tab != opened_tab:
                assert not main_page.is_visible(main_page.panel(other_tab)), \
                    "העמוד " + other_tab + " נשאר גלוי יחד עם " + opened_tab
