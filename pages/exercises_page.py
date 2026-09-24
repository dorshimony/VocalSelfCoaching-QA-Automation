from playwright.sync_api import Page

from pages.base_page import BasePage


class ExercisesPage(BasePage):
    """
    עמוד התרגילים: נעול עד שיש אבחנה, ואז מציג תוכנית מותאמת.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # מסך הנעילה
        self.gate = page.locator("#exGate")
        self.gate_heading = page.locator("#exGate .assess-head h2")
        self.go_to_test_button = page.locator("#goToTestBtn")

        # שורת האבחנה
        self.banner = page.locator("#exBanner")
        self.banner_verdict = page.locator("#exVerdict")
        self.banner_date = page.locator("#exDate")
        self.change_button = page.locator("#changeVerdictBtn")

        # התוכנית
        self.program = page.locator("#programSection")
        self.program_subtitle = page.locator("#programSub")
        self.program_cards = page.locator("#programGrid .ex-card")
        self.program_titles = page.locator("#programGrid .ex-title")
        self.reference_note_select = page.locator("#refNote")
        self.play_buttons = page.locator("#programGrid .ex-play")
        self.done_buttons = page.locator("#programGrid .ex-done")

        # ההצצה לתרגילים שנפתחים בשיעור
        self.peek_section = page.locator("#peekSection")
        self.peek_items = page.locator("#peekList li")
        self.peek_whatsapp = page.locator("#waPeekBtn")

    def choose_manual_verdict(self, verdict):
        self.page.locator('#manualRow .choice[data-verdict="' + verdict + '"]').click()

    def get_program_titles(self):
        return [text.strip() for text in self.program_titles.all_inner_texts()]

    def get_verdict_text(self):
        return self.get_text(self.banner_verdict)

    def get_banner_date_text(self):
        return self.get_text(self.banner_date)

    def play_first_reference_tone(self):
        self.play_buttons.first.click()

    def mark_first_exercise_done(self):
        self.done_buttons.first.click()

    def is_first_exercise_marked_done(self):
        return self.done_buttons.first.is_disabled()

    def select_reference_note(self, value):
        self.reference_note_select.select_option(value)

    def get_selected_reference_note(self):
        return self.reference_note_select.input_value()

    def get_peek_titles(self):
        return [text.strip() for text in self.peek_items.all_inner_texts()]
