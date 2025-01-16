from pages.playground.PlaygroundBasePage import PlaygroundBasePage


class AllTeamsPage(PlaygroundBasePage):

    def __init__(self, driver):

        PlaygroundBasePage.__init__(self, driver)

        self.create_team_btn = self.find_create_btn("role")
