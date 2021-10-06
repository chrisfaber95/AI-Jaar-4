def make_prefixes(file_name):
  prefixes = dict()
  with open(file_name, 'r') as words:
    for word in words:
        w = word.strip()
        current = prefixes
        for i in w:
            if i not in current:
                current[i] = dict()
            current = current[i]
        current['#']=1
  return prefixes


def search(word):
    global prefix
    word = word.lower()
    current = prefix
    for l in word:
        if l not in current:
                return False
        current = current[l]
    if '#' in current:        
        return True
    return len(current)

def get_neighbour_coords(x, y, boardsize):
  neighbours = []
  for diff in [-1, 1]:
    new_x = x + diff
    new_y = y + diff
    
    new_x = 0 if new_x >= boardsize else (boardsize - 1 if new_x < 0 else new_x)
    new_y = 0 if new_y >= boardsize else (boardsize - 1 if new_y < 0 else new_y)
    
    neighbours.append((new_x, y))
    neighbours.append((x, new_y))

  return neighbours


def get_neighbours(x,y, board):
  coords = get_neighbour_coords(x, y, len(board))
  return [(coord[0], coord[1], board[coord[0]][coord[1]]) for coord in coords]
  
def find_words(letter, path, string, successors, solutions=list()):
    path = path + [letter]
    string = string + letter[2]
    is_word = search(string)
    if is_word is False:
        return []
    elif is_word is True:
        if string not in solutions:
            solutions.append([string, path])
    for neighbour in successors(letter[0], letter[1]):
        if neighbour not in path:
            find_words(neighbour, path, string, successors, solutions)
    return solutions
  
  
def find_all(board):
    neighbours = lambda x, y: get_neighbours(x, y, board)
    words = []
    for x in range(len(board)):
        for y in range(len(board)):
            words.extend(find_words((x, y, board[x][y]), [], '', neighbours))
    return words

def print_results(results):
    r = list()
    for k in results:
        r.append(k)
    r.sort()
    unique = set()
    for k in r:
        unique.add(k[0])
        #print(f'{k[0]}  {k[1]}')
    print(unique)

if __name__ == '__main__':
	board = [
	  ['P', 'I', 'E', 'T'],
	  ['G', 'A', 'A', 'T'],
	  ['A', 'T', 'M', 'S'],
	  ['H', 'U', 'I', 'S']
	]

	prefix = make_prefixes('words.txt')
	results = find_all(board)
	print_results(results)