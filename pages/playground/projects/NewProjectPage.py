from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions

from pages.playground.PlaygroundBaseItem import PlaygroundBaseItem


class NewProjectPage(PlaygroundBaseItem):

    def __init__(self, driver):

        PlaygroundBaseItem.__init__(self, driver)
        self.driver = driver

        self.title_input = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.NAME, "project_title"))
        )

        self.people_drop_down = self.driver.find_element_by_class_name("react-dropdown-select")

        self.people_drop_down_arrow = self.driver.find_element_by_class_name("react-dropdown-select-dropdown-handle")

    def select_people(self, people):
        self.people_drop_down.click()
        for person in people:
            self.select_person(person)
        self.people_drop_down_arrow.click()

    def select_person(self, person):
        try:
            drop_down_item = WebDriverWait(self.driver, 10).until(
                ExpectedConditions.element_to_be_clickable((By.CSS_SELECTOR, "span[aria-label='{}']".format(person)))
            )
            drop_down_item.click()
        except TimeoutException:
            print "Value: {} is not selectable in dropdown".format(person)