from turtle import RawTurtle
from typing import Union
import sys


def _prim_min_distance(
    visited: set[str], costs: dict[tuple[str, str], int]
) -> Union[int, None]:
    """
    Finds the node that has not been visited with the shortest distance
    to a node that has been visited and returns the node.

    If there are no nodes to traverse to, None is returned.
    """

    valid_edges = dict(
        # '!=' is logical xor. This means that all valid edges start
        # with a node that has been visited and ends in a node that has not.
        # item[0] is the edge
        filter(
            lambda item: (item[0][0] in visited) != (item[0][1] in visited),
            costs.items(),
        )
    )

    # No valid edge
    if len(valid_edges) == 0:
        return None

    min_edge: tuple[str, str] = min(
        valid_edges.keys(), key=lambda key: valid_edges[key]
    )

    return min_edge[0] if min_edge[0] not in visited else min_edge[1]


def prims_algorithm(source: str, costs: dict[tuple[str, str], int]):
    """
    An implementation of prims algorithm. Finds the order nodes traversed using the prims algorithm.
    This algorithm is a greedy algorithm to find paths in a graph. Each iteration, the closest
    node to the visited nodes is marked as visited.

    :param source:    The start node to calculate distances form.
                      This should be given as an integer equal to the
                      index of that node in the adjecency matrix
    :param costs:     A dict where the keys are tuples of nodes (representing and edge)
                      and the value is the cost of traverseing this edge.
    :returns: The order of what nodes are added to the tree according to prims algorithm.
    """
    visited: set[str] = set()
    visited.add(source)
    order = [source]

    # Gets next_node from the return of the minimum_distance function
    # and continues to loop while the output of the function is not None
    # (meaning all nodes have been visited).
    while (next_node := _prim_min_distance(visited, costs)) is not None:
        visited.add(next_node)
        order.append(next_node)

    return order


def dijaska(source: str, costs: dict[tuple[str, str], int]) -> dict[str, int]:
    """
    Takes the properties of a weighted graph and a start node,
    and returns a dictionary of the distance to all other nodes in the graph
    """
    nodes: set[str] = set(node for edge in costs.keys() for node in edge)  # All nodes
    unvisited: set[str] = set(nodes)  # Unvisited nodes
    distance: dict[str, int] = {
        node: float("inf") for node in nodes
    }  # Current best lowest distance
    distance[source] = 0  # Distance to start is zero
    costs = dict(costs)  # Copies the dict

    # While there still are nodes that have not been investigated
    while len(unvisited):
        # Finds the unvisited node with the least current distance
        current = min(unvisited, key=(lambda key: distance[key]))
        # The distance to the current node
        current_dist = distance[current]

        for edge, cost in costs.copy().items():
            # Discard all edges that are not adjecent to the current edge
            if current not in edge:
                continue
            # next is the node in the edge that is not current
            next = edge[0] if edge[0] != current else edge[1]

            # Updates distance if the new distance is less than the current distance
            distance[next] = min(distance[next], current_dist + cost)
            # Removes investigated edge
            costs.pop(edge)
        # Removes investigated node
        unvisited.remove(current)
    return dict(sorted(distance.items(), key=lambda item: item[1]))
