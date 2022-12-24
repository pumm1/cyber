class SkillInfo:
    def __init__(self, skill, level, attribute):
        self.skill = skill
        self.lvl = level
        self.attribute = attribute


    def toStr(self):
        return f'{self.skill} {self.lvl} [{self.attribute}]'
