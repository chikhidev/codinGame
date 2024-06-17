import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

player_idx = int(input())
nb_games = int(input())
prioroty:int = 0 # iwa hada dyal priority, this variable is gonna be used to make benifits based on the game index
"""
    if the game index matches the priority, the benefits gonna be 2 not just 1 !!!!!
"""
games: list = ["racing", "archery", "skateboarding", "diving"]
scores:list = [0, 0, 0] # g s b

def debug(args):
    print(args, file=sys.stderr, flush=True)

# racing scope ----------------------------------
def barriers_remaining(gpu, current_idx) -> bool:
    for i in range(current_idx, len(gpu)):
        if gpu[i] == "#": return True
    return False

def distance_to_barrier(gpu, current_idx):
    if barriers_remaining(gpu, current_idx) == False: return 100
    dist = 0
    for i in range(current_idx, len(gpu)):
        if gpu[i] == "#":
            return dist - 1 if dist != 0 else 0
        dist += 1
    return dist

def racing(gpu, reg_0: int = 0, others_poses = []) -> str:
    """ racing scope 
    UP -> jumps from pos to pos + 2
    LEFT -> runs one block pos -> pos + 1
    DOWN -> runs two blocks pos -> pos + 2
    RIGHT -> runs three blocks pos -> pos + 3
    """
    
    importance = 2
    
    # urgent cases
    if reg_0 <= others_poses[0] and reg_0 <= others_poses[1]: importance = 4
    
    if not barriers_remaining(gpu, reg_0): return {"name": "RIGHT", "benefits": importance}
    if distance_to_barrier(gpu, reg_0) >= 3:
        return {"name": "RIGHT", "benefits": importance}
    elif distance_to_barrier(gpu, reg_0) >= 1:
        return {"name": "DOWN", "benefits": importance}
    elif distance_to_barrier(gpu, reg_0) >= 1:
        return {"name": "LEFT", "benefits": importance}
    return {"name": "UP", "benefits": 2}
# racing scope ----------------------------------


# archery scope ----------------------------------
def archery(gpu: str, x: int, y: int):
    """ archery scope 
    gpu -> contains wind's strength, example: 9914113315261
    x -> player's position
    y -> player's position
    """
    wind_strength = int(gpu[0])
    debug("Inside archery scope")
    debug(f"wind_strength: {wind_strength}")
    
    # urgent cases
    if x < -10: return {"name": "RIGHT", "benefits": 2}
    if x > 10: return {"name": "LEFT", "benefits": 2}
    if y < -10: return {"name": "UP", "benefits": 2}
    if y > 10: return {"name": "DOWN", "benefits": 2}
    
    if x < 0: return {"name": "RIGHT", "benefits": 1}
    if x > 0: return {"name": "LEFT", "benefits": 1}
    if y < 0: return {"name": "DOWN", "benefits": 1}
    if y > 0: return {"name": "UP", "benefits": 1}
    return {"name": "RIGHT", "benefits": 0}
        


# skateboarding scope ----------------------------------
def skateboarding(gpu: str, pos: int, other_poses = []):
    """ skateboarding scope 
    gpu -> contains obstacles, example:
    pos -> player's position
    """
    debug("Inside skateboarding scope")
    
    # urgent cases
    if pos < other_poses[0] and pos < other_poses[1]: return {"name": "RIGHT", "benefits": 2}
       
    return {"name": "DOWN", "benefits": 1}


def update_recommended_actions(recommended_actions, action, game_index, priority):
    if len(recommended_actions) > 0:
        for i in range(len(recommended_actions)):
            if recommended_actions[i]["name"] == action["name"]:
                recommended_actions[i]["benefits"] += action["benefits"]
                return
    new = {"name": action["name"], "benefits": action["benefits"]}
    recommended_actions.append(new)


def col_sum(matrix)-> list:
    """ 
    matrix -> 2D array
    """
    res = [0, 0, 0]
    for row in matrix:
        for i in range(0, 3):
            res[i] += int(row[i])
    return res
            

# game loop
while True:

    recommended_actions = [] # structure gonna include {"name": "ACTION", "benefits": 0}

    for i in range(3):
        score_info = input()
        if i == 0:
            debug(f"Score info: {score_info}")
            score_info = score_info[2:]
            score_info = score_info.split()
            score = []
            i = 0
            while i < len(score_info):
                score.append(score_info[i:i+3])
                i += 3
            scores = col_sum(score)
        
    for i in range(nb_games):   
        inputs = input().split()
        gpu = inputs[0]
        reg_0 = int(inputs[1])
        reg_1 = int(inputs[2])
        reg_2 = int(inputs[3])
        if gpu == "GAME_OVER":
            prioroty = prioroty + 1 if prioroty < 2 else 0 # 7ydha mn be3d
            continue # here we check if a game finished go ahead to the next game
        if i == 0: update_recommended_actions(recommended_actions, racing(gpu, reg_0, [reg_1, reg_2]), i, prioroty)
        if i == 1: update_recommended_actions(recommended_actions, archery(gpu, reg_0, reg_1), i, prioroty)
        if i == 2: update_recommended_actions(recommended_actions, skateboarding(gpu, reg_0, [reg_1, reg_2]), i, prioroty)

    debug(f"Scores: {scores}")
    # debug(f"Doubling is offered for -> {games[prioroty]}")
    if len(recommended_actions) > 0: print(max(recommended_actions, key=lambda x: x["benefits"])["name"])
    else: print("UP")