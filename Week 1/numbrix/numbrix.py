n = 9
board = [[0] * n for i in range(n)]
clues = []
start = None,
visited = None,
path = []
stepcount = [0]
	
def printBoard(board):
	for row in board:
		print(' '.join([str(elem) for elem in row]))

def neighbors(cell):
	global n
	global board
	c = []
	if cell[0] > 0:
		c.append([board[cell[0]-1][cell[1]], (cell[0]-1, cell[1])])
	if cell[1] > 0:
		c.append([board[cell[0]][cell[1]-1], (cell[0], cell[1]-1)])
	if cell[1] <  n-1:
		c.append([board[cell[0]][cell[1]+1], (cell[0], cell[1]+1)])
	if cell[0] < n-1:
		c.append([board[cell[0]+1][cell[1]], (cell[0]+1, cell[1])])
	
	return c

def fillBoard():
	global board, clues, start, s	
	
	for r, row in enumerate(s.splitlines()):
		for c, cell in enumerate(row.split()):
			val = int(cell)
			board[r-1][c] = val
			clues.append(val)
			if val == 1:
				start = (r-1, c)
	clues.sort()

def clueLoc(value):
	global board, clues, start, s	
	
	for r, row in enumerate(s.splitlines()):
		for c, cell in enumerate(row.split()):
			val = int(cell)
			board[r-1][c] = val
			clues.append(val)
			if val == value:
				start = (r-1, c)
				break
	return start
	
def solve(position, next_clue_in_list):
	global board, stepcount, clues
	k = None
	if len(stepcount) == 81:
		print("Done")
		print(path)
		print("-----------")
		printBoard(board)
	else:
		k = [item for item in neighbors(position)]
		step  = stepcount[0]
		neighbor = -1
		if stepcount[-1] > len(k) - 1:
			if len(stepcount) not in clues:
				board[path[-1][0]][path[-1][1]] = 0
			else:
				loc = clueLoc(len(stepcount))
				if path[-1][0] != loc[0] or path[-1][0] != loc[1]:
					board[path[-1][0]][path[-1][1]] = 0
			path.pop()
			stepcount.pop()
			stepcount[-1] += 1
			solve(path[-1], next_clue_in_list)
		else:
			for idx, item in enumerate(k):
				if item[0] == next_clue_in_list and len(stepcount) +1 == next_clue_in_list:
					neighbor = idx
					node = k[idx]
					break
				else:
					node = k[stepcount[-1]]
			if neighbor != -1:
				board[node[1][0]][node[1][1]] = len(stepcount) + 1
				newPosition = (node[1][0], node[1][1])
				stepcount.append(0)
				next = 0
				for item in clues:
					if item > len(stepcount):
						next = item
						break			
				path.append(newPosition)
				solve(newPosition, next)
			else:
				if node[0] == 0:
					if len(stepcount) + 1 == next_clue_in_list:
						if len(stepcount) not in clues:
							board[path[-1][0]][path[-1][1]] = 0
						else:
							loc = clueLoc(len(stepcount))
							if path[-1][0] != loc[0] or path[-1][0] != loc[1]:
								board[path[-1][0]][path[-1][1]] = 0
						path.pop()
						stepcount.pop()
						stepcount[-1] += 1
						solve(path[-1], next_clue_in_list)
					elif len(stepcount) +1 < next_clue_in_list:
						stepcount.append(0)
						board[node[1][0]][node[1][1]] = len(stepcount)
						newPosition = (node[1][0], node[1][1])
						path.append(newPosition)
						solve(newPosition, next_clue_in_list)
				elif node[0] != 0:
					if stepcount[-1] < len(k)-1:
						stepcount[-1] += 1
						solve(path[-1], next_clue_in_list)
					elif stepcount[-1] == len(k)-1:
						if len(stepcount) not in clues:						
							board[path[-1][0]][path[-1][1]] = 0
						else:
							loc = clueLoc(len(stepcount))
							if path[-1][0] != loc[0] or path[-1][0] != loc[1]:
								board[path[-1][0]][path[-1][1]] = 0
						path.pop()
						stepcount.pop()
						stepcount[-1] += 1
						solve(path[-1], next_clue_in_list)
					
s = """
0 0 0 0 0 0 0 0 81
0 0 46 45 0 55 74 0 0
0 38 0 0 43 0 0 78 0
0 35 0 0 0 0 0 71 0
0 0 33 0 0 0 59 0 0
0 17 0 0 0 0 0 67 0
0 18 0 0 11 0 0 64 0
0 0 24 21 0 1 2 0 0
0 0 0 0 0 0 0 0 0 """ 
	
	
fillBoard()
for item in clues:
	if item > len(stepcount):
		first = item
		break

solve(start, first)