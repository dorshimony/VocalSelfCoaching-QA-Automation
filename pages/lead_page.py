from playwright.sync_api import Page

from pages.base_page import BasePage


class LeadPage(BasePage):
    """
    כל מה שקשור להבאת תלמידים: מסך הפתיחה, קריאת הפעולה שאחרי האבחון,
    ההזמנה לשיעור שבתוך כל תרגיל, וטופס ההשארת פרטים.
    """

    WHATSAPP_PREFIX = "https://wa.me/972544837553"

    def __init__(self, page: Page):
        super().__init__(page)

        # מסך הפתיחה
        self.hero = page.locator("#heroCard")
        self.hero_title = page.locator("#heroCard h2")
        self.hero_lead = page.locator("#heroCard .hero-lead")
        self.hero_start_button = page.locator("#heroStartBtn")
        self.teacher_name = page.locator("#heroCard .teacher .tt b")
        self.teacher_role = page.locator("#heroCard .teacher .tt span")

        # קריאת הפעולה שאחרי האבחון
        self.result_cta = page.locator("#resultCta")
        self.result_title = page.locator("#rcTitle")
        self.result_plain = page.locator("#rcPlain")
        self.result_next = page.locator("#rcNext")
        self.result_whatsapp = page.locator("#waResultBtn")

        # ההזמנה שבתוך התרגילים
        self.exercise_invites = page.locator("#programGrid .ex-cta")
        self.exercise_whatsapp = page.locator("#programGrid .ex-wa")

        # טופס השארת פרטים
        self.lead_form = page.locator("#leadForm")
        self.lead_name = page.locator("#leadName")
        self.lead_phone = page.locator("#leadPhone")
        self.lead_error = page.locator("#leadErr")
        self.lead_send_button = page.locator("#leadSendBtn")

    def start_from_hero(self):
        self.hero_start_button.click()

    def fill_lead_form(self, name, phone):
        self.lead_name.fill(name)
        self.lead_phone.fill(phone)

    def send_lead_form(self):
        self.lead_send_button.click()

    def get_error_text(self):
        return self.get_text(self.lead_error)

    def get_result_link(self):
        return self.result_whatsapp.get_attribute("href")

    def get_first_exercise_link(self):
        return self.exercise_whatsapp.first.get_attribute("href")
