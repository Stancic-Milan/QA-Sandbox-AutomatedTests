import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Environment
    ENV = os.getenv('ENV', 'qa')  # Default to 'qa' if not set
    
    # URLs based on environment
    BASE_URLS = {
        'qa': os.getenv('QA_BASE_URL'),
        'dev': os.getenv('DEV_BASE_URL'),
        'staging': os.getenv('STAGING_BASE_URL')
    }
    BASE_URL = BASE_URLS.get(ENV)
    
    # Timeouts (in seconds)
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', 10))
    EXTENDED_TIMEOUT = int(os.getenv('EXTENDED_TIMEOUT', 30))
    
    # WebDriver Settings
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    
    # Test User Credentials
    class Users:
        QA = {
            'email': os.getenv('QA_USER_EMAIL'),
            'password': os.getenv('QA_USER_PASSWORD')
        }
        ADMIN = {
            'email': os.getenv('ADMIN_USER_EMAIL'),
            'password': os.getenv('ADMIN_USER_PASSWORD')
        }
        STANDARD = {
            'email': os.getenv('STANDARD_USER_EMAIL'),
            'password': os.getenv('STANDARD_USER_PASSWORD')
        }
    
    # API Credentials
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    
    # Database Configuration
    DB_CONFIG = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME')
    }
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Element wait conditions
    POLL_FREQUENCY = 0.5  # How often to check for the element
    ELEMENT_PRESENCE_TIMEOUT = 10  # Timeout for element presence
    ELEMENT_VISIBILITY_TIMEOUT = 10  # Timeout for element visibility
    ELEMENT_CLICKABLE_TIMEOUT = 10  # Timeout for element to be clickable

    # Test Execution Settings
    RETRY_COUNT = int(os.getenv('RETRY_COUNT', 2))  # Number of times to retry failed tests
    PARALLEL_WORKERS = int(os.getenv('PARALLEL_WORKERS', 2))  # Number of parallel test workers
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    VIDEO_RECORDING = os.getenv('VIDEO_RECORDING', 'False').lower() == 'true'

    # Report Settings
    REPORT_TITLE = os.getenv('REPORT_TITLE', 'Test Automation Report')
    REPORT_TEMPLATE = os.getenv('REPORT_TEMPLATE', 'report_template.html')

    @classmethod
    def validate_config(cls):
        """Validate that all required environment variables are set"""
        required_vars = {
            'QA_USER_EMAIL': cls.Users.QA['email'],
            'QA_USER_PASSWORD': cls.Users.QA['password'],
            f'{cls.ENV.upper()}_BASE_URL': cls.BASE_URL
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                f"Please check your .env file and ensure all required variables are set."
            )
