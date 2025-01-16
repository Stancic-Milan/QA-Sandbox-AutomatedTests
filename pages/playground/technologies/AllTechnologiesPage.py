from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.playground.PlaygroundBasePage import PlaygroundBasePage
from selenium.webdriver.support import expected_conditions as ExpectedConditions


class AllTechnologiesPage(PlaygroundBasePage):

    def __init__(self, driver):

        PlaygroundBasePage.__init__(self, driver)

        self.create_technology_btn = self.find_create_btn("technology")

