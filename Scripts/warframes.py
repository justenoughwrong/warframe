'''Module to handle Warframes'''


class Warframe():
    '''warframe object'''

    def __init__(
            self,
            name,
            level,
            is_mastered=False,
            is_built=False):
        self.name = name
        self.level = level
        self.is_mastered = is_mastered
        self.is_built = is_built

    def mastered(self):
        '''set warframe to mastered'''
        self.is_mastered = True

    def level_change(self, new_level):
        '''change warframe level'''
        self.level = new_level
        if self.level == 30:
            self.mastered()


class Components():
    '''for handling warframe components'''

    def __init__(
            self,
            blueprint=False,
            neuroptics=False,
            systems=False,
            chassis=False):
        self.blueprint = blueprint
        self.neuroptics = neuroptics
        self.systems = systems
        self.chassis = chassis

    def build(self, warframe):
        '''build warframe'''
        if self.blueprint and self.neuroptics and self.systems and self.chassis:
            warframe.is_built = True
            warframe.level = 0
            self.blueprint = False
            self.neuroptics = False
            self.systems = False
            self.chassis = False
