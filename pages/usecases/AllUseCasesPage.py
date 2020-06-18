from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from pages.usecases.UseCasePage import UseCasePage
from selenium.common.exceptions import TimeoutException


class AllUseCasesPage:

    def __init__(self, driver):

        self.driver = driver

        self.create_use_case_btn = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.CSS_SELECTOR, "a[data-testid='create_use_case_btn']"))
        )

        self.return_to_dashboard_btn = driver.find_element(By.CSS_SELECTOR, "a[href='/dashboard']")

    def get_use_case(self, title):

        saved_use_case = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located(
                (By.XPATH, "//*[text()='{}']".format(title)))
        )
        saved_use_case.click()

        return UseCasePage(self.driver)

    def get_first_use_case(self):

        saved_use_cases = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_all_elements_located(
                (By.CLASS_NAME, "list-group-item"))
        )

        saved_use_cases[0].click()

        return UseCasePage(self.driver)

    def use_case_exist(self, title):
        try:
            WebDriverWait(self.driver, 10).until(
                ExpectedConditions.visibility_of_element_located(
                    (By.XPATH, "//*[text()='{}']".format(title)))
            )
            return True
        except TimeoutException:
            return False
