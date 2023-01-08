import os
import json

def readSecrets() -> dict:
    filename = os.path.join('src/secrets.json')
    try:
        with open(filename, mode='r') as f:
            res = json.loads(f.read())
            return dict(res)
    except FileNotFoundError:
        print(f'!! Secrets not found !!')
        return {}

secrets = readSecrets()

db = secrets['DB_NAME']
user = secrets['DB_USER']
password = secrets['DB_PASSWORD']
host = secrets['DB_HOST']
schema = secrets['DB_SCHEMA']

head_column = 'head'
body_column = 'body'
l_arm_column = 'l_arm'
l_leg_column = 'l_leg'
r_arm_column = 'r_arm'
r_leg_column = 'r_leg'

table_characters = f'{schema}.characters'
table_character_skills = f'{schema}.character_skills'
table_skills = f'{schema}.skills'
table_combat_session = f'{schema}.combat_session'
table_reputation = f'{schema}.character_reputation'
table_character_armors = f'{schema}.character_armor'
table_character_weapons = f'{schema}.character_weapons'
table_character_sp = f'{schema}.character_sp'
table_events = f'{schema}.events'
table_character_chrome = f'{schema}.character_chrome'
table_character_statuses = f'{schema}.character_statuses'
