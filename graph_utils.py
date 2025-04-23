import turtle
import time
from typing import Dict, Generic, List, Set, Tuple, TypeVar
from dataclasses import dataclass, field
from math import sqrt

NodeId = str

T = TypeVar('T')

WeightedNeighbors = Set[Tuple[T, float]]


@dataclass(frozen=True, order=True)
class Node(Generic[T]):
    weighted_neighbors: WeightedNeighbors[T] = field(default_factory=set,
                                                     init=False,
                                                     hash=False,
                                                     repr=False,
                                                     compare=False)
    neighbors: Set[T] = field(default_factory=set,
                              init=False,
                              hash=False,
                              repr=False,
                              compare=False)

    def add_neighbor(self, neighbor: T, weight: float = 0):
        self.weighted_neighbors.add((neighbor, weight))
        self.neighbors.add(neighbor)

    def get_weighted_neighbors(self) -> WeightedNeighbors[T]:
        return self.weighted_neighbors


@dataclass(frozen=True, order=True)
class LocationNode(Node['LocationNode']):
    position: Tuple[int, int] = field(compare=False)
    node_id: NodeId = field(compare=True)


WIDTH = 600
HEIGHT = 600
NODE_RADIUS = 20

class Graph:

    nodes: Dict[NodeId, LocationNode]

    def __init__(self, graph_file: str, undirected: bool = True):
        """Builds a graph from a graph file.
        
        Each line in the graph file represents a node and has the syntax:

        ```
        node_id:node_x,node_y neighbor_id1 neighbor_id2 ...
        ```
        
        The order of the lines isn't important. The exact whitespace in each line is
        important.
        """
        self.screen = turtle.Screen()
        self.screen.setup(WIDTH, HEIGHT)
        self.screen.setworldcoordinates(0, HEIGHT, WIDTH, 0)
        turtle.hideturtle()
        # turtle.speed(1)
        self.original_tracer = self.screen.tracer()
        self.screen.tracer(0)
        turtle.colormode(255)


        self.nodes = {}
        self.undirected = undirected

        with open(graph_file) as f:
            neighbors_defs: List[Tuple[NodeId, List[str]]] = []
            for line in f.readlines():
                parts = line.split()
                node_def = parts[0]
                [node_id, node_pos] = node_def.split(':')
                position = tuple(map(int, node_pos.split(',')))
                node = LocationNode(position=position, node_id=node_id)
                self.nodes[node.node_id] = node

                if len(parts) > 1:
                    neighbors_defs.append((node.node_id, parts[1:]))

            for node_id, neighbors in neighbors_defs:
                for neighbor_def in neighbors:
                    neighbor = self.nodes[neighbor_def]
                    current_node = self.nodes[node_id]
                    current_node.add_neighbor(
                        neighbor, self.calc_distance(current_node, neighbor))
                    if self.undirected:
                        neighbor.add_neighbor(
                            current_node,
                            self.calc_distance(neighbor, current_node))

    def draw_graph(self):
        for node in self.nodes.values():
            node_x, node_y = node.position
            node_top = self.get_node_circle_position(node)
            turtle.penup()
            turtle.goto(node_top)
            turtle.pendown()
            turtle.circle(NODE_RADIUS)
            turtle.penup()
            turtle.goto(node_x + NODE_RADIUS, node_y + NODE_RADIUS * 2 + 5)
            turtle.write(node.node_id, font=("Arial", 15, "bold"))

            for neighbor in node.neighbors:
                turtle.penup()
                turtle.goto(node.position)

                # Point towards neighbor from current
                angle = turtle.towards(neighbor.position)
                turtle.setheading(angle)

                turtle.pendown()
                turtle.goto(neighbor.position)

                # Draw arrow heads for directed graph
                if not self.undirected:
                    prev_pen = turtle.pensize()
                    turtle.pensize(3)
                    turtle.left(30)
                    turtle.backward(10)
                    turtle.forward(10)
                    turtle.right(60)
                    turtle.backward(10)
                    turtle.pensize(prev_pen)

                # Reset so that circles are drawn correctly
                turtle.setheading(0)

        turtle.update()

    def draw_path(self, path: List[LocationNode], draw_lines: bool = True):
        self.screen.tracer(self.original_tracer)

        if len(path) == 0:
            return

        current_node = path[0]
        turtle.penup()
        turtle.goto(current_node.position)

        if len(path) == 1:
            return

        for next_node in path:
            turtle.pencolor(0, 255, 0)
            turtle.pensize(5)

            turtle.penup()
            turtle.goto(current_node.position)

            if draw_lines and next_node in current_node.neighbors:
                turtle.pendown()
                turtle.goto(next_node.position)

            node_top = self.get_node_circle_position(next_node)
            turtle.penup()
            turtle.goto(node_top)
            turtle.pendown()
            turtle.circle(NODE_RADIUS)
            time.sleep(0.3)
            current_node = next_node

        self.screen.tracer(0)

    def calc_distance(self, n1: LocationNode, n2: LocationNode) -> float:
        n1p = n1.position
        n2p = n2.position
        return sqrt((n1p[0] - n2p[0])**2 + (n1p[1] - n2p[1])**2)

    def get_node_circle_position(self, node: LocationNode) -> Tuple[int, int]:
        node_x, node_y = node.position
        return node_x, node_y - NODE_RADIUS
