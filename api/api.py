import time
from flask import Flask, request
from flask.json import jsonify
import random
from api import puzzle

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time':time.time()}

@app.route('/initial')
def get_initial_state():
    """
    Generate solution using breath first search
    """
    return jsonify(random.sample(range(9), 9))

@app.route('/solution', methods=['POST'])
def get_solution():
    """
    Generate solution using breath first search
    """
    agent = puzzle.EightPuzzle(request.json)
    return jsonify(agent.solution())

