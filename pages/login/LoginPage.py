from selenium.webdriver.common.by import By
from pages.base import BasePage
from config import Config


class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-testid='submit_btn']")
    PROFILE_CARD = (By.CSS_SELECTOR, "div[data-testid='profile_card_id']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.error-message")

    def __init__(self, driver):
        super().__init__(driver)
        self.email_input = self.find_visible_element(self.EMAIL_INPUT)
        self.password_input = self.find_visible_element(self.PASSWORD_INPUT)
        self.submit_btn = self.find_clickable_element(self.SUBMIT_BUTTON)

    def set_email(self, email: str):
        """Set email in the email input field"""
        self.input_text(self.EMAIL_INPUT, email)

    def set_password(self, password: str):
        """Set password in the password input field"""
        self.input_text(self.PASSWORD_INPUT, password)

    def login(self, email: str = None, password: str = None, user_type: str = 'QA'):
        """
        Login with provided credentials or default to specified user type
        :param email: Optional email to override default
        :param password: Optional password to override default
        :param user_type: Type of user to login as (QA, ADMIN, or STANDARD)
        """
        if not email or not password:
            user_creds = getattr(Config.Users, user_type, Config.Users.QA)
            email = email or user_creds['email']
            password = password or user_creds['password']
        
        self.set_email(email)
        self.set_password(password)
        
        try:
            self.click_element(self.SUBMIT_BUTTON)
            self.find_visible_element(self.PROFILE_CARD)
            self.logger.info(f"Successfully logged in as {email}")
        except TimeoutException as e:
            self.logger.error(f"Failed to login as {email}")
            self.take_screenshot(f"login_failure_{email}")
            raise e

    def check_validation(self, email: str, password: str, expected_validation: str) -> bool:
        """
        Check validation message after login attempt
        :param email: Email to test
        :param password: Password to test
        :param expected_validation: Expected validation message
        :return: True if validation message matches expected
        """
        self.set_email(email)
        self.set_password(password)
        self.click_element(self.SUBMIT_BUTTON)

        if "Password" in expected_validation:
            return self.find_password_validation_message(expected_validation)
        else:
            return self.find_email_validation_message(expected_validation)

    def find_email_validation_message(self, expected_validation: str) -> bool:
        """
        Find and verify email validation message
        :param expected_validation: Expected validation message
        :return: True if message matches expected
        """
        validation_element = self.find_visible_element(
            (By.XPATH, f"//*[text()='{expected_validation}']")
        )
        return expected_validation == validation_element.text

    def find_password_validation_message(self, expected_validation: str) -> bool:
        """
        Find and verify password validation message
        :param expected_validation: Expected validation message
        :return: True if message matches expected
        """
        validation_element = self.find_visible_element(
            (By.XPATH, f"//*[text()='{expected_validation}']")
        )
        return expected_validation == validation_element.text

    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.is_element_visible(self.PROFILE_CARD)

    def get_error_message(self) -> str:
        """Get error message if present"""
        return self.get_text(self.ERROR_MESSAGE)
