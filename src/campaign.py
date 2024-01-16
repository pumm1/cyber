import cyberdao as DAO
from logger import Log, log_neg, log_pos, log_neutral, log_event
from src.character import CharacterShort


class Campaign:
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.info = row['info']

    def asJson(self):
        json = {
            'id': self.id,
            'name': self.name,
            'info': self.info
        }
        return json

class CampaignEvent:
    def __init__(self, row, event_char_rows):
        characters = map(lambda r: (
            CharacterShort(r).asJson()
        ), event_char_rows)
        self.id = row['id']
        self.characters = list(characters)
        self.campaignId = row['campaign_id']
        self.info = row['info']


    def asJson(self):
        json = {
            'id': self.id,
            'campaignId': self.campaignId,
            'characters': self.characters,
            'info': self.info
        }
        return json


def allCampaigns():
    rows = DAO.listCampaigns()
    campaigns = map(lambda r: (
        Campaign(r).asJson()
    ), rows)

    return list(campaigns)


def addCampaign(name: str, info: str | None):
    DAO.addCampaign(name, info)
    logs = log_event([], f'Campaign {name} added', log_pos)
    return logs

def campaignEvents(campaignId: int):
    rows = DAO.campaignEvents(campaignId)
    events = map(lambda r: (
        CampaignEvent(r, DAO.eventChracters(r['id'])).asJson()
    ), rows)
    return list(events)

def addCampaignEvent(campaignId: int, character_ids: list[int], info: str | None):
    DAO.addEvent(campaignId, character_ids, info)
