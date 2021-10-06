"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""
import random
import time

# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()

def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

def make_move(move, player, board):
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
    
    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())

# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy, white_strategy):
    # play a game of Othello and return the final board and score
    board = initial_board()
    player = BLACK
    strategies = { BLACK: black_strategy, WHITE: white_strategy }

    while player:
        move = get_move(strategies[player], player, board)
        board = make_move(move, player, board)
        print(f'{PLAYERS[player]} plays {move}')
        player = next_player(board, player)

    black_score = score(BLACK, board)
    white_score = score(WHITE, board)
    winner = BLACK if black_score > white_score else WHITE
    if black_score == white_score:
        print(f'I\'ts a draw! ({black_score} vs {white_score})')
    else:
        print(f'{PLAYERS[winner]} wins! ({black_score} vs {white_score})')
    print(print_board(board))

    return (black_score, white_score)

def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    new_player = opponent(prev_player)
    if any_legal_move(new_player, board):
        return new_player
    elif any_legal_move(prev_player, board):
        return prev_player
    return None

def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    move = strategy(player, board)
    if is_legal(move, player, board):
        return move
    raise IllegalMoveError(player, move, board)

def score(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    return board.count(player) - board.count(opponent(player))

# Play strategies
def player_strategy(player, board):
    moves = legal_moves(player, board)
    print(print_board(board))
    print('legal moves:', ', '.join(map(str, moves)))
    move = -1
    while move < 0:
        text = input('Your move: ')
        try:
            move = int(text)
        except ValueError:
            print('Move must be a number')
            continue
        if move in moves:
            return move
        else:
            print(move, 'is not a valid move')
            move = -1

def random_move_strategy(player, board):
    moves = legal_moves(player, board)
    return random.choice(moves)

MAX_DEPTH = 3
def minimax_strategy(player, board):
    heuristic = lambda b: board_score_heuristic(player, b)
    t1 = time.time()
    # ga er vanuit dat er minstens een geldige zet is omdat het onze beurt is
    moves = legal_moves(player, board)
    top_move = None  
    top_score = 0
    for move in moves:
        new_board = make_move(move, player, board[:])
        s1 = time.time()
        score = basic_minimax(opponent(player), new_board, MAX_DEPTH, False, heuristic, None)
        s2 = time.time()
        print(f'[MINIMAX] Move {move}  Score: {score}  Time: {(s2 - s1) * 1000}')
        if score > top_score or not top_move:
            top_move = move
            top_score = score
    t2 = time.time()
    print(f'[MINIMAX] Result: {top_move}  Total time: {(t2 - t1) * 1000}')
    return top_move
    
# TODO: pruning en betere heuristieke functie!
def basic_minimax(player, board, depth, max_score, heuristic, time_limit):
    child_nodes = legal_moves(player, board)

    # Basecase, recursie diepte en spel einde
    if depth <= 0 or (len(child_nodes) < 1 and not any_legal_move(opponent(player), board)):
        return heuristic(board)

    # Als deze speler geen zet meer kan doen, dan kan de tegenstander wel
    if len(child_nodes) == 0:
        return basic_minimax(opponent(player), board, depth, not max_score, heuristic, time_limit)

    scores = [
            basic_minimax(opponent(player), make_move(node, player, board[:]), depth-1, not max_score, heuristic, time_limit)
            for node in child_nodes]

    if max_score:
        return max(scores)
    else:
        return min(scores)

def create_time_limitter(limit):
    "Create a function that returns True once `limit` in seconds has passed."
    starting_time = time.time()
    return lambda: time.time() - starting_time > limit

def board_score_heuristic(player, board):
    scoring = score(player, board)
    for i in [11, 18, 82, 89]:
        if board[i] == player:
            scoring += 10
    return scoring


play(random_move_strategy, minimax_strategy)