from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    val: int
    neighbors: List[Node]

    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
