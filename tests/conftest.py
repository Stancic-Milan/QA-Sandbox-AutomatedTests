import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pages.login import LoginPage
from pages.dashboard import DashboardPage
from config import Config
import logging
import os
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)

def pytest_addoption(parser):
    """Add command-line options for test configuration"""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Browser to run tests: chrome, firefox, or edge"
    )
    parser.addoption(
        "--env", 
        action="store", 
        default="qa", 
        help="Environment to run tests: qa, dev, or staging"
    )

@pytest.fixture(scope="session")
def browser(request):
    """Get browser type from command line"""
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def env(request):
    """Get environment from command line"""
    return request.config.getoption("--env")

@pytest.fixture(scope="function")
def driver(browser, env):
    """
    Create WebDriver instance based on browser type
    Scope is function level to ensure clean browser state for each test
    """
    if env:
        os.environ["ENV"] = env
    
    if browser.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument('--headless')
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )
    elif browser.lower() == "edge":
        options = webdriver.EdgeOptions()
        if Config.HEADLESS:
            options.add_argument('--headless')
        driver = webdriver.Edge(
            service=Service(EdgeChromiumDriverManager().install()),
            options=options
        )
    else:  # default to Chrome
        options = webdriver.ChromeOptions()
        if Config.HEADLESS:
            options.add_argument('--headless')
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    
    driver.get(Config.BASE_URL)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

@pytest.fixture
def login_page(driver):
    """Create LoginPage instance"""
    return LoginPage(driver)

@pytest.fixture
def dashboard_page(driver):
    """Create DashboardPage instance"""
    return DashboardPage(driver)

@pytest.fixture(autouse=True)
def test_context(request):
    """Setup test context with logging and reporting"""
    # Start test
    test_name = request.node.name
    logging.info(f"Starting test: {test_name}")
    
    yield
    
    # End test
    logging.info(f"Finished test: {test_name}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extend test reporting with screenshots and additional info
    Automatically capture screenshot on test failure
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if report.failed and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            take_screenshot(driver, item.name)

def take_screenshot(driver, name):
    """Capture screenshot on test failure"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)
    
    screenshot_path = os.path.join(screenshot_dir, f"failure_{name}_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    logging.info(f"Screenshot saved to: {screenshot_path}")

@pytest.fixture(scope="session", autouse=True)
def config_validation():
    """Validate configuration at the start of test session"""
    Config.validate_config()
