"""Entity and component definitions for the roguelike.

We keep this module intentionally lightweight: entities hold
position, a render character, and optional inventory.  Future
extensions (AI, stats, etc.) can be added as needed.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Entity:
    x: int
    y: int
    char: str = "?"
    hp: int = 10

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy


@dataclass
class Player(Entity):
    def __post_init__(self):
        self.char = "@"
        self.hp = 20


@dataclass
class Monster(Entity):
    def __post_init__(self):
        self.char = "M"
        self.hp = 15


# Additional entity types can be added here (e.g., NPC, Item)
