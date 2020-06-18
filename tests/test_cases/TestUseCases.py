import pytest
from pages.usecases.AllUseCasesPage import AllUseCasesPage
from pages.usecases.UseCasePage import UseCasePage
from tests.test_cases.BaseTest import BaseTest
from tests.tests_data.UseCaseMockData import UseCaseDataMock


@pytest.mark.usefixtures("driver_init")
class Test_Use_Cases(BaseTest):

    def test_create_use_cases(self):

        mock_data = UseCaseDataMock()

        dashboard_page = self.login_to_app(self.driver)
        dashboard_page.use_cases_card.click()

        for test_case_index in range(len(mock_data.all_use_cases)):

            data = mock_data.all_use_cases[test_case_index]

            all_use_cases_page = AllUseCasesPage(self.driver)
            all_use_cases_page.create_use_case_btn.click()

            self.create_new_use_case(self.driver, data.title, data.description, data.expected_result, data.steps)

            saved_use_case = all_use_cases_page.get_first_use_case()

            assert data.title == saved_use_case.get_title(), "Title is not saved correctly."
            assert data.description == saved_use_case.get_description(), "Description is not saved correctly."
            assert data.expected_result == saved_use_case.get_expected_result(), \
                "Expected result is not saved correctly."
            assert len(data.steps) == saved_use_case.get_num_of_steps(), \
                "Number of saved steps is not correct."

            for step_index in range(len(data.steps)):
                assert data.steps[step_index] == saved_use_case.get_step_value(step_index), "Step value is not correct."

            saved_use_case.return_to_dashboard_btn.click()

    def test_use_case_validations(self):

        mock_data = UseCaseDataMock()

        dashboard_page = self.login_to_app(self.driver)
        dashboard_page.use_cases_card.click()

        all_use_cases_page = AllUseCasesPage(self.driver)
        all_use_cases_page.create_use_case_btn.click()

        new_use_case = UseCasePage(self.driver)
        new_use_case.submit_btn.click()

        assert new_use_case.find_title_validation_message("Title is required"), \
            "Validation 'Title is required.' is not displayed"
        assert new_use_case.find_expected_result_validation_message("Expected result is required"), \
            "Expected result is empty."
        assert new_use_case.find_step_validation_message("There must be at least one test step"), \
            "There is no test step validation"

        new_use_case.set_title("Tit")
        new_use_case.set_expected_result("Exp")
        new_use_case.set_step_value(0, mock_data.too_long_string)
        new_use_case.submit_btn.click()
        assert new_use_case.find_title_validation_message("Title needs to be between 5 and 255"), \
            "Validation 'Title needs to be between 5 and 255' is not displayed."
        assert new_use_case.find_expected_result_validation_message(
            "Expected results needs to be between 5 and 255"), \
            "Validation 'Expected results needs to be between 5 and 255' is not displayed."
        assert new_use_case.find_step_validation_message("Test step needs to be between 0 and 255"), \
            "There is no test step validation"

    def test_edit_use_cases(self):
        dashboard_page = self.login_to_app(self.driver)
        dashboard_page.use_cases_card.click()
        mock_data = UseCaseDataMock()

        for test_case_index in range(len(mock_data.all_use_cases)):

            data = mock_data.all_use_cases[test_case_index]
            all_use_cases_page = AllUseCasesPage(self.driver)
            use_case_by_title = all_use_cases_page.get_use_case(data.title)

            expected_value = "This field previously had {} characters"
            self.edit_use_case(use_case_by_title, expected_value)

            edited_use_case = all_use_cases_page.get_use_case(expected_value.format(len(data.title)))

            assert expected_value.format(len(data.title)) == edited_use_case.get_title(), \
                "Title is not correctly edited."
            assert expected_value.format(len(data.description)) == edited_use_case.get_description(), \
                "Description is not correctly edited."
            assert expected_value.format(len(data.expected_result)) == edited_use_case.get_expected_result(), \
                "Expected result is not correctly edited."
            assert len(data.steps) == edited_use_case.get_num_of_steps(), \
                "Number of steps is not as expected after edit."

            for step_index in range(len(data.steps)):
                assert expected_value.format(len(data.steps[step_index])) == edited_use_case.get_step_value(step_index), \
                    "Step value is not correctly edited."

            edited_use_case.return_to_dashboard_btn.click()

    def test_delete_use_cases_by_title(self):

        dashboard_page = self.login_to_app(self.driver)
        dashboard_page.use_cases_card.click()

        all_use_cases_page = AllUseCasesPage(self.driver)
        all_use_cases_page.create_use_case_btn.click()

        self.create_new_use_case(self.driver, "Use case for delete", "Description",
                                 "Test will be deleted.", ["Add use case", "Delete use case"])

        assert all_use_cases_page.use_case_exist("Use case for delete"), "Delete use case is not added."

        use_case = all_use_cases_page.get_use_case("Use case for delete")
        use_case.remove()

        assert not all_use_cases_page.use_case_exist("Use case for delete"), "Use case is not removed."

    def edit_use_case(self, use_case, new_value):

        # Edit each field with 'This field previously had x number of characters'
        new_title = new_value.format(len(use_case.get_title()))
        new_description = new_value.format(len(use_case.get_description()))
        new_expected_result = new_value.format(len(use_case.get_expected_result()))

        use_case.set_title(new_title)
        use_case.set_description(new_description)
        use_case.set_expected_result(new_expected_result)

        for step_index in range(use_case.get_num_of_steps()):
            new_step_value = new_value.format(len(use_case.get_step_value(step_index)))
            use_case.set_step_value(step_index, new_step_value)

        use_case.submit_btn.click()

    def create_new_use_case(self, driver, title, description, expected_result, steps):
        new_use_case = UseCasePage(driver)

        new_use_case.set_title(title)
        new_use_case.set_description(description)
        new_use_case.set_expected_result(expected_result)
        new_use_case.set_steps(steps)

        new_use_case.submit_btn.click()
