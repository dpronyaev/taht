# Game Configuration File
# This file contains all configuration parameters for the roguelike game

# Default dimensions for new levels
DEFAULT_LEVEL_SIZES = {
    "small": (20, 15),   # width, height
    "medium": (30, 22),
    "large": (40, 30),
}

# Mapping of entity characters to entity types
ENTITY_MAP = {
    "@": "player",
    "M": "monster",
    # Add more mappings here if needed
}

# Tile options for drawing
TILE_OPTIONS = {
    0: "#",  # wall
    1: ".",  # floor
}

# Tile properties
TILE_PROPERTIES = {
    "#": {
        "char": "#",
        "name": "Wall",
        "can_pass_through": False,
        "description": "Impassable wall"
    },
    ".": {
        "char": ".",
        "name": "Floor",
        "can_pass_through": True,
        "description": "Walkable floor"
    }
}

# Entity types that can be placed in the editor
# Each entity can have a 'unique' property to indicate if only one can exist
ENTITY_TYPES = [
    {
        "char": "@",
        "name": "Player",
        "unique": True,  # Only one player allowed per level
        "can_pass_through": False,
        "description": "The main character"
    },
    {
        "char": "M",
        "name": "Monster",
        "unique": False,  # Multiple monsters allowed
        "can_pass_through": False,
        "description": "Enemy creature"
    },
    {
        "char": "T",
        "name": "Treasure",
        "unique": False,
        "can_pass_through": True,
        "description": "Collectible item"
    },
    {
        "char": "D",
        "name": "Door",
        "unique": False,
        "can_pass_through": True,
        "description": "Openable door"
    }
]