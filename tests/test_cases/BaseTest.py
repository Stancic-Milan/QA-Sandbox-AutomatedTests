import pytest
from selenium import webdriver
from pages.login.LoginPage import LoginPage
from pages.dashboard.DashboardPage import DashboardPage
from pages.qaSandbox.QASandboxPage import QASandboxPage


class BaseTest:

    #@pytest.fixture(params=["firefox", "chrome"], scope="function")
    @pytest.fixture(params=["chrome"], scope="function")
    def driver_init(self, request):
        if request.param == "chrome":
            web_driver = webdriver.Chrome()
        if request.param == "firefox":
            web_driver = webdriver.Firefox()
        request.cls.driver = web_driver
        yield
        web_driver.close()

    def login_to_app(self, driver):
        qa_sandbox_page = QASandboxPage(driver)
        qa_sandbox_page.login_btn.click()

        login_page = LoginPage(driver)
        login_page.login("stancicmilan06@gmail.com", "lINKINpARK06")

        return DashboardPage(driver)
