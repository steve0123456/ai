from collections import deque, defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = [[] for _ in range(vertices)]

    def add_edge(self, u, v):
        self.adj_list[u].append(v)

    def bfs(self, start, goal):
        visited = [False] * self.V
        queue = deque([start])
        visited[start] = True

        while queue:
            s = queue.popleft()
            print(s, end=" ")
            if s == goal:
                print(f"\nGoal node {goal} reached, stopping BFS.")
                return

            for neighbor in self.adj_list[s]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

        print(f"\nGoal node {goal} not found in the graph.")

# DFS Helper
def dfs_recursive(adj, visited, node, goal):
    visited[node] = True
    print(node, end=" ")
    if node == goal:
        print(f"\nGoal node {goal} reached, stopping DFS.")
        return True

    for neighbor in adj[node]:
        if not visited[neighbor]:
            if dfs_recursive(adj, visited, neighbor, goal):
                return True

    return False

# DFS Main
def dfs(adj, start, goal):
    visited = [False] * len(adj)
    if not dfs_recursive(adj, visited, start, goal):
        print(f"\nGoal node {goal} not found in the graph.")

# Menu Driven
def main():
    g = None
    adj = []
    while True:
        print("\nMenu:")
        print("1. Initialize Graph")
        print("2. Add Edge")
        print("3. Perform BFS")
        print("4. Perform DFS")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            V = int(input("Enter the number of vertices: "))
            g = Graph(V)
            adj = [[] for _ in range(V)]
            print(f"Graph initialized with {V} vertices.")

        elif choice == '2':
            if g is None:
                print("Graph not initialized. Please initialize the graph first.")
                continue
            u, v = map(int, input("Enter the edge (u v): ").split())
            g.add_edge(u, v)
            adj[u].append(v)
            adj[v].append(u)  # Undirected for DFS
            print(f"Edge ({u}, {v}) added.")

        elif choice == '3':
            if g is None:
                print("Graph not initialized. Please initialize the graph first.")
                continue
            start = int(input("Enter the starting vertex for BFS: "))
            goal = int(input("Enter the goal vertex for BFS: "))
            print(f"Following is Breadth First Traversal starting from vertex {start}")
            g.bfs(start, goal)

        elif choice == '4':
            if not adj:
                print("Graph not initialized. Please initialize the graph first.")
                continue
            start = int(input("Enter the starting vertex for DFS: "))
            goal = int(input("Enter the goal vertex for DFS: "))
            print(f"DFS starting from vertex {start}")
            dfs(adj, start, goal)

        elif choice == '5':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
