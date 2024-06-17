import sys
import math

def can_jump_3(p_idx: int, track :str):
    track_len = len(track)
    if p_idx < track_len - 3:
        if track[p_idx + 1] != '.' or track[p_idx + 2] != '.' or track[p_idx + 3] != '.':
            return False
    return True

def can_jump_2(p_idx: int, track :str):
    track_len = len(track)
    if p_idx < track_len - 2:
        if track[p_idx + 1] != '.' or track[p_idx + 2] != '.':
            return False
    return True

def can_jump_1(p_idx: int, track :str):
    track_len = len(track)
    if p_idx < track_len - 1:
        if track[p_idx + 1] != '.':
            return False
    return True

def debug(msg, var):
    print(msg, var, file=sys.stderr, flush=True)

player_idx = int(input())
nb_games = int(input())

def get_worst_case(poss, maps) -> int:
    i = 0
    while i < len(poss):
        idx = poss[i]
        map = maps[i]
        if idx < 29 and map[idx + 1] == '#':
            return i
        i = i + 1
    i = 0
    while i < len(poss):
        idx = poss[i]
        map = maps[i]
        if idx < 28 and (map[idx + 1] == '#' or map[idx + 2] == '#'):
            return i
        i = i + 1
    i = 0
    while i < len(poss):
        idx = poss[i]
        map = maps[i]
        if idx < 27 and (map[idx + 1] == '#' or map[idx + 2] == '#' or map[idx + 3] == '#'):
            return i
        i = i + 1
    return 0


# game loop
while True:
    poss = []
    maps = []
    for i in range(3):
        score_info = input()
    for i in range(nb_games):
        inputs = input().split()
        gpu = inputs[0]
        reg_0 = int(inputs[1])
        reg_1 = int(inputs[2])
        reg_2 = int(inputs[3])
        reg_3 = int(inputs[4])
        reg_4 = int(inputs[5])
        reg_5 = int(inputs[6])
        reg_6 = int(inputs[7])
        if gpu != "GAME_OVER":
            maps.append(gpu)
            poss.append(reg_0)
    worst = get_worst_case(poss, maps)
    debug("worst", worst)
    debug("worst map", maps[worst])
    if can_jump_3(poss[worst], maps[worst]):
        print("RIGHT")
    elif can_jump_2(poss[worst], maps[worst]):
        print("DOWN")
    elif can_jump_1(poss[worst], maps[worst]):
        print("LEFT")
    else:
        print("UP")
    maps.clear()
    poss.clear()