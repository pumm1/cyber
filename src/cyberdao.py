import psycopg2.extras
from colorama import Fore

from cyberschema import db, user, password, host, table_skills, table_characters, table_character_skills, \
    table_reputation, table_character_armors, table_character_weapons, table_combat_session, table_character_sp, \
    table_events, table_character_chrome, table_character_statuses, table_character_quick_notice, \
    table_item_atr_bonuses, table_item_bonuses, table_item_skill_bonus
from character import Character
from skill import SkillInfo
from armor import Armor
from gameHelper import EMP, INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, woundEffect, calculateModifierBonus, \
    BODY_TYPE_MOD, t_thrown, coloredText
from chrome import Chrome
from status import Status
from weapon import Weapon

conn = psycopg2.connect(dbname=db, user=user, password=password, host=host)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def clean_fetch_all(rows):
    return [i[0] for i in rows]


insert = 'INSERT INTO'
select_from = 'SELECT * FROM'
delete_from = 'DELETE FROM'
update = 'UPDATE'

character_q = f'{select_from} {table_characters} c '
character_skills_q = f'{select_from} {table_character_skills}'
character_weapons_q = f'{select_from} {table_character_weapons}'
character_armors_q = f'{select_from} {table_character_armors}'
character_chrome_q = f'{select_from} {table_character_chrome}'
character_statuses_q = f'{select_from} {table_character_statuses}'
skills_q = f'{select_from} {table_skills}'


def getAllCharacters():
    cur.execute(character_q)
    rows = cur.fetchall()
    # cleaned_rows = clean_fetch_all(rows)
    print(f'rows fetched: {rows}')
    conn.commit()
    return rows


# TODO: some fuzzy character search logic and to character class
def getCharactersByName(name: str):
    cur.execute(
        f"""{character_q} WHERE c.name like '%{name}%';"""
    )
    rows = cur.fetchall()
    cleaned_rows = clean_fetch_all(rows)
    print(f'rows fetched: {cleaned_rows}')
    conn.commit()


def getCharacterRowByName(name: str):
    cur.execute(
        f"""{character_q} WHERE c.name = '{name}';"""
    )
    char_row = cur.fetchone()
    conn.commit()
    return char_row


def getCharcaterRowById(id):
    cur.execute(
        f"""{character_q} WHERE c.id = {id};"""
    )
    char_row = cur.fetchone()
    conn.commit()

    return char_row


def getCharacter(char_row) -> Character | None:
    character = None
    if char_row is not None:
        id = char_row['id']
        skills = getCharacterSkillsById(id)
        rep_rows = getReputationRows(id)
        reputation = sum(map(lambda rep: (
            rep['rep_level']
        ), rep_rows))
        sp_row = characterSpById(id)
        ev_total = characterEV(id)
        armors = getCharacterArmors(id)
        statuses = getCharacterStatuses(id)

        cybernetics = getCharacterChrome(id)

        dmg_taken = char_row['dmg_taken']

        (ref, int, cool) = woundEffect(dmg_taken, char_row['atr_ref'], char_row['atr_int'], char_row['atr_cool'])

        armor_body_type_bonus = calculateModifierBonus(armors, BODY_TYPE_MOD)

        bodyTypeModifier = char_row['body_type_modifier'] + armor_body_type_bonus

        armor_modifier_bonuses = {
            INT: calculateModifierBonus(armors, INT),
            REF: calculateModifierBonus(armors, REF),
            TECH: calculateModifierBonus(armors, TECH),
            COOL: calculateModifierBonus(armors, COOL),
            ATTR: calculateModifierBonus(armors, ATTR),
            MA: calculateModifierBonus(armors, MA),
            BODY: calculateModifierBonus(armors, BODY),
            LUCK: calculateModifierBonus(armors, LUCK),
            EMP: calculateModifierBonus(armors, EMP),
        }

        attributes = {
            INT: int,
            REF: ref - ev_total + armor_modifier_bonuses[REF],
            TECH: char_row['atr_tech'] + armor_modifier_bonuses[TECH],
            COOL: cool + armor_modifier_bonuses[TECH],
            ATTR: char_row['atr_attr'] + armor_modifier_bonuses[ATTR],
            MA: char_row['atr_ma'] + armor_modifier_bonuses[MA],
            BODY: char_row['atr_body'] + armor_modifier_bonuses[BODY],
            LUCK: char_row['atr_luck'] + armor_modifier_bonuses[LUCK],
            EMP: char_row['atr_emp'] + armor_modifier_bonuses[EMP]
        }

        weapon_rows = characterWeapons(id, body=attributes[BODY])

        character = Character(char_row, skills, reputation, sp_row, weapon_rows, ev_total, armors, statuses,
                              bodyTypeModifier, attributes, cybernetics)
    else:
        print('No character found')

    return character


def getCharacterById(id):
    char_row = getCharcaterRowById(id)
    char = getCharacter(char_row)

    return char

def getCharacterByName(name: str):
    char_row = getCharacterRowByName(name)
    char = getCharacter(char_row)

    return char


def healCharacter(character_id, new_dmg_taken):
    cur.execute(
        f"""{update} {table_characters}
            SET dmg_taken = {new_dmg_taken}
            WHERE id = {character_id};"""
    )
    conn.commit()

def characterSpById(character_id):
    cur.execute(
        f"""SELECT * FROM {table_character_sp} WHERE character_id = {character_id};
        """
    )
    sp_row = cur.fetchone()
    conn.commit()

    return sp_row


def addReputation(character_id, info, rep_level):
    assert 0 < abs(rep_level) <= 10

    cur.execute(
        f"""{insert} {table_reputation} (character_id, known_for, rep_level)
            VALUES ({character_id}, '{info}', {rep_level});"""
    )
    conn.commit()


def getReputationRows(character_id):
    cur.execute(
        f'{select_from} {table_reputation} where character_id = {character_id};'
    )
    rows = cur.fetchall()
    conn.commit()
    return rows


def listCombatInitiative(ascending: bool):
    ordering = 'DESC'
    if ascending:
        ordering = 'ASC'
    cur.execute(
        f"""{select_from} {table_combat_session} cs 
        JOIN {table_characters} c ON cs.character_id = c.id
        ORDER BY cs.initiative {ordering};
        """
    )
    rows = cur.fetchall()
    conn.commit()

    return rows


def addCharacterToCombat(character, initiative):
    cur.execute(
        f"""{insert} {table_combat_session} (character_id, initiative, current)
        VALUES ('{character}', {initiative}, {False});"""
    )
    conn.commit()


def clearCombat():
    cur.execute(
        f"""{delete_from} {table_combat_session};"""
    )
    conn.commit()
    print('Combat table cleared')


def resetCurrentOrder():
    cur.execute(
        f"""{update} {table_combat_session} SET current = {False} WHERE current = {True};"""
    )
    conn.commit()


def setNextInOrder(character_id):
    cur.execute(
        f"""{update} {table_combat_session} SET current = {True} WHERE character_id = '{character_id}';"""
    )
    conn.commit()


def dmgCharacterSP(character_id, body_part, dmg):
    cur.execute(
        f"""{update} {table_character_sp} SET {body_part} = {body_part} - {dmg}
            WHERE character_id = {character_id};
        """
    )
    conn.commit()


def dmgCharacter(character_id, dmg):
    cur.execute(
        f"""{update} {table_characters} SET dmg_taken = dmg_taken + {dmg} WHERE id = {character_id};"""
    )
    conn.commit()


def updateCharSkill(char_id, skill_row, value):
    cur.execute(
        f"""{insert} {table_character_skills} (character_id, skill_id, skill_lvl)
        VALUES ({char_id}, {skill_row['id']}, {value})
        ON CONFLICT(character_id, skill_id)
        DO
            UPDATE SET skill_lvl = cyberpunk.character_skills.skill_lvl + {value};"""
    )
    conn.commit()


def updateCharSpecial(char_id, value):
    cur.execute(
        f"""{update} {table_characters} SET special_ability = special_ability + {value}
        WHERE id = {char_id};"""
    )


def addCharacter(name, role, special_ability, body_type_modifier, atr_int, atr_ref, atr_tech, atr_cool, atr_attr,
                 atr_luck, atr_ma, atr_body, atr_emp):
    cur.execute(
        f"""{insert} {table_characters} 
            (name, role, special_ability, body_type_modifier, humanity,
            atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp, dmg_taken)
            VALUES ('{name}', '{role}', {special_ability}, {body_type_modifier}, {atr_emp * 10},
            {atr_int}, {atr_ref}, {atr_tech}, {atr_cool}, {atr_attr}, {atr_luck}, {atr_ma}, {atr_body}, {atr_emp}, 0)
            RETURNING id;
        """
    )
    new_char = cur.fetchone()

    cur.execute(
        f"""
            {insert} {table_character_sp} 
            (character_id, head, head_max, body, body_max, r_arm, r_arm_max, 
            l_arm, l_arm_max, r_leg, r_leg_max, l_leg, l_leg_max)
            VALUES ({new_char['id']}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            ON CONFLICT DO NOTHING;
            """
    )

    cur.execute(
        f"""{insert} {table_character_weapons} 
        (character_id, item, weapon_type, is_chrome, dice_number, dice_dmg, dmg_bonus, range, rof, 
        clip_size, shots_left, effect_radius, wa, con, reliability, weight)
        VALUES
        ({new_char['id']}, 'unarmed', 'melee', false, 1, 6, 0, 1, 1, 1, 1, 0, 0, 'P', 'ST', 0);
        """
    )
    conn.commit()
    print(f'Character {name} ({role}) added to game')


def characterSkillsFromRows(skill_rows) -> list[SkillInfo]:
    skills = map(lambda skill: (
        SkillInfo(skill['skill'], skill['skill_lvl'], skill['attribute'])
    ), skill_rows)

    return list(skills)


def getSkillById(id):
    cur.execute(
        f"{skills_q} WHERE id = {id};"
    )
    row = cur.fetchone()
    conn.commit()
    return row


def skillsFromRows(skill_rows):
    skills = map(lambda skill: (
        skill['id'], skill
    ), skill_rows)

    return dict(skills)


def skillsByFuzzyLogic(string: str):
    cur.execute(
        f"{skills_q} WHERE skill LIKE '%{string}%' OR description LIKE '%{string}%';"
    )
    rows = cur.fetchall()
    skills = skillsFromRows(rows)
    conn.commit()
    return skills


def skillByName(s_name: str):
    cur.execute(
        f"{skills_q} WHERE skill = '{s_name}';"
    )
    skill = cur.fetchone()

    conn.commit()
    return skill


def getCharacterSkillsById(id) -> list[SkillInfo]:
    cur.execute(
        f"""{character_skills_q} cs 
        JOIN {table_skills} s ON cs.skill_id = s.id
        WHERE cs.character_id = {id};"""
    )
    skill_rows = cur.fetchall()
    conn.commit()
    skills = characterSkillsFromRows(skill_rows)

    return skills


def listSkillsByAttribute(atr: str):
    cur.execute(
        f"""{skills_q} WHERE attribute = '{atr.upper()}';"""
    )
    skill_rows = cur.fetchall()
    conn.commit()

    skills = skillsFromRows(skill_rows)
    return skills


def getSkillByName(skill_name):
    cur.execute(
        f"""{skills_q} WHERE skill = '{skill_name}';"""
    )
    skill_row = cur.fetchone()
    conn.commit()

    if skill_row is None:
        print(f'Skill not found by name {skill_name}')
    return skill_row


def listSkills():
    cur.execute(
        f"""{skills_q};"""
    )
    skill_rows = cur.fetchall()
    conn.commit()

    skills = skillsFromRows(skill_rows)
    return skills


def addArmor(character_id, item, sp, body_parts, ev, atr_dict, skill_bonuses: list = []):
    bod_parts = map(lambda bp: (
        f"'{bp}'"
    ), body_parts)
    bod_parts_str = ', '.join(bod_parts)

    item_bonus_id = insertItemBonuses(atr_dict, skill_bonuses)

    cur.execute(
        f"""{insert} {table_character_armors} (character_id, item, sp, body_parts, ev, item_bonus_id)
            VALUES ({character_id}, '{item}', {sp}, ARRAY[{bod_parts_str}], {ev}, {item_bonus_id});"""
    )
    conn.commit()
    for body_part in body_parts:
        updateCharacterMaxSp(character_id, body_part, sp)


def insertItemBonuses(atr_bonuses_dict: dict, skill_bonuses: list):
    print(f'..... atr bonuses: {atr_bonuses_dict}')
    print(f'..... atr bonus for REF: {atr_bonuses_dict.get(REF, 0)}')
    cur.execute(
        f"""{insert} {table_item_atr_bonuses} 
        (body_type_modifier, atr_int, atr_ref, atr_tech, atr_cool, atr_attr, 
        atr_luck, atr_ma, atr_body, atr_emp)
        VALUES ({atr_bonuses_dict.get(BODY_TYPE_MOD, 0)}, {atr_bonuses_dict.get(INT, 0)},
        {atr_bonuses_dict.get(REF, 0)}, {atr_bonuses_dict.get(TECH, 0)}, {atr_bonuses_dict.get(COOL, 0)}, 
        {atr_bonuses_dict.get(ATTR, 0)}, {atr_bonuses_dict.get(LUCK, 0)}, {atr_bonuses_dict.get(MA, 0)}, 
        {atr_bonuses_dict.get(BODY, 0)}, {atr_bonuses_dict.get(EMP, 0)})
        RETURNING id;
        """)
    atr_id = cur.fetchone()['id']

    cur.execute(
        f"""{insert} {table_item_bonuses} (item_atr_id)
        VALUES ({atr_id}) RETURNING id;"""
    )

    bonus_id = cur.fetchone()['id']

    for bonus in skill_bonuses:
        cur.execute(
            f"""{insert} {table_item_skill_bonus} (item_bonus_id, skill_id, skill_bonus)
            VALUES ({bonus_id}, {bonus.skill_id}, {bonus.skill_bonus})
            """
        )
    conn.commit()

    return bonus_id



#potentially bonuses could be for multiple skills, each being own row
def getItemSkillBonuses(bonus_id):
    cur.execute(
        f"""
        {select_from} {table_item_bonuses} b 
        JOIN {table_item_skill_bonus} sb on b.id = sb.item_bonus_id
        WHERE b.id = {bonus_id};
        """
    )
    skill_bonus_rows = cur.fetchall()
    conn.commit()

    return skill_bonus_rows


#all bonuses are in single row for item
def getItemAtrBonuses(bonus_id):
    cur.execute(
        f"""
            {select_from} {table_item_bonuses} b 
            JOIN {table_item_atr_bonuses} ab on b.id = ab.item_bonus_id
            WHERE b.id = {bonus_id};
            """
    )
    atr_bonuses = cur.fetchone()
    conn.commit()

    return atr_bonuses




def getCharacterArmors(character_id):
    cur.execute(
        f"""{character_armors_q} a
        JOIN {table_item_bonuses} b 
        ON a.item_bonus_id = b.id
        JOIN {table_item_atr_bonuses} ab
        ON b.item_atr_id = ab.id
        WHERE character_id = {character_id};"""
    )
    rows = cur.fetchall()
    conn.commit()
    armors = []
    for row in rows:
        armor = Armor(row)
        armors.append(armor)
    return armors


def getCharacterChrome(character_id):
    cur.execute(
        f"""{character_chrome_q} where character_id = {character_id};"""
    )
    rows = cur.fetchall()
    cybernetics = []
    conn.commit()
    for row in rows:
        chrome = Chrome(row)
        cybernetics.append(chrome)
    return cybernetics


def repairCharacterSP(character_id):
    cur.execute(
        f"""{update} {table_character_sp} SET head = head_max, body = body_max, r_arm = r_arm_max, l_arm = l_arm_max,
            r_leg = r_leg_max, l_leg = l_leg_max
            WHERE character_id = {character_id};
            """
    )
    conn.commit()


def updateCharacterMaxSp(character_id, body_part, amount):
    cur.execute(
        f"""{update} {table_character_sp} SET {body_part}_max = {body_part}_max + {amount}, {body_part} = {body_part} + {amount}
        WHERE character_id = {character_id};
        """
    )
    conn.commit()


def reduceHumanity(character_id, humanity, emp):
    cur.execute(
        f"""{update} {table_characters} SET humanity = {humanity}, atr_emp = {emp}
            WHERE id = {character_id};
        """
    )
    conn.commit()


def addEvent(event):
    cur.execute(
        f"""{insert} {table_events} (event) VALUES ('{event}');"""
    )
    conn.commit()


def listEvents():
    cur.execute(
        f"""{select_from} {table_events};"""
    )
    rows = cur.fetchall()
    conn.commit()

    return rows


def addWeapon(character_id, item, weapon_type, is_chrome, dice_number, dice_dmg, dmg_bonus, range, rof, clip_size,
              effect_radius, wa, con, reliability, weight):
    cur.execute(
        f"""{insert} {table_character_weapons} 
            (character_id, item, weapon_type, is_chrome, dice_number, dice_dmg, dmg_bonus, range, rof, clip_size, 
            shots_left, effect_radius, wa, con, reliability, weight)
            VALUES
            ({character_id}, '{item}', '{weapon_type}', {is_chrome}, {dice_number}, {dice_dmg}, {dmg_bonus}, {range}, 
            {rof}, {clip_size}, {clip_size}, {effect_radius}, {wa}, '{con}', '{reliability}', {weight});
        """
    )
    conn.commit()


def addChrome(character_id, item, humanity_cost, description):
    cur.execute(
        f"""
        {insert} {table_character_chrome} (character_id, item, humanity_cost, description)
        VALUES ({character_id}, '{item}', {humanity_cost}, '{description}');
        """
    )
    conn.commit()


def getWeaponById(weapon_id):
    cur.execute(
        f"""{character_weapons_q} WHERE id = {weapon_id}"""
    )
    row = cur.fetchone()
    conn.commit()
    weapon = None
    if row is None:
        print(f'Weapon not found by id = {weapon_id}')
    else:
        weapon = Weapon(row, None)

    return weapon


def updateShotsInClip(wpn_id, shots_in_clip):
    cur.execute(
        f"""{update} {table_character_weapons} SET shots_left = {shots_in_clip} WHERE id = {wpn_id};"""
    )
    conn.commit()


def deleteThrown(wpn_id):
    cur.execute(
        f"""{delete_from} {table_character_weapons} WHERE id = {wpn_id};"""
    )
    conn.commit()


def characterWeapons(character_id, body: int) -> list:
    cur.execute(
        f"""
        {character_weapons_q} WHERE character_id = {character_id};
        """
    )
    rows = cur.fetchall()
    conn.commit()

    def weaponMapFn(w):
        if w['weapon_type'] == t_thrown:
            weight = w['weight'] - 1
            if weight < 0:
                weight = 0
            range = body*3
            reduce_range = weight * 10
            range = range - reduce_range
            if range < 0:
                range = 0
            return Weapon(w, custom_range=range)
        else:
            return Weapon(w, None)

    weapons = map(lambda w: (
        weaponMapFn(w)
    ), rows)

    return list(weapons)


def characterEV(character_id) -> int:
    cur.execute(
        f"""
            {character_armors_q} WHERE character_id = {character_id};
            """
    )
    rows = cur.fetchall()
    conn.commit()
    evs = map(lambda a: (
        a['ev']
    ), rows)

    ev_total = sum(evs)
    return ev_total


def getArmor(character_id, id):
    cur.execute(
        f"""{character_armors_q} WHERE id = {id} AND character_id = {character_id};"""
    )
    row = cur.fetchone()
    conn.commit()
    if row is None:
        print(f'Armor not found by id {id} for character {character_id}')
    return row


def deleteCharacterArmor(character_id, armor_id):
    a_row = getArmor(character_id, armor_id)
    if a_row is not None:
        armor = Armor(a_row)
        for body_part in armor.body_parts:
            updateCharacterMaxSp(character_id, body_part, -1 * armor.sp)
        cur.execute(
            f"""{delete_from} {table_character_armors} WHERE character_id = {character_id} AND id = {armor_id};"""
        )
        conn.commit();
        print(f'Character armor removed')


def addCharacterStatus(character_id, status, effect):
    cur.execute(
        f"""{insert} {table_character_statuses} (character_id, status, effect)
        VALUES ({character_id}, '{status}', '{effect}');"""
    )
    conn.commit()
    print('Status added')


def getCharacterStatuses(character_id):
    cur.execute(
        f"""{select_from} {table_character_statuses}
        WHERE character_id = {character_id};"""
    )
    rows = cur.fetchall()
    conn.commit()

    statuses = map(lambda row: (
        Status(row)
    ), rows)
    return statuses


def removeStatus(status_id, character_id):
    cur.execute(
        f"""{delete_from} {table_character_statuses}
        WHERE id = {status_id} AND character_id = {character_id};
        """
    )
    conn.commit()
    print('Status removed')


def addCharacterForQuickNoticeCheck(character_id, name):
    cur.execute(
        f"""{insert} {table_character_quick_notice} (character_id)
        VALUES ({character_id});"""
    )
    conn.commit()
    print(f'{coloredText(Fore.GREEN, name)} added to quick notice check')

def charactersForQuickNoticeCheck():
    cur.execute(
        f"""{select_from} {table_character_quick_notice};"""
    )
    rows = cur.fetchall()
    conn.commit()

    characters = []
    for row in rows:
        c = getCharacterById(row['character_id'])
        characters.append(c)
    return characters


def clearQuickNoticeCheck():
    cur.execute(
        f"""{delete_from} {table_character_quick_notice};"""
    )
    conn.commit()
    print(f'Quick notice checks cleared')
