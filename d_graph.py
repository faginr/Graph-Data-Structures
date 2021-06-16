# Course: CS261 - Data Structures
# Author: Rex Fagin
# Assignment: HW6
# Description: Methods for directed graphs

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a vertex to the graph
        """

        # add a new row
        self.adj_matrix.append([])
        # build columns
        for col in self.adj_matrix:
            # make sure each row has cols == v_count
            while len(col) <= self.v_count:
                col.append(0)

        # increment v_count, return current count
        self.v_count += 1
        return self.v_count



    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds an edge to the graph
        """
        # if u and v are identical, return None
        if src == dst:
            return None

        # if source is outside graph bounds, return None
        if src < 0 or src >= self.v_count:
            return None

        # if destination is outside grapsh bounds, return None
        if dst < 0 or dst >= self.v_count:
            return None

        # if weight is not positive, return None
        if weight < 1:
            return None

        self.adj_matrix[src][dst] = weight




    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove an edge from the graph
        """

        # if source is outside graph bounds, return None
        if src < 0 or src >= self.v_count:
            return None

        # if destination is outside grapsh bounds, return None
        if dst < 0 or dst >= self.v_count:
            return None

        self.adj_matrix[src][dst] = 0




    def get_vertices(self) -> []:
        """
        Return the vertices of the graph
        """

        vertices = []
        for vertex in range(0,self.v_count,1):
            vertices.append(vertex)
        return vertices

    def get_edges(self) -> []:
        """
        Return a list of the edges in the graph
        """

        # create empty list of edges
        edges = []

        # counter for rows
        row_coord = 0
        # iterate through rows
        for row in self.adj_matrix:
            # counter for columns
            col = 0
            # for each edge in row
            for edge in row:
                # append edges that exist
                if edge != 0:
                    edges.append((row_coord,col,edge))
                # increment column counter
                col += 1
            # increment row counter
            row_coord += 1

        # return edges
        return edges

    def get_edge(self, row, col):
        """Takes a row and col and return the weight of the cooresponding edge"""

        # return edge at row/col
        return self.adj_matrix[row][col]


    def is_valid_path(self, path: []) -> bool:
        """
        Return True if sequence is a valid path in the graph. Otherwise return False
        """
        # if path is empty, return true
        if path == []:
            return True

        # if path has only one element, check if vertex is in graph
        if len(path) < 2:
            if path[0] not in self.get_vertices():
                return False
            return True

        # iterate through path
        for i in range(0, len(path) - 1, 1):
            # check if vertex exists
            if path[i] not in self.get_vertices():
                return False
            # check if edge exists
            if self.get_edge(path[i], path[i+1]) == 0:
                return False

        return True

    def shell_sort(self, arr):
        """Sort an unordered list in acsending order"""

        # initialize array size and gap value
        arr_size = len(arr)
        gap = arr_size // 2

        # only sort arrays with size > 2
        if arr_size < 2:
            return arr

        # iterate until gap is adjacent
        while gap > 0:
            # iterate pairs of current gap distance
            for i in range(gap, arr_size):

                # get value at i
                value = arr[i]
                pos = i

                # insertion sort
                while pos >= gap and arr[pos - gap] > value:
                    arr[pos] = arr[pos - gap]
                    pos -= gap
                arr[pos] = value
            # halve gap
            gap = gap // 2

        # return sorted array
        return arr

    def get_adjacents(self, vertex):
        """Find all adjacent edges to a vertex, return as a list"""

        # initialize empty list
        adjacents = []

        count = 0
        # append count for nonzero edges
        for edge in self.adj_matrix[vertex]:
            if edge != 0:
                adjacents.append(count)
            count += 1

        # return list
        return adjacents

    def dfs_traverse(self, vertex, visited, v_end):
        """depth first traversal of list of vertices"""

        # # add vertex to list
        visited.append(vertex)

        # if a valid end vertex is present, check for end condition
        if v_end is not None:
            if vertex == v_end:
                # if end has been reached, return
                return

        # get adjacent vertices to vertex
        adjacents = self.get_adjacents(vertex)

        # sort vertex edges by ascending lexicographical order
        self.shell_sort(adjacents)

        # iterate through adjacents
        for adjacent in adjacents:
            # if adjacent is not visited and not in v_end
            if adjacent not in visited and v_end not in visited:
                # make recursive call
                self.dfs_traverse(adjacent, visited,v_end)

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        vertices = self.get_vertices()

        # check if starting vertex is in the graph
        if v_start not in vertices:
            return []

        # check if end is valid
        if v_end not in vertices:
            v_end = None

        #  create empty list
        visited = []

        self.dfs_traverse(v_start, visited, v_end)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """

        vertices = self.get_vertices()

        # check if starting vertex is in the graph
        if v_start not in vertices:
            return []

        # check if end is valid
        if v_end not in vertices:
            v_end = None

        #  create empty list
        visited = []

        # initialize empty deque
        vertex_deque = deque()

        # add v_start to deque
        vertex_deque.appendleft(v_start)

        # if deque has vertices, pop a vertex
        while vertex_deque != deque([]):
            # take the first element out of the queue
            vertex = vertex_deque.pop()

            # add vertex to visited if its not a duplicate
            if vertex not in visited:
                visited.append(vertex)

            # check if vertex is end
            if v_end is not None:
                if vertex == v_end:
                    # if end has been reached, return
                    return visited

            # get adjacent vertices to vertex
            adjacents = self.get_adjacents(vertex)

            # sort vertex edges by ascending lexicographical order
            self.shell_sort(adjacents)

            # iterate through each edge
            for adjacent in adjacents:
                # if an adjacent vertex has not been visited
                if adjacent not in visited:
                    # add vertex to queue
                    vertex_deque.appendleft(adjacent)

        # return results
        return visited

    def cycle_traverse(self, vertex, visited, stack):
        """Helper traversal method for has_cycle"""

        # add vertex to list
        visited[vertex] = True
        stack[vertex] = True

        # get adjacent vertices to vertex
        adjacents = self.get_adjacents(vertex)

        # sort vertex edges by ascending lexicographical order
        self.shell_sort(adjacents)

        # iterate through each edge
        for adjacent in adjacents:

            # if an adjacent vertex has not been visited
            if visited[adjacent] == False:
                if self.cycle_traverse(adjacent,visited,stack) == True:
                    return True

            # if adjacent is true in stack, return True
            elif stack[adjacent] == True:
                return True

        stack[vertex] = False
        return False

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        # initialize empty dicts
        visited = {}
        stack = {}

        # populate with vertices
        vertices = self.get_vertices()
        stack = self.get_vertices()

        # set all values to False
        for vertex in vertices:
            visited[vertex] = False
            stack[vertex] = False

        # Make recursive calls for vertecies that have not been visited
        for vertex in vertices:
            if visited[vertex] == False:
                if (self.cycle_traverse(vertex, visited, stack)) == True:
                    return True

        return False

    def dijkstra(self, src: int) -> []:
        """
        Return a list of vertices with shortest possible path from the source
        """

        # create list of distances for each vertex, initialize to infinity
        distances = self.get_vertices()
        for dist in distances:
            if distances[dist] ==  distances[src]:
                # set src distance as 0
                distances[dist] = 0
            else:
                distances[dist] = float("inf")
        # create a set for visited
        visited = set()

        # iterate as long as source is updated
        while src != -1:
            # set src to -1, min_distance to infinity
            src, min_distance = -1, float('inf')
            # for vertex in vertices
            for v in range(self.v_count):
                # if a vertex dist < min_distance and not visited
                if distances[v] < min_distance and v not in visited:
                    # set src to vertex, min_distance to vertex
                    src, min_distance = v, distances[v]

            # if there are no shorter unvisited vertecies than inf, return distances
            if src == -1:
                return distances

            # add current vertex to set
            visited.add(src)
            # iterate through all dsts in vertices
            for dist in range(self.v_count):
                # if dst hasn't been visited and the edge exists
                if dist not in visited and self.adj_matrix[src][dist] > 0:
                    # check if dst value is an edge to source and if src to dist is lower
                    if distances[dist] > distances[src] + self.adj_matrix[src][dist]:
                        # if so, set new quicker path to that vertex's distance
                        distances[dist] = distances[src] + self.adj_matrix[src][dist]

        # return list of distances
        return distances



if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
