"""
Test File 1
-----------

Tests simple functions can be run UNIQUELY. It only calls one function at a time.

PLEASE NOTE: These tests are not equivalent to the tests run for grading,
they are only here to be used as a guideline!

To run this file, in your terminal from the folder above
(the one with edge.py, graph.py and vertex.py):

python3 -m unittest tests/test_single_functions.py

(or on some systems)

python -m unittest tests/test_single_functions.py
"""

import math
import unittest
import timeout_decorator

from vertex import Vertex
from graph import Graph

# Tolerance for the threshold of distances
TOLERANCE_THRESHOLD = 0.001


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

    assert p is not None, "Path returned was None when it shouldn't be."

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


class SingularFunctionTest(unittest.TestCase):
    """
    Tests one function at a time, to ensure that BASIC implementation
    has been completed.

    These tests should give you an understanding about HOW the graph
    is expected to work function by function.
    """

    ##################################################
    # Vertex: move_vertex
    ##################################################

    @timeout_decorator.timeout(0.5)
    def test_can_move_vertex_once_from_vertex(self):
        """ #score(1) """

        v = Vertex(4, 4)

        # Check that the init has not changed.
        assert v.x_pos == 4 and v.y_pos == 4, "Vertex initialisation failed!"

        # Check that you can move it.
        v.move_vertex(7, 7)

        assert v.x_pos == 7, "Vertex X position didn't change! " + \
            "Expected: {}, Got: {}".format(7, v.x_pos)

        assert v.y_pos == 7, "Vertex Y position didn't change! " + \
                             "Expected: {}, Got: {}".format(7, v.y_pos)

    @timeout_decorator.timeout(0.5)
    def test_can_move_vertex_n_times_from_vertex(self):
        """ #score(1) """

        v = Vertex(3, 3)

        for i in range(3, 20):
            v.move_vertex(i, i-1)

            assert v.x_pos == i, "Vertex x_pos didn't change! " + \
                "Expected: {}, Got: {}".format(i, v.x_pos)

            assert v.y_pos == i-1, "Vertex y_pos didn't change! " + \
                                 "Expected: {}, Got: {}".format(i-1, v.y_pos)

    @timeout_decorator.timeout(0.5)
    def test_can_move_more_than_one_vertex(self):
        """ #score(2) """

        v1 = Vertex(3, 7)
        v2 = Vertex(6, 2)

        v1.move_vertex(4, 5)

        assert v1.x_pos == 4, "Vertex x_pos didn't change! " + \
                             "Expected: {}, Got: {}".format(4, v1.x_pos)

        assert v1.y_pos == 5, "Vertex y_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(5, v1.y_pos)

        v2.move_vertex(6, 7)

        assert v2.x_pos == 6, "Vertex x_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(6, v2.x_pos)
        assert v2.y_pos == 7, "Vertex y_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(7, v2.y_pos)

    @timeout_decorator.timeout(0.5)
    def test_can_move_to_old_spot(self):
        """ #hidden #score(2) """

        v1 = Vertex(3, 7)
        v2 = Vertex(6, 2)

        v1.move_vertex(4, 5)

        assert v1.x_pos == 4, "Vertex x_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(4, v1.x_pos)

        assert v1.y_pos == 5, "Vertex y_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(5, v1.y_pos)

        v2.move_vertex(6, 7)

        assert v2.x_pos == 6, "Vertex x_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(6, v2.x_pos)
        assert v2.y_pos == 7, "Vertex y_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(7, v2.y_pos)

        v1.move_vertex(3, 7)

        assert v1.x_pos == 3, "Vertex x_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(4, v1.x_pos)

        assert v1.y_pos == 7, "Vertex y_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(5, v1.y_pos)


    ##################################################
    # Graph: move_vertex
    ##################################################

    @timeout_decorator.timeout(0.5)
    def test_graph_can_move_single_vertex(self):
        """ #score(1) """

        G = Graph()

        v = G.insert_vertex(6, 8)
        G.move_vertex(v, 8, 6)

        assert v.x_pos == 8, "Vertex x_pos didn't change! " + \
                             "Expected: {}, Got: {}".format(8, v.x_pos)

        assert v.y_pos == 6, "Vertex y_pos didn't change! " + \
                             "Expected: {}, Got: {}".format(6, v.y_pos)

    @timeout_decorator.timeout(0.5)
    def test_graph_can_move_different_vertices(self):
        """ #score(1) """

        G = Graph()

        v1 = G.insert_vertex(2, 3)
        v2 = G.insert_vertex(4, 5)

        G.insert_edge(v1, v2)

        G.move_vertex(v2, 6, 2)

        assert v2.x_pos == 6, "Vertex x_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(6, v2.x_pos)

        assert v2.y_pos == 2, "Vertex y_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(2, v2.y_pos)

        assert v1.x_pos == 2, "A different Vertex x_pos changed! " + \
                              "Expected: {}, Got: {}".format(2, v1.x_pos)

        assert v1.y_pos == 3, "A different Vertex y_pos changed! " + \
                              "Expected: {}, Got: {}".format(3, v1.y_pos)

        # Move v1 where v2 originally was
        G.move_vertex(v1, 4, 5)

        assert v1.x_pos == 4, "Vertex x_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(5, v2.x_pos)

        assert v1.y_pos == 5, "Vertex y_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(5, v2.y_pos)

        assert v2.x_pos == 6, "A different Vertex x_pos changed! " + \
                              "Expected: {}, Got: {}".format(6, v1.x_pos)

        assert v2.y_pos == 2, "A different Vertex y_pos changed! " + \
                              "Expected: {}, Got: {}".format(2, v1.y_pos)

    @timeout_decorator.timeout(0.5)
    def test_graph_move_ontop_of_other_vertex(self):
        """ #hidden #score(2) """
        G = Graph()

        v1 = G.insert_vertex(4, 5)
        v2 = G.insert_vertex(4, 6)

        G.insert_edge(v1, v2)

        assert v1.x_pos == 4, "Vertex x_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(4, v1.x_pos)

        assert v1.y_pos == 5, "Vertex y_pos didn't change! " + \
                              "Expected: {}, Got: {}".format(5, v1.y_pos)

        G.move_vertex(v1, 4, 6)

        assert v1.x_pos == 4 and v1.y_pos == 5, \
            """Vertex shouldn't move ontop of other! 
               Expected: {}, Got: {}""".format((4, 5), (v1.x_pos, v1.y_pos))

    ##################################################
    # Graph: Find Emergency Range
    ##################################################

    @timeout_decorator.timeout(0.5)
    def test_can_find_emergency_range(self):
        """ #score(1) """

        G = Graph()

        v = G.insert_vertex(1, 2)
        v2 = G.insert_vertex(4, 10)

        G.insert_edge(v, v2)
        
        res = G.find_emergency_range(v)
        expected_value = 8.54400

        assert approx_value(res, expected_value), \
            "Expected: {} Got: {}".format(expected_value, res)

    @timeout_decorator.timeout(0.5)
    def test_find_emergency_range_solo(self):
        """ #hidden #score(2) """
        G = Graph()

        v = G.insert_vertex(1, 2)

        res = G.find_emergency_range(v)

        assert res == 0, "Emergency range with only one node should be 0."

    @timeout_decorator.timeout(0.5)
    def test_can_find_emergency_range_connected_vertex(self):
        """ #score(1) """

        G = Graph()
        v = G.insert_vertex(0, 0)
        v1 = G.insert_vertex(1, 1)
        v2 = G.insert_vertex(9, 3)
        v3 = G.insert_vertex(2, 7)
        v4 = G.insert_vertex(5, 3)

        G.insert_edge(v, v1)
        G.insert_edge(v, v2)
        G.insert_edge(v, v4)
        G.insert_edge(v2, v3)
        G.insert_edge(v4, v3)
        G.insert_edge(v2, v4)

        res = G.find_emergency_range(v)
        expected_value = 9.48683

        assert approx_value(res, expected_value), \
            "Expected: {} Got: {}".format(expected_value, res)

        res = G.find_emergency_range(v3)
        expected_value = 8.06226

        assert approx_value(res, expected_value), \
            "Expected: {} Got: {}".format(expected_value, res)

        res = G.find_emergency_range(v2)
        expected_value = 9.48683

        assert approx_value(res, expected_value), \
            "Expected: {} Got: {}".format(expected_value, res)

    @timeout_decorator.timeout(0.5)
    def test_find_emergency_range_surrounded(self):
        """ #hidden #score(1) """
        G = Graph()

        #    A
        # B--.--C
        #    D

        v_mid = G.insert_vertex(0, 0)
        B = G.insert_vertex(-3.2, 0)
        C = G.insert_vertex(4.8, 0)
        A = G.insert_vertex(0, 4.6)
        D = G.insert_vertex(0, -5)
        
        G.insert_edge(v_mid, B)
        G.insert_edge(v_mid, C)
        G.insert_edge(v_mid, A)
        G.insert_edge(v_mid, D)


        r = 5

        res = G.find_emergency_range(v_mid)

        assert approx_value(r, res), \
            """
            Incorrect range from emergency range.
            Expected: {}, Got: {}.""".format(r, res)

    ##################################################
    # Graph: Find Path
    ##################################################

    @timeout_decorator.timeout(0.5)
    def test_can_find_path_two_vertices_only(self):
        """ #score(1) """

        G = Graph()

        b = G.insert_vertex(3, 5)
        s = G.insert_vertex(4, 10)

        G.insert_edge(b, s)

        r = 10
        r_path = G.find_path(b, s, r)

        check_is_path(G, b, r_path, r)

        assert r_path[0] == b, "Path did not start from starting vertex!"
        assert r_path[-1] == s, "Path did not end at destination vertex!"

    @timeout_decorator.timeout(0.5)
    def test_find_path_self_solo(self):
        """ #score(2) """

        G = Graph()

        b = G.insert_vertex(3, 5)

        r = 5
        r_path = G.find_path(b, b, r)

        check_is_path(G, b, r_path, r)
        assert len(r_path) == 1, "Path to self should only include own node."
        assert r_path[0] == b, "Path should include node."


    @timeout_decorator.timeout(0.5)
    def test_find_path_self_many_nodes(self):
        """ #score(2) #hidden """

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

        r_path = G.find_path(A, A, 10)
        check_is_path(G, A, r_path, 10)
        assert len(r_path) == 1, "Path to self should only include own node."
        assert r_path[0] == A, "Path should include node."

        r_path = G.find_path(D, D, 10)
        check_is_path(G, D, r_path, 10)
        assert len(r_path) == 1, "Path to self should only include own node."
        assert r_path[0] == D, "Path should include node."


    @timeout_decorator.timeout(0.5)
    def test_can_find_path_simple_line(self):
        """ #score(1) """

        G = Graph()

        A = G.insert_vertex(0, 0)
        B = G.insert_vertex(1, 1)
        C = G.insert_vertex(2, 2)

        G.insert_edge(A, B)
        G.insert_edge(C, B)

        r_path = G.find_path(A, C, 4)
        check_is_path(G, A, r_path, 4)

        assert A == r_path[0], \
            "Path did not start at correct vertex in G.find_path"
        assert C == r_path[-1], \
            "Path did not end at destination vertex in G.find_path"

    def test_can_find_path_simple_norange(self):
        """ #score(1) """

        G = Graph()

        A = G.insert_vertex(0, 0)
        B = G.insert_vertex(1, 1)
        C = G.insert_vertex(2, 2)

        G.insert_edge(A, B)
        G.insert_edge(C, B)

        r_path = G.find_path(A, C, 2)

        assert r_path is None, \
            "Path {} is outside of range {}".format(r_path, 2)

    @timeout_decorator.timeout(0.5)
    def test_can_find_path_for_graph_within_range(self):
        """ #score(1) """

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

        expected = [[A, C, F], [A, D, F]]
        check_is_path(G, A, p, r)

        assert A == p[0], "Path did not start at correct vertex in G.find_path"
        assert F == p[-1], \
            "Path did not end at destination vertex in G.find_path"

        assert p in expected, "Path {} was not the expected path".format(p)

    @timeout_decorator.timeout(0.5)
    def test_returns_only_path_within_range(self):
        """ #score(1) """

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

        # Now get the path
        r = 7.7
        p = G.find_path(A, F, r)

        expected = [A, D, F]

        check_is_path(G, A, p, r)

        assert A == p[0], "Path did not start at correct vertex in G.find_path"
        assert F == p[-1], "Did not end at destination vertex in G.find_path"

        assert p == expected, "Path p did not have minimal number of hops".format(p)

    @timeout_decorator.timeout(0.5)
    def test_find_path_norange(self):
        """ #hidden #score(2) """

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
        r = 3
        p = G.find_path(A, F, r)

        assert p is None, "A path that only exists out of range should be None"

    ##################################################
    # Graph: Minimum range
    ##################################################

    @timeout_decorator.timeout(0.5)
    def test_find_minimum_range_simple_a_b(self):
        """ #score(1) """

        G = Graph()

        A = G.insert_vertex(0, 0)
        B = G.insert_vertex(7, 7)

        G.insert_edge(A, B)

        expected = 9.89949
        res = G.minimum_range(A, B)

        assert approx_value(expected, res), \
            "[find_minimum_range] Expected: {} | Got: {}".format(expected, res)

    @timeout_decorator.timeout(0.5)
    def test_find_minimum_range_simple_graph(self):
        """ #score(1) """

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

        # Find the minimum range

        r = G.minimum_range(A, F)

        # quick maths.
        expected_r = 7.2111

        assert approx_value(expected_r, r), \
            "[find_minimum_range] Expected: {} | Got: {}".format(expected_r, r)

    @timeout_decorator.timeout(0.5)
    def test_find_minimum_range_similar_paths(self):
        """ #score(1) """

        G = Graph()

        # Layer 1
        A = G.insert_vertex(0, 0)

        # Layer 2
        B = G.insert_vertex(2, 0)
        C = G.insert_vertex(2, 98)
        D = G.insert_vertex(2, 99)

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

        # Find the minimum range

        r = G.minimum_range(A, F)

        # quick maths.
        expected_r = 98.02041

        assert approx_value(expected_r, r), \
            "[find_minimum_range] Expected: {} | Got: {}".format(expected_r, r)

        G.remove_vertex(E)
        G.remove_vertex(C)

        r = G.minimum_range(A, F)

        # quick maths.
        expected_r = 99.02041

        assert approx_value(expected_r, r), \
            "[find_minimum_range] Expected: {} | Got: {}".format(expected_r, r)

    @timeout_decorator.timeout(0.5)
    def test_find_minimum_range_same_node(self):
        """ #hidden #score(2) """
        G = Graph()

        # Layer 1
        A = G.insert_vertex(0, 0)

        # Layer 2
        B = G.insert_vertex(2, 0)
        C = G.insert_vertex(2, 98)
        D = G.insert_vertex(2, 99)

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

        # Find the minimum range

        r = G.minimum_range(D, D)

        # quick maths.
        expected_r = 0

        assert approx_value(expected_r, r), \
            "[find_minimum_range] Expected: {} | Got: {}".format(expected_r, r)

