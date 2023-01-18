import math

from colorama import Fore

import cyberdao as DAO
import dice
from skills import skillBonusForSkill, skill_first_aid, difficultyCheckInfo, very_difficult_check, easy_check, average_check, difficult_check, very_difficult_check, nearly_impossible_check
from gameHelper import TECH, askInput, safeCastToInt, checkListCommand, list_str, yes_no, printGreenLine, printRedLine, \
    coloredText
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
        med_tech_bonus = 0  # house rule
        healing_rate = 1
        if character.role == meditechie:
            healing_rate += 1
            med_tech_bonus = math.ceil(character.specialAbility / 2)

        print(f'Patient will heal {healing_rate}hp/day')


        print(f'House rule by programmer: med tech bonus gives (med_tech / 2) bonus to first aid skill and also +1 to healing rate')
        print(f"""Select difficulty of medical check or {list_str} for roll info:
1 = Easy
2 = Average
3 = Difficult
4 = Very difficult
5 = Nearly impossible 
""")
        to_beat = 0
        while True:
            input = askInput()
            i = safeCastToInt(input) - 1
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
            printGreenLine(f'Medical check successful! {info}')
        else:
            printRedLine(f'Medical check unsuccessful! {info}')


#TODO: add other bonuses, e.g. nanomachines
def calculateHealingAmount(days):
    print(f'Include medtech bonus (+1)? {yes_no}')
    healing_rate = 1
    heal_days = safeCastToInt(days)
    i = askInput()
    med_tech_bonus = 0
    while True:
        if i == 'y':
            healing_rate += 1
            printGreenLine('+1 To healing rate')
            med_tech_bonus = heal_days
            break
        elif i == 'n':
            break
    print(f'Use nano machines? (+1) {yes_no}')
    give_nano_bonus = False
    i = askInput()
    while True:
        if i == 'y':
            healing_rate += 1
            printGreenLine('+1 To healing rate')
            give_nano_bonus = True
            break
        elif i == 'n':
            break
    print(f"Use speedheal? (+1/day) {coloredText(Fore.GREEN, 'Give doses')}")
    i = askInput()
    speed_doses = safeCastToInt(i)
    if speed_doses > heal_days:
        speed_doses = heal_days
    healing = heal_days * healing_rate + speed_doses
    nano_bonus = 0
    if give_nano_bonus:
        nano_bonus = heal_days
    printGreenLine(f'{healing}HP recovered in {heal_days} days \n'
                   f'[days healed = {heal_days}, nano machine bonus = {nano_bonus}, speedheal bonus = {speed_doses}, med tech bonus = {med_tech_bonus}]')


def healCharacter(name, amount):
    char = DAO.getCharacterByName(name)
    healing = safeCastToInt(amount)
    if char is not None:
        dmg_taken = char.dmg_taken
        dmg_taken -= healing
        if dmg_taken < 0:
            dmg_taken = 0
        DAO.healCharacter(char.id, dmg_taken)
        print(f"{char.name} {coloredText(Fore.GREEN, f'healed by {healing}')}")
