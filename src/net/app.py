from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# getting the name of the directory
# where the this file is present.

current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

# now we can import the module in the parent
# directory.
import dice, game, skills, combat, armor, logger, characterBuilder, weapon, chrome, notice, cyberdao, status, cyberService

app = Flask(__name__)
CORS(app)

post = 'POST'
get = 'GET'
put = 'PUT'
delete = 'DELETE'

def invalid_req():
    return "Invalid request", 400


cyberdao.check_system_version()


@app.route('/test')
def hello():
    return 'Welcome to the NET!'


# TODO
@app.route('/create-character', methods=[post])
def createCharacter():
    if request.method == post:
        data = request.get_json()
        name = data['name']
        randomize = data['randomize']
        gear_tier = data.get('gearTier')
        if randomize:
            (logs, character_id) = characterBuilder.createCharacterFromReq(name, role='', given_body_type='',
                                                                           attributes=[], randomize=True,
                                                                           gear_tier=gear_tier)
            resJson = {
                'logs': logs,
                'charId': character_id
            }

            return jsonify(resJson)
        else:
            attributes = data['attributes']
            role = data['role']
            body_type = data['btm']
            print(f'body type req: {body_type}')
            (logs, character_id) = characterBuilder.createCharacterFromReq(name, role, body_type, attributes)

            resJson = {
                'logs': logs,
                'charId': character_id
            }

            return jsonify(
                resJson
            )
    else:
        return invalid_req()


@app.route('/roll', methods=[post])
def roll():
    if request.method == post:
        data = request.get_json()
        n = data.get('numberOfDice', 1)
        d_die = data.get('dDie', 10)
        dice_roll_res = dice.roll(n, d_die)
        return jsonify(dice_roll_res)
    else:
        return invalid_req()


@app.route('/roll-skill', methods=[post])
def rollSkill():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        skill_id = data['skillId']
        added_luck = data['addedLuck']
        modifier = data['modifier']
        roll = data['roll']
        return jsonify(cyberService.rollCharacterSkillById(char_id, skill_id, roll, modifier, added_luck))
    else:
        return invalid_req()


@app.route('/roll-initiative', methods=[post])
def rollInitiative():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        return jsonify(game.rollInitiativeByCharacterId(char_id))
    else:
        return invalid_req()


@app.route('/roll-melee-dmg', methods=[post])
def rollMeleeDmg():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        weapon_id = data['weaponId']
        method = data['method']
        print(f'... data: {data} ... method: {method}')
        return jsonify(cyberService.handleMeleeDmgByCharacterId(char_id, roll=0, wep_id=weapon_id, method=method))
    else:
        return invalid_req()


@app.route('/roll-face-off', methods=[post])
def rollFaceOff():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        return jsonify(game.faceOffRollById(char_id))
    else:
        return invalid_req()


@app.route('/char', methods=[get])
def getChar():
    if request.method == get:
        id = request.args.get('id')
        return jsonify(game.getCharacterById(id))
    else:
        return invalid_req()


@app.route('/list-skills', methods=[get])
def listSkills():
    if request.method == get:
        return jsonify(cyberService.fetchAllSkils())
    else:
        return invalid_req()


@app.route('/list-characters', methods=[get])
def listCharacters():
    if request.method == get:
        return jsonify(game.listCharacters())
    else:
        return invalid_req()


@app.route('/attack', methods=[post])
def attack():
    if request.method == post:
        data = request.get_json()
        weapon_id = data['weaponId']
        given_roll = data['givenRoll']
        char_id = data['charId']
        attack_type = data['attackType']
        attack_range = data['attackRange']
        attack_modifier = data['attackModifier']
        targets: int = data.get('targets', 1)
        shots_fired = data.get('shotsFired', 1)
        return jsonify(
            cyberService.characterAttackByCharacterAndWeaponId(
                char_id, weapon_id, attack_type, attack_range, given_roll=given_roll, attack_modifier=attack_modifier,
                targets=targets, shots_fired=shots_fired
            )
        )
    else:
        return invalid_req()


@app.route('/reload', methods=[put])
def reload():
    if request.method == put:
        data = request.get_json()
        weapon_id = data['weaponId']
        shots = data['shots']
        return jsonify(cyberService.reloadWeapon(weapon_id, shots))
    else:
        return invalid_req()


@app.route('/repair-sp', methods=[put])
def repairSP():
    if request.method == put:
        char_id = request.get_json()
        return jsonify(cyberService.repairSPById(char_id)), 200
    else:
        return invalid_req()


@app.route('/heal', methods=[put])
def heal():
    if request.method == put:
        data = request.get_json()
        char_id = data['charId']
        amount = data['amount']

        return jsonify(cyberService.healCharacterById(char_id, amount))
    else:
        return invalid_req()


@app.route('/lvl-up', methods=[post])
def lvlUp():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        skill_id = data['skillId']
        amount = data['amount']

        return jsonify(cyberService.updateCharSkillById(char_id, skill_id, amount))
    else:
        return invalid_req()


@app.route('/dmg', methods=[post])
def dmg():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        body_part = data['bodyPart']
        dmg = data['dmg']
        is_ap = data.get('isAp', False)
        pass_sp = data.get('passSp', False)
        res = cyberService.hitCharacterById(char_id, body_part=body_part, dmg_str=dmg, pass_sp=pass_sp, is_ap=is_ap)
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/save-ip', methods=[post])
def saveIP():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        ipAmount = data['ipAmount']
        res = cyberService.saveIP(char_id, ipAmount)
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/restore-emp', methods=[put])
def restoreEMP():
    if request.method == put:
        data = request.get_json()
        char_id = data['charId']
        emp = data['emp']
        res = game.restoreEMP(char_id, emp)
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/stun-check', methods=[post])
def stunCheck():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        res = cyberService.stunCheckById(char_id)
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/add-weapon', methods=[post])
def addWeapon():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        item = data['item']
        weapon_type = data['weaponType']
        dice_num = data['dice']
        die = data['die']
        dmg_bonus = data['dmgBonus']
        divide_by = data['divideBy']
        clip_size = data['clipSize']
        rof = data['rof']
        humanity_cost = data['humanityCost']
        wa = data['wa']
        con = data['con']
        weight = data['weight']
        reliability = data['reliability']
        effect_radius = data['effectRadius']
        custom_range = data.get('customRange', None)
        res = cyberService.addCharacterWeaponById(
            char_id, dice_num, die, divide_by, dmg_bonus, item, clip_size, rof,
            humanity_cost, weapon_type, wa, con, weight, reliability, effect_radius, custom_range
        )
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/add-chrome', methods=[post])
def addChrome():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        item = data['item']
        description = data['description']
        atr_bonuses = data['attributeBonuses']
        skill_bonuses = data['skillBonuses']
        humanity_cost = data['humanityCost']

        res = cyberService.addChromeByCharacterId(
            char_id, item, description, humanity_cost, atr_bonuses, skill_bonuses
        )
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/add-armor', methods=[post])
def addArmor():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        item = data['item']
        sp = data['sp']
        ev = data['ev']
        body_parts = data['bodyParts']
        atr_bonuses = data['attributeBonuses']
        skill_bonuses_dict = data['skillBonuses']
        humanity_cost = data['humanityCost']

        res = cyberService.addArmorForCharacterById(
            char_id, item, ev, sp, body_parts, humanity_cost, atr_bonuses, skill_bonuses_dict
        )
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/remove-armor', methods=[post])
def removeArmor():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        armor_id = data['armorId']

        res = cyberService.removeArmorByCharacterId(
            char_id, armor_id
        )
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/remove-weapon', methods=[delete])
def removeWeapon():
    if request.method == delete:
        data = request.get_json()
        char_id = data['charId']
        weapon_id = data['weaponId']

        res = cyberService.removeWeaponByCharacterId(char_id, weapon_id)
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/remove-chrome', methods=[delete])
def removeChrome():
    if request.method == delete:
        data = request.get_json()
        char_id = data['charId']
        chrome_id = data['chromeId']

        res = cyberService.removeChromeByCharacterId(char_id, chrome_id)
        return jsonify(res)
    else:
        return invalid_req()


@app.route('/list-initiative', methods=[get])
def initiativeOrder():
    if request.method == get:
        return jsonify(game.combatInitiativeOrder())
    else:
        return invalid_req()


@app.route('/add-to-combat', methods=[post])
def addToCombat():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        initiative = data['initiative']

        return jsonify(game.addToCombatByid(char_id, initiative))
    else:
        return invalid_req()

@app.route('/update-initiative-bonus', methods=[put])
def updateInitiativeBonus():
    if request.method == put:
        data = request.get_json()
        char_id = data['charId']
        bonus = data['bonus']
        turns = data['turns']

        return jsonify(game.updateInitiativeBonus(char_id, bonus, turns))
    else:
        return invalid_req()

@app.route('/advance-combat-seq', methods=[post])
def advanceCombatSeq():
    if request.method == post:
        return jsonify(game.advanceCombatSeq())
    else:
        return invalid_req()


@app.route('/clear-initiatives', methods=[post])
def clearInitiative():
    if request.method == post:
        return jsonify(game.clearCombat())
    else:
        return invalid_req()


@app.route('/list-quick-notice', methods=[get])
def listQuickNotice():
    if request.method == get:
        return "TODO"
    else:
        return invalid_req()


@app.route('/add-reputation', methods=[post])
def addRep():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        rep = data['rep']
        rep_for = data['repFor']
        return jsonify(game.addReputationById(char_id, rep, rep_for))
    else:
        return invalid_req()


@app.route('/update-money', methods=[put])
def updateMoney():
    if request.method == put:
        data = request.get_json()
        char_id = data['charId']
        money = data['money']
        return jsonify(game.updateCharacterMoneyByCharacterId(char_id, money))
    else:
        return invalid_req()


@app.route('/delete-character', methods=[delete])
def deleteCharacter():
    if request.method == delete:
        data = request.get_json()
        char_id = data['charId']
        return jsonify(game.deleteCharacter(char_id))
    else:
        return invalid_req()


@app.route('/update-name', methods=[put])
def updateName():
    if request.method == put:
        data = request.get_json()
        char_id = data['charId']
        name = data['name']
        return jsonify(game.updateCharacterName(char_id, name))
    else:
        return invalid_req()


@app.route('/update-background', methods=[put])
def updateBackground():
    if request.method == put:
        data = request.get_json()
        char_id = data['charId']
        background = data['background']
        return jsonify(game.updateCharacterBackground(char_id, background))
    else:
        return invalid_req()


@app.route('/add-character-status/<int:id>', methods=[post])
def addCharacterStatus(id):
    if request.method == post:
        data = request.get_json()
        stat = data['status']
        effect = data['effect']
        status_type = data['statusType']
        return jsonify(cyberService.addStatus(id, stat, effect, status_type))
    else:
        return invalid_req()


@app.route('/delete-character-status/<int:id>', methods=[delete])
def deleteCharacterStatus(id):
    if request.method == delete:
        status_id = request.get_json()
        return jsonify(cyberService.removeStatusByCharId(id, status_id))
    else:
        return invalid_req()


@app.route('/manual-weapon-roll', methods=[post])
def manualWeaponCheck():
    if request.method == post:
        data = request.get_json()
        roll_total = data['rollTotal']
        weapon_type = data['weaponType']
        wa = data['wa']
        attack_range = data['attackRange']
        num_of_targets = data['targets']
        num_of_shots = data['shots']

        return jsonify(combat.weaponToolResultFromReq(
            roll_total, weapon_type, wa, attack_range, num_of_targets, num_of_shots
        ))
    else:
        return invalid_req()


@app.route('/campaigns', methods=[get])
def fetchCampaigns():
    if request.method == get:
        # TODO: fetch actual data
        return jsonify(cyberService.allCampaigns())
    else:
        return invalid_req()


@app.route('/add-campaign', methods=[post])
def addCampaign():
    if request.method == post:
        data = request.get_json()
        name = data['name']
        info = data['info']
        return jsonify(cyberService.addCampaign(name, info))
    else:
        return invalid_req()


@app.route('/update-campaign-info/<int:id>', methods=[put])
def updateCampaignInfo(id):
    if request.method == put:
        info = request.get_json()
        cyberService.updateCampaignInfo(id, info)
        return jsonify(True)
    else:
        return invalid_req()


@app.route('/campaing-events/<int:id>', methods=[get])
def campaignEvents(id):
    if request.method == get:
        return jsonify(cyberService.campaignEvents(id))
    else:
        return invalid_req()

@app.route('/add-campaign-event/<int:id>', methods=[post])
def addCampaignEvent(id):
    if request.method == post:
        data = request.get_json()
        session_number = data['sessionNumber']
        info = data['info']
        cyberService.addCampaignEvent(id, session_number, info)
        return jsonify(True)
    else:
        return invalid_req()


@app.route('/update-event-info/<int:id>', methods=[put])
def updateEventInfo(id):
    if request.method == put:
        info = request.get_json()
        cyberService.updateEventInfo(id, info)
        return jsonify(True)
    else:
        return invalid_req()



@app.route('/add-event-character/<int:id>', methods=[post])
def addEventCharacter(id):
    if request.method == post:
        character_id = request.get_json()
        return jsonify(cyberService.addEventCharacter(id, character_id))
    else:
        return invalid_req()


@app.route('/add-gig-character/<int:id>', methods=[post])
def addGigCharacter(id):
    if request.method == post:
        character_id = request.get_json()
        return jsonify(cyberService.addGigCharacter(id, character_id))
    else:
        return invalid_req()

@app.route('/campaign-gigs/<int:id>', methods=[get])
def campaignGigs(id):
    if request.method == get:
        return jsonify(cyberService.campaignGigs(id))
    else:
        return invalid_req()

@app.route('/add-campaign-gig/<int:id>', methods=[post])
def addCampaignGig(id):
    if request.method == post:
        data = request.get_json()
        name = data['name']
        info = data['info']
        status = data['status']
        cyberService.addCampaignGig(id, name, info, status)
        return jsonify(True)
    else:
        return invalid_req()


@app.route('/update-gig-status/<int:id>', methods=[put])
def updateGigStatus(id):
    if request.method == put:
        status = request.get_json()
        cyberService.updateGigStatus(id, status)
        return jsonify(True)
    else:
        return invalid_req()


@app.route('/update-gig-info/<int:id>', methods=[put])
def updateGigInfo(id):
    if request.method == put:
        info = request.get_json()
        cyberService.updateGigInfo(id, info)
        return jsonify(True)
    else:
        return invalid_req()


@app.route('/delete-gig-character/<int:id>', methods=[delete])
def deleteGigCharacter(id):
    if request.method == delete:
        character_id = request.get_json()
        cyberService.deleteGigCharacter(id, character_id)
        return jsonify(True)
    else:
        return invalid_req()

@app.route('/delete-event-character/<int:id>', methods=[delete])
def deleteEventCharacter(id):
    if request.method == delete:
        character_id = request.get_json()
        cyberService.deleteEventCharacter(id, character_id)
        return jsonify(True)
    else:
        return invalid_req()
