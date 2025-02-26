from colorama import Fore

from src.gameHelper import askInput, safeCastToInt, yes_no, printGreenLine, coloredText

default_healing_rate = 1
default_medtech_healing_rate = 2

bonus_per_item = 1 #e.g. speedheal, other drugs
#TODO: ks speedheal, nanotech

#serious wound = -2 REF
#critical wound = -4 REF
#mortal wound = bedridden, requires constant care


#TODO: add other bonuses, e.g. nanomachines
#TODO: add to app?
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
