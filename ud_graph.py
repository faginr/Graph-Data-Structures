# Course: CS261
# Author: Rex Fagin
# Assignment: HW6
# Description: Methods for an undirected Graph

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        # help(self.add_vertex)
        # if vertex is not a key in adj_list, add as key, initialize empty list
        if v not in self.adj_list:
            self.adj_list[v] = []



    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """

        # if u and v are identical, return none
        if u == v:
            return None

        # add u,v as vertices if they don't exist
        self.add_vertex(u)
        self.add_vertex(v)


        # insert u in v
        if len(u) == 0:
            self.adj_list[u].append(v)

        #
        else:
            # check if v in u
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)

        # insert u in v
        if len(v) == 0:
            self.adj_list[v].append(u)
            #
        else:
            # check if v in u
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # check if vertices exist. If not, return None
        if u not in self.adj_list or v not in self.adj_list:
            return

        # if u and v are the same vertex, return None
        if u == v:
            return

        # if v present in u, remove v
        if u in self.adj_list[v]:
            self.adj_list[v].remove(u)

        # if u present in v, remove u
        if v in self.adj_list[u]:
            self.adj_list[u].remove(v)


    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # if v doesn't exist as a vertex, return None
        if v not in self.adj_list:
            return None

        # remove all edges to/from v in graph
        for vertex in self.adj_list:
            if v in self.adj_list[vertex]:
                self.remove_edge(vertex, v)

        # remove vertex 'v' from graph
        self.adj_list.pop(v)


    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """

        # initialize empty list
        vertices = []
        # append each vertex to list
        for i in self.adj_list:
            vertices.append(i)
        # return list
        return vertices

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """

        # initialize empty list
        edges = []

        # iterate through all vertices
        for vertex in self.adj_list:
            # collect each vertex/edge pair
            for edge in self.adj_list[vertex]:
                # each each edge, skip duplicate edges
                if (edge, vertex) not in edges:
                    edges.append((vertex, edge))

        # return list
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """

        # if path is empty, return true
        if path == []:
            return True

        # if path has only one element, check if vertex is in graph
        if len(path) < 2:
            if path[0] not in self.adj_list:
                return False
            return True

        # iterate through path
        for i in range(0,len(path)-1,1):
            # check if vertex exists
            if path[i] not in self.adj_list:
                return False
            # check if edge exists
            if path[i+1] not in self.adj_list[path[i]]:
                return False

        # if path is complete, return true
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


    def dfs_traverse(self, vertex, visited, v_end):
        """depth first traversal of list of vertices"""

        # add vertex to list
        visited.append(vertex)

        # if a valid end vertex is present, check for end condition
        if v_end is not None:
            if vertex == v_end:
                # if end has been reached, return
                return

        # sort vertex edges by ascending lexicographical order
        self.shell_sort(self.adj_list[vertex])

        # iterate through each edge
        for adjacent in self.adj_list[vertex]:
            # if an adjacent vertex has not been visited
            if adjacent not in visited and v_end not in visited:
                # path down adjacent vertex
                self.dfs_traverse(adjacent, visited, v_end)

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        # check if starting vertex is in the graph
        if v_start not in self.adj_list:
            return []

        # check if end is valid
        if v_end not in self.adj_list:
            v_end = None

        #  create empty list
        visited = []

        # start recursive path from start vertex
        self.dfs_traverse(v_start, visited, v_end)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """

        # check if starting vertex is in the graph
        if v_start not in self.adj_list:
            return []

        # check if end is valid
        if v_end not in self.adj_list:
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

            # sort vertex edges by ascending lexicographical order
            self.shell_sort(self.adj_list[vertex])

            # iterate through each edge
            for adjacent in self.adj_list[vertex]:
                # if an adjacent vertex has not been visited
                if adjacent not in visited:
                    # add vertex to queue
                    vertex_deque.appendleft(adjacent)

        # return results
        return visited


    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """

        # initialize empty count list and visited dictionary
        count = []
        visited = {}

        # set all vertices in visited to False
        for vertex in self.adj_list:
            visited[vertex] = False

        for vertex in self.adj_list:
            # visit each vertex
            if visited[vertex] == False:
                # append dfs for a vertex
                count.append(self.dfs(vertex))
                for visit in visited:
                    for element in count:
                        if visit in element:
                            visited[visit] = True


        return len(count)

    def cycle_traverse(self, vertex, visited, parent):
        """Helper traversal method for has_cycle"""

        # add vertex to list
        visited[vertex] = True

        # sort vertex edges by ascending lexicographical order
        self.shell_sort(self.adj_list[vertex])

        # iterate through each edge
        for adjacent in self.adj_list[vertex]:

            # if an adjacent vertex has not been visited
            if visited[adjacent] == False:
                if self.cycle_traverse(adjacent, visited,vertex) == True:
                    return True

            # if visited = True and adjacent isn't the direct parent, return True
            elif visited[adjacent] == True and adjacent != parent:
                return True

        return False

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        # initialize empty dictionary
        visited = {}

        # populate each vertex with false in visited dictionary
        for vertex in self.adj_list:
            visited[vertex] = False

        # visit each vertex
        for vertex in self.adj_list:
            if visited[vertex] == False:
                # make recursive call
                if(self.cycle_traverse(vertex, visited, None)) == True:
                    return True

        return False




if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
