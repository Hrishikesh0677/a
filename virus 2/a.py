import heapq
import copy

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.g = self.h = 0

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def __hash__(self):
        return hash(str(self.state))

    def heuristic(self, goal_state):
        return sum(1 for i in range(3) for j in range(3) if self.state[i][j] != goal_state[i][j])

def get_blank_position(state):
    return next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)

def get_neighbors(node):
    i, j = get_blank_position(node.state)
    neighbors = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        ni, nj = i + dx, j + dy
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_state = copy.deepcopy(node.state)
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
            neighbors.append(Node(new_state, node))
    return neighbors

def astar(initial_state, goal_state):
    open_list = []
    closed_set = set()

    start = Node(initial_state)
    start.h = start.heuristic(goal_state)
    heapq.heappush(open_list, start)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.state == goal_state:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node)

        for neighbor in get_neighbors(current_node):
            neighbor.g = current_node.g + 1
            neighbor.h = neighbor.heuristic(goal_state)
            if neighbor not in closed_set:
                heapq.heappush(open_list, neighbor)

    return None

def print_board(state):
    for row in state:
        print(" ".join(map(str, row)))

def create_state(prompt):
    print(prompt)
    state = []
    for _ in range(3):
        row = list(map(int, input().split()))
        if len(row) != 3:
            print("Error: Each row must contain exactly 3 numbers.")
            return create_state(prompt)
        state.append(row)
    return state

def main():
    initial_state = create_state("Enter the initial state (3x3 grid, use 0 to represent the blank space):")
    goal_state = create_state("Enter the goal state (3x3 grid, use 0 to represent the blank space):")

    path = astar(initial_state, goal_state)
    if path:
        print("\nSolution:")
        for state in path:
            print_board(state)
            print()
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
