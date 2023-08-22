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
import dice, game, skills, combat, armor, healing, logger, characterBuilder, ip, weapon, chrome

app = Flask(__name__)
CORS(app)

post = 'POST'
get = 'GET'

@app.route('/test')
def hello():
    return 'Welcome to the NET!'


#TODO
@app.route('/create-character', methods = [post])
def createCharacter():
    if request.method == post:
        data = request.get_json()
        attributes = data['attributes']
        name = data['name']
        role = data['role']
        body_type = data['btm']

        return jsonify(
            characterBuilder.createCharacterFromReq(name, role, body_type, attributes)
        )
    else:
        return "Invalid request", 400

@app.route('/roll', methods = [post])
def roll():
    if request.method == post:
        data = request.get_json()
        n = data.get('numberOfDice', 1)
        d_die = data.get('dDie', 10)
        dice_roll_res = dice.roll(n, d_die)
        return jsonify(dice_roll_res)
    else:
        return "Invalid request", 400


@app.route('/roll-skill', methods = [post])
def rollSkill():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        skill_id = data['skillId']
        added_luck = data['addedLuck']
        modifier = data['modifier']
        roll = data['roll']
        return jsonify(skills.rollCharacterSkillById(char_id, skill_id, roll, modifier, added_luck))
    else:
        return "Invalid request", 400

@app.route('/roll-initiative', methods = [post])
def rollInitiative():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        return jsonify(game.rollInitiativeByCharacterId(char_id))
    else:
        return "Invalid request", 400

@app.route('/roll-melee-dmg', methods = [post])
def rollMeleeDmg():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        weapon_id = data['weaponId']
        method = data['method']
        print(f'... data: {data} ... method: {method}')
        return jsonify(combat.handleMeleeDmgByCharacterId(char_id, roll=0, wep_id=weapon_id, method=method))
    else:
        return "Invalid request", 400



@app.route('/char', methods = [get])
def getChar():
    if request.method == get:
        name = request.args.get('name')
        return jsonify(game.getCharacter(name))
    else:
        return "Invalid request", 400

@app.route('/list-skills', methods = [get])
def listSkills():
    if request.method == get:
        return jsonify(skills.fetchAllSkils())
    else:
        return "Invalid request", 400

@app.route('/attack', methods = [post])
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
            combat.characterAttackByCharacterAndWeaponId(
                char_id, weapon_id, attack_type, attack_range, given_roll=given_roll, attack_modifier=attack_modifier, targets=targets, shots_fired=shots_fired
            )
        )
    else:
        return "Invalid request", 400

@app.route('/reload', methods = [post])
def reload():
    if request.method == post:
        data = request.get_json()
        weapon_id = data['weaponId']
        shots = data['shots']
        return jsonify(combat.reloadWeapon(weapon_id, shots))
    else:
        return "Invalid request", 400

@app.route('/repair-sp', methods = [post])
def repairSP():
    if request.method == post:
        char_id = request.get_json()
        return jsonify(armor.repairSPById(char_id)), 200
    else:
        return "Invalid request", 400

@app.route('/heal', methods = [post])
def heal():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        amount = data['amount']

        return jsonify(healing.healCharacterById(char_id, amount))
    else:
        return "Invalid request", 400

@app.route('/lvl-up', methods = [post])
def lvlUp():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        skill_id = data['skillId']
        amount = data['amount']

        return jsonify(skills.updateCharSkillById(char_id, skill_id, amount))
    else:
        return "Invalid request", 400

@app.route('/dmg', methods = [post])
def dmg():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        body_part = data['bodyPart']
        dmg = data['dmg']
        is_ap = data.get('isAp', False)
        pass_sp = data.get('passSp', False)
        res = combat.hitCharacterById(char_id, body_part=body_part, dmg_str=dmg, pass_sp=pass_sp, is_ap=is_ap)
        return jsonify(res)
    else:
        return "Invalid request", 400

@app.route('/save-ip', methods = [post])
def saveIP():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        ipAmount = data['ipAmount']
        res = ip.saveIP(char_id, ipAmount)
        return jsonify(res)
    else:
        return "Invalid request", 400

@app.route('/add-weapon', methods = [post])
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
        print(f'....data: {data}')
        res = weapon.addCharacterWeaponById(
            char_id, dice_num, die, divide_by, dmg_bonus, item, clip_size, rof,
            humanity_cost, weapon_type, wa, con, weight, reliability, effect_radius, custom_range
        )
        return jsonify(res)
    else:
        return "Invalid request", 400

@app.route('/add-chrome', methods = [post])
def addChrome():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        item = data['item']
        description = data['description']
        atr_bonuses = data['attributeBonuses']
        skill_bonuses = data['skillBonuses']
        humanity_cost = data['humanityCost']

        res = chrome.addChromeByCharacterId(
            char_id, item, description, humanity_cost, atr_bonuses, skill_bonuses
        )
        return jsonify(res)
    else:
        return "Invalid request", 400

@app.route('/add-armor', methods = [post])
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

        res = armor.addArmorForCharacterById(
            char_id, item, ev, sp, body_parts, humanity_cost, atr_bonuses, skill_bonuses_dict
        )
        return jsonify(res)
    else:
        return "Invalid request", 400

@app.route('/remove-armor', methods = [post])
def removeArmor():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        armor_id = data['armorId']

        res = armor.removeArmorByCharacterId(
            char_id, armor_id
        )
        return jsonify(res)
    else:
        return "Invalid request", 400

@app.route('/remove-weapon', methods = [post])
def removeWeapon():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        weapon_id = data['weaponId']

        res = weapon.removeWeaponByCharacterId(
            char_id, weapon_id
        )
        return jsonify(res)
    else:
        return "Invalid request", 400


@app.route('/remove-chrome', methods = [post])
def removeChrome():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        chrome_id = data['chromeId']

        res = chrome.removeChromeByCharacterId(char_id, chrome_id)
        return jsonify(res)
    else:
        return "Invalid request", 400


@app.route('/list-initiative', methods = [get])
def initiativeOrder():
    if request.method == get:
        return jsonify(game.combatInitiativeOrder())
    else:
        return "Invalid request", 400


@app.route('/add-to-combat', methods = [post])
def addToCombat():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        initiative = data['initiative']

        return jsonify(game.addToCombatByid(char_id, initiative))
    else:
        return "Invalid request", 400


@app.route('/advance-combat-seq', methods = [post])
def advanceCombatSeq():
    if request.method == post:
        return jsonify(game.advanceCombatSeq())
    else:
        return "Invalid request", 400


@app.route('/clear-initiatives', methods = [post])
def clearInitiative():
    if request.method == post:
        return jsonify(game.clearCombat())
    else:
        return "Invalid request", 400


@app.route('/add-reputation', methods = [post])
def addRep():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        rep = data['rep']
        rep_for = data['repFor']
        return jsonify(game.addReputationById(char_id, rep, rep_for))
    else:
        return "Invalid request", 400

@app.route('/update-money', methods = [post])
def updateMoney():
    if request.method == post:
        data = request.get_json()
        char_id = data['charId']
        money = data['money']
        return jsonify(game.updateCharacterMoneyByCharacterId(char_id, money))
    else:
        return "Invalid request", 400