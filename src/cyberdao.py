import psycopg2
import psycopg2.extras
from character import Character

db = 'cyberpunk'
user = 'cyber'
password = 'cyber1'
host = '127.0.0.1'
schema = 'cyberpunk'
table_characters = f'{schema}.characters'
table_skills = f'{schema}.character_skills'

conn = psycopg2.connect(dbname=db, user=user, password=password, host=host)
cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

def clean_fetch_all(rows):
    return [i[0] for i in rows]

character_q = f"""SELECT * FROM {table_characters} c """

def getAllCharacters():
    cur.execute(character_q)
    rows = cur.fetchall()
    #cleaned_rows = clean_fetch_all(rows)
    print(f'rows fetched: {rows}')
    conn.commit()
    return rows


def getCharactersByName(name: str):
    cur.execute(
        f"""{character_q} WHERE c.name = '{name}';"""
    )
    rows = cur.fetchall()
    cleaned_rows = clean_fetch_all(rows)
    print(f'rows fetched: {cleaned_rows}')
    conn.commit()

def getCharacterByName(name: str):
    cur.execute(
        f"""{character_q} WHERE c.name = '{name}';"""
    )
    char_row = cur.fetchone()
    character = None
    if char_row is not None:
        id = char_row['id']
        cur.execute(
            f'SELECT * FROM {table_skills} where character_id = {id};'
        )
        skill_rows = cur.fetchall()

        skills = map(lambda skill: (
            skill['skill'], {skill['skill_value'], skill['attribute']}
        ), skill_rows)
        cleaned_skills = dict(skills)
        character = Character(char_row, cleaned_skills)
    else:
        print('No character found')

    conn.commit()
    return character

