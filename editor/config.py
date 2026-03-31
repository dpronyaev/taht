# Editor Configuration File
# This file allows customization of entity types and tile options

# Tile options for drawing
TILE_OPTIONS = {
    0: "#",  # wall
    1: ".",  # floor
}

# Entity types that can be placed in the editor
# Each entity can have a 'unique' property to indicate if only one can exist
ENTITY_TYPES = [
    {
        "char": "@",
        "name": "Player",
        "unique": True,  # Only one player allowed per level
        "description": "The main character"
    },
    {
        "char": "M",
        "name": "Monster",
        "unique": False,  # Multiple monsters allowed
        "description": "Enemy creature"
    },
    {
        "char": "T",
        "name": "Treasure",
        "unique": False,
        "description": "Collectible item"
    },
    {
        "char": "D",
        "name": "Door",
        "unique": False,
        "description": "Openable door"
    }
]

# Default level sizes
DEFAULT_LEVEL_SIZES = {
    "small": (20, 15),   # width, height
    "medium": (30, 22),
    "large": (40, 30),
}