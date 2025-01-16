import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login import LoginPage
from pages.dashboard import DashboardPage
from config import Config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver():
    """Setup WebDriver for each test"""
    chrome_options = webdriver.ChromeOptions()
    if Config.HEADLESS:
        chrome_options.add_argument('--headless')
    
    # Setup ChromeDriver using webdriver_manager
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    driver.get(Config.BASE_URL)
    driver.maximize_window()
    
    yield driver
    
    # Cleanup
    driver.quit()

@pytest.fixture
def login_page(driver):
    """Create LoginPage instance"""
    return LoginPage(driver)

@pytest.fixture
def dashboard_page(driver):
    """Create DashboardPage instance"""
    return DashboardPage(driver)

class TestLogin:
    """Test suite for login functionality"""

    def test_successful_login_qa_user(self, login_page, dashboard_page):
        """Test successful login with QA user credentials"""
        # Login with default QA user
        login_page.login(user_type='QA')
        
        # Verify successful login
        assert login_page.is_logged_in(), "Login failed - user not logged in"
        assert dashboard_page.get_profile_title(), "Dashboard profile title not found"

    def test_successful_login_admin_user(self, login_page, dashboard_page):
        """Test successful login with admin credentials"""
        # Login with admin user
        login_page.login(user_type='ADMIN')
        
        # Verify successful login
        assert login_page.is_logged_in(), "Login failed - admin not logged in"
        assert dashboard_page.get_profile_title(), "Dashboard profile title not found"

    def test_invalid_email_format(self, login_page):
        """Test login with invalid email format"""
        invalid_email = "invalid_email"
        
        # Attempt login with invalid email
        with pytest.raises(TimeoutException):
            login_page.login(email=invalid_email, password="anypassword")
        
        # Verify error message
        assert "Invalid email format" in login_page.get_error_message()

    def test_invalid_password(self, login_page):
        """Test login with invalid password"""
        # Use valid email but invalid password
        with pytest.raises(TimeoutException):
            login_page.login(
                email=Config.Users.QA['email'],
                password="wrongpassword"
            )
        
        # Verify error message
        assert "Invalid password" in login_page.get_error_message()

    @pytest.mark.parametrize("email,password,expected_message", [
        ("", "password123", "Email is required"),
        ("test@email.com", "", "Password is required"),
        ("", "", "Email is required"),
    ])
    def test_validation_messages(self, login_page, email, password, expected_message):
        """Test validation messages for various invalid inputs"""
        login_page.check_validation(email, password, expected_message)

    def test_navigation_after_login(self, login_page, dashboard_page):
        """Test navigation to different sections after login"""
        # Login
        login_page.login()
        
        # Navigate to different sections
        dashboard_page.navigate_to_use_cases()
        assert "Use Cases" in dashboard_page.get_page_title()
        
        dashboard_page.navigate_to_playground()
        assert "Playground" in dashboard_page.get_page_title()
        
        dashboard_page.navigate_to_reports()
        assert "Reports" in dashboard_page.get_page_title()

    def test_session_persistence(self, login_page, dashboard_page):
        """Test session persistence after page refresh"""
        # Login
        login_page.login()
        
        # Refresh page
        dashboard_page.refresh_page()
        
        # Verify still logged in
        assert login_page.is_logged_in(), "Session lost after page refresh"
