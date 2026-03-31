# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Tasks

- **Run the game**: `python game.py` – starts the curses-based roguelike.
- **Reload a level**: edit the JSON in `levels/sample.json` and restart the game.
- **View the log**: the game displays the last few combat events at the bottom of the screen.
- **Edit levels**: run `python editor/windowed_editor.py` to open the cross-platform windowed level editor.
- **Inspect code**: use `ls` or `grep` to locate modules (`entities.py`, `render.py`, `ui/`).

## Building and Testing

No build step is required; the project is pure Python and runs with the standard interpreter.

There are no automated tests bundled. To add tests, create a `tests/` directory and run `pytest`.

## Code Architecture

```
┌─ game.py              # Main entry point, game loop, level loading
├─ entities.py          # Data classes for Player, Monster, Entity
├─ render.py            # Draws the map and entities on a curses window
├─ editor/windowed_editor.py  # Cross-platform windowed level editor
└─ ui/
   ├─ dialogue.py      # Simple dialogue popup
   ├─ inventory.py     # Inventory UI (placeholder)
   └─ quest.py        # Static quest journal UI
```

- **Game loop** in `game.py` handles input, movement, combat, and rendering.
- **Entities** are lightweight dataclasses storing position, character, and hit points.
- **Renderer** draws the static tile map and overlays entities.
- **UI components** use `curses.newwin` to display modal panels.
- **Level editor** is now a cross-platform windowed application in `editor/windowed_editor.py`.

## File-Level Notes

- `levels/sample.json` defines a simple 2-D grid and entity placement.
- All UI modules expose a `show` method that creates a modal window.
- Combat logic is triggered with the `c` key, damaging adjacent monsters and returning damage to the player.

## Tips for Developers

- Use `curses` documentation to experiment with colors or key bindings.
- Add more entity types by extending the `Entity` dataclass.
- To persist game state, consider writing the map and entities to JSON.