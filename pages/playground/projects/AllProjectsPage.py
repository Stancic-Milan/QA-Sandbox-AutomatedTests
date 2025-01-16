from pages.playground.PlaygroundBasePage import PlaygroundBasePage


class AllProjectsPage(PlaygroundBasePage):

    def __init__(self, driver):

        PlaygroundBasePage.__init__(self, driver)

        self.create_project_btn = self.find_create_btn("project")
