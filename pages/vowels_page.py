from playwright.sync_api import Page

from pages.base_page import BasePage


class VowelsPage(BasePage):
    """
    עמוד ההגייה המיטבית: סולמות עולים על חמש הגיות, וטבלת תוצאות.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.stage_intro = page.locator("#vowelIntro")
        self.heading = page.locator("#vowelIntro .assess-head h2")
        self.male_button = page.locator('#vowelGenderRow .choice[data-gender="male"]')
        self.female_button = page.locator('#vowelGenderRow .choice[data-gender="female"]')
        self.start_button = page.locator("#startVowelBtn")
        self.hint = page.locator("#vowelHint")

        self.stage_run = page.locator("#vowelRun")
        self.step_label = page.locator("#vowelStep")
        self.current_vowel = page.locator("#vowelBig")
        self.phase_label = page.locator("#vowelPhase")
        self.skip_button = page.locator("#vowelSkipBtn")
        self.cancel_button = page.locator("#vowelAbortBtn")

        self.stage_results = page.locator("#vowelResults")
        self.results_table = page.locator("#vowelTable")
        self.results_rows = page.locator("#vowelTable tr")
        self.recommendations = page.locator("#vowelRecs .rec")
        self.banner = page.locator("#vowelBanner")

    def choose_gender(self, gender):
        self.page.locator('#vowelGenderRow .choice[data-gender="' + gender + '"]').click()

    def is_start_enabled(self):
        return self.start_button.is_enabled()

    def start_check(self):
        self.start_button.click()

    def skip_vowel(self):
        self.skip_button.click()

    def cancel_check(self):
        self.cancel_button.click()

    def get_current_vowel(self):
        return self.get_text(self.current_vowel)
