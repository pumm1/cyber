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
import dice, game, skills, combat

app = Flask(__name__)
CORS(app)

@app.route('/test')
def hello():
    return 'Welcome to the NET!'

@app.route('/roll', methods = ['GET'])
def roll():
    if (request.method == 'GET'):
        dice_roll_res = dice.roll(1, 10)
        return jsonify(dice_roll_res)
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
        return jsonify(skills.fetchAllSkils())
    else:
        return "Invalid request", 400
