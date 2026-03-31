# Timur and his Team ASCII Roguelike

A simple ASCII roguelike game built with Python and curses.

## Features

- Console-based gameplay with ASCII graphics
- Level editing capability
- Simple combat system
- Entity management (player, monsters)

## Requirements

- Python 3.x
- Standard library only (no external dependencies required for gameplay)

## Getting Started

1. Run the game:
   ```
   python game.py
   ```

2. Use arrow keys or WASD to move
3. Press 'c' to attack adjacent monsters
4. Press 'q' or ESC to quit

## Level Editing

The game now includes a cross-platform windowed level editor that works on both Windows and macOS (requires tkinter support):

1. Run the editor:
   ```
   python editor/windowed_editor.py
   ```

   **Note**: On some macOS systems, you may need to install tkinter separately or ensure you're using a compatible Python version. If you encounter issues with the windowed editor, you can still use the original console-based editor by running:
   ```
   python editor/main.py
   ```

2. Select a level from the dropdown or create a new one
3. Click on tiles to change them or place entities
4. Use the tile and entity selection buttons to choose what to place
5. Save your levels using the Save or Save As buttons

## Game Controls

- Arrow keys or WASD: Move
- 'c': Attack adjacent monsters
- 'q' or ESC: Quit
- 'i': Inventory (placeholder)
- 'Enter': Interact with tile below player

## Code Structure

- `game.py`: Main game loop, level loading, and game logic
- `entities.py`: Data classes for Player, Monster, and Entity
- `render.py`: Draws the map and entities on screen
- `editor/windowed_editor.py`: Cross-platform windowed level editor
- `ui/`: UI modules (dialogue, inventory, quest journal)
- `levels/`: Level JSON files

## Custom Levels

Create custom levels by editing JSON files in the `levels/` directory or using the level editor.

## Development

No build step is required; the project is pure Python and runs with the standard interpreter.

To add tests, create a `tests/` directory and run `pytest`.

## Compatibility Note

The new windowed editor uses tkinter which is part of Python's standard library. However, on some older macOS systems (like version 16.x), there may be compatibility issues with tkinter. If the windowed editor fails to launch, the original console-based editor (`editor/main.py`) is still available as a fallback option.