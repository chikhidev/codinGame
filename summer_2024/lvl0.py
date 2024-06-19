import sys
import math

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
diving_wrong_moves = 0
remaining_to_shoot = 15
diving_moves = ""
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

def racing(gpu, reg_0: int = 0, others_poses = []) -> str:
    """ racing scope 
    UP -> jumps from pos to pos + 2
    LEFT -> runs one block pos -> pos + 1
    DOWN -> runs two blocks pos -> pos + 2
    RIGHT -> runs three blocks pos -> pos + 3
    """
    
    urgency = False
    importance = 1
    
    # if reg_0 <= others_poses[0] and reg_0 <= others_poses[1]:
    #     return {
    #         "name": "RIGHT",
    #         "benefits": 0,
    #         "owner": "racing"
    #     } # give up the game so give opotunity to others games
    
    # urgent cases
    if reg_0 <= others_poses[0] or reg_0 >= others_poses[1]:
        importance = 1
        urgency = True
    
    if scores[1] >= 4:
        return {
            "name": "RIGHT",
            "benefits": 1,
            "owner": "racing",
            "urgent": True
        }
    
    if not barriers_remaining(gpu, reg_0): return {"name": "RIGHT", "benefits": importance, "owner": "racing", "urgent": urgency}
    if distance_to_barrier(gpu, reg_0) >= 3:
        return {"name": "RIGHT", "benefits": importance, "owner": "racing", "urgent": urgency}
    elif distance_to_barrier(gpu, reg_0) >= 1:
        return {"name": "DOWN", "benefits": importance, "owner": "racing", "urgent": urgency}
    elif distance_to_barrier(gpu, reg_0) >= 1:
        return {"name": "LEFT", "benefits": importance, "owner": "racing", "urgent": urgency}
    return {"name": "UP", "benefits": importance, "owner": "racing", "urgent": urgency}


# archery scope ----------------------------------
def archery(gpu: str, x: int, y: int):
    """ archery scope 
    gpu -> contains wind's strength, example: 9914113315261
    x -> player's position
    y -> player's position
    """
    global remaining_to_shoot
    wind_strength = int(gpu[0])
    debug("Inside archery scope")
    debug(f"wind_strength: {wind_strength}")
    
    # urgent cases
    if x < -(2 * (20 / 3)): return {"name": "RIGHT", "benefits": 1, "owner": "archery", "urgent": True}
    if x > (2 * (20 / 3)): return {"name": "LEFT", "benefits": 1, "owner": "archery", "urgent": True}
    if y < -(2 * (20 / 3)): return {"name": "UP", "benefits": 1, "owner": "archery", "urgent": True}
    if y > (2 * (20 / 3)): return {"name": "DOWN", "benefits": 1, "owner": "archery", "urgent": True}
    
    if remaining_to_shoot > 3:
        remaining_to_shoot -= 1
        return {"name": "RIGHT", "benefits": 0, "owner": "archery"} # we have time until shoot
    
    remaining_to_shoot -= 1
    if x < 0: return {"name": "RIGHT", "benefits": 1, "owner": "archery"}
    if x > 0: return {"name": "LEFT", "benefits": 1, "owner": "archery"}
    if y < 0: return {"name": "DOWN", "benefits": 1, "owner": "archery"}
    if y > 0: return {"name": "UP", "benefits": 1, "owner": "archery"}
    return {"name": "RIGHT", "benefits": 0, "owner": "archery"}
        

# skateboarding scope ----------------------------------
def skateboarding(gpu: str, pos: int, other_poses = []):
    """ skateboarding scope 
    gpu -> contains obstacles, example:
    pos -> player's position
    """
    debug("Inside skateboarding scope")
    
    # urgent cases
    if pos < other_poses[0] or pos < other_poses[1]: return {"name": "RIGHT", "benefits": 1, "owner": "skateboarding", "urgent": True}
    
    if pos < other_poses[0] and pos < other_poses[1]: return {"name": "RIGHT", "benefits": 0, "owner": "skateboarding"}   
    
    return {
        "name": switcher.get(gpu[0]),
        "benefits": 1,
        "owner": "skateboarding"
    }


# diving scope ----------------------------------
def diving(gpu: str, pos: int):
    """ diving scope 
    gpu -> contains moves to make, example: UUDRLLDUDR
    pos -> player's position
    """
    debug("Inside diving scope")
    
    urgency = False    
    importance = 1
    
    if diving_wrong_moves > 3:
        urgency = True
        importance = 1

    # if scores[0] > 5:
    #     urgency = True
    #     importance = 8
    
    global diving_moves
    diving_moves += gpu[0]
    return {
        "name": switcher.get(gpu[0]),
        "benefits": importance,
        "owner": "diving",
        "urgent": urgency
    }


def update_recommended_actions(recommended_actions, action, game_index: int, priority: int):
    benefits = action["benefits"]
    owner = action["owner"]
    
    for recommended_action in recommended_actions:
        owner = recommended_action["owner"]
        urgent = recommended_action["urgent"]
        name = recommended_action["name"]

        if name == action["name"]:
            recommended_action["benefits"] += benefits
            recommended_action["urgent"] = action.get("urgent", False)
            return

        if (owner == "racing" or owner == "skateboarding") and not urgent and moves_power.get(action["name"]) > moves_power.get(name):
            recommended_action["name"] = action["name"]
            recommended_action["benefits"] += benefits
            recommended_action["urgent"] = action.get("urgent", False)
            return

    new_action = {"name": action["name"], "benefits": benefits, "owner": action["owner"], "urgent": action.get("urgent", False)}
    recommended_actions.append(new_action)

def poor(recommended_actions):
    # poor_game = "racing"
    # for game in medals:
    #     if medals[game][0] < medals[poor_game][0] and medals[game][1] < medals[poor_game][1]:
    #         poor_game = game
    # for action in recommended_actions:
    #     if action["owner"] == poor_game:
    #         return action["name"]
    return max(recommended_actions, key=lambda x: x["benefits"])["name"]

def col_sum(matrix)-> list:
    """ 
    matrix -> 2D array
    """
    res = [0, 0, 0]
    for row in matrix:
        for i in range(0, len(row)):
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
            #track position of player and give him medal:
            if i == 0:
                if reg_0 < reg_1 and reg_0 < reg_2: medals["racing"][2] += 1
                elif reg_0 > reg_1 and reg_0 > reg_2: medals["racing"][0] += 1
                else: medals["racing"][1] += 1
            if i == 1:
                remaining_to_shoot = 15
                x, y = reg_0, reg_1
                if x > (2 * (20 / 3)) or x < -(2 * (20 / 3)) or y > (2 * (20 / 3)) or y < -(2 * (20 / 3)): medals["archery"][2] += 1
                elif x > (20 / 3) or x < -(20 / 3) or y > (20 / 3) or y < -(20 / 3): medals["archery"][1] += 1
                else: medals["archery"][0] += 1
            if i == 2:
                if reg_0 < reg_1 and reg_0 < reg_2: medals["skateboarding"][2] += 1
                elif reg_0 > reg_1 and reg_0 > reg_2: medals["skateboarding"][0] += 1
                else: medals["skateboarding"][1] += 1
            if i == 3:
                diving_wrong_moves = 0
                if diving_wrong_moves == 0: medals["diving"][0] += 1
            if i == priority:
                priority = priority + 1 if priority < 3 else 0
            continue # here we check if a game finished go ahead to the next game
        if i == 0: update_recommended_actions(recommended_actions, racing(gpu, reg_0, [reg_1, reg_2]), i, priority)
        if i == 1: update_recommended_actions(recommended_actions, archery(gpu, reg_0, reg_1), i, priority)
        if i == 2: update_recommended_actions(recommended_actions, skateboarding(gpu, reg_0, [reg_1, reg_2]), i, priority)
        if i == 3: update_recommended_actions(recommended_actions, diving(gpu, reg_0), i, priority)

    chosen = "RIGHT"
    if len(recommended_actions) > 0:
        chosen = poor(recommended_actions)
        debug(f"Poor: {chosen}")
        # find actions owners that have less golds and selvers and give them the oppo
    debug(f"Medals: {medals}")
    debug(f"Diving wrong moves: {diving_wrong_moves}")
    print(chosen)