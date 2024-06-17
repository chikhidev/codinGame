import sys

player_idx = int(input())
nb_games = int(input())
move = "LEFT"

def debug(args):
    print(args, file=sys.stderr, flush=True)

def barriers_remaining(gpu, index):
    count = 0
    for i in range(index, len(gpu)):
        if gpu[i] == "#":
            count += 1
    return count

def next_position(index, move):
    if move == "UP":
        return index + 2
    elif move == "LEFT":
        return index + 1
    elif move == "DOWN":
        return index + 2
    elif move == "RIGHT":
        return index + 3
    return index

def valid_move(gpu, index, move):
    next_pos = next_position(index, move)
    next_pos = len(gpu) - 1 if next_pos >= len(gpu) else next_pos
    if move == "UP" or move == "LEFT":
        return gpu[next_pos] != "#"
    for i in range(index, next_pos + 1):
        if gpu[i] == "#":
            return False
    return True

def distance_to_barrier(gpu, index):
    dist = 0
    for i in range(index, len(gpu)):
        if gpu[i] == "#":
            return dist - 1 if dist != 0 else 0
        dist += 1
    return dist

def move_benefits(gpus, reg_positions, move):
    benefit_count = 0
    for i in range(len(gpus)):
        gpu = gpus[i]
        index = reg_positions[i]
        if valid_move(gpu, index, move):
            benefit_count += 1
            debug(f"Player {i} can move {move}")
    return benefit_count

def choose_moves(gpus, reg_positions, moves):
    for i in range(len(gpus)):
        gpu = gpus[i]
        index = reg_positions[i]
        dist = distance_to_barrier(gpu, index)
        debug(f"For player {i} distance to barrier: {dist}")
        if dist == 0 and not {"name": "UP", "benefit": 0} in moves:
            moves.append({"name": "UP", "benefit": 0})
        elif dist >= 3 and not {"name": "RIGHT", "benefit": 0} in moves:
            moves.append({"name": "RIGHT", "benefit": 0})
        elif dist >= 2 and not {"name": "DOWN", "benefit": 0} in moves:
            moves.append({"name": "DOWN", "benefit": 0})
        elif dist >= 1 and not {"name": "LEFT", "benefit": 0} in moves:
            moves.append({"name": "LEFT", "benefit": 0})

def best_move(gpus, reg_positions):
    moves = []
    no_barriers = 0

    # find required moves for each player and put them in the moves list for za moment
    choose_moves(gpus, reg_positions, moves)

    # if at least 2 two players have no barriers in front of them, go crazy
    for i in range(len(gpus)):
        gpu = gpus[i]
        index = reg_positions[i]
        if barriers_remaining(gpu, index) == 0: no_barriers += 1
    if no_barriers >= 2: return "RIGHT" # ---------------------------------

    # if there are no moves in the list, just go right
    if len(moves) == 0:
        return "RIGHT"

    best_move = moves[0]["name"]

    if len(moves) == 1: return best_move
    for move in moves:
        move["benefit"] = move_benefits(gpus, reg_positions, move["name"])
        debug(f"Move {move['name']} benefit: {move['benefit']}")

    return max(moves, key=lambda x: x["benefit"])["name"]

while True:
    gpus = []
    reg_positions = []
    inputs_list = []
    for _ in range(3):
        score_info = input()
    for _ in range(nb_games):
        inputs = input().split()
        gpu = inputs[0]
        debug(f"Gpu: {gpu}")
        gpus.append(gpu)
        inputs_list.append(inputs)
        reg_positions.append(int(inputs[1]))

    for inputs in inputs_list:
        gpu = inputs[0]
        if gpu == "GAME_OVER":
            continue
    move = best_move(gpus, reg_positions)
    debug(f"Chosen move: {move}")

    print(move)
