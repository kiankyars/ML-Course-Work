"""
An example of detecting cycles in a graph using depth first search.

Note: stepping through a debug session in VSCode may be helpful here.

Sources:
 - https://algotree.org/algorithms/tree_graph_traversal/dfs_detecting_cycles_in_graphs/cycle_detection_in_directed_graphs/
 
Challenges:
 - Create two new graphs: one with a cycle and one without, and test out our
   cycle detection function with both.
"""

# Default dict import are only necessary for the challenge solution
from collections import defaultdict
import turtle

import sys
sys.path.append('.')

from graph_utils import Node, Graph


def detect_cycle(source: Node,
                 visited = None,
                 in_path = None) -> bool:
    """Returns whether there is a cycle in the given graph.

    A cycle is present in a graph when there exists path from a node which leads
    back onto itself. For example if node A leads to node B, which leads to node
    C, which leads to node A, that is a cycle.

    The algorithm is as follows:

    While doing a depth-first search traversal, we keep track of the nodes
    visited in the current traversal path in addition to the list of all the
    visited nodes. During the traversal if we visit a node that was already in
    the current path of the traversal a cycle is found.
    """
    # When the function is first called, we initialize our memory
    if visited is None:
        visited = defaultdict(bool)
    if in_path is None:
        in_path = defaultdict(bool)

    # Keep track of all the visited nodes
    visited[source] = True

    # Remember that this node is in the current traversal path
    in_path[source] = True

    # Go through all of the siblings of the current node in a DFS manner
    for adj_node in source.neighbors:
        # If we have looped back to a node we have already visited, we have
        # found a cycle
        if in_path[adj_node]:
            return True
        # Otherwise if this not a node that we have already visited, we try to
        # detect a cycle starting from it
        elif not visited[adj_node]:
            if detect_cycle(adj_node, visited, in_path):
                return True

    # We are now backtracking (i.e. going back up where we came from), so we
    # unset the flag for the current vertex so it will no longer be in the
    # traversal path
    in_path[source] = False

    # No cycle has been detected for this node
    return False


# graph1 = Graph('week-1/dfs-cycle1.txt', undirected=False)
# nodes1 = graph1.nodes
# graph1.draw_graph()
# print(detect_cycle(nodes1['0']))

graph2 = Graph('week-1/dfs-cycle2.txt', undirected=False)
nodes2 = graph2.nodes
graph2.draw_graph()
print(detect_cycle(nodes2['0']))

turtle.done()