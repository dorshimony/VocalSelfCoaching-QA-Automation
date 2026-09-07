from playwright.sync_api import Page

from pages.base_page import BasePage


class ProgressPage(BasePage):
    """
    עמוד ההתקדמות: אריחי סיכום, גרף שבועי ויומן אימונים.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.streak_value = page.locator("#statStreak")
        self.total_minutes_value = page.locator("#statTotal")
        self.sessions_value = page.locator("#statSessions")

        self.chart = page.locator("#chartSvg")
        self.chart_bars = page.locator("#chartSvg rect")
        self.chart_labels = page.locator("#chartSvg text")

        self.log_items = page.locator("#logList li")
        self.log_empty_message = page.locator("#logList .empty")

    def get_total_minutes(self):
        return int(self.get_text(self.total_minutes_value))

    def get_sessions_count(self):
        return int(self.get_text(self.sessions_value))

    def get_streak(self):
        return int(self.get_text(self.streak_value))

    def get_log_texts(self):
        return [text.strip() for text in self.log_items.all_inner_texts()]
