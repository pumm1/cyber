import os
import json
from pathlib import Path, PureWindowsPath


def readSecrets() -> dict:
    secrets = 'secrets.json'
    filename = ''
    path = ''
    if os.name == 'nt':
        path = PureWindowsPath(secrets)
    else:
        path = Path(f'src/{secrets}')

    filename = os.path.join(path)
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
table_character_quick_notice = f'{schema}.character_notice_quick_checks'
table_item_bonuses = f'{schema}.item_bonuses'
table_item_atr_bonuses = f'{schema}.item_atr_bonuses'
table_item_skill_bonus = f'{schema}.item_skill_bonus'
table_character_notice_rolls = f'{schema}.character_notice_rolls'
