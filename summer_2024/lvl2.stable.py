import sys
import math
import random

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

player_idx = int(input())
nb_games = int(input())
priority:int = 0 # iwa hada dyal priority, this variable is gonna be used to make benefits based on the game index
"""
    if the game index matches the priority, the benefits gonna be 2 not just 1 !!!!!
"""
games: list = ["racing", "archery", "skateboarding", "diving"]
scores:list = [0, 0, 0] # gold silver bronze medals respectively

switcher = {
        "U": "UP",
        "D": "DOWN",
        "R": "RIGHT",
        "L": "LEFT"
    }
back_switcher = {
        "UP": "U",
        "DOWN": "D",
        "RIGHT": "R",
        "LEFT": "L"
    }
moves_power = {
    "RIGHT": 3,
    "DOWN": 2,
    "LEFT": 1,
    "UP": 0
}
medals = {
    "racing": [0, 0, 0],
    "archery": [0, 0, 0],
    "skateboarding": [0, 0, 0],
    "diving": [0, 0, 0]
}

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

def racing(gpu, reg_0: int = 0, stunning: int = 0):
    """ racing scope 
    UP -> jumps from pos to pos + 2
    LEFT -> runs one block pos -> pos + 1
    DOWN -> runs two blocks pos -> pos + 2
    RIGHT -> runs three blocks pos -> pos + 3
    """
    
    urgency = False
    importance = 1
    
    if stunning > 0: return {"name": "RIGHT", "benefits": 0, "owner": "racing"}
    if not barriers_remaining(gpu, reg_0): return {"name": "RIGHT", "benefits": importance, "owner": "racing"}
    if distance_to_barrier(gpu, reg_0) >= 3:
        return {"name": "RIGHT", "benefits": importance, "owner": "racing"}
    elif distance_to_barrier(gpu, reg_0) >= 1:
        return {"name": "DOWN", "benefits": importance, "owner": "racing"}
    elif distance_to_barrier(gpu, reg_0) >= 1:
        return {"name": "LEFT", "benefits": importance, "owner": "racing"}
    return {"name": "UP", "benefits": importance, "owner": "racing"}

# archery scope ----------------------------------
def archery(gpu: str, x: int, y: int):
    """ archery scope 
    gpu -> contains wind's strength, example: 9914113315261
    x -> player's position
    y -> player's position
    """
    
    wind = int(gpu[0])
    close = 1000
    move = "UP"
    
    if ((x + wind) ** 2) + (y ** 2) < close:
        close = ((x + wind) ** 2) + (y ** 2)
        move = "RIGHT"
    if ((x - wind) ** 2) + (y ** 2) < close:
        close = ((x - wind) ** 2) + (y ** 2)
        move = "LEFT"
    if ((x) ** 2) + ((y + wind) ** 2) < close:
        close = ((x) ** 2) + ((y + wind) ** 2)
        move = "DOWN"
    if ((x) ** 2) + ((y - wind) ** 2) < close:
        move = "UP"
        
    debug(f"archery: {move}")
    
    return {"name": move, "benefits": 1, "owner": "archery"}
        

# skateboarding scope ----------------------------------
def skateboarding(gpu: str, pos: int, other_poses: list, risk: int):
    """ skateboarding scope 
    gpu -> contains obstacles, example:
    pos -> player's position
    """
    
    # if pos < other_poses[0] and pos < other_poses[1]: return {"name": "RIGHT", "benefits": 100, "owner": "skateboarding"}
    if risk < 5: return {"name": "RIGHT", "benefits": 1, "owner": "skateboarding"}
    
    return {
        "name": switcher.get(gpu[0]),
        "benefits": 1,
        "owner": "skateboarding"
    }


# diving scope ----------------------------------

def diving(gpu: str, my_points, other_points):
    """ diving scope 
    gpu -> contains moves to make, example: UUDRLLDUDR
    pos -> player's position
    """

    return {
        "name": switcher.get(gpu[0]),
        "benefits": 1,
        "owner": "diving",
    }



def poor() -> str:
    poor_game = "racing"
    for game in games:
        if medals[game][0] < medals[poor_game][0]:
            poor_game = game
        elif medals[game][0] == medals[poor_game][0]:
            if medals[game][1] < medals[poor_game][1]:
                poor_game = game
    return poor_game


def update_recommended_actions(recommended_actions, action, game_index: int, priority: int, allow_merging: bool = False):
    benefits = action["benefits"]
    owner = action["owner"]
        
    if games[game_index] == poor():
        debug(f"Poor game: {games[game_index]}")
        benefits += 2
    
    for recommended_action in recommended_actions:
        name = recommended_action["name"]

        if name == action["name"]:
            recommended_action["benefits"] += benefits
            return

    new_action = {"name": action["name"], "benefits": benefits, "owner": action["owner"]}
    recommended_actions.append(new_action)

def score_sum():
    # return as [gold, silver, bronze]
    res = [0, 0, 0]
    for game in games:
        res[0] += medals[game][0]
        res[1] += medals[game][1]
        res[2] += medals[game][2]
    return res

# game loop
while True:
    recommended_actions = [] # structure gonna include {"name": "ACTION", "benefits": 0, "owner": "GAME"}
    registers = []

    for i in range(3):
        score_info = input()
        if i == 0:
            debug(f"Score info: {score_info}")
            score_info = score_info.split()
            score_info = score_info[1:]
            int_scores = [int(score) for score in score_info]
            # take every 3 characters and parse to int and add to scores
            # [2, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1]
            for i in range(4): medals[games[i]] = int_scores[i*3:i*3+3]
            scores = score_sum()

    for i in range(nb_games):   
        inputs = input().split()
        gpu = inputs[0]
        reg_0 = int(inputs[1])
        reg_1 = int(inputs[2])
        reg_2 = int(inputs[3])
        reg_3 = int(inputs[4])
        reg_4 = int(inputs[5])
        reg_5 = int(inputs[6])
        registers = [reg_0, reg_1, reg_2, reg_3, reg_4, reg_5]
    
        if gpu == "GAME_OVER":
            continue # here we check if a game finished go ahead to the next game

        if i == 0:
            stunning = [reg_3, reg_4, reg_5]
            update_recommended_actions(recommended_actions, racing(gpu, reg_0, stunning[player_idx]), i, priority)
        if i == 3:
            points = [reg_3, reg_4, reg_5]
            my_points = points[player_idx]
            other_points = [points[i] for i in range(3) if i != player_idx]
            update_recommended_actions(recommended_actions, diving(gpu, my_points, other_points), i, priority)
        if i == 1:
            arrows = [
                {"x": reg_0, "y": reg_1},
                {"x": reg_2, "y": reg_3},
                {"x": reg_4, "y": reg_5}
            ]
            update_recommended_actions(recommended_actions, archery(gpu, arrows[player_idx]["x"], arrows[player_idx]["y"]), i, priority)
        if i == 2: 
            risks = [reg_3, reg_4, reg_5]
            my_risk = risks[player_idx]
            update_recommended_actions(recommended_actions, skateboarding(gpu, registers[player_idx], [registers[i] for i in range(3) if i != player_idx], my_risk), i, priority)
    chosen = "RIGHT"
    if len(recommended_actions) > 0:
        chosen = max(recommended_actions, key=lambda x: x["benefits"])["name"]
        debug(f"Poor: {chosen}")
        # find actions owners that have less golds and selvers and give them the oppo
    debug(f"Medals: {medals}")
    print(chosen)
