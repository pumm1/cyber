import sys
from collections import defaultdict
import psycopg
from colorama import Fore

from cyberschema import db, user, password, host, table_skills, table_characters, table_character_skills, \
    table_reputation, table_character_armors, table_character_weapons, table_combat_session, table_character_sp, \
    table_events, table_character_chrome, table_character_statuses, table_character_quick_notice, \
    table_item_atr_bonuses, table_item_bonuses, table_item_skill_bonus, table_character_notice_rolls, \
    table_system_version, expected_system_version, table_campaigns
from character import Character, CharacterShort
from skill import SkillInfo
from armor import Armor
from gameHelper import EMP, INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, woundEffect, calculateModifierBonus, \
    BODY_TYPE_MOD, t_thrown, coloredText, body_type_mod, atr_int, atr_tech, atr_ref, atr_cool, atr_attr, atr_luck, \
    atr_ma, atr_body, atr_emp, init_bonus, INIT_BONUS
from chrome import Chrome
from roles import solo
from status import Status
from weapon import Weapon
from psycopg.rows import dict_row

conn = psycopg.connect(dbname=db, user=user, password=password, host=host, row_factory=dict_row)


def clean_fetch_all(rows):
    return [i[0] for i in rows]


insert_into = 'INSERT INTO'
select_from = 'SELECT * FROM'
delete_from = 'DELETE FROM'
update = 'UPDATE'

character_q = f'{select_from} {table_characters} c '
character_skills_q = f'{select_from} {table_character_skills}'
character_weapons_q = f'{select_from} {table_character_weapons}'
character_armors_q = f'{select_from} {table_character_armors}'
character_armors_with_bonuses_q = f"""
{character_armors_q} a
JOIN {table_item_bonuses} b 
ON a.item_bonus_id = b.id
JOIN {table_item_atr_bonuses} ab
ON b.item_atr_id = ab.id
"""
character_chrome_q = f'{select_from} {table_character_chrome}'
character_statuses_q = f'{select_from} {table_character_statuses}'
skills_q = f'{select_from} {table_skills}'


def check_system_version():
    with conn.cursor() as cur:
        row = cur.execute(f'{select_from} {table_system_version}').fetchone()
        conn.commit()

        version = row['version']
        if version != expected_system_version:
            print(f'System version is set wrong. Got {version}, but expected {expected_system_version}')
            sys.exit()
        else:
            print(f'System version is up to date')


def getAllCharacters():
    with conn.cursor() as cur:
        rows = cur.execute(character_q).fetchall()
        # cleaned_rows = clean_fetch_all(rows)
        #print(f'rows fetched: {rows}')
        conn.commit()
        return rows


def getCharacterRowByName(name: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""{character_q} WHERE c.name = '{name}';"""
        )
        char_row = cur.fetchone()
        conn.commit()
    return char_row


def getCharcaterRowById(id):
    with conn.cursor() as cur:
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
        cybernetics = getCharacterChrome(id)
        cybernetic_skill_bonus_ids = []
        chrome_item_bonus_ids = []
        for c in cybernetics:
            for skill_bonus in c.skill_bonuses:
                cybernetic_skill_bonus_ids.append(skill_bonus.skill_id)
                chrome_item_bonus_ids.append(skill_bonus.item_bonus_id)
        skills = getCharacterSkillsById(id)
        rep_rows = getReputationRows(id)
        reputation = sum(map(lambda rep: (
            rep['rep_level']
        ), rep_rows))
        sp_row = characterSpById(id)
        ev_total = characterEV(id)
        armors = getCharacterArmors(id)
        statuses = getCharacterStatuses(id)

        dmg_taken = char_row['dmg_taken']

        (ref, int, cool) = woundEffect(dmg_taken, char_row['atr_ref'], char_row['atr_int'], char_row['atr_cool'])

        item_body_type_bonus = calculateModifierBonus(armors, cybernetics, BODY_TYPE_MOD)
        item_init_bonus = calculateModifierBonus(armors, cybernetics, INIT_BONUS)

        bodyTypeModifier = char_row['body_type_modifier'] + item_body_type_bonus
        initiativeBonus = char_row['initiative_bonus'] + item_init_bonus

        item_modifier_bonuses = {
            INT: calculateModifierBonus(armors, cybernetics, INT),
            REF: calculateModifierBonus(armors, cybernetics, REF),
            TECH: calculateModifierBonus(armors, cybernetics, TECH),
            COOL: calculateModifierBonus(armors, cybernetics, COOL),
            ATTR: calculateModifierBonus(armors, cybernetics, ATTR),
            MA: calculateModifierBonus(armors, cybernetics, MA),
            BODY: calculateModifierBonus(armors, cybernetics, BODY),
            LUCK: calculateModifierBonus(armors, cybernetics, LUCK),
            EMP: calculateModifierBonus(armors, cybernetics, EMP),
        }

        attributes = {
            INT: int + item_modifier_bonuses[INT],
            REF: ref - ev_total + item_modifier_bonuses[REF],
            TECH: char_row['atr_tech'] + item_modifier_bonuses[TECH],
            COOL: cool + item_modifier_bonuses[COOL],
            ATTR: char_row['atr_attr'] + item_modifier_bonuses[ATTR],
            MA: char_row['atr_ma'] + item_modifier_bonuses[MA],
            BODY: char_row['atr_body'] + item_modifier_bonuses[BODY],
            LUCK: char_row['atr_luck'] + item_modifier_bonuses[LUCK],
            EMP: char_row['atr_emp'] + item_modifier_bonuses[EMP]
        }

        weapon_rows = characterWeapons(id, body=attributes[BODY])

        character = Character(
            char_row, skills, reputation, sp_row, weapon_rows, ev_total, armors, statuses,
            bodyTypeModifier, initiativeBonus, attributes, cybernetics
        )
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

def listCharacters() -> list[CharacterShort]:
    characters = []
    with conn.cursor() as cur:
        cur.execute(
            f""" {select_from} {table_characters};"""
        )
        rows = cur.fetchall()
        characters = map(lambda c_row: (
            CharacterShort(c_row)
        ), rows)
        conn.commit()
    return characters


def updateCharacterIp(character_id, ip_amount):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_characters}
           SET ip = ip + {ip_amount}
           WHERE id = {character_id};"""
        )
        conn.commit()


def updateCharacterMoney(character_id, money):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_characters}
            SET money = {money}
            WHERE id = {character_id};"""
        )
        conn.commit()


def healCharacter(character_id, new_dmg_taken):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_characters}
            SET dmg_taken = {new_dmg_taken}
            WHERE id = {character_id};"""
        )
        conn.commit()


def characterSpById(character_id):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT * FROM {table_character_sp} WHERE character_id = {character_id};
                            """
        )
        sp_row = cur.fetchone()
        conn.commit()

        return sp_row


def addReputation(character_id, info, rep_level):
    assert 0 < abs(rep_level) <= 10
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_reputation} (character_id, known_for, rep_level)
                VALUES ({character_id}, '{info}', {rep_level});"""
        )
        conn.commit()


def getReputationRows(character_id):
    with conn.cursor() as cur:
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

    with conn.cursor() as cur:
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
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_combat_session} (character_id, initiative, current)
                            VALUES ('{character}', {initiative}, {False});"""
        )
        conn.commit()


def clearCombat():
    with conn.cursor() as cur:
        cur.execute(
            f"""{delete_from} {table_combat_session};"""
        )
        conn.commit()


def resetCurrentOrder():
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_combat_session} SET current = {False} WHERE current = {True};"""
        )
        conn.commit()


def setNextInOrder(character_id):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_combat_session} SET current = {True} WHERE character_id = '{character_id}';"""
        )
        conn.commit()


def dmgCharacterSP(character_id, body_part):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_character_sp} SET {body_part} = {body_part} - {1}
                WHERE character_id = {character_id};
                            """
        )
        conn.commit()


def dmgCharacter(character_id, dmg):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_characters} SET dmg_taken = dmg_taken + {dmg} WHERE id = {character_id};"""
        )
        conn.commit()


def updateCharSkill(char_id, skill_row, value):
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_character_skills} (character_id, skill_id, skill_lvl)
                VALUES ({char_id}, {skill_row['id']}, {value})
                ON CONFLICT(character_id, skill_id)
                DO
                UPDATE SET skill_lvl = cyberpunk.character_skills.skill_lvl + {value};"""
        )
        conn.commit()


def updateCharSpecial(char_id, role, value):
    initiative_bonus_added = 0
    if role == solo:
        initiative_bonus_added = value
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_characters} 
                            SET 
                                special_ability = special_ability + {value},
                                initiative_bonus = initiative_bonus + {initiative_bonus_added}
                            WHERE id = {char_id};"""
        )
        conn.commit()



def addCharacter(name, role, special_ability, body_type_modifier, atr_int, atr_ref, atr_tech, atr_cool, atr_attr,
                 atr_luck, atr_ma, atr_body, atr_emp, initiative_bonus=0):
    if role == solo:
        initiative_bonus = special_ability

    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_characters} 
            (name, role, special_ability, body_type_modifier, humanity, ip, initiative_bonus,
            atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp, dmg_taken, emp_max)
            VALUES ('{name}', '{role}', {special_ability}, {body_type_modifier}, {atr_emp * 10}, 0, {initiative_bonus},
            {atr_int}, {atr_ref}, {atr_tech}, {atr_cool}, {atr_attr}, {atr_luck}, {atr_ma}, {atr_body}, {atr_emp}, 0, {atr_emp})
            RETURNING id;"""
        )
        new_char = cur.fetchone()

        cur.execute(
            f"""
                                {insert_into} {table_character_sp} 
                                (character_id, head, head_max, body, body_max, r_arm, r_arm_max, 
                                l_arm, l_arm_max, r_leg, r_leg_max, l_leg, l_leg_max)
                                VALUES ({new_char['id']}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                                ON CONFLICT DO NOTHING;
                                """
        )

        cur.execute(
            f"""{insert_into} {table_character_weapons} 
                            (character_id, item, weapon_type, is_chrome, dice_number, dice_dmg, dmg_bonus, range, rof, 
                            clip_size, shots_left, effect_radius, wa, con, reliability, weight, divide_by)
                            VALUES
                            ({new_char['id']}, 'unarmed', 'melee', false, 1, 6, 0, 1, 1, 1, 1, 0, 0, 'P', 'ST', 0, 1);
                            """
        )
        conn.commit()
    character_id = new_char['id']
    print(f'Character {name} ({role}) added to game')
    return character_id



def characterSkillsFromRows(is_original: bool, skill_rows) -> list[SkillInfo]:
    skills = list()
    for skill in skill_rows:
        skill_lvl = skill['skill_lvl']
        if skill_lvl is None:
            skill_lvl = 0

        s = SkillInfo(skill['skill_id'], skill['skill'], skill_lvl, skill['attribute'], is_original)
        skills.append(s)

    skill_groups = defaultdict(list)
    for skill in skills:
        skill_groups[skill.id].append(skill)
    return list(skills)


def getSkillById(id):
    with conn.cursor() as cur:
        cur.execute(
            f"{skills_q} WHERE id = {id};"
        )
        row = cur.fetchone()
        if row is None:
            print(f'Skill not found by id = {id}')
        conn.commit()
        return row


def skillsFromRows(skill_rows):
    skills = map(lambda skill: (
        skill['id'], skill
    ), skill_rows)

    return dict(skills)


def skillsByFuzzyLogic(string: str):
    with conn.cursor() as cur:
        cur.execute(
            f"{skills_q} WHERE skill LIKE '%{string}%' OR description LIKE '%{string}%';"
        )
        rows = cur.fetchall()
        skills = skillsFromRows(rows)
        conn.commit()
        return skills


def skillByName(s_name: str):
    with conn.cursor() as cur:
        cur.execute(
            f"{skills_q} WHERE skill = '{s_name}';"
        )
        skill = cur.fetchone()
        conn.commit()
        return skill


def getCharacterSkillsById(id) -> list[SkillInfo]:
    with conn.cursor() as cur:
        char_skills_q = f"""{character_skills_q} cs
                        JOIN {table_skills} s ON cs.skill_id = s.id
                        JOIN {table_characters} c ON cs.character_id = c.id
                        WHERE c.id = {id};
                        """

        item_bonus_skills_q = f"""SELECT skill_bonus as skill_lvl, * FROM {table_item_skill_bonus} isb
                        JOIN {table_item_bonuses} ib ON isb.item_bonus_id = ib.id
                        JOIN {table_character_chrome} cc on cc.item_bonus_id = ib.id
                        JOIN {table_characters} c ON c.id = cc.character_id
                        JOIN {table_skills} s ON isb.skill_id = s.id
                        WHERE c.id = {id};
                        """

        cur.execute(char_skills_q)
        char_skill_rows = cur.fetchall()
        cur.execute(item_bonus_skills_q)
        item_bonus_skill_rows = cur.fetchall()
        skills = characterSkillsFromRows(is_original=True, skill_rows=char_skill_rows)
        item_bonus_skills = characterSkillsFromRows(is_original=False, skill_rows=item_bonus_skill_rows)

        original_skill_lvl_dict = dict([])
        for skill in skills:
            t_skill = original_skill_lvl_dict.get(skill.id)
            if t_skill is None:
                original_skill_lvl_dict[skill.id] = skill.lvl

        all_skills = skills + item_bonus_skills

        skill_dict = dict([])

        for skill in all_skills:
            t_skill = skill_dict.get(skill.id)
            t_orig_skill_lvl = original_skill_lvl_dict.get(skill.id)
            if t_orig_skill_lvl is not None:
                skill.updateOriginalLevel(t_orig_skill_lvl)

            if t_skill is None:
                skill_dict[skill.id] = skill
            else:
                t_skill.updateSkill(skill.lvl)
                skill_dict[skill.id] = t_skill
    conn.commit()

    return skill_dict.values()

def updateCharacterName(character_id, name):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_characters} SET name = '{name}' WHERE id = {character_id};"""
        )
        conn.commit()

def listSkillsByAttribute(atr: str):
    skills = []
    with conn.cursor() as cur:
        cur.execute(
            f"""{skills_q} WHERE attribute = '{atr.upper()}';"""
        )
        skill_rows = cur.fetchall()
        skills = skillsFromRows(skill_rows)
        conn.commit()
    return skills


def getSkillByName(skill_name):
    with conn.cursor() as cur:
        cur.execute(
            f"""{skills_q} WHERE skill = '{skill_name}';"""
        )
        skill_row = cur.fetchone()

        if skill_row is None:
            print(f'Skill not found by name {skill_name}')
        conn.commit()
        return skill_row


def listSkills():
    skills = []
    with conn.cursor() as cur:
        cur.execute(
            f"""{skills_q};"""
        )
        skill_rows = cur.fetchall()
        skills = skillsFromRows(skill_rows)
    conn.commit()
    return skills


def addArmor(character_id, item, sp, body_parts, ev, atr_dict: dict, skill_bonuses: list = []):
    bod_parts = map(lambda bp: (
        f"'{bp}'"
    ), body_parts)
    bod_parts_str = ', '.join(bod_parts)

    with conn.cursor() as cur:
        item_bonus_id = insertItemBonusesReturningBonusId(dict(atr_dict), skill_bonuses)

        cur.execute(
            f"""{insert_into} {table_character_armors} (character_id, item, sp, body_parts, ev, item_bonus_id)
                                VALUES ({character_id}, '{item}', {sp}, ARRAY[{bod_parts_str}], {ev}, {item_bonus_id});"""
        )
        for body_part in body_parts:
            updateCharacterMaxSp(character_id, body_part, sp)
        conn.commit()
        return item_bonus_id


def insertItemBonusesReturningBonusId(atr_bonuses_dict: dict, skill_bonuses: list):
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_item_atr_bonuses} 
                (body_type_modifier, initiative_bonus, atr_int, atr_ref, atr_tech, atr_cool, atr_attr, 
                atr_luck, atr_ma, atr_body, atr_emp)
                VALUES ({atr_bonuses_dict.get(body_type_mod, 0)}, ({atr_bonuses_dict.get(init_bonus, 0)}), {atr_bonuses_dict.get(INT, 0)},
                {atr_bonuses_dict.get(REF, 0)}, {atr_bonuses_dict.get(TECH, 0)}, {atr_bonuses_dict.get(COOL, 0)}, 
                {atr_bonuses_dict.get(ATTR, 0)}, {atr_bonuses_dict.get(LUCK, 0)}, {atr_bonuses_dict.get(MA, 0)}, 
                {atr_bonuses_dict.get(BODY, 0)}, {atr_bonuses_dict.get(EMP, 0)})
                RETURNING id;
                """)
        atr_id = cur.fetchone()['id']

        cur.execute(
            f"""{insert_into} {table_item_bonuses} (item_atr_id)
                VALUES ({atr_id}) RETURNING id;"""
        )

        bonus_id = cur.fetchone()['id']

        for skill_bonus in skill_bonuses:
            cur.execute(
                f"""{insert_into} {table_item_skill_bonus} (item_bonus_id, skill_id, skill_bonus)
                    VALUES ({bonus_id}, {skill_bonus.skill_id}, {skill_bonus.bonus})
                    """
            )
    conn.commit()
    return bonus_id


# potentially bonuses could be for multiple skills, each being own row
def getItemSkillBonuses(bonus_id):
    with conn.cursor() as cur:
        cur.execute(
            f"""{select_from} {table_item_bonuses} b 
            JOIN {table_item_skill_bonus} sb on b.id = sb.item_bonus_id
            WHERE b.id = {bonus_id};
            """
        )
        skill_bonus_rows = cur.fetchall()
    conn.commit()
    return skill_bonus_rows


# all bonuses are in single row for item
def getItemAtrBonuses(bonus_id):
    with conn.cursor() as cur:
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
    with conn.cursor() as cur:
        cur.execute(
            f"""{character_armors_q} a
                JOIN {table_item_bonuses} b 
                ON a.item_bonus_id = b.id
                JOIN {table_item_atr_bonuses} ab
                ON b.item_atr_id = ab.id
                WHERE character_id = {character_id};"""
        )
        rows = cur.fetchall()
        armors = []
        for row in rows:
            armor = Armor(row)
            armors.append(armor)
    conn.commit()
    return armors


def getCharacterChrome(character_id):
    with conn.cursor() as cur:
        cur.execute(
            f"""{character_chrome_q} c
            JOIN {table_item_bonuses} b 
            ON c.item_bonus_id = b.id
            JOIN {table_item_atr_bonuses} ab
            ON b.item_atr_id = ab.id
            WHERE character_id = {character_id};"""
        )
        rows = cur.fetchall()
        conn.commit()
        cybernetics = []
        for row in rows:
            chrome = Chrome(row)
            cybernetics.append(chrome)
        return cybernetics


def repairCharacterSP(character_id):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_character_sp} SET head = head_max, body = body_max, r_arm = r_arm_max, l_arm = l_arm_max,
                r_leg = r_leg_max, l_leg = l_leg_max
                WHERE character_id = {character_id};
                """
        )
        conn.commit()


def updateCharacterMaxSp(character_id, body_part, amount):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_character_sp} SET {body_part}_max = {body_part}_max + {amount}, {body_part} = {body_part} + {amount}
            WHERE character_id = {character_id};
            """
        )
        conn.commit()


def changeHumanityAndEmp(character_id, humanity, emp):
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_characters} SET humanity = {humanity}, atr_emp = {emp} WHERE id = {character_id};"""
        )
        conn.commit()


def addEvent(event):
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_events} (event) VALUES ('{event}');"""
        )
        conn.commit()


def listEvents():
    rows = []
    with conn.cursor() as cur:
        cur.execute(
            f"""{select_from} {table_events};"""
        )
        rows = cur.fetchall()
        conn.commit()

    return rows


def addWeapon(character_id, item, weapon_type, is_chrome, dice_number, dice_dmg, divide_by,
              dmg_bonus, range, rof, clip_size, effect_radius, wa, con, reliability, weight):
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_character_weapons} 
                (character_id, item, weapon_type, is_chrome, dice_number, dice_dmg, divide_by, dmg_bonus, range, rof, clip_size, 
                shots_left, effect_radius, wa, con, reliability, weight)
                VALUES
                ({character_id}, '{item}', '{weapon_type}', {is_chrome}, {dice_number}, {dice_dmg}, {divide_by}, {dmg_bonus}, {range}, 
                {rof}, {clip_size}, {clip_size}, {effect_radius}, {wa}, '{con}', '{reliability}', {weight});
            """
        )
        conn.commit()


def addChrome(character_id, item, humanity_cost, description, item_bonus_id: int | None, atr_dict,
              skill_bonuses: list = []):
    if item_bonus_id is None:
        item_bonus_id = insertItemBonusesReturningBonusId(atr_dict, skill_bonuses)

    with conn.cursor() as cur:
        cur.execute(
            f"""
            {insert_into} {table_character_chrome} (character_id, item, humanity_cost, description, item_bonus_id)
            VALUES ({character_id}, '{item}', {humanity_cost}, '{description}', {item_bonus_id});
            """
        )
        conn.commit()


def getWeaponById(weapon_id):
    with conn.cursor() as cur:
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
    with conn.cursor() as cur:
        cur.execute(
            f"""{update} {table_character_weapons} SET shots_left = {shots_in_clip} WHERE id = {wpn_id};"""
        )
        conn.commit()


def deleteThrown(wpn_id):
    with conn.cursor() as cur:
        cur.execute(
            f"""{delete_from} {table_character_weapons} WHERE id = {wpn_id};"""
        )
        conn.commit()


def characterWeapons(character_id, body: int) -> list:
    with conn.cursor() as cur:
        cur.execute(
            f"""{character_weapons_q} WHERE character_id = {character_id};"""
        )
        conn.commit()
        rows = cur.fetchall()

        def weaponMapFn(w):
            if w['weapon_type'] == t_thrown:
                weight = w['weight'] - 1
                if weight < 0:
                    weight = 0
                range = body * 3
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
    with conn.cursor() as cur:
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


def getArmorById(character_id, id):
    with conn.cursor() as cur:
        cur.execute(
            f"""{character_armors_with_bonuses_q} WHERE armor_id = {id} AND character_id = {character_id};"""
        )
        row = cur.fetchone()
        conn.commit()
        if row is None:
            print(f'Armor not found by armor_id {id} for character {character_id}')
        return row


def deleteCharacter(c: Character):
    with conn.cursor() as cur:
        for chrome in c.cybernetics:
            deleteCharacterChrome(c.id, chrome.id)
        for weapon in c.weapons:
            deleteCharacterWeapon(c.id, weapon.weapon_id)
        for armor in c.armors:
            deleteCharacterArmor(c.id, armor.id)

        cur.execute(
            f"""{delete_from} {table_combat_session} WHERE character_id = {c.id};"""
        )
        cur.execute(
            f"""{delete_from} {table_reputation} WHERE character_id = {c.id};"""
        )
        cur.execute(
            f'{delete_from} {table_characters} WHERE id = {c.id};'
        )
        conn.commit()


def deleteCharacterArmor(character_id, armor_id):
    with conn.cursor() as cur:
        a_row = getArmorById(character_id, armor_id)
        if a_row is not None:
            armor = Armor(a_row)
            for body_part in armor.body_parts:
                updateCharacterMaxSp(character_id, body_part, -1 * armor.sp)
            cur.execute(
                f"""
                    {delete_from} {table_character_armors} 
                    WHERE character_id = {character_id} AND armor_id = {armor_id}
                    RETURNING item_bonus_id;"""
            )
            item_bonus = cur.fetchone()
            item_bonus_id = item_bonus['item_bonus_id']

            cur.execute(
                f"""
                    {delete_from} {table_character_chrome} c
                    WHERE c.item_bonus_id = {item_bonus_id};
                    """
            )

            cur.execute(
                f"""
                    {delete_from} {table_item_skill_bonus}
                    WHERE item_bonus_id = {item_bonus_id};
                    """
            )

            cur.execute(
                f"""
                    {delete_from} {table_item_bonuses}
                    WHERE id = {item_bonus_id};
                    """
            )
            conn.commit()


def deleteCharacterWeapon(character_id, weapon_id):
    with conn.cursor() as cur:
        weapon = getWeaponById(weapon_id)
        if weapon is not None:
            cur.execute(f"""{delete_from} {table_character_weapons} 
                    WHERE character_id = {character_id} AND id = {weapon_id}
                    RETURNING item_bonus_id;""")
            item_bonus = cur.fetchone()
            item_bonus_id = item_bonus.get('item_bonus_id', None)

            if item_bonus_id is not None:
                cur.execute(f"""
                       {delete_from} {table_character_chrome} c
                       WHERE c.item_bonus_id = {item_bonus_id};
                       """)

                cur.execute(f"""
                       {delete_from} {table_item_skill_bonus}
                       WHERE item_bonus_id = {item_bonus_id};
                       """)

                cur.execute(f"""
                       {delete_from} {table_item_bonuses}
                       WHERE id = {item_bonus_id};
                       """)
                conn.commit()


def deleteCharacterChrome(character_id, chrome_id):
    with conn.cursor() as cur:
        chrome_rows = getCharacterChrome(character_id)
        chrome = None
        for row in chrome_rows:
            if row.id == chrome_id:
                chrome = row
        if chrome is not None:
            cur.execute(f"""{select_from} {table_character_chrome} 
                            WHERE character_id = {character_id} AND chrome_id = {chrome_id};""")
            chrome_row = cur.fetchone()
            item_bonus_id = chrome_row.get('item_bonus_id', None)
            connected_armor = None
            cur.execute(
                f"""{select_from} {table_character_armors} 
                    WHERE character_id = {character_id} AND item_bonus_id = {item_bonus_id}
                    """
            )
            connected_armor = cur.fetchone()
            if connected_armor is not None:
                armor_id = connected_armor['armor_id']
                deleteCharacterArmor(character_id, armor_id)
            elif item_bonus_id is not None:
                cur.execute(f"""
                       {delete_from} {table_item_skill_bonus}
                       WHERE item_bonus_id = {item_bonus_id};
                       """
                            )

                cur.execute(
                    f"""
                       {delete_from} {table_item_bonuses}
                       WHERE id = {item_bonus_id};
                       """
                )
                cur.execute(
                    f"""{delete_from} {table_character_weapons} 
                        WHERE character_id = {character_id} AND item_bonus_id = {item_bonus_id}
                        """
                )
                cur.execute(
                    f"""{delete_from} {table_character_chrome} 
                            WHERE character_id = {character_id} AND chrome_id = {chrome_id}"""
                )
                conn.commit()


def addCharacterStatus(character_id, status, effect):
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_character_statuses} (character_id, status, effect)
                VALUES ({character_id}, '{status}', '{effect}');"""
        )
        conn.commit()
    print('Status added')


def getCharacterStatuses(character_id):
    with conn.cursor() as cur:
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
    with conn.cursor() as cur:
        cur.execute(
            f"""{delete_from} {table_character_statuses}
            WHERE id = {status_id} AND character_id = {character_id};
            """
        )
        conn.commit()
        print('Status removed')


def addCharacterForQuickNoticeCheck(character_id, name):
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_character_quick_notice} (character_id)
                            VALUES ({character_id});"""
        )
        conn.commit()
        print(f'{coloredText(Fore.GREEN, name)} added to quick notice check')


def charactersForQuickNoticeCheck():
    with conn.cursor() as cur:
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
    with conn.cursor() as cur:
        cur.execute(
            f"""{delete_from} {table_character_quick_notice};"""
        )
        conn.commit()
        print(f'Quick notice checks cleared')


def listCampaigns():
    with conn.cursor() as cur:
        cur.execute(
            f"""{select_from} {table_campaigns};"""
        )
        rows = cur.fetchall()
        conn.commit()
        return rows


def addCampaign(name: str, info: str | None):
    with conn.cursor() as cur:
        cur.execute(
            f"""{insert_into} {table_campaigns} (name, info) VALUES ('{name}', '{info}');"""
        )
        conn.commit()
