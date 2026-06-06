'''Module to handle Warframes'''

if __name__ == "__main__":

    class Warframe():
        '''warframe object'''

        def __init__(
                self,
                name,
                level=0,
                is_mastered=False,
                is_built=False):
            self.name = name
            self.level = level
            self.is_mastered = is_mastered
            self.is_built = is_built
            self.components = {'blueprint': 0,
                               'chassis': 0,
                               'neuroptics': 0,
                               'systems': 0}

        def __str__(self):
            return 'Name: ' + self.name

        def mastered(self):
            '''set warframe to mastered'''
            self.is_mastered = True

        def pc(self):
            '''print components'''
            for k, v in self.components.items():
                print(k, v)

        def level_change(self, new_level):
            '''change warframe level'''
            self.level = new_level
            if self.level == 30:
                self.mastered()

        def add_component(self, component):
            '''increment component'''
            self.components[component] += 1
