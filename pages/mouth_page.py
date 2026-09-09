from playwright.sync_api import Page

from pages.base_page import BasePage


class MouthPage(BasePage):
    """
    עמוד "חסימות לשון ופה משוחרר": מצלמה מודדת את פתיחת הלסת ואת השפתיים,
    והמיקרופון מודד את התהודה. שלושה שלבים — פתיחה, הרצה, תוצאות.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # מסך הפתיחה
        self.stage_intro = page.locator("#mouthIntro")
        self.heading = page.locator("#mouthIntro .assess-head h2")
        self.male_button = page.locator('#mouthGenderRow .choice[data-gender="male"]')
        self.female_button = page.locator('#mouthGenderRow .choice[data-gender="female"]')
        self.start_button = page.locator("#startMouthBtn")
        self.hint = page.locator("#mouthHint")

        # מסך ההרצה
        self.stage_run = page.locator("#mouthRun")
        self.video = page.locator("#mouthVideo")
        self.guide_frame = page.locator("#mouthGuide")
        self.step_label = page.locator("#mouthStep")
        self.phase_label = page.locator("#mouthPhase")
        self.instruction = page.locator("#mouthInstruction")
        self.ready_button = page.locator("#mouthReadyBtn")
        self.cancel_button = page.locator("#mouthAbortBtn")
        self.heard_badge = page.locator("#mouthHeard")

        # מסך התוצאות
        self.stage_results = page.locator("#mouthResults")
        self.meters = page.locator("#mouthMeters .meter")
        self.meter_values = page.locator("#mouthMeters .mval")
        self.verdict = page.locator("#mouthVerdict")
        self.verdict_title = page.locator("#mouthVerdict h3")
        self.tips = page.locator("#mouthVerdict .tips li")
        self.banner = page.locator("#mouthBanner")
        self.banner_main = page.locator("#mouthBannerMain")
        self.retest_button = page.locator("#mouthRetestBtn")

    def choose_gender(self, gender):
        self.page.locator('#mouthGenderRow .choice[data-gender="' + gender + '"]').click()

    def is_start_enabled(self):
        return self.start_button.is_enabled()

    def start_check(self):
        self.start_button.click()

    def confirm_frame(self):
        self.ready_button.click()

    def cancel_check(self):
        self.cancel_button.click()

    def get_phase_text(self):
        return self.get_text(self.phase_label)

    def get_hint_text(self):
        return self.get_text(self.hint)

    def get_meter_values(self):
        return [int(text.strip()) for text in self.meter_values.all_inner_texts()]
