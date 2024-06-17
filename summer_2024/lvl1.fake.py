import sys

player_idx = int(input())
nb_games = int(input())

def debug(args):
    print(args, file=sys.stderr, flush=True)

def can_jump(p_idx: int, track: str, distance: int) -> bool:
    track_len = len(track)
    if p_idx < track_len - distance:
        for d in range(1, distance + 1):
            if track[p_idx + d] != '.':
                return False
    return True

def best_in(positions, gpus):
    worst_idx = 0
    worst_priority = -1

    for i, (idx, map) in enumerate(zip(positions, gpus)):
        if idx < 29 and map[idx + 1] == '#':
            priority = 3
        elif idx < 28 and (map[idx + 1] == '#' or map[idx + 2] == '#'):
            priority = 2
        elif idx < 27 and (map[idx + 1] == '#' or map[idx + 2] == '#' or map[idx + 3] == '#'):
            priority = 1
        else:
            priority = 0

        if priority > worst_priority:
            worst_priority = priority
            worst_idx = i

    return worst_idx

def best(worst, map, positions):
    if can_jump(positions[worst], gpus[worst], 3):
        return "RIGHT"
    elif can_jump(positions[worst], gpus[worst], 2):
        return "DOWN"
    elif can_jump(positions[worst], gpus[worst], 1):
        return "LEFT"
    return "UP"

while True:
    positions = []
    gpus = []

    for _ in range(3):
        input()
    for _ in range(nb_games):
        inputs = input().split()
        gpu = inputs[0]
        reg_0 = int(inputs[1])
        if gpu == "GAME_OVER": continue
        gpus.append(gpu)
        positions.append(reg_0)

    best_idx = best_in(positions, gpus)
    print(best(best_idx, gpus[best_idx], positions))

