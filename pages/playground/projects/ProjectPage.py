from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.common.exceptions import NoSuchElementException

from pages.playground.projects.Team import Team


class ProjectPage:

    def __init__(self, driver):

        self.driver = driver

        self.title = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.TAG_NAME, "h3 b"))
        ).text

        self.edit_btn = self.driver.find_element_by_xpath("//a[contains(@href, '/editProjects')]")

        self.teams = self.create_teams()

    def create_teams(self):

        all_teams = []

        team_elements = self.driver.find_elements_by_class_name('col-md-12')

        for team_element in team_elements:
            team = Team(team_element)
            all_teams.append(team)

        return all_teams

    def get_num_of_teams(self):
        try:
            items = WebDriverWait(self.driver, 10).until(
                ExpectedConditions.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "col-md-12"))
            )
            return len(items)
        except NoSuchElementException:
            return 0

    def get_teams(self):
        return WebDriverWait(self.driver, 10).until(
                ExpectedConditions.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "col-md-12"))
            )

    def click_item(self, title):
        item = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located(
                (By.XPATH, "//*[text()='{}']".format(title)))
        )

        item.click()
