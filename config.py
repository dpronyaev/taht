# config.py

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
