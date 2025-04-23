"""
An example of depth first search through a graph.

Note: stepping through a debug session in VSCode may be helpful here.

Sources:
 - https://likegeeks.com/depth-first-search-in-python/#Implementing-Depth-First-Searcha-non-recursive-approach

Challenge problems:
 - Change the source node (the node to start at) for either of the functions to
   one that we haven't tried, and without running the code try to predict what
   the function will return. You can do this by either tracing through the code,
   or figure it out from your understanding of DFS.
 - Update both DFS functions to take in a parameter specifying a value to find
   in the graph. The updated functions should return `True` if the value is
   found, and `False` if not.
"""

from typing import List

import sys
sys.path.append('.')

from graph_utils import Node, Graph


def dfs_non_recursive(source: Node, value: Node):
    """Returns a string representation of the path a DFS would take on `graph`
    starting from `source`."""

    # Stores the traversal path we take through the graph
    path: List[Node] = []
    """
    We will treat this list like a stack, and use it to store the nodes we need
    to visit.
    
    A stack is a First-in Last-out (FILO) data structure. You can add items to
    it and remove items from it. The first item to get added is the last item to
    be removed. You can think of it like a stack of plates, if you stack 3
    plates on top of each other, the first one to be removed from that stack
    will be the last plate you added.
    
    The stack data structure is useful for DFS because we want to traverse down
    an entire path of nodes, and only after we can go no further do we want to
    come back up.
    """
    stack = [source]
    # We loop until there are no more nodes to visit
    while len(stack) != 0:
        # We remove the node which was most recently added
        s = stack.pop()
        # We check if s = value
        if s == value:
            return (path, True)
        # We explore its siblings only if we have not already seen it before
        if s not in path:
            path.append(s)

            # This could be a leaf node, meaning it has no siblings and is not a
            # key in our graph dictionary
            if len(s.neighbors) == 0:
                #leaf node
                continue

            # We remember each of the siblings of this node, and add them to the
            # stack so that, on future iterations, they are explored before
            # anything else
            for neighbor in s.neighbors:
                stack.append(neighbor)

    return (path, False)

graph = Graph('dfs-graph.txt', undirected=False)
nodes = graph.nodes

# print(dfs_non_recursive(nodes['A'], nodes['B'])[1])

# DFS_path = dfs_non_recursive(nodes['A'], nodes['D'])


def dfs_recursive(source: Node, path=[]) -> List[Node]:
    """Returns a list of the nodes in the path a DFS would take on `graph`
    starting from `source`.

    This implementation is recursive and is almost exactly the same as the
    previous implementation, except instead of manually creating a stack to
    remember which nodes to visit and in what order, we make use of the function
    call stack.
    """
    # One base case occurs when we have reached a node that we have already
    # visited
    if source not in path:
        path.append(source)

        # Another base case occurs if this node does not have any siblings
        if len(source.neighbors) == 0:
            # leaf node, backtrack
            return path

        # For each of the siblings of this node, we repeat the entire process
        for neighbor in source.neighbors:
            path = dfs_recursive(neighbor, path)

    return path


DFS_path = dfs_recursive(nodes['A'])
graph.draw_graph()
graph.draw_path(DFS_path, draw_lines=False)