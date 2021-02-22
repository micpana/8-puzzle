import numpy as np
import math
import copy

goal_state = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8]).reshape(3, 3)

class Node:
    def __init__(self, state, parent=None, depth=0, path_cost=0, cost=0, move=''):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.move = move
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __repr__(self):
        return "Node(%s)" % (self.state)

    def __eq__(self, other):
        if isinstance(other, Node):
            return ((np.array_equal(self.state, other.state)))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

    def calculate_heuristic(self, goal_state, h="manhattan"):
        self.heuristic = 0
        if h == 'manhattan':
            for i in range(0, self.state.size):
                current_y, current_x = np.where(self.state == i)
                goal_y, goal_x = np.where(goal_state == i)
                self.heuristic += abs(current_x - goal_x) + abs(current_y - goal_y)

        elif h == 'euclidean':
            for i in range(0, self.state.size):
                current_y, current_x = np.where(self.state == i)
                goal_y, goal_x = np.where(goal_state == i)
                self.heuristic += math.sqrt((current_x - goal_x) ** 2 + (current_y - goal_y) ** 2)

    def calculate_cost(self, goal_state, h):
        self.calculate_heuristic(goal_state, h)
        if self.parent is None:
            self.cost = self.heuristic
        else:
            self.path_cost = self.parent.path_cost + 1
            self.cost = self.path_cost + self.heuristic

    def decrease_key(self, frontier):
        for n in frontier:
            if np.array_equal(self.state, n.state) and self.cost < n.cost:
                self = copy.deepcopy(n)
                break


def go_down(node, x, y):
    if y > 0:
        new_state = copy.deepcopy(node.state)
        new_state[y, x], new_state[y - 1, x] = new_state[y - 1, x], new_state[y, x]
    else:
        return -1
    return Node(new_state, node, node.depth + 1, move='down')


def go_up(node, x, y):
    if y != 2:
        new_state = copy.deepcopy(node.state)
        new_state[y, x], new_state[y + 1, x] = new_state[y + 1, x], new_state[y, x]
    else:
        return -1
    return Node(new_state, node, node.depth + 1, move='up')


def go_right(node, x, y):
    if x > 0:
        new_state = copy.deepcopy(node.state)
        new_state[y, x - 1], new_state[y, x] = new_state[y, x], new_state[y, x - 1]
    else:
        return -1
    return Node(new_state, node, node.depth + 1, move='right')


def go_left(node, x, y):
    if x != 2:
        new_state = copy.deepcopy(node.state)
        new_state[y, x + 1], new_state[y, x] = new_state[y, x], new_state[y, x + 1]
    else:
        return -1
    return Node(new_state, node, node.depth + 1, move='left')


def check_in_list(node_chk, node_list):
    for node in node_list:
        if np.array_equal(node_chk.state, node.state):
            return True
    return False


def get_neighbors(node):
    children = []
    #   print("start"+'\n',state)
    zero_y, zero_x = np.where(node.state == 0)

    down = go_down(node, zero_x, zero_y)
    #   print("down"+'\n',down)
    if type(down) is not int:
        children.append(down)

    up = go_up(node, zero_x, zero_y)
    #   print("up"+'\n',up)
    if type(up) is not int:
        children.append(up)

    left = go_left(node, zero_x, zero_y)
    #   print("left"+'\n',left)
    if type(left) is not int:
        children.append(left)

    right = go_right(node, zero_x, zero_y)
    #   print("right"+'\n',right)
    if type(right) is not int:
        children.append(right)
    return children


def get_path(goal_node):
    path = []
    while goal_node.parent != None:
        path.insert(0, goal_node.move)
        goal_node = goal_node.parent
    return path


def get_nps(start, list):
    if int(timeit.default_timer() - start) == 1:
        print(' visiting', len(list), 'nodes/sec')
        # !clear
    if int(timeit.default_timer() - start) % 60 == 0 and int(timeit.default_timer() - start) > 1:
        print(' ', int(timeit.default_timer() - start) / 60, ' minutes have passed')
        print('visited: ', len(list), 'max depth reached: ', max(list, key=attrgetter('depth')).depth)
        print(' now visiting', int(len(list) / (int(timeit.default_timer() - start))), 'nodes/sec')
        # !clear


from queue import Queue, LifoQueue, PriorityQueue
from operator import attrgetter
import timeit


def bfs(start_state, goal_state):
    start = timeit.default_timer()
    root = Node(start_state, depth=0, move='Start')
    frontier = Queue()
    frontier.put(root)
    frontier_set = set()
    frontier_set.add(root)
    visited = set()

    while not frontier.empty():
        node = frontier.get()
        frontier_set.remove(node)
        #     print("Expanding Node with depth:"+str(node.depth)+'\nSliding '+node.move+', Visited='+str(len(visited))+'\n'+str(node.state))
        visited.add(node)
        get_nps(start, visited)

        if np.array_equal(node.state, goal_state):
            stop = timeit.default_timer()
            return True, get_path(node), node.depth, (stop - start), len(visited)

        for n in get_neighbors(node):
            if n not in visited and n not in frontier_set:
                frontier.put(n, n.cost)
                frontier_set.add(n)

    return False


def dfs(start_state, goal_state):
    start = timeit.default_timer()
    root = Node(start_state, depth=0, move='Start')
    frontier = LifoQueue()
    frontier.put(root)
    frontier_set = set()
    frontier_set.add(root)
    visited = set()

    while not frontier.empty():
        node = frontier.get()
        frontier_set.remove(node)
        #     print("Expanding Node with depth:"+str(node.depth)+'\nSliding '+node.move+', Visited='+str(len(visited))+'\n'+str(node.state))
        visited.add(node)
        get_nps(start, visited)

        if np.array_equal(node.state, goal_state):
            stop = timeit.default_timer()
            return True, get_path(node), max(visited, key=attrgetter('depth')).depth, (stop - start), len(visited)

        for n in get_neighbors(node):
            if n not in visited and n not in frontier_set:
                frontier.put(n, n.cost)
                frontier_set.add(n)

    return False


def a_star(start_state, goal_state, heuristic='manhattan'):
    start = timeit.default_timer()
    root = Node(start_state, depth=0, move='Start')
    frontier = PriorityQueue()
    frontier.put(root, root.cost)
    frontier_set = set()
    frontier_set.add(root)
    visited = set()

    while not frontier.empty():
        node = frontier.get()
        frontier_set.remove(node)
        #     print("Expanding Node with depth:"+str(node.depth)+', fn = '+str(node.cost)+'\nSliding '+node.move+'\n'+str(node.state))
        visited.add(node)
        get_nps(start, visited)

        if np.array_equal(node.state, goal_state):
            stop = timeit.default_timer()
            return True, get_path(node), max(visited, key=attrgetter('depth')).depth, (stop - start), len(visited)

        for n in get_neighbors(node):
            n.calculate_cost(goal_state, heuristic)
            if n not in visited and n not in frontier_set:
                frontier.put(n, n.cost)
                frontier_set.add(n)
            else:
                n.decrease_key(frontier.queue)