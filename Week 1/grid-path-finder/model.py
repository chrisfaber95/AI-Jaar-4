import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value

def is_node_blocked(node):
    return get_grid_value(node) == 'b'


def search(app, start, goal):
    # plot a sample path for demonstration
    for i in range(cf.SIZE-1):
        app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
        app.plot_line_segment(i, i+1, i+1, i+1, color=cf.FINAL_C)
        app.pause()

def cost(node, next):
    return 1

def get_neighbors(node):
    neighbors = []
    for dif in [-1, 1]:
        new_x = node[0] + dif
        new_y = node[1] + dif
        if len(grid) > new_x >= 0: neighbors.append((new_x, node[1]))
        if len(grid) > new_y >= 0: neighbors.append((node[0], new_y))
    return neighbors

def UCS(app, start, goal):
    frontier = PriorityQueue()
    visited = dict()
    path = dict()
    print(start)
    visited[start] = 0
    frontier.put(start, 0)
    count = 0
    while not frontier.empty():
        node = frontier.get()

        if node == goal:
            print(f'Found goal node in {count} steps')
            return path
        
        for neighbor in get_neighbors(node):
            if is_node_blocked(node):
                continue
            new_cost = visited[node] + cost(node, neighbor)
            if(neighbor not in visited) or new_cost < visited[node]:
                visited[neighbor] = new_cost
                frontier.put(neighbor, new_cost + visited[node])
                path[neighbor] = node
                #app.plot_node(node, cf.PATH_C)
                #app.plot_line_segment(node[0], node[1], neighbor[0], neighbor[1], color=cf.PATH_C)
        count += 1
    return path

def a_star(app, start, goal):
    
    def heuristic(node1, node2):
        (x1, y1) = node1
        (x2, y2) = node2
        heuristic = abs(x1-x2) + abs(y1-y2)
        return heuristic

    frontier = PriorityQueue()
    visited = dict()
    path = dict()
    visited[start] = 0
    frontier.put(start, 0)
    count = 0
    while not frontier.empty():
        node = frontier.get()

        if node == goal:
            print(f'Found goal node in {count} steps')
            return path
        
        for neighbor in get_neighbors(node):
            if is_node_blocked(node):
                continue
            new_cost = visited[node] + heuristic(node, neighbor)
            if(neighbor not in visited) or new_cost < visited[node]:
                visited[neighbor] = new_cost
                frontier.put(neighbor, new_cost + visited[node])
                path[neighbor] = node
        count += 1
    return path

algorithms = {
  'UC': UCS,
  'A*': a_star
}
def search(app, start, goal):
  alg = algorithms.get(app.alg.get(), lambda a,s,g: print('Unknown algorithm:', app.alg.get()))
  path = alg(app, start, goal)
  if path is not None and path.get(goal):
    app.draw_path(path)
  else:
    print('No path found')