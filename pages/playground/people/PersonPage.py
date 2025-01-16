from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions

from pages.playground.PlaygroundBaseItem import PlaygroundBaseItem


class PersonPage(PlaygroundBaseItem):

    def __init__(self, driver):

        PlaygroundBaseItem.__init__(self, driver)
        self.driver = driver

        self.name_input = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.NAME, "people_name"))
        )
        self.drop_down_technologies = self.get_drop_down("technologies")
        self.drop_down_teams = self.get_drop_down("role")
        self.drop_down_seniority = self.get_drop_down("seniority")
        self.technologies_drop_down_arrow = self.get_arrow_drop_down("technologies")

    def set_title(self, title):
        self.name_input.clear()
        self.name_input.send_keys(title)

    def select_seniority(self, value):
        self.drop_down_seniority.click()
        self.select_item(value)
        return self

    def select_technologies(self, technologies):
        self.drop_down_technologies.click()
        for tech in technologies:
            self.select_item(tech)
        self.technologies_drop_down_arrow.click()

    def select_team(self, team):
        self.drop_down_teams.click()
        self.select_item(team)

    def get_selected_seniority(self):
        return self.get_selected(self.drop_down_seniority)

    def get_selected_team(self):
        return self.get_selected(self.drop_down_teams)

    def get_drop_down(self, dd_type):
        drop_down_inner_element = self.driver.find_element_by_name(dd_type)
        return drop_down_inner_element.find_element_by_xpath("./preceding-sibling::div")

    def get_arrow_drop_down(self, dd_type):
        drop_down_inner_element = self.driver.find_element_by_name(dd_type)
        return drop_down_inner_element.find_element_by_xpath("./following-sibling::div[2]")

    def select_item(self, value):
        try:
            drop_down_item = WebDriverWait(self.driver, 10).until(
                ExpectedConditions.element_to_be_clickable((By.CSS_SELECTOR, "span[aria-label='{}']".format(value)))
            )
            drop_down_item.click()
        except TimeoutException:
            print "Value: {} is not selectable in dropdown".format(value)

    def get_selected(self, element):
        selected_item = WebDriverWait(element, 10).until(
                ExpectedConditions.visibility_of_element_located((By.TAG_NAME, "span"))
            )

        return selected_item.text

    def get_selected_technologies(self):
        selected_technologies = []
        selected_items = WebDriverWait(self.drop_down_technologies, 10).until(
                ExpectedConditions.visibility_of_all_elements_located((By.CLASS_NAME, "react-dropdown-select-option-label"))
            )

        for item in selected_items:
            selected_technologies.append(item.text)

        return selected_technologies
