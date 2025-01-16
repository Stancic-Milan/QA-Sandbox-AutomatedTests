from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from pages.playground.PlaygroundBaseItem import PlaygroundBaseItem


class SeniorityPage(PlaygroundBaseItem):

    def __init__(self, driver):
        PlaygroundBaseItem.__init__(self, driver)
        self.driver = driver

        self.title_input = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.NAME, "seniority_title"))
        )
