from selenium.webdriver.common.by import By
from pages.base import BasePage
from config import Config


class DashboardPage(BasePage):
    # Locators
    PROFILE_CARD = (By.CSS_SELECTOR, "div[data-testid='profile_card_id']")
    USE_CASES_CARD = (By.CSS_SELECTOR, "div[data-testid='use_cases_card_id']")
    PLAYGROUND_CARD = (By.CSS_SELECTOR, "div[data-testid='playground_card_id']")
    REPORTS_CARD = (By.CSS_SELECTOR, "div[data-testid='reports_card_id']")
    CARD_TITLE = (By.CLASS_NAME, "card-title")

    def __init__(self, driver):
        super().__init__(driver)
        # Wait for dashboard to load by checking for profile card
        self.profile_card = self.find_visible_element(self.PROFILE_CARD)
        self.use_cases_card = self.find_visible_element(self.USE_CASES_CARD)
        self.playground_card = self.find_visible_element(self.PLAYGROUND_CARD)
        self.reports_card = self.find_visible_element(self.REPORTS_CARD)
        self.profile_card_title = self.profile_card.find_element(*self.CARD_TITLE).text.encode(encoding='utf-8')

    def navigate_to_use_cases(self):
        """Navigate to Use Cases page"""
        self.click_element(self.USE_CASES_CARD)

    def navigate_to_playground(self):
        """Navigate to Playground page"""
        self.click_element(self.PLAYGROUND_CARD)

    def navigate_to_reports(self):
        """Navigate to Reports page"""
        self.click_element(self.REPORTS_CARD)

    def get_profile_title(self) -> str:
        """Get the profile card title text"""
        return self.get_text(self.CARD_TITLE)
