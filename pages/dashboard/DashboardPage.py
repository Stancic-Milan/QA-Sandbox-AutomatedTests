from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions


class DashboardPage:

    def __init__(self, driver):

        self.driver = driver
        self.profile_card = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='profile_card_id']"))
        )
        self.use_cases_card = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='use_cases_card_id']"))
        )
        self.playground_card = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='playground_card_id']"))
        )
        self.reports_card = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='reports_card_id']"))
        )
        self.profile_card_title = self.profile_card.find_element_by_class_name("card-title").text.encode(encoding='utf-8')
