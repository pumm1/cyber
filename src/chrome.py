import math

import cyberdao as DAO
from dice import roll
from gameHelper import askInput, roll_str, askForRoll, safeCastToInt, EMP, printGreenLine, printRedLine


class Chrome:
    def __init__(self, row):
        self.item = row['item']
        self.description = row['description']

    def toStr(self):
        return f"{self.item} ({self.description})"

def addChrome(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        print('Give name of cybernetic:')
        item = askInput()
        print('Give description:')
        descr = askInput()
        addChromeWithHumanityCost(character, item, descr)
        printGreenLine(f'Chrome added for {character.name}')


def addChromeWithHumanityCost(character, item, descr):
    humanity_cost = handleHumanity(character)
    DAO.addChrome(character.id, item, humanity_cost, descr)


def handleHumanity(char):
    print(f'Reduce humanity for chrome ({roll_str} or <amount>)')
    humanity_cost = 0
    while True:
        i = askInput()
        if i == roll_str:
            (dice, die, bonus) = askForRoll()
            humanity_cost = roll(dice, die) + bonus
            print(f'Rolled {humanity_cost}')
            break
        else:
            cost = safeCastToInt(i)
            if cost > 0:
                humanity_cost = cost
                break

    curr_hum = char.humanity
    t_hum = curr_hum - humanity_cost
    emp = math.ceil(t_hum / 10)
    print(f'Curr emp: {char.attributes[EMP]} - new emp: {emp}')
    printRedLine(f'Current humanity: {curr_hum} - new humanity: {t_hum}')
    DAO.reduceHumanity(char.id, t_hum, emp)
    print(f'Updated humanity and empathy')
    return humanity_cost
