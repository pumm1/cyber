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
