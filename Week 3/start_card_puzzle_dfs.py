'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
import itertools
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0:[3], 1:[2], 2:[1,4,3], 3:[0,2,5], 4:[2,5], 5:[3,4,6,7], 6:[5], 7:[5]}

def is_valid(b):
    #print(b)
    for i, type in enumerate(b):
        #print(i, type)
        if(b[i] != '.'):
            #print(b, neighbors[i])
            neigh = []
            for j in neighbors[i]:
                if len(b) > j:
                    if b[j] != '.':
                        neigh.append(b[j])
            #neigh = [b[j] for j in neighbors[i]]
            if b[i] in neigh and len(neigh) == len(neighbors[i]):
                return False
            if len(neigh) != 0 and b[i] == 'A' and 'Q' in neigh and len(neigh) == len(neighbors[i]):
                return False
            if len(neigh) != 0 and b[i] == 'A' and 'K' not in neigh and len(neigh) == len(neighbors[i]):
                return False
            if len(neigh) != 0 and b[i] == 'K' and 'Q' not in neigh and len(neigh) == len(neighbors[i]):
                return False
            if len(neigh) != 0 and b[i] == 'Q' and 'J' not in neigh and len(neigh) == len(neighbors[i]):
                return False
            #print("234455----" + b[i])
    return True


def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ',is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('f ',is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})) # [1]
    print('f ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})) # [3]
    print('t ',is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})) # [3] 
    print('f ',is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})) # [3]
    print('f ',is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})) # [4]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})) # [5]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})) # [5]
    print('t ',is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))

start = {}
def dfs1(dict, cardslist, path=()):
    new_path = path + (dict, )
    print('22222' + str(new_path))
    if (len(dict) == len(cards) and is_valid(dict)):
        print(dict)
        return True
    dict[len(dict)] = ''
    for i, v in enumerate(cardslist):
        dict[len(dict)-1] = v
        newcards = cardslist.copy()
        print('----1111' + str(newcards))
        newcards.pop(i)
        print()
        print('----' + str(newcards))
        print()
        if dict not in path and is_valid(dict):
            print(dict)
            dfs(dict, newcards, new_path)
        else:
            return False
    #return False
count1 = 0
def dfs(dict, cardlist):
    global count1
    print(count1)
    if(len(cardlist) < 1 and is_valid(dict)):
        print("-----"+str(dict))
        return True
    for i, v in enumerate(cardlist):
        dict[len(dict)-len(cardlist)] = v
        remain = cardlist.copy()
        remain.pop(i)
        newdict = dict.copy()
        count1 += 1
        if is_valid(newdict):
            dfs(newdict, remain)

count = 0

amount = 8*7*6*5*4*3*2
print(amount)

for f in itertools.permutations(cards, len(start_board)):
    count += 1
print("Options: " +str(count))
   
count = 0 
for f in set(itertools.permutations(cards, len(start_board))):    
        count += 1
print("Unique options: " +str(count))

count = 0
for f in set(itertools.permutations(cards, len(start_board))):        
    if is_valid(f):
        print(f)
        count += 1
print("Valid options: " +str(count))


#test()
dfs(start_board, cards)
#for i, solution in enumerate(solutions):
#  print(f'Solution {i+1}, length {len(solution)}')
#print()

#print("DFS options: " +str(count))


#test()