from pages.playground.PlaygroundBasePage import PlaygroundBasePage
from pages.playground.projects.AllProjectsPage import AllProjectsPage
from pages.playground.projects.NewProjectPage import NewProjectPage
from pages.playground.projects.ProjectPage import ProjectPage
from tests.test_cases.BaseTest import BaseTest
from pages.playground.technologies.AllTechnologiesPage import AllTechnologiesPage
from pages.playground.technologies.TechnologyPage import TechnologyPage
from pages.playground.seniorities.AllSenioritiesPage import AllSenioritiesPage
from pages.playground.seniorities.SeniorityPage import SeniorityPage
from pages.playground.teams.AllTeamsPage import AllTeamsPage
from pages.playground.teams.TeamPage import TeamPage
from pages.playground.people.AllPeoplePage import AllPeoplePage
from pages.playground.people.PersonPage import PersonPage

import pytest


@pytest.mark.usefixtures("driver_init")
class Test_Remove_Playground_Items(BaseTest):

    @pytest.mark.parametrize("technology", ["JavaScript", "Java"])
    def test_remove_technology(self, technology):
        playground = self.get_playground(self.driver)
        playground.technologies_tab.click()
        all_technologies_page = AllTechnologiesPage(self.driver)
        all_technologies_page.click_item(technology)
        saved_technology = TechnologyPage(self.driver)
        saved_technology.remove()
        assert not all_technologies_page.item_exist(technology), "{} technology is not removed!".format(technology)


    @pytest.mark.parametrize("seniority", ["Junior", "Senior"])
    def test_remove_seniority(self, seniority):
        playground = self.get_playground(self.driver)
        playground.seniorities_tab.click()
        all_seniorities_page = AllSenioritiesPage(self.driver)
        all_seniorities_page.click_item(seniority)
        saved_seniority = SeniorityPage(self.driver)
        saved_seniority.remove()
        assert not all_seniorities_page.item_exist(seniority), "{} technology is not removed!".format(seniority)

    @pytest.mark.parametrize("team", ["Frontend", "Backend"])
    def test_remove_team(self, team):
        playground = self.get_playground(self.driver)
        playground.teams_tab.click()
        all_teams_page = AllTeamsPage(self.driver)
        all_teams_page.click_item(team)
        saved_team = TeamPage(self.driver)
        saved_team.remove()
        assert not all_teams_page.item_exist(team), "{} technology is not removed!".format(team)

    @pytest.mark.parametrize("person", ["Boban Marlijanovic"])
    def test_remove_person(self, person):
        playground = self.get_playground(self.driver)
        playground.people_tab.click()
        people_page = AllPeoplePage(self.driver)
        people_page.click_item(person)
        saved_person = PersonPage(self.driver)
        saved_person.remove()

        assert not people_page.item_exist(person), "{} person is not removed!".format(person)

    @pytest.mark.parametrize("project", ["Dalas"])
    def test_remove_project(self, project):
        playground = self.get_playground(self.driver)
        playground.projects_tab.click()
        all_projects_page = AllProjectsPage(self.driver)
        all_projects_page.click_item(project)
        saved_project = ProjectPage(self.driver)
        saved_project.edit_btn.click()
        edit_project = NewProjectPage(self.driver)
        edit_project.remove()

        assert not all_projects_page.item_exist(project), "{} project is not removed!".format(project)

    def get_playground(self, driver):
        dashboard_page = self.login_to_app(driver)
        dashboard_page.playground_card.click()
        return PlaygroundBasePage(driver)
