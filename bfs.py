"""
An example of breadth first search through a graph.

Note: stepping through a debug session in VSCode may be helpful here.

Sources:
 - https://algotree.org/algorithms/tree_graph_traversal/breadth_first_search/

Challenge problems:
 - Change the source node (the node to start at) for either of the functions to
   one that we haven't tried, and without running the code try to predict what
   the function will return. You can do this by either tracing through the code,
   or figure it out from your understanding of BFS.
 - Update our BFS function to take in a parameter specifying a value to find
   in the graph. The updated functions should return `True` if the value is
   found, and `False` if not.
"""

from collections import defaultdict
from queue import SimpleQueue
from typing import List

import sys
sys.path.append('.')

from graph_utils import Node, Graph


def breadth_first_search(src: Node, target: Node):
    "Visits the vertices of `graph` in a breadth first order."
    # We keep track of which nodes we have already visited
    visited = defaultdict(bool)

    """
    We will use the queue data structure to store the vertices which we want to
    visit.

    A queue is a First-in First-out (FIFO) data structure. You can add items to
    it and take items out of it, and whichever items get added first get removed
    first. This is like a queue (aka a line-up) in real life: if you enter the
    line first, you are the first one to leave the line. If you enter behind
    other people, those people leave the line before you.
    
    The queue is useful for breadth first search. Remember in BFS we visit all
    adjacent nodes, then go a level deeper for each of those nodes. The queue
    will help use remember which adjacent nodes we need to visit, and what order
    we need to visit them in.
    """
    path: List[Node] = []

    q: SimpleQueue[Node] = SimpleQueue()
    # We add the starting node to the front of the line, and remember that we
    # have visited it
    q.put(src)
    visited[src] = (True, path)
    path.append(src)

    # We loop until there are no more nodes to visit
    while not q.empty():
        # We remove the node that was at the front of the line
        node = q.get()
        if node == target:
            return (True, path)
        if len(node.neighbors) > 0:
            # We visit all of this node's adjacent nodes, as long as they have
            # not been visited before
            for adj_node in node.neighbors:
                if visited[adj_node] == False:
                    # We add this adjacent node to the back of the line so that
                    # we can remember to visit it on another iteration
                    q.put(adj_node)
                    visited[adj_node] = True
                    path.append(adj_node)

    return (False, path)

graph = Graph('bfs-graph.txt', undirected=False)
nodes = graph.nodes

returnVal = (breadth_first_search(nodes['0'], nodes['1']))
path = returnVal[1]
print(returnVal[0])
# For this one try swapping the graph between directed and undirected
# path = breadth_first_search(nodes['3'])

graph.draw_graph()
graph.draw_path(path, draw_lines=False)
