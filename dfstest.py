import turtle
from graph_utils import Graph, Node

def dfs_non_recursive(source: Node) -> list:
    """
    Performs DFS on graph at node "source"
    """
    # the path is the nodes already traversed
    path = []
    # the stack is the nodes that still need to be visited
    stack = [source]
    while stack:
        current = stack.pop()
        path.append(current)
        for neighbour in current.neighbors:
            if neighbour not in path:
                stack.append(neighbour)
    return path

def dfs_recursive2(source: Node, path=[]) -> list:
    if source in path:
        return path
    path.append(source)
    for n in source.neighbors:
        path = dfs_recursive2(n, path)
    return path

# def dfs_recursive(source: Node) -> list:
#     dfs_recursive.path.append(source)
#     for neighbour in source.neighbors:
#             if neighbour not in dfs_recursive.path:
#                 dfs_recursive(neighbour)

def dfs_recursive(source: Node) -> list:
    # global path
    path.append(source)
    for neighbour in source.neighbors:
            if neighbour not in path:
                dfs_recursive(neighbour)



graph = Graph("dfs-graph.txt")
nodes = graph.nodes


# dfs_path = dfs_non_recursive(nodes['A'])

# dfs_recursive.path = []
# dfs_recursive(nodes['A'])
# dfs_path = dfs_recursive.path

path = []
dfs_recursive(nodes['A'])


print(path)
graph.draw_graph()
graph.draw_path(path)
turtle.done()
quit()