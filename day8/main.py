from dataclasses import dataclass
import collections
from math import gcd

@dataclass
class Node:
    name: str
    left: str
    right: str

    def __key(self):
        return (self.name, self.left, self.right)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.__key() == other.__key()
        return NotImplemented

@dataclass
class Directions:
    directions: list[str]
    current_pos: int = 0

    def get_next_direction(self) -> str:
        res = self.directions[self.current_pos]
        self.current_pos += 1
        if self.current_pos > len(self.directions) - 1:
            self.current_pos = 0
        return res

def decode_input(input: str) -> (Directions, list[Node]):
    parts = input.split("\n\n")
    directions_array: list[str] = []
    for character in parts[0]:
        directions_array.append(character)
    directions = Directions(directions_array)
    node_array: list[Node] = []
    for line in parts[1].split("\n"):
        node_array.append(Node(line[0:3], line[7:10], line[12:15],))
    return directions, node_array

def find_nodes_that_end_in(nodes: list[Node], search_char: str) -> list[Node]:
    res: list[Node] = []
    for node in nodes:
        if node.name[-1] == search_char:
            res.append(node)
    return res

def find_node_by_name(nodes: list[Node], node_name: str) -> Node:
    return nodes[next(i for i, node in enumerate(nodes) if node.name == node_name)]

def get_next_node(nodes: list[Node], direction: str, current_node: Node) -> Node:
    next_node_name = current_node.left if direction == "L" else current_node.right
    res = find_node_by_name(nodes, next_node_name)
    return res

def solve_part_one(directions: Directions, nodes: list[Node]) -> int:

    current_node = find_node_by_name(nodes, "AAA")
    target_node = find_node_by_name(nodes, "ZZZ")
    steps_counter = 0

    while current_node != target_node:
        direction = directions.get_next_direction()
        current_node = get_next_node(nodes, direction, current_node)
        steps_counter += 1
    return steps_counter

def nodes_are_the_same(list1: list[Node], list2: list[Node]) -> bool:
    return collections.Counter(list1) == collections.Counter(list2)

def find_lcm(input: list[int]) -> int:
    lcm = 1
    for i in input:
        lcm = lcm*i//gcd(lcm, i)
    return lcm

def solve_part_two(directions: Directions, nodes: list[Node]) -> int:
    cycle_lengths: dict[Node, int] = {}
    current_nodes = find_nodes_that_end_in(nodes, "A")
    end_nodes = find_nodes_that_end_in(nodes, "Z")
    steps_counter = 0

    print("finding cycle lengths")
    while len(end_nodes) != len(cycle_lengths):
        direction = directions.get_next_direction()
        steps_counter += 1
        for i, node in enumerate(current_nodes):
            current_nodes[i] = get_next_node(nodes, direction, node)
            if current_nodes[i].name[-1] == "Z" and current_nodes[i] not in cycle_lengths:
                cycle_lengths[current_nodes[i]] = steps_counter
        if steps_counter % 2500 == 0:
            print("still searching, steps so far: {}".format(steps_counter))

    print("all cyle lengths found at step number: {}, calculating LCM".format(steps_counter))
    return find_lcm(cycle_lengths.values())

txt_input = open("input.txt").read()

directions, nodes = decode_input(txt_input)
print("Part one solution: {}".format(solve_part_one(directions, nodes)))

directions, nodes = decode_input(txt_input)
print("Part two solution: {}".format(solve_part_two(directions, nodes)))
