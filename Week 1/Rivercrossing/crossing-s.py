# Tijdscomplexitijd:
# Ik denk O(N) als worst case. Je gaat overal maar een keer bij langs, en doet niets opnieuw.

def print_state(state):
    print('{0:<4} || {1:4>}'.format(*(''.join(side) for side in state)))

    
def state_from_string(string):
  return tuple(frozenset(side) for side in string.split('|'))


def is_valid_state(state):
  return is_valid_side(state[0]) and is_valid_side(state[1])


def is_valid_side(side):
  if 'F' in side:
    return True
  elif ('G' in side) and ('W' in side):
    return False
  elif ('G' in side) and ('C' in side):
    return False
  return True


def next_states(state):
  # vind de index van de side met de farmer
  farmer = 0 if 'F' in state[0] else 1
  no_farmer = 1 if 'F' in state[0] else 0
  
  def move(actors):
    new_state = [0,0]
    new_state[farmer] = state[farmer] - actors
    new_state[no_farmer] = state[no_farmer] | actors
    return tuple(new_state)

  return list(move({'F', actor}) for actor in state[farmer])
  

# Recursieve DFS aanpak om de oplossingen te vinden
def find_solutions(goal_state, state, path=(), solutions=set()):
  new_path = path + (state,)
  if state == goal_state:
    return solutions | {new_path}
  
  new_solutions = set()
  for new_state in next_states(state):
    if new_state not in path and is_valid_state(new_state):
      new_solutions.update(find_solutions(goal_state, new_state, new_path, new_solutions))
  
  return solutions | new_solutions
  

start_state = state_from_string('FCWG|')
end_state = state_from_string('|FCWG')

solutions = find_solutions(end_state, start_state)
for i, solution in enumerate(solutions):
  print(f'Solution {i+1}, length {len(solution)}')
  for state in solution:
    print_state(state)
  print()
