import cyberdao as DAO
from logger import log_event, log_pos, log_neg

def saveIP(character_id, ipAmount):
    logs = []
    character = DAO.getCharacterById(character_id)
    if character is not None:
        DAO.updateCharacterIp(character_id, ipAmount)
        logs = log_event(logs, f'{ipAmount} IP for {character.name}', log_pos)
    else:
        logs = log_event(logs, f'Character not found [character_id = {character_id}]')

    return logs