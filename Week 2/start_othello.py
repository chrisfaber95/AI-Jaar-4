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

CURRENT_PLAYER = BLACK
BLACK_STRATEGY = "random"
WHITE_STRATEGY = "random"

def play(black_strategy, white_strategy):
    global CURRENT_PLAYER
    BLACK_STRATEGY = black_strategy
    WHITE_STRATEGY = white_strategy
    board = initial_board()
    print(print_board(board))
    while True:
        print(CURRENT_PLAYER)
        if CURRENT_PLAYER == None: break
        print("Player:" + CURRENT_PLAYER)
        #score(BLACK, board)
        print("Score:" + str(score(BLACK, board)) + "-" + str(score(WHITE, board)))
        if CURRENT_PLAYER == BLACK: get_move(BLACK_STRATEGY, CURRENT_PLAYER, board)
        elif CURRENT_PLAYER == WHITE: get_move(WHITE_STRATEGY, CURRENT_PLAYER, board)
        print(print_board(board))
        next_player(board, CURRENT_PLAYER)

def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
	global CURRENT_PLAYER
	if prev_player == BLACK: CURRENT_PLAYER = WHITE
	elif prev_player == WHITE: CURRENT_PLAYER = BLACK
	if any_legal_move(CURRENT_PLAYER, board) == False:
		CURRENT_PLAYER = None

def get_move(strategy, player, board):
	if strategy == "random":
		randomStrategy(player, board)
	elif strategy == "heuristic":
		heuristic(player, board)
	elif strategy == "minimax":
		minimax(player, board, 20)

def score(player, board):
	return board.count(player)

def movescore(player, board):
	return board.count(player) - board.count(opponent(player))
# Play strategies

import random
import time
def randomStrategy(player, board):
	n = random.choice(legal_moves(player, board))
	make_move(n, player, board)
	
#hoogste max steps gezien is 44 voor maximaal 2 seconde.
def minimax(player, board, maxDepth):
    global CURRENT_PLAYER
    stepcount = 0
    best = (None, 0)
    copyBoard = board.copy()
    start = time.time()
    for move in legal_moves(player, board):
        for i, item in enumerate(legal_moves(player, copyBoard)):
            counter = 0
            movedata = evaluateMoves(item, player, copyBoard)
            if movedata[0][1] > best[1]:
                best = (move, movedata[0][1])
                copyBoard = movedata[1]
            if player == BLACK: player = WHITE
            elif player == WHITE: player = BLACK
            counter += 1
            if counter >= maxDepth:
                break
            stepcount += 1
            if time.time() - start > 2:
                break
            if stepcount == maxDepth:
                break
    
    print("max-steps:", stepcount)
    make_move(best[0], CURRENT_PLAYER, board)

def evaluateMoves(first, player, board):
	global CURRENT_PLAYER
	bestmove = [None, 0]
	make_move(first, player, board)
	score1 = 0
	score1 += movescore(player, board)
	if first == any([11, 18, 89, 82]) and player == CURRENT_PLAYER:
		score1 += 1000
	elif first == any([11, 18, 89, 82]) and player != CURRENT_PLAYER:
		return bestmove, board
	if movescore(player, board) > bestmove[1]:
		bestmove[0] = first
		bestmove[1] = score1
	
	return bestmove, board

def heuristic(player, board):
	bestmove = (None, 0)
	for move in legal_moves(player, board):
		copyBoard = board.copy()
		make_move(move, player, copyBoard)
		if score(player, copyBoard) > bestmove[1]:
			bestmove = (move, score(player, copyBoard))
	if bestmove[0] == None:
		return False
	else:
		make_move(bestmove[0], player, board)

play("random", "minimax")