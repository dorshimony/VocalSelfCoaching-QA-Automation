from playwright.sync_api import Page

from pages.base_page import BasePage


class VocalTestPage(BasePage):
    """
    עמוד המבחן הקולי: בחירת מין, בדיקת מיקרופון, הרצת הסולמות ותוצאות.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # שלב ההתחלה
        self.stage_intro = page.locator("#stageIntro")
        self.heading = page.locator("#stageIntro .assess-head h2")
        self.male_button = page.locator('#genderRow .choice[data-gender="male"]')
        self.female_button = page.locator('#genderRow .choice[data-gender="female"]')
        self.mic_check_button = page.locator("#micCheckBtn")
        self.mic_check_box = page.locator("#micCheckBox")
        self.mic_check_note = page.locator("#micCheckNote")
        self.start_button = page.locator("#startTestBtn")
        self.hint = page.locator("#testHint")

        # שלב ההרצה
        self.stage_run = page.locator("#stageRun")
        self.step_label = page.locator("#testStep")
        self.phase_label = page.locator("#testPhase")
        self.stop_button = page.locator("#stopEarlyBtn")
        self.cancel_button = page.locator("#abortTestBtn")

        # שלב התוצאות
        self.stage_results = page.locator("#stageResults")
        self.air_value = page.locator("#airVal")
        self.pressure_value = page.locator("#presVal")
        self.results_table_rows = page.locator("#notesTable tr")

        # סיכום אחרי המבחן
        self.result_banner = page.locator("#resultBanner")
        self.banner_verdict = page.locator("#rbVerdict")
        self.retest_button = page.locator("#retestBtn")

    def choose_gender(self, gender):
        self.page.locator('#genderRow .choice[data-gender="' + gender + '"]').click()

    def is_start_enabled(self):
        return self.start_button.is_enabled()

    def start_test(self):
        self.start_button.click()

    def stop_test(self):
        self.stop_button.click()

    def cancel_test(self):
        self.cancel_button.click()

    def choose_verdict(self, verdict):
        self.page.locator('#verdictRow .choice[data-verdict="' + verdict + '"]').click()

    def get_step_text(self):
        return self.get_text(self.step_label)

    def get_hint_text(self):
        return self.get_text(self.hint)
