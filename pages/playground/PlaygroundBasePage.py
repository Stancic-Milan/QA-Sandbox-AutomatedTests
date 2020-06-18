from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class PlaygroundBasePage:

    def __init__(self, driver):

        self.driver = driver
        self.page_title = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CLASS_NAME, "page-title"))
        ).text

        self.return_to_dashboard_btn = driver.find_element(By.CSS_SELECTOR, "a[href='/dashboard']")

        self.projects_tab = driver.find_element_by_id('test0')
        self.teams_tab = driver.find_element_by_id('test1')
        self.people_tab = driver.find_element_by_id('test2')
        self.seniorities_tab = driver.find_element_by_id('test3')
        self.technologies_tab = driver.find_element_by_id('test4')

    def get_num_of_items(self):
        try:
            items = WebDriverWait(self.driver, 10).until(
                ExpectedConditions.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "list-group-item"))
            )
            return len(items)
        except NoSuchElementException:
            return 0

    def click_first_item(self):
        items = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_all_elements_located(
                (By.CLASS_NAME, "list-group-item"))
        )
        items[0].click()

    def click_item(self, title):
        item = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located(
                (By.XPATH, "//*[text()='{}']".format(title)))
        )

        item.click()

    def item_exist(self, title):
        try:
            WebDriverWait(self.driver, 2).until(
                ExpectedConditions.visibility_of_element_located(
                    (By.XPATH, "//*[text()='{}']".format(title)))
            )
            return True
        except TimeoutException:
            return False

    def find_create_btn(self, button_name):
        return WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((
                By.CSS_SELECTOR, "a[href='/create-{}']".format(button_name)))
        )
