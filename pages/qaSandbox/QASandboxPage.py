from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions


class QASandboxPage:

    def __init__(self, driver):

        self.driver = driver

        self.driver.get("https://qa-sandbox.apps.htec.rs/")

        self.login_btn = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
