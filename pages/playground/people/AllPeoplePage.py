from pages.playground.PlaygroundBasePage import PlaygroundBasePage


class AllPeoplePage(PlaygroundBasePage):

    def __init__(self, driver):

        PlaygroundBasePage.__init__(self, driver)

        self.create_person_btn = self.find_create_btn("person")
