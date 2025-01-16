import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Environment
    ENV = os.getenv('ENV', 'qa')  # Default to 'qa' if not set
    
    # URLs
    BASE_URLS = {
        'qa': 'https://qa-sandbox.ni.htec.rs',
        'dev': 'https://dev-sandbox.ni.htec.rs',
        'staging': 'https://staging-sandbox.ni.htec.rs'
    }
    BASE_URL = BASE_URLS.get(ENV)
    
    # Timeouts (in seconds)
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', 10))
    EXTENDED_TIMEOUT = int(os.getenv('EXTENDED_TIMEOUT', 30))
    
    # WebDriver Settings
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    
    # Test User Credentials
    TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL', 'default@example.com')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD', 'default_password')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Element wait conditions
    POLL_FREQUENCY = 0.5  # How often to check for the element
    ELEMENT_PRESENCE_TIMEOUT = 10  # Timeout for element presence
    ELEMENT_VISIBILITY_TIMEOUT = 10  # Timeout for element visibility
    ELEMENT_CLICKABLE_TIMEOUT = 10  # Timeout for element to be clickable
