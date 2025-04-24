import heapq
import copy
def heuristic(state, goal):
    """Calculates the number of misplaced tiles"""
    return sum(state[i][j] != goal[i][j] and state[i][j] != 0 for i in range(3) for j in range(3))
def find_blank(state):
    """Find the blank (zero) position"""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
def generate_moves(state):
    """Generate all possible moves for the blank space"""
    x, y = find_blank(state)
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            moves.append(new_state)
    return moves
def a_star_search(start, goal):
    """Performs A* search on the 8-puzzle problem"""
    heap = []
    heapq.heappush(heap, (0, start, [], 0))  # (cost, state, path, g)
    visited = set()
    while heap:
        cost, current_state, path, g = heapq.heappop(heap)
       
        # Generate all possible moves from the current state
        possible_moves = generate_moves(current_state)
        move_info = []
       
        for move in possible_moves:
            move_g = g + 1
            move_h = heuristic(move, goal)
            move_f = move_g + move_h
            move_info.append((move, move_f, move_g, move_h))
       
        # Print all f(n) values for the possible moves at this step
        print(f"Step {g}: Possible moves and their f(n) values:")
        for move, move_f, move_g, move_h in move_info:
            print(f"f(n) = {move_f} (g(n) = {move_g}, h(n) = {move_h})")
       
        # Now choose the move with the smallest f(n)
        best_move = min(move_info, key=lambda x: x[1])
        best_move_state = best_move[0]
        best_move_f = best_move[1]
        best_move_g = best_move[2]
       
        # Display the matrix of the current state if it's the optimal move at this step
        print(f"Selected Optimal Move (f(n) = {best_move_f}):")
        for row in best_move_state:
            print(row)
        print("\n↓\n")
       
        # If we find the goal state, return the path leading to it
        if best_move_state == goal:
            print("\nOptimal Solution Found:")
            for row in best_move_state:
                print(row)  # Only print the matrix for the optimal solution at the end
            return  # Don't return the optimal path, just the final matrix state
       
        # Add the best move to the priority queue for further exploration
        visited.add(tuple(map(tuple, current_state)))  # Mark current state as visited
        heapq.heappush(heap, (best_move_f, best_move_state, path + [current_state], best_move_g))
    # If no solution found
    return None
# Function to take user input for the puzzle
def get_puzzle_input(prompt):
    print(prompt)
    puzzle = []
    for i in range(3):
        row = list(map(int, input(f"Enter row {i+1}: ").split()))
        puzzle.append(row)
    return puzzle
# Get initial and goal states from the user
start_state = get_puzzle_input("Enter the initial state of the puzzle:")
goal_state = get_puzzle_input("Enter the goal state of the puzzle:")
a_star_search(start_state, goal_state)

