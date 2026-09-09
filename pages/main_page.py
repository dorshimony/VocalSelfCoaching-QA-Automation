from playwright.sync_api import Page

from pages.base_page import BasePage


class MainPage(BasePage):
    """
    הכותרת העליונה והניווט בין חמש הלשוניות.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.app_name = page.locator("header.top .brand h1")
        self.subtitle = page.locator("header.top .brand .sub")
        self.all_tabs = page.locator("nav.tabs button")

    def tab(self, name):
        return self.page.locator('nav.tabs button[data-tab="' + name + '"]')

    def panel(self, name):
        return self.page.locator("#panel-" + name)

    def open_tab(self, name):
        self.tab(name).click()

    def get_tab_names(self):
        return [text.strip() for text in self.all_tabs.all_inner_texts()]

    def get_active_tab_name(self):
        return self.page.locator("nav.tabs button.active").inner_text().strip()
