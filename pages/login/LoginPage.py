from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.action_chains import ActionChains

class LoginPage:

    def __init__(self, driver):

        self.driver = driver
        self.email_input = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.NAME, "email"))
        )
        self.password_input = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.NAME, "password"))
        )
        self.submit_btn = WebDriverWait(self.driver, 10).until(
            ExpectedConditions.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='submit_btn']"))
        )

    def set_email(self, email):

        self.email_input.clear()
        self.email_input.send_keys(email)

    def set_password(self, password):

        self.password_input.clear()
        self.password_input.send_keys(password)

    def login(self, email, password):

        self.set_email(email)
        self.set_password(password)
        try:
            ActionChains(self.driver).move_to_element(self.submit_btn).click().perform()
            WebDriverWait(self.driver, 10).until(
                ExpectedConditions.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div[data-testid='profile_card_id']"))
            )
        except TimeoutException:
            login_page = LoginPage(self.driver)
            login_page.submit_btn.click()

    def check_validation(self, email, password, expected_validation):

        self.set_email(email)
        self.set_password(password)
        ActionChains(self.driver).move_to_element(self.submit_btn).click().perform()

        if "Password" in expected_validation:
            return self.find_password_validation_message(expected_validation)
        else:
            return self.find_email_validation_message(expected_validation)

    def find_email_validation_message(self, expected_validation):

        # find expected validation
        WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.XPATH, "//*[text()='{}']".format(expected_validation)))
        )
        # return true if message refers to email field
        return expected_validation == self.email_input.find_element_by_xpath("./following-sibling::div").text

    def find_password_validation_message(self, expected_validation):

        # find expected validation
        WebDriverWait(self.driver, 10).until(
            ExpectedConditions.visibility_of_element_located((By.XPATH, "//*[text()='{}']".format(expected_validation)))
        )
        # return true if message refers to password field
        return expected_validation == self.password_input.find_element_by_xpath("./following-sibling::div").text
