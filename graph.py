"""
The polar expedition graph!
===========================

Contains the graph connecting the vertices (or base stations) on the map.

This is going to be the main file that you are modifying. :)

Usage:
    Contains the graph, requires the connection to vertices and edges.
"""
import math

from vertex import Vertex
from edge import Edge


# Define a "edge already exists" exception
# Don't need to modify me.
class EdgeAlreadyExists(Exception):
    """Raised when edge already exists in the graph"""
    def __init__(self, message):
        super().__init__(message)


class Graph:
    """
    Graph Class
    -----------

    Represents the graph of vertices, which is equivalent to the map of base
    stations for our polar expedition.

    Attributes:
        * vertices (list): The list of vertices
    """

    def __init__(self):
        """
        Initialises an empty graph
        """
        self._vertices = []

    def insert_vertex(self, x_pos, y_pos):
        """
        Insert the vertex storing the y_pos and x_pos

        :param x_pos: The x position of the new vertex.
        :param y_pos: The y position of the new vertex.

        :type x_pos: float
        :type y_pos: float

        :return: The new vertex, also stored in the graph.
        """

        v = Vertex(x_pos, y_pos)
        self._vertices.append(v)
        return v

    def insert_edge(self, u, v):
        """
        Inserts the edge between vertex u and v.

        We're going to assume in this assignment that all vertices given to
        this will already exist in the graph.

        :param u: Vertex U
        :param v: Vertex V

        :type u: Vertex
        :type v: Vertex

        :return: The new edge between U and V.
        """

        e = Edge(u, v)

        # Check that the edge doesn't already exist
        for i in u.edges:
            if i == e:
                # Edge already exists.
                raise EdgeAlreadyExists("Edges already exist between vertex!")

        # Add the edge to both nodes.
        u.add_edge(e)
        v.add_edge(e)

    def remove_vertex(self, v):
        """
        Removes the vertex V from the graph.
        :param v:  The pointer to the vertex to remove
        :type v: Vertex
        """

        # Remove it from the list
        del self._vertices[self._vertices.index(v)]

        # Go through and remove all edges from that node.
        while len(v.edges) != 0:
            e = v.edges.pop()
            u = self.opposite(e, v)
            u.remove_edge(e)

    @staticmethod
    def distance(u, v):
        """
        Get the distance between vertex u and v.

        :param u: A vertex to get the distance between.
        :param v: A vertex to get the distance between.

        :type u: Vertex
        :type v: Vertex
        :return: The Euclidean distance between two vertices.
        """

        # Euclidean Distance
        # sqrt( (x2-x1)^2 + (y2-y1)^2 )

        return math.sqrt(((v.x_pos - u.x_pos)**2) + ((v.y_pos - u.y_pos)**2))

    @staticmethod
    def opposite(e, v):
        """
        Returns the vertex at the other end of v.
        :param e: The edge to get the other node.
        :param v: Vertex on the edge.
        :return: Vertex at the end of the edge, or None if error.
        """

        # It must be a vertex on the edge.
        if v not in (e.v, e.u):
            return None

        if v == e.u:
            return e.v

        return e.u

    ##############################################
    # Implement the functions below
    ##############################################

    def find_emergency_range(self, v):
        """
        Returns the distance to the vertex W that is furthest from V.oooooo
        :param v: The vertex to start at.
        :return: The distance of the vertex W furthest away from V.
        """

        # Easy way, loop through all the vertices, work out the distances
        # and keep the maximum..
        # However, this is not the best way!
        max = 0
        for u in self._vertices:
            d = self.distance(v, u)
            if d > max:
                max = d
        return max

    ########################################
    # DFS
    ########################################

    def _DFS_visit(self, visited, parent, start, u, r):
        """
        Visit the nodes
        :param visited: The set of visited nodes
        :param parent: The parents of nodes
        :param start: The starting node
        :param u: The current node being visited
        :param r: The range
        """
        visited.append(u)

        for e in u.edges:
            v = self.opposite(e, u)
            if v not in visited:
                parent[v] = u
                if self.distance(start, v) <= r:
                    self._DFS_visit(visited, parent, start, v, r)

    def _DFS_path(self, b, s, r):
        """
        Perform a DFS to find the path
        :param b: The start node
        :param s: The destination
        :param r: The range to stay within

        :type b: Vertex
        :type s: Vertex
        :type r: float
        :return: The path of nodes
        """

        visited = []
        parent = {x: None for x in self._vertices}

        # Start the DFS from this node, we know it's connected so we'll get
        # to every node we need to visit.
        self._DFS_visit(visited, parent, b, b, r)

        # now find the path by backtracing
        c = s
        path = []
        while c != b:
            path.append(c)
            c = parent[c]
            if c is None:
                # We've reached the end, and we didn't find the node
                # Therefore it's an invalid path
                return None
        if c not in path:
            path.append(c)
        path.reverse()
        return path

    ########################################
    # BFS
    ########################################

    def _BFS_path(self, b, s, r):
        """
        Do a BFS
        :param b: The start node.
        :param s: The node to reach
        :param r: The range to stay within.
        :return: The path of the nodes
        """

        seen = []
        layers = []
        next = []
        current = [b]
        parents = {x: None for x in self._vertices}

        v = None
        seen.append(b)
        while len(current) != 0:
            layers.append(current)

            for current_node in current:
                # Loop through the current node's connections
                for current_edge in current_node.edges:
                    # Get the correct node from the edge
                    v = self.opposite(current_edge, current_node)
                    if v not in seen:
                        seen.append(v)
                        if self.distance(b, v) <= r:
                            next.append(v)
                            parents[v] = current_node
                    if v == s:
                        break
            # Sneaky hax
            if v == s:
                break

            # Update the current and next
            current = next
            next = []

        # now find the path by backtracing
        c = s
        path = []
        while c != b:
            path.append(c)
            c = parents[c]
            if c is None:
                # We've reached the end, and we didn't find the node
                # Therefore it's an invalid path
                return None
        if c not in path:
            path.append(c)
        path.reverse()
        return path

    def find_path(self, b, s, r):
        """
        Find a path from vertex B to vertex S, such that the distance from B to
        every vertex in the path is within R.  If there is no path between B
        and S within R, then return None.

        :param b: Vertex B to start from.
        :param s: Vertex S to finish at.
        :param r: The maximum range of the radio.
        :return: The LIST of the VERTICES in the path.
        """
        if b == s:
            return [b]
        p = self._BFS_path(b, s, r)
        # p = self._DFS_path(b, s, r)
        return p

    def minimum_range(self, b, s):
        """
        Returns the minimum range required to go from Vertex B to Vertex S.
        :param b: Vertex B to start from.
        :param s: Vertex S to finish at.
        :return: The minimum range in the path to go from B to S.
        """

        # Get the maximum distance, so we know where to start the range.
        path_range = self.find_emergency_range(b) + 0.1

        current_path = self.find_path(b, s, path_range)
        result_path = None

        # Keep decreasing the range until we hit no path
        while current_path is not None:
            result_path = current_path
            path_range = max([self.distance(b, i) for i in result_path]) - 0.01
            if path_range <= 0:
                break
            current_path = self.find_path(b, s, path_range)

        # Now that we have the shortest available path, return the distance

        res_dist = max([self.distance(b, v) for v in result_path])

        return res_dist

    def move_vertex(self, v, new_x, new_y):
        """
        Move the defined vertex.
        :param v: The vertex to move
        :param new_x: The new X position
        :param new_y: The new Y position
        """

        for u in self._vertices:
            # Check if there exists a node in the way
            if u.x_pos == new_x and u.y_pos == new_y:
                return

        v.move_vertex(new_x, new_y)
