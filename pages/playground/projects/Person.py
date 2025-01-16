class Person:
    def __init__(self, person_element):

        self.name = person_element.find_element_by_tag_name('b').text
        self.seniority = person_element.find_element_by_tag_name('i').text
        self.technologies = self.get_technologies(person_element)

    def get_technologies(self, person_element):
        all_technologies = []
        technologies = person_element.find_elements_by_tag_name('span')
        for tech in technologies:
            all_technologies.append(tech)

        return all_technologies
