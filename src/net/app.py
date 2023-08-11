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
import dice, game, skills, combat, armor, healing, logger, characterBuilder, ip

app = Flask(__name__)
CORS(app)

@app.route('/test')
def hello():
    return 'Welcome to the NET!'


#TODO
@app.route('/create-character', methods = ['POST'])
def createCharacter():
    if (request.method == 'POST'):
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

@app.route('/roll', methods = ['GET'])
def roll():
    if (request.method == 'GET'):
        (dice_roll_res, _) = dice.rollWithCrit(skip_luck=True)
        return jsonify(dice_roll_res)
    else:
        return "Invalid request", 400


@app.route('/roll-skill', methods = ['POST'])
def rollSkill():
    if (request.method == 'POST'):
        data = request.get_json()
        print(f'..... data: {data} ... request: {request}')
        char_id = data['charId']
        skill_id = data['skillId']
        added_luck = data['addedLuck']
        print(f'.... roll char {char_id} skill {skill_id} added luck {added_luck}')
        return jsonify(skills.rollCharacterSkillById(char_id, skill_id, 0, 0, added_luck))
    else:
        return "Invalid request", 400

@app.route('/char', methods = ['GET'])
def getChar():
    if (request.method == 'GET'):
        name = request.args.get('name')
        return jsonify(game.getCharacter(name))
    else:
        return "Invalid request", 400

@app.route('/list-skills', methods = ['GET'])
def listSkills():
    if (request.method == 'GET'):
        return jsonify(skills.fetchAllSkils())
    else:
        return "Invalid request", 400

@app.route('/attack', methods = ['POST'])
def attack():
    if (request.method == 'POST'):
        data = request.get_json()
        print(f'..... data: {data}')
        weapon_id = data['weaponId']
        char_id = data['charId']
        attack_type = data['attackType']
        attack_range = data['attackRange']
        attack_modifier = data['attackModifier']
        targets: int = data.get('targets', 1)
        return jsonify(combat.characterAttackByCharacterAndWeaponId(char_id, weapon_id, attack_type, attack_range, attack_modifier, targets=targets)) #TODO
    else:
        return "Invalid request", 400

@app.route('/reload', methods = ['POST'])
def reload():
    if (request.method == 'POST'):
        data = request.get_json()
        weapon_id = data['weaponId']
        shots = data['shots']
        return jsonify(combat.reloadWeapon(weapon_id, shots))
    else:
        return "Invalid request", 400

@app.route('/repair-sp', methods = ['POST'])
def repairSP():
    if (request.method == 'POST'):
        char_id = request.get_json()
        return jsonify(armor.repairSPById(char_id)), 200
    else:
        return "Invalid request", 400

@app.route('/heal', methods = ['POST'])
def heal():
    if (request.method == 'POST'):
        data = request.get_json()
        char_id = data['charId']
        amount = data['amount']

        return jsonify(healing.healCharacterById(char_id, amount))
    else:
        return "Invalid request", 400

@app.route('/lvl-up', methods = ['POST'])
def lvlUp():
    if (request.method == 'POST'):
        data = request.get_json()
        char_id = data['charId']
        skill_id = data['skillId']
        amount = data['amount']

        return jsonify(skills.updateCharSkillById(char_id, skill_id, amount))
    else:
        return "Invalid request", 400

@app.route('/dmg', methods = ['POST'])
def dmg():
    if (request.method == 'POST'):
        data = request.get_json()
        char_id = data['charId']
        body_part = data['bodyPart']
        dmg = data['dmg']
        res = combat.hitCharacterById(char_id, body_part=body_part, dmg_str=dmg, pass_sp=False)
        print(f'... res: {res}')
        return jsonify(res)
    else:
        return "Invalid request", 400

@app.route('/save-ip', methods = ['POST'])
def saveIP():
    if (request.method == 'POST'):
        data = request.get_json()
        char_id = data['charId']
        ipAmount = data['ipAmount']
        res = ip.saveIP(char_id, ipAmount)
        print(f'... res: {res}')
        return jsonify(res)
    else:
        return "Invalid request", 400
