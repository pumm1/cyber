import math

import cyberdao as DAO
import dice
from skills import skillBonusForSkill, skill_first_aid, difficultyCheckInfo, very_difficult_check, easy_check, average_check, difficult_check, very_difficult_check, nearly_impossible_check
from gameHelper import TECH, askInput, safeCastToInt, checkListCommand, list_str
from roles import meditechie

#values are changed from offial rules a bit, then they would be 0.5 and 1
default_healing_rate = 1
default_medtech_healing_rate = 2

bonus_per_item = 1 #e.g. speedheal, other drugs
#TODO: ks speedheal, nanotech

#serious wound = -2 REF
#critical wound = -4 REF
#mortal wound = bedridden, requires constant care

def medicalCheck(name, given_roll):
    character = DAO.getCharacterByName(name)
    if character is not None:
        tech_bonus = character.attributes[TECH]
        first_aid_bonus = skillBonusForSkill(character.skills, skill_first_aid)
        med_tech_bonus = 0
        if character.role == meditechie:
            print(f'Patient will heal 1hp/day')
            med_tech_bonus = math.ceil(character.specialAbility / 2)
        else:
            print('Patient will heal')


        print(f'House rule by programmer: med tech bonus gives (med_tech / 2) bonus to first aid skill')
        print(f"""Select difficulty of medical check or {list_str} for roll info:
0 = Easy
1 = Average
2 = Difficult
3 = Very difficult
4 = Nearly impossible 
""")
        to_beat = 0
        while True:
            input = askInput()
            i = safeCastToInt(input)
            if checkListCommand(input):
                difficultyCheckInfo()
            elif i == 0:
                to_beat = easy_check
                break
            elif i == 1:
                to_beat = average_check
                break
            elif i == 2:
                to_beat = difficult_check
                break
            elif i == 3:
                to_beat = very_difficult_check
                break
            elif i == 4:
                to_beat = nearly_impossible_check
                break

        t_roll = safeCastToInt(given_roll)
        if t_roll > 0:
            roll = t_roll
        else:
            roll = dice.rollWithCrit()
        total = tech_bonus + first_aid_bonus + med_tech_bonus + roll

        info = f'Roll total ({total}) vs {to_beat} [roll = {roll}, first aid bonus = {first_aid_bonus}, medtech bonus = {med_tech_bonus}, tech_bonus = {tech_bonus}]'
        if total >= to_beat:
            print(f'Medical check successful! {info}')
        else:
            print(f'Medical check unsuccessful! {info}')