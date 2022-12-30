import cyberdao as DAO
from gameHelper import askInput, safeCastToInt, body_parts_armor_info, body_parts, body_part_head, body_part_body, \
    body_part_r_leg, body_part_l_leg, body_part_r_arm, body_part_l_arm, uniqueArr
from cyberschema import r_leg_column, l_leg_column, r_arm_column, l_arm_column


def checkBodyPartNum(i):
    num = safeCastToInt(i)
    body_part = None
    if num == 1:
        body_part = body_part_head
    elif num == 2:
        body_part = body_part_body
    elif num == 3:
        body_part = l_arm_column
    elif num == 4:
        body_part = r_arm_column
    elif num == 5:
        body_part = r_leg_column
    elif num == 6:
        body_part = l_leg_column
    return body_part

def addArmorForCharacter(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        print(f'Give armor name:')
        item = askInput()
        print(f'Give SP:')
        sp = 0
        while True:
            sp_i = askInput()
            sp = safeCastToInt(sp_i)
            if sp > 0:
                break;
        print(f'Give covered body parts: (end with -1 if there is at least one body part)')
        print(body_parts_armor_info)
        covered_parts = []
        while len(covered_parts) < 6:
            input = askInput()
            if (body_parts.__contains__(input)):
                covered_parts = uniqueArr(covered_parts.append(input))
            elif input == '-1' and len(covered_parts) > 0:
                break
            else:
                input = checkBodyPartNum(input)
                if input is not None:
                    covered_parts.append(input)
                    covered_parts = uniqueArr(covered_parts)

        DAO.addArmor(character.id, item, sp, covered_parts)
        print(f'Armor added!')
