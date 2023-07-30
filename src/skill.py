from gameHelper import coloredText
from colorama import Fore
class SkillInfo:
    def __init__(self, skill_id, skill, level, attribute):
        self.id = skill_id
        self.skill = skill
        self.lvl = level
        self.attribute = attribute

    def updateSkill(self, lvl_up):
        self.lvl += lvl_up


    def asJson(self):
        resJson = {
            'id': self.id,
            'lvl': self.lvl,
            'skill': self.skill,
            'attribute': self.attribute,
        }

        return resJson


    def toStr(self):
        return f'{coloredText(Fore.LIGHTCYAN_EX, self.skill)} {self.lvl} [{self.attribute}]'
