"""
Test more complex interaction between functions, e.g. path + move + path
"""

import math
import unittest
import timeout_decorator

from vertex import Vertex
from graph import Graph

# Tolerance for the threshold of distances
TOLERANCE_THRESHOLD=0.001

def approx_value(a, b):
    """
    Asserts that the value of a and b are approximately close.
    :param a: A number to compare to.
    :param b: A number to compare against.
    :return: The bool if they're approximate
    """

    return math.isclose(a, b, abs_tol=TOLERANCE_THRESHOLD)


def check_is_path(G, start, p, r):
    """
    Check that the path is indeed correct
    :param G: the graph
    :param start: The starting vertex.
    :param p: Path of vertices to visit.
    :param r: Range for the path
    :return bool if is a path
    """

    assert p is not None, "Path returned was 'None' when it should be a path."

    # start the path with vertex 0
    current_v = p[0]
    next_in_path = 1

    while next_in_path < len(p):
        assert current_v is not None, "Found None in path: {}".format(p)
        # Get all the vertices in the edges:
        e_set = [G.opposite(e, current_v) for e in current_v.edges]
        assert p[next_in_path] in e_set, \
            """
            Your path ({}) includes non-existing edge
            from {} to {}.""".format(
                p,
                current_v,
                p[next_in_path]
            )

        assert G.distance(start, current_v) <= r, \
            """
            Vertex {} is outside range {} from start {}.
            Its range is {}""".format(
                current_v,
                r,
                start,
                G.distance(start, current_v)
            )
        current_v = p[next_in_path]
        next_in_path += 1

    assert current_v == p[-1], \
        "Your path ({}) didn't return a full path!".format(p)


class TestComplexInteractions(unittest.TestCase):

    @timeout_decorator.timeout(1)
    def test_path_move_path(self):
        """ #score(3) """

        G = Graph()

        # Layer 1
        A = G.insert_vertex(0, 0)

        # Layer 2
        B = G.insert_vertex(2, 0)
        C = G.insert_vertex(2, 4)
        D = G.insert_vertex(2, 6)

        # Layer 3
        E = G.insert_vertex(3, 3)
        F = G.insert_vertex(4, 6)

        # Make the edges
        G.insert_edge(A, B)
        G.insert_edge(A, C)
        G.insert_edge(A, D)
        G.insert_edge(C, E)
        G.insert_edge(C, F)
        G.insert_edge(D, F)

        # Now get the path
        r = 7.7
        p = G.find_path(A, F, r)
        check_is_path(G, A, p, r)

        expected = [[A, C, F], [A, D, F]]

        assert A == p[0], "Path did not start at correct vertex in G.find_path"
        assert F == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        G.move_vertex(C, 2, 10)

        p = G.find_path(A, F, r)
        check_is_path(G, A, p, r)

        expected = [[A, D, F]]

        assert A == p[0], "Path did not start at correct vertex in G.find_path"
        assert F == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p in expected, "Path {} was not the most minimal hop path".format(p)

        G.move_vertex(D, 2, 12)
        p = G.find_path(A, F, r)
        assert p is None, "Path {} was returned " \
                          "when no paths exist within {}".format(p, r)


    @timeout_decorator.timeout(1)
    def test_emergency_move_emergency(self):
        """ #score(3) """

        G = Graph()

        m = G.insert_vertex(0, 0)
        a = G.insert_vertex(0, 7)
        b = G.insert_vertex(7, 7)
        c = G.insert_vertex(7, 0)
        d = G.insert_vertex(7, -7)
        e = G.insert_vertex(0, -7)
        f = G.insert_vertex(-7, -7)
        g = G.insert_vertex(-7, 0)
        h = G.insert_vertex(-7, 7)

        G.insert_edge(m, a)
        G.insert_edge(a, b)
        G.insert_edge(b, c)
        G.insert_edge(c, d)
        G.insert_edge(d, e)
        G.insert_edge(e, f)
        G.insert_edge(f, g)
        G.insert_edge(g, h)


        expected_r = 9.8995
        r = G.find_emergency_range(m)
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        G.move_vertex(f, -18, -19)
        expected_r = 26.17250
        r = G.find_emergency_range(m)

        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        expected_r = 36.06938
        r = G.find_emergency_range(b)

        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

    @timeout_decorator.timeout(1)
    def test_emergency_minimum(self):
        """ #score(4) """

        G = Graph()

        m = G.insert_vertex(0, 0)
        a = G.insert_vertex(0, 7)
        b = G.insert_vertex(7, 7)
        c = G.insert_vertex(7, 0)
        d = G.insert_vertex(7, -7)
        e = G.insert_vertex(0, -7)
        f = G.insert_vertex(-7, -7)
        g = G.insert_vertex(-7, 0)
        h = G.insert_vertex(-7, 7)

        G.insert_edge(m, a)
        G.insert_edge(a, b)
        G.insert_edge(b, c)
        G.insert_edge(c, d)
        G.insert_edge(d, e)
        G.insert_edge(e, f)
        G.insert_edge(f, g)
        G.insert_edge(g, h)

        expected_r = 9.8995
        r = G.find_emergency_range(m)
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        r = G.minimum_range(m, h)

        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        G.move_vertex(f, -18, -19)
        expected_r = 26.17250
        r = G.find_emergency_range(m)
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        r = G.minimum_range(m, h)
        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        G.move_vertex(d, 17, 20)
        expected_r = 26.24881
        r = G.find_emergency_range(m)
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        r = G.minimum_range(m, h)
        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        # Let's add an edge between m and h
        G.insert_edge(m, h)
        r = G.find_emergency_range(m)
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        expected_r = 9.89949
        r = G.minimum_range(m, h)
        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

    @timeout_decorator.timeout(1)
    def test_path_move_remove(self):
        """ #score(3) """

        G = Graph()

        # Layer 1
        A = G.insert_vertex(0, 0)

        # Layer 2
        B = G.insert_vertex(2, 0)
        C = G.insert_vertex(2, 20)
        D = G.insert_vertex(2, 6)

        # Layer 3
        E = G.insert_vertex(3, 3)
        F = G.insert_vertex(4, 6)

        # Make the edges
        G.insert_edge(A, B)
        G.insert_edge(A, C)
        G.insert_edge(A, D)
        G.insert_edge(C, E)
        G.insert_edge(C, F)
        G.insert_edge(D, F)

        # Get the path
        r = 7.7
        p = G.find_path(A, F, r)
        check_is_path(G, A, p, r)

        expected = [[A, C, F], [A, D, F]]

        assert A == p[0], "Path did not start at correct vertex in G.find_path"
        assert F == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p in expected, "Path {} did not have the most minimal hops.".format(p)

        # Now let's move

        G.move_vertex(C, 20, 20)
        p = G.find_path(A, F, r)
        check_is_path(G, A, p, r)

        expected = [[A, D, F]]

        assert A == p[0], "Path did not start at correct vertex in G.find_path"
        assert F == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p in expected, "Path {} did not have the most minimal hops.".format(p)

        # Now let's remove the node connecting them all
        G.remove_vertex(D)
        p = G.find_path(A, F, r)
        assert p is None, \
            "Path returned {} does not exist within range {}".format(p, r)

        G.move_vertex(C, 2, 3)
        p = G.find_path(A, F, r)
        check_is_path(G, A, p, r)

        expected = [[A, C, F]]

        assert A == p[0], "Path did not start at correct vertex in G.find_path"
        assert F == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p in expected, "Path {} did not have the most minimal hops.".format(p)

    @timeout_decorator.timeout(1)
    def test_emergency_move_remove(self):
        """ #score(3) """
        G = Graph()

        m = G.insert_vertex(0, 0)
        a = G.insert_vertex(0, 7)
        b = G.insert_vertex(7, 7)
        c = G.insert_vertex(7, 0)
        d = G.insert_vertex(7, -7)
        e = G.insert_vertex(0, -7)
        f = G.insert_vertex(-7, -7)
        g = G.insert_vertex(-7, 0)
        h = G.insert_vertex(-7, 7)

        G.insert_edge(m, a)
        G.insert_edge(a, b)
        G.insert_edge(b, c)
        G.insert_edge(c, d)
        G.insert_edge(d, e)
        G.insert_edge(e, f)
        G.insert_edge(f, g)
        G.insert_edge(g, h)

        expected_r = 9.89949
        r = G.find_emergency_range(m)
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        G.move_vertex(e, 0, -18)
        r = G.find_emergency_range(m)
        expected_r = 18
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        G.move_vertex(f, -33, -21)
        r = G.find_emergency_range(m)
        expected_r =  39.11521
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

        G.remove_vertex(f)

        r = G.find_emergency_range(m)
        expected_r = 18
        assert approx_value(expected_r, r), \
            "[emergency_range] Expected: {} | Got: {}".format(expected_r, r)

    @timeout_decorator.timeout(1)
    def test_min_move_min(self):
        """ #score(3)"""

        G = Graph()

        A = G.insert_vertex(1, 1)

        B = G.insert_vertex(1, 0.5)
        C = G.insert_vertex(20, 7)

        D = G.insert_vertex(1, 0.2)
        E = G.insert_vertex(1, 0)
        F = G.insert_vertex(0, 2)

        G.insert_edge(A, B)
        G.insert_edge(A, C)
        G.insert_edge(C, F)

        G.insert_edge(B, D)
        G.insert_edge(D, E)
        G.insert_edge(E, F)

        # Find the minimum range
        r = G.minimum_range(A, F)
        # expected_r = 19.2949
        expected_r = 1.41421

        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        G.move_vertex(B, -20, -24)
        r = G.minimum_range(A, F)
        expected_r = 19.9248
        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        expected_r = 2.0
        G.move_vertex(B, 1, 3)
        r = G.minimum_range(A, F)
        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        r = G.minimum_range(A, D)
        expected_r = 2.0
        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        G.remove_vertex(B)
        r = G.minimum_range(A, F)
        expected_r = 19.9248
        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        r = G.minimum_range(A, D)
        assert approx_value(expected_r, r), \
            "[minimum_range] Expected: {} | Got: {}".format(expected_r, r)

    @timeout_decorator.timeout(1)
    def test_is_most_minimal_hops(self):
        """ #score(5) #hidden """

        G = Graph()

        M = G.insert_vertex(0, 0)
        A = G.insert_vertex(2, 0)
        B = G.insert_vertex(1, 1)
        C = G.insert_vertex(0, 2)
        D = G.insert_vertex(-1, 2)
        E = G.insert_vertex(-2, 0)
        F = G.insert_vertex(-2, -4)
        H = G.insert_vertex(0, -5)
        I = G.insert_vertex(4, -1)
        J = G.insert_vertex(3, 0)

        # Edges
        G.insert_edge(M, A)
        G.insert_edge(A, B)
        G.insert_edge(B, C)
        G.insert_edge(C, D)
        G.insert_edge(D, E)
        G.insert_edge(E, F)
        G.insert_edge(F, H)
        G.insert_edge(H, I)
        G.insert_edge(I, J)


        # Path checks
        p = G.find_path(M, I, 10)

        assert M == p[0], "Path did not start at correct vertex in G.find_path"
        assert I == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        expected = [M, A, B, C, D, E, F, H, I]

        assert p == expected, "Path {} was not the most minimal hop path".format(p)


        p = G.find_path(M, I, 2)

        assert p is None, "Path {} returned but is out of range.".format(p)

        G.insert_edge(M, C)

        p = G.find_path(M, I, 7)

        check_is_path(G, M, p, 7)

        expected = [M, C, D, E, F, H, I]

        assert M == p[0], "Path did not start at correct vertex in G.find_path"
        assert I == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p == expected, "Path {} was not the most minimal hop path".format(p)

        G.insert_edge(A, I)

        p = G.find_path(M, I, 6)

        check_is_path(G, M, p, 6)

        expected = [M, A, I]

        assert M == p[0], "Path did not start at correct vertex in G.find_path"
        assert I == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p == expected, "Path {} was not the most minimal hop path".format(p)

        p = G.find_path(M, E, 6)

        expected = [M, C, D, E]

        check_is_path(G, M, p, 6)

        assert M == p[0], "Path did not start at correct vertex in G.find_path"
        assert E == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p == expected, "Path {} was not the most minimal hop path".format(p)

        G.insert_edge(M, E)

        p = G.find_path(M, E, 6)

        check_is_path(G, M, p, 7)

        expected = [M, E]

        assert M == p[0], "Path did not start at correct vertex in G.find_path"
        assert E == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p == expected, "Path {} was not the most minimal hop path".format(p)

        G.remove_vertex(C)

        p = G.find_path(M, H, 7)

        expected = [M, A, I, H]

        check_is_path(G, M, p, 7)

        assert M == p[0], "Path did not start at correct vertex in G.find_path"
        assert H == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p == expected, "Path {} was not the most minimal hop path".format(p)

        p = G.find_path(M, D, 7)

        expected = [M, E, D]

        check_is_path(G, M, p, 7)

        assert M == p[0], "Path did not start at correct vertex in G.find_path"
        assert D == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p == expected, "Path {} was not the most minimal hop path".format(p)

        p = G.find_path(M, D, 2)

        assert p is None, "Path {} was returned when it is outside of range".format(p)
