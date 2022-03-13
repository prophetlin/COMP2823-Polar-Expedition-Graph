# Polar Expedition


## Story

We have been asked to help with the preparations for a polar expedition. There will be various measurement stations on icebergs and we know the routes that can be travelled between them. We'll represent these as vertices and edges of an undirected graph.
For safety reasons, it might not be possible to travel directly from every station to every other station (hazardous terrain, or distance is too far and would leave you exposed to the elements for too long). However, you can assume that the graph is connected.

Informally, our implementation should support the following operations:

When an iceberg moves, the location of the station on it needs to be updated. Implement a method move_vertex(v, newX, newY) that updates station $v$'s location to (newX, newY).

In case of emergency, we want a given station $s$ to be able to reach every other station, so we need to be able to compute the distance from $s$ to the station furthest from it. The distance between stations is measured using the Euclidean distance. Implement a method find_emergency_range(v) that returns the distance to the vertex $w$ that is furthest from $v$, i.e., the broadcast range required to reach all vertices in the graph.

We also want to make sure that the expedition members can safely inspect the measurement stations using the equipment they have. Specifically, we want to know if taking a radio with range $r$ suffices to get them safely from base station $b$ to station $s$. Implement a method find_path(b, s, r) that returns a path from the base station $b$ to $s$ such that every station visited along the way is within range $r$ of $b$ (if such a path exists), and null otherwise.

However, unfortunately the funding agencies are a bit stingy, so they want us to use the cheapest radios that'll suffice to get us from base station $b$ to station $s$. Implement a method minimum_range(b, s) that returns the minimum range needed to go from $b$ to $s$. (This is a hard question, so leave this one for last.)

Information about the graph

Every Vertex has an X and Y coordinate indicating its location.

The graph is NOT necessarily complete, but you can assume that it is connected.

Since the stations are placed on icebergs, their location may change!



## Code to implement:

You are given 3 files. graph.py, edge.py and vertex.py, and there are functions you must implement.

### vertex.py

* ``move_vertex(self, x_pos, y_pos)`` - Move the position of the vertex to the defined x and y provided as arguments.


### graph.py

* ``find_emergency_range(self, v)`` - Find the distance to the vertex w that is furthest away from v.
* ``find_path(self, b, s, r)`` - Find a path from the vertex b to vertex s such that the distance from b to every vertex along this path is within range r. Such that the path returned has the minimum number of hops.
* ``minimum_range(self, b, s)`` - Return the minimum range required to go from b to s.
* ``move_vertex(self, v, new_x, new_y)`` - Move vertex v to the new x and y positions provided.


## About the code

### Vertex Class - vertex.py

Represents the "station" on the iceberg.

**Attributes**:

* ``x_pos`` - x position of the vertex
* ``y_pos`` - y position of the vertex
* ``edges`` - set of edges that are linked to this vertex.

**Functions**:

* ``init(x_pos, y_pos)`` - initialises the x and y position of the vertex.
* ``add_edge(e)`` - adds the edge to the vertex.
* ``remove_edge(e)`` - removes the edge from the vertex.
* [TO IMPLEMENT] ``move_vertex(x_pos, y_pos)`` - moves the position of the vertex to the new x and y.

### Edge Class - edge.py

Represents the connection between two vertices.

**Attributes**:

* `u` - A vertex connected with this edge.
* `v` - A vertex connected with this edge.


### Graph Class - graph.py (This is the main class you will implement)

* Represents the graph (or the map) of the base stations situated for the polar expedition. It is the graph containing vertices, which are connected by edges.
* This is the class containing the interaction between all aspects.

**Attributes**:

* ``_vertices`` - List of the vertices contained in the graph.

**Functions**:

* ``insert_vertex(x_pos, y_pos)`` - Creates, stores and returns a new vertex at the provided x and y coordinates.
* ``insert_edge(u, v)`` - Creates and returns a new edge between vertex u and vertex v.\
* ``remove_vertex(v)`` - Removes the vertex v from the graph.
* ``distance(u, v)`` - Returns the Euclidian distance between vertex u and vertex v.
* [TO IMPLEMENT] ``find_emergency_range(v)`` - Returns the distance to the vertex v that is furthest from v.
* [TO IMPLEMENT] ``find_path(b, s, r)`` - Returns a path from b to s, such that all vertices in the path are within range r from b. Such that the path returned has the minimum number of hops.
* [TO IMPLEMENT] ``minimum_range(b, s)`` - Returns the minimum range required to go from b to s.
* [TO IMPLEMENT] ``move_vertex(v, new_x, new_y)`` - Moves vertex v to the coordinates provided by new_x and new_y.
