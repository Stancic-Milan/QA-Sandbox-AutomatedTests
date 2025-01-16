class UseCase:

    def __init__(self, title, description, expected_result, steps):
        self.title = title
        self.description = description
        self.expected_result = expected_result
        self.steps = steps