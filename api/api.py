import time
from flask import Flask, request
from flask.json import jsonify
import random
import numpy as np
import math
import logic

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time':time.time()}

@app.route('/startState')
def startState():

    return jsonify(random.sample(range(9), 9))

@app.route('/solution')
def get_solutions():

    start_state = request.form['initial_state']
    start_state = np.array(start_state).reshape((3, 3))

    run_call = getattr(logic,'bfs')
    print(run_call)
    if run_call and 'manhattan':
        can_solve, steps, depth, run_time, visited = run_call(start_state,logic.goal_state,)
    elif run_call:
        can_solve, steps, depth, run_time, visited = run_call(start_state, logic.goal_state)

    response = {
        "steps": steps,
        "nodes_visited": visited,
        "run_time": run_time,
        "solvable": can_solve,
        "depth": depth
    }
    """
    Generate solution using breath first search
    """
    return jsonify(response)
