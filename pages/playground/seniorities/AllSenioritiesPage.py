from pages.playground.PlaygroundBasePage import PlaygroundBasePage


class AllSenioritiesPage(PlaygroundBasePage):

    def __init__(self, driver):

        PlaygroundBasePage.__init__(self, driver)

        self.create_seniority_btn = self.find_create_btn("seniority")

