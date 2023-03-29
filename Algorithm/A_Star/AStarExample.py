import heapq

class Node:
    def __init__(self, x, y, g_score=float('inf'), h_score=0, parent=None):
        self.x = x
        self.y = y
        self.g_score = g_score
        self.h_score = h_score
        self.parent = parent

    def __lt__(self, other):
        return (self.g_score + self.h_score) < (other.g_score + other.h_score)

class AStar:
    def __init__(self, start_point, end_point, obstacles):
        self.start_point = Node(*start_point)
        self.end_point = Node(*end_point)
        self.obstacles = obstacles
        self.heapq = heapq
        
        self.open_list = []
        self.closed_set = set()

        self.heapq.heappush(self.open_list, self.start_point)

    def get_neighbors(self, node):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = node.x + dx, node.y + dy
            if (x, y) not in self.obstacles:
                neighbors.append(Node(x, y))
        return neighbors

    def get_distance(self, node1, node2):
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    def search(self):
        while self.open_list:
            current_node = self.heapq.heappop(self.open_list)

            if current_node == self.end_point:
                path = []
                while current_node:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return list(reversed(path))

            for neighbor_node in self.get_neighbors(current_node):
                if neighbor_node in self.closed_set:
                    continue

                new_g_score = current_node.g_score + self.get_distance(current_node, neighbor_node)

                if (new_g_score < neighbor_node.g_score):
                    neighbor_node.g_score = new_g_score
                    neighbor_node.h_score = self.get_distance(neighbor_node, self.end_point)
                    neighbor_node.parent = current_node

                    if neighbor_node not in self.open_list:
                        self.heapq.heappush(self.open_list, neighbor_node)

            self.closed_set.add(current_node)

        return None  # no path found


def main():
    list = []
    for i, j in zip(range(0,10), range(10, 20)):
        heapq.heappush(list,(i, j))
    print(list)
    heapq.heappop(list)
    heapq.heappop(list)
    print(list)


if __name__ == "__main__":
    main()