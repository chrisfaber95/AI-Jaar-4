import time
start_state = 'FGCW'
goal_state = 'FGCW'

current_state = [set(start_state), set()]

def isValid(state):
    if side_is_valid(state[0]) and side_is_valid(state[1]): return True
    return False


def side_is_valid(side):
    if 'F' in side:
        return True
    elif 'G' in side and 'C' in side:
        return False
    elif 'G' in side and 'W' in side:
        return False
    elif 'F' in side and len(side) == 2:
        return False
    return True

def next_states(state):
  # vind de index van de side met de farmer
    farmer = 0 if 'F' in state[0] else 1
    no_farmer = 1 if 'F' in state[0] else 0
    
    def move(actors):
        if actors[0] == actors[1] or (len(actors) == 1 and 'F' in state[0]):
            actors.pop()
        new_state = [set(state[0]), set(state[1])]
        for actor in actors:
            new_state[farmer].remove(actor)
            new_state[no_farmer].add(actor)
        return new_state
        
    possible_states = list()
    for actor in state[farmer]:
        possible_states.append(move(['F', actor]))
    return possible_states

def find_solutions(state, path=(), solutions=list()):
    new_path = path + (state, )
    if set(state[1]) == set(goal_state):
        return solutions.append(new_path)
    for new_state in next_states(state):
        if state not in path and isValid(new_state):
            find_solutions(new_state, new_path, solutions)            
    return solutions

solutions = find_solutions(current_state)
for i, solution in enumerate(solutions):
  print(f'Solution {i+1}, length {len(solution)}')
  for state in solution:
    print(f'{"".join(state[0])}||{"".join(state[1])}')
print()