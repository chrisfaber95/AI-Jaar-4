import random
import itertools
import math
import numpy

def merge_left(b):
    # merge the board left
    # this function is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left
        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accu
        if len(row) == 1:
            return acc + [x]
        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accu, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accu, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]

def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]

def merge_down(b):
    # merge the board downward
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]

# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                # if same value or an empty cell
                if x == y or x == 0 or y == 0:
                    return True
        return False

    # check horizontally and vertically
    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b

def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b

def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue
            
def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert merge_down(b) == [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [[2, 8, 4, 0], [16, 0, 2, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
    assert (merge_down(b)) == [[0, 0, 0, 0], [2, 0, 0, 0], [16, 0, 4, 0], [4, 8, 2, 0]]
    assert (move_exists(b)) == True
    b = [[32, 64, 2, 16], [8, 32, 16, 2], [4, 16, 8, 4], [2, 8, 4, 2]]
    assert (move_exists(b)) == False
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    for i in range(11):
        add_two_four(b)
        print(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))

MAX_DEPTH = 3
def get_expectimax_move(board):
    move, score = expectimax(board, MAX_DEPTH)
    #  print(f'[RESULT]:\t{move}  {score}')
    return move

def expectimax(board, depth):
    if depth <= 0: # or game_state(board) == 'win':
        return 'left', calc_move_score(board)  # maximale diepte bereikt, geef de bordwaarde terug
    
    top_move = 'left'
    top_score = 0
    for direction, merge in MERGE_FUNCTIONS.items():
        score = 0
        new_board = merge(board)
        if new_board == board:
            continue

        free_tiles = get_free_tiles(new_board)
        if len(free_tiles) == 0:
            score = expectimax(new_board, depth-1)[1]
        else:
            if len(free_tiles) > 7:
                free_tiles = free_tiles[:len(free_tiles)//2]
            for row, col in free_tiles:
                tile_score = 0
                for val, prob in [(2, 0.9), (4, 0.1)]:
                        new_board[row][col] = val
                        tile_score += prob  * expectimax(new_board, depth-1)[1]
                        new_board[row][col] = 0
                score += tile_score / 2  # voor een correcte oplossing moet dit door 2 gedeeld worden, echter wanneer dit niet gedaan wordt is er een 100% winst ratio (score wordt omlaag gehaald door 10% van 4)
            score = score / len(free_tiles)

        if score > top_score or top_score == 0:
            top_move = direction
            top_score = score
    return top_move, top_score

def get_free_tiles(board):
    tiles = []
    for row, col in itertools.product(range(4), range(4)):
        if board[row][col] == 0:
            tiles.append((row, col))
    return tiles

TILE_VALUE_MATRIX = [
        [0.1, 0.2, 0.9, 1.0],
        [0.2, 0.4, 0.8, 1.0],
        [0.5, 0.5, 0.7, 1.1],
        [0.5, 0.5, 0.6, 1.3],
        ]

def calc_move_score(board):
    if not move_exists(board):
        return 1
    board_score = 0
    for row, multipliers in zip(board, TILE_VALUE_MATRIX):
        row_score = sum([ tile * multiplier for tile, multiplier in zip(row, multipliers)])
        board_score += row_score
    return board_score