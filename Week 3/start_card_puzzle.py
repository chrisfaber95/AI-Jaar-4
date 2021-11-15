'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

a) 1. Hoeveel (verschillende) permutaties zijn er eigenlijk? Hoe kun je dit zelf berekenen? 
    Er zijn 8 plaatsen op het bord, waar 8 kaarten gelegd kunnen worden. Wanneer je een kaart neerlegd zijn er nog 7 plaatsen over waar nog 7 mogelijke kaarten neergelegd kunnen worden, enzovoort. Dit maakt uiteindelijk voor 8! mogelijke permutaties.
    Voor een willekeurige permutatie kunnen de kaarten van de 4 paren onderling gewisseld worden (bijv. aas met aas) zonder dat het bord echt veranderd. Dit betekend dat er 4^2 mogelijke varianten zijn van een permutatie die hetzelfde betekenen. Anders gezegd: 1 op de 16 mogelijke permutaties is uniek.
    8! / 16 = 2520
    Er zijn dus 2520 unieke permutaties.

Nota variable-ordering:
    Na wat testen lijkt de ordering 0-7 toch de meest effiënte volgorde te zijn.
'''
import itertools

# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
unique_cards = ['K', 'Q', 'J', 'A']
neighbors = {0:[3], 1:[2], 2:[1,4,3], 3:[0,2,5], 4:[2,5], 5:[3,4,6,7], 6:[5], 7:[5]}

def is_valid(board):
    card_count = {card: 0 for card in cards}
    tiles = board.items() if type(board) is dict else enumerate(board)

    for index, card in tiles:
        if card == '.':
            continue

        # Beperk het aantal kaarten dat gelegd mag worden
        card_count[card] += 1
        if card_count[card] > 2:
            return False

        neighbour_cards = [board[i] for i in neighbors[index]]

        if card in neighbour_cards:
            return False
        elif card == 'A':
           if 'Q' in neighbour_cards or ('K' not in neighbour_cards and '.' not in neighbour_cards):
               return False
        elif card == 'Q':
            if 'A' in neighbour_cards or ('J' not in neighbour_cards and '.' not in neighbour_cards):
                return False
        elif card == 'K':
            if 'Q' not in neighbour_cards and '.' not in neighbour_cards:
                return False
    return True

def dfs(board, remaining_cards, solutions=[]):
    global calls
    calls += 1
    if not '.' in board.values():
        print('Found solution after', calls, 'calls')
        print_board(board)
        print()
        solutions.append(board.copy())
        return solutions

    board_idx = len(board) - len(remaining_cards)  # Doorloop het bord 0, 1, 2, etc.
    for card in unique_cards:
        if card not in remaining_cards:
            continue
        board[board_idx] = card
        remaining_cards.remove(card)
        if is_valid(board):
            dfs(board, remaining_cards, solutions)
        remaining_cards.append(card)
        board[board_idx] = '.'

    return solutions

def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('1.  f ',is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('2.  f ',is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('3.  t ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('4.  t ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('5.  f ',is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})) # [1]
    print('6.  f ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})) # [3]
    print('7.  t ',is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})) # [3] 
    print('8.  f ',is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})) # [3]
    print('9.  f ',is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})) # [4]
    print('10. f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})) # [5]
    print('11. f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})) # [5]
    print('12. t ',is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    # extra testen
    print('13. f ', is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'Q', 6: 'J', 7: 'J'}))


def board_from_list(l):
    return dict(enumerate(l))


def print_board(board):
    grid = [[' '] * 4 for i in range(4)]
    grid[0][2] = board[0]
    grid[1][0] = board[1]
    grid[1][1] = board[2]
    grid[1][2] = board[3]
    grid[2][1] = board[4]
    grid[2][2] = board[5]
    grid[2][3] = board[6]
    grid[3][2] = board[7]
    print_grid(grid)


def print_grid(grid):
    for row in grid:
        print(' '.join(row))


if __name__ == '__main__':
    print('Opdracht 1a.1:')
    print('8! / 16 = 2520 unieke permutaties')
    print('Zie script for beredenering')
    print()
    print('Opdracht 1a.2:')

    count = 0
    for permutation in itertools.permutations(cards, 8):
        count += 1
        if is_valid(permutation):
            print('Eerste oplossing gevonden na', count, 'permutaties')
            break
    count = 0
    for permutation in set(itertools.permutations(cards, 8)):
        count += 1
        if is_valid(permutation):
            print('Eerste oplossing gevonden na', count, 'unieke permutaties')
            break

    print('\nOpdracht 1b:')
    calls = 0
    dfs_solutions = dfs(start_board.copy(), cards.copy())  # 181, 389 (457 tot)
    print('Total calls:', calls)

""" REPL
test()
test2()
board = {0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}

unique_permutations = set(itertools.permutations(cards, 8))
valid_permutations = [perm for perm in unique_permutations if is_valid(perm)]
calls = 0
dfs_solutions = dfs(start_board.copy(), cards.copy(), list(range(8)))  # 83, 106 (116 tot)

dfs_solutions = dfs(start_board.copy(), cards.copy(), list(range(8)))  # 83, 106 (116 tot)
dfs_solutions = dfs(start_board.copy(), cards.copy(), list(reversed(range(8))))  # 12, 14 (167 tot)
dfs_solutions = dfs(start_board.copy(), cards.copy(), [0, 3, 2, 1, 4, 5, 6, 7])  # 106, 134 (152 tot)
dfs_solutions = dfs(start_board.copy(), cards.copy(), [5, 3, 2, 4, 6, 7, 0, 1])  # 355, 380 (1469 tot)
dfs_solutions = dfs(start_board.copy(), cards.copy(), [1, 2, 3, 0, 4, 5, 6, 7])  # 114, 143, 165

print_board({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'})
print_board({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'})
print_board({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'})
print_board({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'})
print_board({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})
print_board({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})
print_board({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})
print_board({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})
print_board({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})
print_board({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})
print_board({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})
print_board({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'})
print_board({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'Q', 6: 'J', 7: 'J'})
"""