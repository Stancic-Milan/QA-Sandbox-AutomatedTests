from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions


class PlaygroundBaseItem:

    def __init__(self, driver):

        self.driver = driver
        self.page_title = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CLASS_NAME, "page-title"))
        ).text
        self.submit_btn = driver.find_element_by_css_selector("button[value='Submit']")

    def set_title(self, title):
        self.title_input.clear()
        self.title_input.send_keys(title)

    def remove(self):

        WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='delete-button']"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CLASS_NAME, "btn-danger"))
        ).click()
