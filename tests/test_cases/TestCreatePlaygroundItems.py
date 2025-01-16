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
class Test_Create_Playground_Items(BaseTest):

    @pytest.mark.parametrize("technology", ["JavaScript", "Java"])
    def test_create_technologies(self, technology):
        playground = self.get_playground(self.driver)
        playground.technologies_tab.click()
        all_technologies_page = AllTechnologiesPage(self.driver)
        all_technologies_page.create_technology_btn.click()
        new_technology = TechnologyPage(self.driver)
        new_technology.set_title(technology)
        new_technology.submit_btn.click()
        assert all_technologies_page.item_exist(technology), "New technology is not created."

    @pytest.mark.parametrize("seniority", ["Junior", "Senior"])
    def test_create_seniority(self, seniority):
        playground = self.get_playground(self.driver)
        playground.seniorities_tab.click()
        all_seniorities_page = AllSenioritiesPage(self.driver)
        all_seniorities_page.create_seniority_btn.click()
        new_seniority = SeniorityPage(self.driver)
        new_seniority.set_title(seniority)
        new_seniority.submit_btn.click()
        assert all_seniorities_page.item_exist(seniority), "New seniority is not created."

    @pytest.mark.parametrize("team", ["Frontend", "Backend"])
    def test_create_team(self, team):
        playground = self.get_playground(self.driver)
        playground.teams_tab.click()
        all_teams_page = AllTeamsPage(self.driver)
        all_teams_page.create_team_btn.click()
        new_team = TeamPage(self.driver)
        new_team.set_title(team)
        new_team.submit_btn.click()
        assert all_teams_page.item_exist(team), "New team is not created."

    @pytest.mark.parametrize("person, team, seniority, technologies",
                             [("Boban Marlijanovic", "Frontend", "Senior", ["JavaScript", "Java"])])
    def test_create_person(self, person, team, seniority, technologies):
        playground = self.get_playground(self.driver)
        playground.people_tab.click()
        people_page = AllPeoplePage(self.driver)
        people_page.create_person_btn.click()
        new_person = PersonPage(self.driver)
        new_person.set_title(person)
        new_person.select_seniority(seniority)
        new_person.select_team(team)
        new_person.select_technologies(technologies)
        new_person.submit_btn.click()
        assert people_page.item_exist(person), "Person {} is not created!".format(person)

        people_page.click_item(person)
        saved_person = PersonPage(self.driver)
        assert saved_person.get_selected_seniority() == seniority, \
            "Seniority {} is not preserved for {} person".format(seniority, person)
        assert saved_person.get_selected_team() == team, \
            "Team {} is not preserved for {} person".format(team, person)
        saved_technologies = saved_person.get_selected_technologies()
        assert len(saved_technologies) == len(technologies), "Technologies are not preserved for {} ".format(person)
        for index in range(len(saved_technologies)):
            assert technologies[index] == saved_technologies[index]

    @pytest.mark.parametrize("project, people",
                             [("Dalas", ["Boban Marlijanovic"])])
    def test_create_project(self, project, people):
        playground = self.get_playground(self.driver)
        playground.projects_tab.click()

        all_projects_page = AllProjectsPage(self.driver)
        all_projects_page.create_project_btn.click()

        new_project = NewProjectPage(self.driver)
        new_project.set_title(project)
        new_project.select_people(people)

        new_project.submit_btn.click()

        assert all_projects_page.item_exist(project), "Project {} is not created!".format(project)

        all_projects_page.click_item(project)
        saved_project = ProjectPage(self.driver)
        assert 1 == len(saved_project.teams)
        assert "Frontend" == saved_project.teams[0].name
        assert people[0] == saved_project.teams[0].people[0].name
        assert "Senior" == saved_project.teams[0].people[0].seniority
        assert 2 == len(saved_project.teams[0].people[0].technologies)

    def get_playground(self, driver):
        dashboard_page = self.login_to_app(driver)
        dashboard_page.playground_card.click()
        return PlaygroundBasePage(driver)
