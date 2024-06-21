import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# global variables
player_idx = int(input())
nb_games = int(input())
best_action = {"name": "LEFT", "score": 0}
moves = ["LEFT", "RIGHT", "UP", "DOWN"]
moves_strength = {
    "LEFT": 1,
    "UP": 2,
    "DOWN": 2,
    "RIGHT": 3
    }
official_medals = [
        {"gold": 0, "silver": 0, "bronze": 0},
        {"gold": 0, "silver": 0, "bronze": 0},
        {"gold": 0, "silver": 0, "bronze": 0},
        {"gold": 0, "silver": 0, "bronze": 0}
    ]
racer_knoked = {"knoked": False, "time": 0}
shooting_targets = {
    "A": [(-20 / 3), 20 / 3],
    "B": [2 * (-20 / 3), 2 * (20 / 3)]
}
shooting_time = 0







# helping functions
def debug(args):
    print(args, file=sys.stderr, flush=True)

def apply_move(positions, move, game, gpu, game_idx):
    if game_idx == 0: # racing
        if racer_knoked["knoked"] and racer_knoked["time"] == 1: racer_knoked["knoked"] = False
        if not racer_knoked["knoked"]: positions[0] += moves_strength[move]
        else: racer_knoked["time"] += 1
        if gpu[positions[0]] == "#": racer_knoked["knoked"] = True
    elif game_idx == 1: # shooting
        x, y = positions[0], positions[1]
        wind_power = int(gpu[0])
     
        if move == "UP": y += wind_power
        elif move == "DOWN": y -= wind_power
        elif move == "LEFT": x -= wind_power
        elif move == "RIGHT": x += wind_power
           
        if shooting_time == 15:
            if x in shooting_targets["A"] and y in shooting_targets["A"]:
                official_medals[0]["gold"] += 1
            elif x in shooting_targets["B"] and y in shooting_targets["B"]:
                official_medals[0]["silver"] += 1
            else:
                official_medals[0]["bronze"] += 1
            shooting_time = 0
        shooting_time += 1
        
        
        
        
def best_medals(medals1, medals2):
    gold_diff = [0, 0, 0, 0]
    silver_diff = [0, 0, 0, 0]
    for i in range(4):
        gold_diff[i] = medals1[i]["gold"] - medals2[i]["gold"]
        silver_diff[i] = medals1[i]["silver"] - medals2[i]["silver"]
    if gold_diff > 0:
        return medals1
    elif gold_diff < 0:
        return medals2
    else:
        if silver_diff > 0:
            return medals1
        elif silver_diff < 0:
            return medals2
    return medals1
    
# logic functions
def simulate_game(gpus, registers, move):
    positions = {
        "racing": registers[0], # my player position, second player position, third player position
        "shooting": registers[1], 
        "skating": registers[2],
        "diving": registers[3]
    }
    
    score = 0
    for i in range(nb_games):
        for position in positions:
            positions[position] = apply_move(positions[position], move, gpus[i], registers[i], i)
        # we dont know other players next move so we will take each move in consideration

# game loop
while True:
    gpus = []
    registers = []
    
    for i in range(3):
        score_info = input()
    for i in range(nb_games):
        inputs = input().split()
        gpus.append(inputs[0])
        mini_game_registers = inputs[1:]
        for i in range(4):
            mini_game_registers[i] = int(mini_game_registers[i])
        registers.append(mini_game_registers)
            
    # here m gonna start simmulation
    best_action["score"] = 0
    best_action["name"] = "LEFT"
    # here find the best action by simmulating all the mini games and find wich action will have the best score in future
    for move in moves:
        medals = simulate_game(gpus, registers, move)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    print("LEFT")

