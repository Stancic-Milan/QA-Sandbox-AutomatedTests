from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, Optional, List
from config import Config
import logging

class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.wait = WebDriverWait(self.driver, Config.DEFAULT_TIMEOUT)
        self.actions = ActionChains(self.driver)

    def find_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> 'WebElement':
        """
        Find an element with explicit wait
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        :return: WebElement if found
        :raises: TimeoutException if element not found
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise

    def find_visible_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> 'WebElement':
        """
        Find a visible element with explicit wait
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        :return: WebElement if found and visible
        :raises: TimeoutException if element not visible
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element not visible with locator: {locator}")
            raise

    def find_clickable_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> 'WebElement':
        """
        Find a clickable element with explicit wait
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        :return: WebElement if found and clickable
        :raises: TimeoutException if element not clickable
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element not clickable with locator: {locator}")
            raise

    def find_elements(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List['WebElement']:
        """
        Find all elements matching the locator
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        :return: List of WebElements
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"No elements found with locator: {locator}")
            return []

    def click_element(self, locator: Tuple[By, str], timeout: Optional[int] = None):
        """
        Click an element with explicit wait
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        """
        element = self.find_clickable_element(locator, timeout)
        try:
            element.click()
        except:
            # Fallback to JavaScript click if regular click fails
            self.driver.execute_script("arguments[0].click();", element)

    def input_text(self, locator: Tuple[By, str], text: str, clear_first: bool = True, timeout: Optional[int] = None):
        """
        Input text into an element with explicit wait
        :param locator: Tuple of By strategy and locator string
        :param text: Text to input
        :param clear_first: Whether to clear the field first
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        """
        element = self.find_visible_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """
        Get text from an element with explicit wait
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        :return: Text content of the element
        """
        return self.find_visible_element(locator, timeout).text

    def is_element_present(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """
        Check if element is present
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        :return: True if element is present, False otherwise
        """
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_visible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        :return: True if element is visible, False otherwise
        """
        try:
            self.find_visible_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_to_disappear(self, locator: Tuple[By, str], timeout: Optional[int] = None):
        """
        Wait for element to become invisible
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element still visible with locator: {locator}")
            raise

    def hover_over_element(self, locator: Tuple[By, str], timeout: Optional[int] = None):
        """
        Hover over an element
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        """
        element = self.find_visible_element(locator, timeout)
        self.actions.move_to_element(element).perform()

    def scroll_to_element(self, locator: Tuple[By, str], timeout: Optional[int] = None):
        """
        Scroll element into view
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_element_attribute(self, locator: Tuple[By, str], attribute: str, timeout: Optional[int] = None) -> str:
        """
        Get element attribute
        :param locator: Tuple of By strategy and locator string
        :param attribute: Name of the attribute to get
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        :return: Value of the attribute
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)

    def switch_to_frame(self, frame_locator: Tuple[By, str], timeout: Optional[int] = None):
        """
        Switch to iframe
        :param frame_locator: Tuple of By strategy and locator string for the frame
        :param timeout: Optional custom timeout, defaults to Config.DEFAULT_TIMEOUT
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(frame_locator)
            )
        except TimeoutException:
            self.logger.error(f"Frame not available with locator: {frame_locator}")
            raise

    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()
