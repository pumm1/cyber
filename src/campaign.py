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


class CampaignGig:
    def __init__(self, row, event_char_rows):
        characters = map(lambda r: (
            CharacterShort(r).asJson()
        ), event_char_rows)
        self.id = row['id']
        self.name = row['name']
        self.characters = list(characters)
        self.campaignId = row['campaign_id']
        self.info = row['info']
        self.status = row['status']


    def asJson(self):
        json = {
            'id': self.id,
            'name': self.name,
            'campaignId': self.campaignId,
            'characters': self.characters,
            'info': self.info,
            'status': self.status
        }
        return json



class CampaignEvent:
    def __init__(self, row, event_char_rows):
        characters = map(lambda r: (
            CharacterShort(r).asJson()
        ), event_char_rows)
        self.id = row['id']
        self.sessionNumber = row['session_number']
        self.characters = list(characters)
        self.campaignId = row['campaign_id']
        self.info = row['info']


    def asJson(self):
        json = {
            'id': self.id,
            'campaignId': self.campaignId,
            'sessionNumber': self.sessionNumber,
            'characters': self.characters,
            'info': self.info
        }
        return json


gig_status_not_started = 'NotStarted'
gig_status_started = 'Started'
gig_status_failed = 'Failed'
gig_status_done = 'Done'

valid_gig_statuses = [gig_status_done,  gig_status_failed, gig_status_not_started, gig_status_started]

def allCampaigns():
    rows = DAO.listCampaigns()
    campaigns = map(lambda r: (
        Campaign(r).asJson()
    ), rows)

    return list(campaigns)


def addCampaign(name: str, info: str | None):
    DAO.addCampaign(name, info)


def updateCampaignInfo(campaign_id: int, info: str | None):
    DAO.updateCampaignInfo(campaign_id, info)


def campaignEvents(campaignId: int):
    rows = DAO.campaignEvents(campaignId)
    events = []
    for row in rows:
        event_id = row['id']
        event_character_rows = DAO.eventChracters(event_id)
        ce = CampaignEvent(row, event_character_rows).asJson()
        events.append(ce)
    return list(events)


def campaignGigs(campaignId: int):
    rows = DAO.campaignGigs(campaignId)
    gigs = []
    for row in rows:
        gig_id = row['id']
        gig_character_rows = DAO.gigChracters(gig_id)
        ce = CampaignGig(row, gig_character_rows).asJson()
        gigs.append(ce)
    return list(gigs)


def addCampaignEvent(campaignId: int, session_number, info: str | None):
    DAO.addEvent(campaignId, session_number, info)


def updateEventInfo(event_id: int, info: str | None):
    DAO.updateEventInfo(event_id, info)


def addEventCharacter(eventId: int, characterId: int):
    DAO.addEventCharacter(eventId, characterId)
    event_row = DAO.eventCampaign(eventId)
    campaign_id = event_row['campaign_id']
    return campaignEvents(campaign_id)


def addCampaignGig(campaign_id: int, name: str, info: str | None, status: str):
    DAO.addGig(campaign_id, name, info, status)


def updateGigStatus(gig_id: int, status: str):
    assert(valid_gig_statuses.__contains__(status))
    DAO.updateGigStatus(gig_id, status)


def updateGigInfo(gig_id: int, info: str | None):
    DAO.updateGigInfo(gig_id, info)


def addGigCharacter(gig_id: int, characterId: int):
    DAO.addGigCharacter(gig_id, characterId)
    gig_row = DAO.gigCampaign(gig_id)
    campaign_id = gig_row['campaign_id']
    return campaignGigs(campaign_id)
