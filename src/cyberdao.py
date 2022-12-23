import psycopg2
import psycopg2.extras
from character import Character
from src.skill import SkillInfo

db = 'cyberpunk'
user = 'cyber'
password = 'cyber1'
host = '127.0.0.1'
schema = 'cyberpunk'
table_characters = f'{schema}.characters'
table_character_skills = f'{schema}.character_skills'
table_skills = f'{schema}.skills'
table_combat_session = f'{schema}.combat_session'
table_reputation = f'{schema}.character_reputation'

conn = psycopg2.connect(dbname=db, user=user, password=password, host=host)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def clean_fetch_all(rows):
    return [i[0] for i in rows]


character_q = f'SELECT * FROM {table_characters} c '
character_skills_q = f'SELECT * FROM {table_character_skills}'
skills_q = f'SELECT * FROM {table_skills}'


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


def getCharacterRow(name: str):
    cur.execute(
        f"""{character_q} WHERE c.name = '{name}';"""
    )
    char_row = cur.fetchone()
    conn.commit()
    return char_row


def getCharacterByName(name: str):
    char_row = getCharacterRow(name)
    character = None
    if char_row is not None:
        id = char_row['id']
        skills = getCharacterSkillsById(id)
        rep_rows = getReputationRows(id)
        reputation = sum(map(lambda rep: (
            rep['reputation_value']
        ), rep_rows))
        character = Character(char_row, skills, reputation)
    else:
        print('No character found')

    return character


def addReputation(character_id, info, rep):
    assert abs(rep) == 1
    cur.execute(
        f"""INSERT INTO {table_reputation} (character_id, known_for, reputation_value)
            VALUES ({character_id}, '{info}', {rep});"""
    )
    conn.commit()


def getReputationRows(character_id):
    cur.execute(
        f'SELECT * FROM {table_reputation} where character_id = {character_id};'
    )
    rows = cur.fetchall()
    conn.commit()
    return rows


def listCombatInitiative(ascending: bool):
    ordering = 'DESC'
    if ascending:
        ordering = 'ASC'
    cur.execute(
        f"""SELECT * FROM {table_combat_session} ORDER BY initiative {ordering};"""
    )
    rows = cur.fetchall()
    conn.commit()

    return rows


def clearCombat():
    cur.execute(
        f"""DELETE FROM {table_combat_session};"""
    )
    conn.commit()
    print('Combat table cleared')


def resetCurrentOrder():
    cur.execute(
        f"""UPDATE {table_combat_session} SET current = {False} WHERE current = {True};"""
    )
    conn.commit()


def setNextInOrder(character):
    cur.execute(
        f"""UPDATE {table_combat_session} SET current = {True} WHERE character = '{character}';"""
    )
    conn.commit()


def dmgCharacter(character, dmg):
    cur.execute(
        f"""UPDATE {table_characters} SET dmg_taken = {dmg} WHERE id = {character.id};"""
    )
    conn.commit()


def addCharacterSkill(char_id, skill_row, value):
    cur.execute(
        f"""INSERT INTO {table_character_skills} (character_id, skill, skill_value, attribute)
        VALUES ({char_id}, '{skill_row['skill']}', {value}, '{skill_row['attribute']}');"""
    )
    conn.commit()


def addCharacterToCombat(character, initiative):
    cur.execute(
        f"""INSERT INTO {table_combat_session} (character, initiative, current)
        VALUES ('{character}', {initiative}, {False});"""
    )
    conn.commit()
    print(f'{character} added to combat session')


def addCharacter(name, role, special_ability, body_type_modifier, atr_int, atr_ref, atr_tech, atr_cool, atr_attr,
                 atr_luck, atr_ma, atr_body, atr_emp):
    cur.execute(
        f"""INSERT INTO {table_characters} 
            (name, role, special_ability, body_type_modifier, 
            atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp, dmg_taken)
            VALUES ('{name}', '{role}', {special_ability}, '{body_type_modifier}', 
            {atr_int}, {atr_ref}, {atr_tech}, {atr_cool}, {atr_attr}, {atr_luck}, {atr_ma}, {atr_body}, {atr_emp}, 0);"""
    )
    conn.commit()
    print(f'Character {name} ({role}) added to game')


def characterSkillsFromRows(skill_rows) -> list[SkillInfo]:
    skills = map(lambda skill: (
        SkillInfo(skill['skill'], skill['skill_value'], skill['attribute'])
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




def getCharacterSkillsById(id) -> list[SkillInfo]:
    cur.execute(
        f'{character_skills_q} where character_id = {id};'
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
