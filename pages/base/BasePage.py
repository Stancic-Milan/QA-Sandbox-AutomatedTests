from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.select import Select
from typing import Tuple, Optional, List, Any, Union
from config import Config
import logging
import os
from datetime import datetime

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

    def take_screenshot(self, name: str = None) -> str:
        """
        Take a screenshot and save it to the screenshots directory
        :param name: Optional name for the screenshot
        :return: Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = name or f"screenshot_{timestamp}"
        filename = f"{name}.png"
        
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        self.logger.info(f"Screenshot saved to: {filepath}")
        return filepath

    def select_dropdown_by_text(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None):
        """
        Select dropdown option by visible text
        :param locator: Tuple of By strategy and locator string
        :param text: Visible text to select
        :param timeout: Optional custom timeout
        """
        select = Select(self.find_visible_element(locator, timeout))
        select.select_by_visible_text(text)

    def select_dropdown_by_value(self, locator: Tuple[By, str], value: str, timeout: Optional[int] = None):
        """
        Select dropdown option by value
        :param locator: Tuple of By strategy and locator string
        :param value: Value to select
        :param timeout: Optional custom timeout
        """
        select = Select(self.find_visible_element(locator, timeout))
        select.select_by_value(value)

    def get_selected_dropdown_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """
        Get selected dropdown option text
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout
        :return: Selected option text
        """
        select = Select(self.find_visible_element(locator, timeout))
        return select.first_selected_option.text

    def wait_for_page_load(self, timeout: Optional[int] = None):
        """
        Wait for page to complete loading
        :param timeout: Optional custom timeout
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def wait_for_ajax(self, timeout: Optional[int] = None):
        """
        Wait for all AJAX calls to complete
        :param timeout: Optional custom timeout
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        self.wait.until(
            lambda driver: driver.execute_script("return jQuery.active == 0")
        )

    def wait_for_animation(self, timeout: Optional[int] = None):
        """
        Wait for animations to complete
        :param timeout: Optional custom timeout
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        self.wait.until(
            lambda driver: driver.execute_script(
                "return Array.from(document.querySelectorAll(':animated')).length === 0"
            )
        )

    def press_key(self, key: str):
        """
        Press a keyboard key
        :param key: Key to press (e.g., Keys.RETURN, Keys.TAB)
        """
        self.actions.send_keys(getattr(Keys, key.upper())).perform()

    def get_validation_message(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """
        Get HTML5 validation message
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout
        :return: Validation message
        """
        element = self.find_element(locator, timeout)
        return element.get_property('validationMessage')

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript
        :param script: JavaScript to execute
        :param args: Arguments to pass to the script
        :return: Script result
        """
        return self.driver.execute_script(script, *args)

    def highlight_element(self, locator: Tuple[By, str], timeout: Optional[int] = None):
        """
        Highlight an element (useful for debugging)
        :param locator: Tuple of By strategy and locator string
        :param timeout: Optional custom timeout
        """
        element = self.find_element(locator, timeout)
        original_style = element.get_attribute('style')
        self.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 2px solid red; background: yellow;"
        )
        # Reset style after a brief pause
        self.driver.execute_async_script(
            """
            var element = arguments[0];
            var originalStyle = arguments[1];
            var callback = arguments[2];
            setTimeout(function() {
                element.setAttribute('style', originalStyle);
                callback();
            }, 500);
            """,
            element, original_style
        )

    def retry_on_stale(self, function, *args, max_attempts: int = 3, **kwargs) -> Any:
        """
        Retry a function on StaleElementReferenceException
        :param function: Function to retry
        :param args: Function arguments
        :param max_attempts: Maximum number of retry attempts
        :param kwargs: Function keyword arguments
        :return: Function result
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                return function(*args, **kwargs)
            except StaleElementReferenceException:
                attempts += 1
                if attempts == max_attempts:
                    raise
                self.logger.warning(f"Stale element, retrying... (attempt {attempts})")

    def wait_and_accept_alert(self, timeout: Optional[int] = None):
        """
        Wait for and accept alert
        :param timeout: Optional custom timeout
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert.accept()

    def wait_and_dismiss_alert(self, timeout: Optional[int] = None):
        """
        Wait for and dismiss alert
        :param timeout: Optional custom timeout
        """
        timeout = timeout or Config.DEFAULT_TIMEOUT
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert.dismiss()

    def get_page_title(self) -> str:
        """Get the current page title"""
        return self.driver.title

    def get_page_url(self) -> str:
        """Get the current page URL"""
        return self.driver.current_url

    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()
        self.wait_for_page_load()

    def go_back(self):
        """Navigate back to previous page"""
        self.driver.back()
        self.wait_for_page_load()

    def go_forward(self):
        """Navigate forward to next page"""
        self.driver.forward()
        self.wait_for_page_load()
