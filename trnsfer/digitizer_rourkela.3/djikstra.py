import sys


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class Graph:
    def __init__(self):
        self.max_row = 9
        self.max_col = 9
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm[0] > self.max_row or frm[1] > self.max_col:
            print "Skip " + str(frm)
            return
        if to[0] > self.max_row or to[1] > self.max_col:
            print "Skip " + str(to)
            return

        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous


def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


import heapq


def dijkstra(aGraph, start, target):
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)


        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v)
                           for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


def getPath(frm,to,k,obstacles):

    g = Graph()


    row = 0
    col = 0

    # (0,2),(2,2),(1,3),(2,0),(4,4)]#(0,2),(2,2),(1,3),(2,0),(4,4)

    masterTable = []
    for row in range(0, k):
        for col in range(0, k):
            g.add_vertex((row, col))


    for row in range(0, k):
        for col in range(0, k):

            if((row, col) in obstacles):
                g.add_edge((row, col), (row, col + 1), 999)
                g.add_edge((row, col), (row + 1, col), 999)
                g.add_edge((row, col), (row + 1, col + 1), 999)

            elif ((row, col + 1) in obstacles):
                g.add_edge((row, col), (row, col + 1), 999)
                g.add_edge((row, col), (row + 1, col), 1)
                g.add_edge((row, col), (row + 1, col + 1), k)
            elif ((row + 1, col) in obstacles):
                g.add_edge((row, col), (row, col + 1), 1)
                g.add_edge((row, col), (row + 1, col), 999)
                g.add_edge((row, col), (row + 1, col + 1), k)
            elif ((row + 1, col + 1) in obstacles):
                g.add_edge((row, col), (row, col + 1), 1)
                g.add_edge((row, col), (row + 1, col), 1)
                g.add_edge((row, col), (row + 1, col + 1), 999)
            else:
                g.add_edge((row, col), (row, col + 1), 1)
                g.add_edge((row, col), (row + 1, col), 1)
                g.add_edge((row, col), (row + 1, col + 1), k)


    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()


    dijkstra(g, g.get_vertex(frm), g.get_vertex(to))

    target = g.get_vertex(to)
    path = [target.get_id()]
    shortest(target, path)

    return path[::-1]
