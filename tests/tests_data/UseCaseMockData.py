from UseCase import UseCase


class UseCaseDataMock:

    def __init__(self):
        self.all_use_cases = []

        use_case_1 = UseCase("Login to QA Sandbox",
                             "Verify that corresponding user can Login to QA Sandbox web app, by entering corresponding email and password.",
                             "Expected result",
                             ["step 1", "step 2", "step 3", "step 4", "step 5"])
        self.all_use_cases.append(use_case_1)
        use_case_2 = UseCase("Open Use Cases from Sandbox Dashboard",
                             "Verify whether is possible to open 'Use Cases' page from 'QA Sandbox' dashboard",
                             "It is possible to navigate from Dashboard to Use Cases page",
                             ["step 1", "step 2"])
        self.all_use_cases.append(use_case_2)
        use_case_3 = UseCase("Create 4 Use Cases",
                             "Verify that is possible to create 4 Test Cases with different titles. Also, populate description, expected result and add necessary steps to cover all validations",
                             "4 use cases are created successful with corresponding data within each field",
                             ["step 1", "step 2", "step 3", "step 4", "step 5", "step 6", "step 7", "step 8"])
        self.all_use_cases.append(use_case_3)
        use_case_4 = UseCase("Edit 4 Use Cases",
                             "Edit all input fields in the created test case by replacing it with string 'This field previously had' + no. of characters in the previous string",
                             "Each use case is successful edited with corresponding message about previous num. of character",
                             ["step 1", "step 2", "step 3", "step 4", "step 5", "step 6", "step 7"])
        self.all_use_cases.append(use_case_4)

        self.too_long_string = "Edit all input fields in the created test case by replacing it " \
                               "Edit all input fields in the created test case by replacing it" \
                               "Edit all input fields in the created test case by replacing it" \
                               "Edit all input fields in the created test case by replacing it" \
                               "Edit all input fields in the created test case by replacing it"
