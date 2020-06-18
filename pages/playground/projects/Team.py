from pages.playground.projects.Person import Person


class Team:
    def __init__(self, team_element):

        self.name = team_element.find_element_by_tag_name('h5').text

        self.people = self.crate_people(team_element)

    def crate_people(self, team_element):

        all_people = []

        person_elements = team_element.find_elements_by_class_name('col')

        for person_element in person_elements:
            person = Person(person_element)
            all_people.append(person)

        return all_people