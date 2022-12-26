import dice
from gameHelper import EMP, very_reliables, reliables, unreliables

combat_no_fumble = 'No fumble, you just screw up'
combat_bad_fumble = 'Oh shit! You manage to wound a member of your own party, or yourself if alone. Roll for location and dmg'
ref_no_fumble = 'No fumble, you just mess up and make an idiot of yourself'
ref_mid_fumble = 'You fall miserably. Take 1 point of dmg (sprain, fall, stumble) and make a vs Stun'
ref_bad_fumble = """You fall abysmally. It is physical action, take 1D6 in damage from falling or strained muscles. 
Also make a roll vs Stun at -1"""
tech_no_fumble = 'No fumble, you just can not get it together'
tech_mid_fumble = """You not only fail, you make it worse! You drop the tools you are working with, 
or you lose your grip and damage the thing you are working with even more. 
Raise the difficulty by 5 and try again."""
tech_bad_fumble = """Wow. Did you ever blow it! You damaged the device or creation beyond repair. Buy a new one."""
emp_no_fumble = 'No fumble, they just will not buy it'
emp_mid_fumble = f"""So much for your people skills. You not only do not convince them; 
you leave them totally cold to any other suggestion you might have (-4 to your next {EMP} die roll)"""
emp_bad_fumble = """Yow! You blew it royally. Do only did not convince them, 
but they are actually violently opposed to anything you want to do. 
Roll 1D10. On 1-4, they actually attempt to do you physical harm."""
int_no_fumble = 'No fumble, you just do not know how to do it. You do not know what is going on. You carry on'
int_mid_fumble = """You do not know anything what is going on and you do not have a clue to do anything about it.
Make a Convince check at -2 to see if anyone else notices how dumb you are."""
int_bad_fumble = """Wow, you are oblivious. You not only do not know what is going on or anything about the subject,
but EVERYONE knows how ignorant you are."""
fumble_table_combat = {
    1: combat_no_fumble,
    2: combat_no_fumble,
    3: combat_no_fumble,
    4: combat_no_fumble,
    5: 'You drop your weapon!',
    6: 'Weapon discharges (Make reliability roll for non-autoweap.) or strikes something harmless',
    7: 'Weapon jams (Make reliability roll for non-autoweap.) or imbeds itself on the ground for one turn',
    8: 'You manage to wound yourself. Roll for location and dmg',
    9: combat_bad_fumble,
    10: combat_bad_fumble
}

fumble_table_ref = {
    1: ref_no_fumble,
    2: ref_no_fumble,
    3: ref_no_fumble,
    4: ref_no_fumble,
    5: ref_mid_fumble,
    6: ref_mid_fumble,
    7: ref_mid_fumble,
    8: ref_bad_fumble,
    9: ref_bad_fumble,
    10: ref_bad_fumble
}

fumble_table_tech = {
    1: tech_no_fumble,
    2: tech_no_fumble,
    3: tech_no_fumble,
    4: tech_no_fumble,
    5: tech_mid_fumble,
    6: tech_mid_fumble,
    7: tech_mid_fumble,
    8: tech_bad_fumble,
    9: tech_bad_fumble,
    10: tech_bad_fumble
}

fumble_table_emp = {
    1: emp_no_fumble,
    2: emp_no_fumble,
    3: emp_no_fumble,
    4: emp_no_fumble,
    5: emp_mid_fumble,
    6: emp_mid_fumble,
    7: emp_bad_fumble,
    8: emp_bad_fumble,
    9: emp_bad_fumble,
    10: emp_bad_fumble
}

fumble_table_int = {
    1: int_no_fumble,
    2: int_no_fumble,
    3: int_no_fumble,
    4: int_no_fumble,
    5: int_mid_fumble,
    6: int_mid_fumble,
    7: int_mid_fumble,
    8: int_bad_fumble,
    9: int_bad_fumble,
    10: int_bad_fumble
}

def rollFumble(area):
    roll = dice.roll(1,10)
    fumble_table = dict([])
    match area:
        case 'combat':
            fumble_table = fumble_table_combat
        case 'ref':
            fumble_table = fumble_table_ref
        case 'tech':
            fumble_table = fumble_table_tech
        case 'emp':
            fumble_table = fumble_table_emp
        case 'int':
            fumble_table = fumble_table_int
        case _:
            print(f'Invalid area for fumble table {area})')
    fumble = fumble_table[roll]
    print(fumble)

def rollWeaponJam(reliability):
    roll = dice.roll(1, 10)
    roll_to_beat = 0
    if very_reliables.__contains__(reliability):
        roll_to_beat = 3
    elif reliables.__contains__(reliability):
        roll_to_beat = 5
    elif unreliables.__contains__(reliability):
        roll_to_beat = 8
    else:
        print(f'Unknown reliability - {reliability}')
    if roll > roll_to_beat:
        print('Phew, weapon does not jam')
    else:
        print('Shit, weapon jams!')
        turns_to_unjam = dice.roll(1, 6)
        print(f'It takes {turns_to_unjam} turn to unjam the weapon')