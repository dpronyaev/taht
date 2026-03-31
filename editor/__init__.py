"""Editor package initialization."""

# Import configuration
try:
    from .config import TILE_OPTIONS, ENTITY_TYPES, DEFAULT_LEVEL_SIZES
except ImportError:
    # Fallback to default configuration
    TILE_OPTIONS = {
        0: "#",  # wall
        1: ".",  # floor
    }

    ENTITY_TYPES = [
        {
            "char": "@",
            "name": "Player",
            "unique": True,
            "description": "The main character"
        },
        {
            "char": "M",
            "name": "Monster",
            "unique": False,
            "description": "Enemy creature"
        }
    ]

    DEFAULT_LEVEL_SIZES = {
        "small": (20, 15),
        "medium": (30, 22),
        "large": (40, 30),
    }