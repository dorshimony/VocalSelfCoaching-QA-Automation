from playwright.sync_api import Page


class BasePage:
    """
    מחלקת בסיס לכל דפי האפליקציה.
    כל דף יורש ממנה ומקבל את הפעולות המשותפות.
    """

    def __init__(self, page: Page):
        self.page = page

    def click(self, locator):
        locator.click()

    def get_text(self, locator):
        return locator.inner_text().strip()

    def is_visible(self, locator):
        return locator.is_visible()

    def count(self, locator):
        return locator.count()

    def wait(self, milliseconds):
        self.page.wait_for_timeout(milliseconds)

    def reload(self):
        self.page.reload()
