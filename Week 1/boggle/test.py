from pprint import pprint

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
    
    
# Vorm van prefixes dict:
# 'G': False
# 'A': True
# 'A': False
# 'T': True
# 'K': None
# Het nadeel van deze vorm is dat om te weten dat je de laatste prefix hebt bereikt een stap verder moet gaan dan nodig is.
def make_prefixes(file_name):
  prefixes = dict()
  with open(file_name, 'r') as words:
    for word in words:
      w = word.upper().strip()
      prefixes[w] = True
      for i in range(1, len(w)):
        prefix = w[:i]
        if prefix not in prefixes:
          prefixes[prefix] = False
  return prefixes
          

# Tijdscomplexiteit zou als DFS O=(b^D) moeten zijn, maar door de vorm van de prefixes dict is dit O=(b^d+1) (d= diepte van oplossing en b = <4)
#            (0,1,'I') [(0,0,'P')] 'P'  dict   fun(x,y)
def find_words(letter, path, string, prefixes, successors):
  path = path + [letter]
  string = string + letter[2]
  is_word = prefixes.get(string)
  
  if is_word is None:
    return []
  
  paths = [path] if is_word else []
  for neighbour in successors(letter[0], letter[1]):
    if neighbour not in path:
      paths.extend(find_words(neighbour, path, string, prefixes, successors))
  
  return paths
  
  
def find_all(board, prefixes):
  neighbours = lambda x, y: get_neighbours(x, y, board)
  words = []
  for x in range(len(board)):
    for y in range(len(board)):
      words.extend(find_words((x, y, board[x][y]), [], '', prefixes, neighbours))
  return words


def print_results(results):
  result_and_words = [(''.join(x[2] for x in path), path) for path in results]
  result_and_words.sort(key=lambda r: r[0])
  for i, (word, path) in enumerate(result_and_words):
    print(f'{i}. {word}  {path}')


if __name__ == '__main__':
	board = [
	  ['P', 'I', 'E', 'T'],
	  ['G', 'A', 'A', 'T'],
	  ['A', 'T', 'M', 'S'],
	  ['H', 'U', 'I', 'S']
	]

	prefixes = make_prefixes('words.txt')
	results = find_all(board, prefixes)
	print_results(results)