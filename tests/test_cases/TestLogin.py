# !/usr/bin/python
# coding=utf-8
import pytest
from pages.login.LoginPage import LoginPage
from pages.dashboard.DashboardPage import DashboardPage
from pages.qaSandbox.QASandboxPage import QASandboxPage
from tests.test_cases.BaseTest import BaseTest


@pytest.mark.usefixtures("driver_init")
class Test_Login(BaseTest):

    def test_login_to_sandbox(self):
        qa_sandbox_page = QASandboxPage(self.driver)
        qa_sandbox_page.login_btn.click()
        login_page = LoginPage(self.driver)
        login_page.login("stancicmilan06@gmail.com", "lINKINpARK06")

        dashboard_page = DashboardPage(self.driver)

        assert "Stančić Milan" == dashboard_page.profile_card_title, "Incorrect user is logged in application."

    def test_validate_inputs(self):
        qa_sandbox_page = QASandboxPage(self.driver)
        qa_sandbox_page.login_btn.click()
        login_page = LoginPage(self.driver)
        login_page.submit_btn.click()

        email_incorrect = "someuser@wrongmail.com"
        email_correct = "stancicmilan06@gmail.com"
        password_incorrect = "Password incorrect"
        password_upper_case = "LINKINPARK06"
        password_short = "pass"

        # Empty email and password fields
        assert login_page.find_email_validation_message("Email field is required"), \
            "Validation error message is not visible for empty email."
        assert login_page.find_password_validation_message("Password is required"), \
            "Validation error message is not visible for empty password."

        # Incorrect user and password
        assert login_page.check_validation(email_incorrect, password_incorrect, "User not found"), \
            "Validation error message is not visible for non existing user."

        # Incorrect password with valid user
        assert login_page.check_validation(email_correct, password_incorrect, password_incorrect), \
            "Validation error message is not visible for incorrect password."

        # Check password for case sensitivity with valid user
        assert login_page.check_validation(email_correct, password_upper_case, password_incorrect), \
            "Password is not case sensitive or there isn't expected validation."

        # password must be at least 6 characters long valid user
        assert login_page.check_validation(email_correct, password_short, "Password must be at least 6 characters long"),\
            "Validation for minimum password length is not visible."
