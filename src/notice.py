import src.cyberdao as DAO
from src.cyberService import awarenessSkill
from src.dice import rollWithCrit
from src.gameHelper import printGreenLine, printRedLine, safeCastToInt
#from logger import Log, log_event, log_neutral, log_neg


#TODO: remove these old ones..?
def addCharacterToQuickNotice(name):
    c = DAO.getCharacterByName(name)
    if c is not None:
        DAO.addCharacterForQuickNoticeCheck(c.id, c.name)


def quickNoticeCheckForCharacters(to_beat):
    roll_to_beat = safeCastToInt(to_beat)
    characters = DAO.charactersForQuickNoticeCheck()
    skill_row = awarenessSkill()
    atr = skill_row['attribute']
    if len(characters) > 0:
        for c in characters:
            skill_bonus = 0
            for skill in c.skills:
                if skill.skill == 'awareness':
                    skill_bonus += skill.lvl
            atr_bonus = c.attributes[atr]
            (roll_res, _) = rollWithCrit(skip_luck=True)
            total = skill_bonus + atr_bonus + roll_res
            roll_info = f'(total = {total}, roll = {roll_res}, skill_bonus = {skill_bonus}, atr_bonus = {atr_bonus})'
            if roll_to_beat <= total:
                printGreenLine(f'{c.name} succeeds in notice check {roll_info}')
            else:
                printRedLine(f'{c.name} fails notice check [total = {total} vs {roll_to_beat}] {roll_info}')
    else:
        print(f'No characters found for quick notice check')


def clearQuickNotices():
    DAO.clearQuickNoticeCheck()
