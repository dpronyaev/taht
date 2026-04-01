#!/usr/bin/env python3
"""Cross-platform windowed level editor for the roguelike game."""

import sys
import os
sys.path.append(os.path.abspath("."))

import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

# Import game configuration for editor
try:
    from config import DEFAULT_LEVEL_SIZES, TILE_PROPERTIES, ENTITY_TYPES
except ImportError:
    # Fallback to default configuration if config not found
    DEFAULT_LEVEL_SIZES = {
        "small": (20, 15),
        "medium": (30, 22),
        "large": (40, 30),
    }
    TILE_PROPERTIES = {
        "#": {"can_pass_through": False},
        ".": {"can_pass_through": True}
    }
    ENTITY_TYPES = [
        {
            "char": "@",
            "name": "Player",
            "unique": True,
            "can_pass_through": False,
            "description": "The main character"
        },
        {
            "char": "M",
            "name": "Monster",
            "unique": False,
            "can_pass_through": False,
            "description": "Enemy creature"
        }
    ]

LEVELS_DIR = Path("levels")
LEVELS_DIR.mkdir(exist_ok=True)

class LevelEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Level Editor")
        self.root.geometry("800x600")

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsive layout
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Level selection
        ttk.Label(main_frame, text="Select Level:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.level_var = tk.StringVar()
        self.level_combo = ttk.Combobox(main_frame, textvariable=self.level_var, width=30)
        self.level_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.level_combo.bind('<<ComboboxSelected>>', self.load_selected_level)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="New Level", command=self.new_level).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_level).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save As", command=self.save_level_as).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Run Level", command=self.run_level).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=root.quit).pack(side=tk.LEFT, padx=5)

        # Canvas for level grid
        self.canvas_frame = ttk.Frame(main_frame)
        self.canvas_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Mode selection
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=4, column=0, columnspan=2, pady=5)

        ttk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)

        self.mode_var = tk.StringVar(value="tile")
        ttk.Radiobutton(mode_frame, text="Tile Edit", variable=self.mode_var, value="tile").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Entity Edit", variable=self.mode_var, value="entity").pack(side=tk.LEFT, padx=5)

        # Tile selection
        tile_frame = ttk.Frame(main_frame)
        tile_frame.grid(row=5, column=0, columnspan=2, pady=5)

        ttk.Label(tile_frame, text="Tile Selection:").pack(side=tk.LEFT)

        self.tile_var = tk.StringVar(value=".")
        ttk.Radiobutton(tile_frame, text="Floor (.)", variable=self.tile_var, value=".").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(tile_frame, text="Wall (#)", variable=self.tile_var, value="#").pack(side=tk.LEFT, padx=5)

        # Entity selection
        entity_frame = ttk.Frame(main_frame)
        entity_frame.grid(row=6, column=0, columnspan=2, pady=5)

        ttk.Label(entity_frame, text="Entity Selection:").pack(side=tk.LEFT)

        self.entity_var = tk.StringVar(value=ENTITY_TYPES[0]["char"] if ENTITY_TYPES else "@")

        # Create radio buttons for each entity type
        for entity_type in ENTITY_TYPES:
            ttk.Radiobutton(entity_frame, text=f"{entity_type['name']} ({entity_type['char']})",
                          variable=self.entity_var, value=entity_type["char"]).pack(side=tk.LEFT, padx=5)

        # Initialize editor state
        self.tiles = []
        self.entities = []
        self.grid_width = 0
        self.grid_height = 0
        self.tile_size = 20
        self.selected_x = 0
        self.selected_y = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # Load levels
        self.load_levels()

        # Bind canvas events
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def load_levels(self):
        """Load available levels into the dropdown."""
        levels = []
        for p in LEVELS_DIR.glob("*.json"):
            try:
                data = json.load(p)
                name = data.get("name", p.stem)
            except Exception:
                name = p.stem
            if p.name.startswith("custom_"):
                name += " (Custom)"
            levels.append((p, name))

        # Sort levels by name
        levels.sort(key=lambda x: x[1])

        # Store the actual level data for later use
        self.available_levels = levels

        # Populate combobox with just the names
        level_names = [name for _, name in levels]
        self.level_combo['values'] = level_names

        if levels:
            self.level_combo.set(level_names[0])
            self.load_level(levels[0][0])
        else:
            self.new_level()

    def load_selected_level(self, event=None):
        """Load the selected level from the dropdown."""
        selected_name = self.level_var.get()
        for p, name in self.available_levels:
            if name == selected_name:
                self.load_level(p)
                break

    def load_level(self, path):
        """Load a level from a JSON file."""
        try:
            with open(path) as f:
                data = json.load(f)

            tiles = data["tiles"]
            self.tiles = [list(row) for row in tiles]
            self.entities = data.get("entities", [])
            self.grid_width = len(self.tiles[0]) if self.tiles else 0
            self.grid_height = len(self.tiles)

            self.selected_x = 0
            self.selected_y = 0

            self.draw_grid()
            self.status_var.set(f"Loaded level: {path.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load level: {str(e)}")
            self.new_level()

    def new_level(self):
        """Create a new level with default size."""
        # Default to medium size
        width, height = DEFAULT_LEVEL_SIZES["medium"]
        self.tiles = [["#" if x == 0 or x == width - 1 or y == 0 or y == height - 1 else "."
                      for x in range(width)] for y in range(height)]
        self.entities = []
        self.grid_width = width
        self.grid_height = height
        self.selected_x = 0
        self.selected_y = 0
        self.draw_grid()
        self.status_var.set("New level created")

    def save_level(self):
        """Save the current level."""
        if not self.level_var.get():
            self.save_level_as()
            return

        try:
            # Get the current level path by searching through available levels
            selected_name = self.level_var.get()
            path = None
            for p, name in self.available_levels:
                if name == selected_name:
                    path = p
                    break

            if path is None:
                # If not found, save as new
                self.save_level_as()
                return

            # Clean up entity data to ensure it's properly formatted
            cleaned_entities = []
            for entity in self.entities:
                # Ensure entity has required fields and infer type
                # Find the entity type based on character
                entity_type = "entity"  # default type
                for entity_type_def in ENTITY_TYPES:
                    if entity_type_def["char"] == entity["char"]:
                        if entity_type_def["unique"]:
                            entity_type = "player"
                        else:
                            entity_type = "monster"
                        break

                cleaned_entity = {
                    "x": entity["x"],
                    "y": entity["y"],
                    "char": entity["char"],
                    "type": entity_type
                }
                cleaned_entities.append(cleaned_entity)

            data = {
                "name": path.stem.replace("custom_", ""),
                "tiles": ["".join(row) for row in self.tiles],
                "entities": cleaned_entities,
            }

            with open(path, 'w') as f:
                json.dump(data, f, indent=2)

            self.status_var.set(f"Saved to {path.name}")
            messagebox.showinfo("Success", f"Level saved to {path.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save level: {str(e)}")
            import traceback
            traceback.print_exc()

    def save_level_as(self):
        """Save the current level with a new name."""
        name = tk.simpledialog.askstring("Save Level", "Enter level name:")
        if not name:
            return

        try:
            filename = f"custom_{name}.json"
            path = LEVELS_DIR / filename

            # Process entities to add type information
            processed_entities = []
            for entity in self.entities:
                # Find the entity type based on character
                entity_type = "entity"  # default type
                for entity_type_def in ENTITY_TYPES:
                    if entity_type_def["char"] == entity["char"]:
                        if entity_type_def["unique"]:
                            entity_type = "player"
                        else:
                            entity_type = "monster"
                        break

                processed_entity = {
                    "x": entity["x"],
                    "y": entity["y"],
                    "char": entity["char"],
                    "type": entity_type
                }
                processed_entities.append(processed_entity)

            # Process entities to add type information
            processed_entities = []
            for entity in self.entities:
                # Find the entity type based on character
                entity_type = "entity"  # default type
                for entity_type_def in ENTITY_TYPES:
                    if entity_type_def["char"] == entity["char"]:
                        if entity_type_def["unique"]:
                            entity_type = "player"
                        else:
                            entity_type = "monster"
                        break

                processed_entity = {
                    "x": entity["x"],
                    "y": entity["y"],
                    "char": entity["char"],
                    "type": entity_type
                }
                processed_entities.append(processed_entity)

            data = {
                "name": name,
                "tiles": ["".join(row) for row in self.tiles],
                "entities": processed_entities,
            }

            with open(path, 'w') as f:
                json.dump(data, f, indent=2)

            self.status_var.set(f"Saved to {filename}")
            messagebox.showinfo("Success", f"Level saved to {filename}")

            # Reload levels to include the new one
            self.load_levels()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save level: {str(e)}")

    def draw_grid(self):
        """Draw the grid and entities on the canvas."""
        self.canvas.delete("all")

        if not self.tiles:
            return

        # Calculate canvas dimensions
        self.canvas_width = self.grid_width * self.tile_size
        self.canvas_height = self.grid_height * self.tile_size

        # Configure canvas scroll region
        self.canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height))

        # Draw tiles
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                x1 = x * self.tile_size
                y1 = y * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size

                # Draw tile
                if tile == "#":
                    color = "#808080"  # Gray for walls
                else:
                    color = "#ffffff"  # White for floors

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#000000")

                # Draw entity if exists
                for entity in self.entities:
                    if entity["x"] == x and entity["y"] == y:
                        entity_char = entity["char"]
                        self.canvas.create_text(x1 + self.tile_size//2, y1 + self.tile_size//2,
                                               text=entity_char, font=("Arial", 12))

        # Draw selection highlight
        if self.grid_width > 0 and self.grid_height > 0:
            x1 = self.selected_x * self.tile_size
            y1 = self.selected_y * self.tile_size
            x2 = x1 + self.tile_size
            y2 = y1 + self.tile_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

    def on_canvas_resize(self, event):
        """Handle canvas resize."""
        self.draw_grid()

    def on_canvas_click(self, event):
        """Handle canvas click events."""
        # Convert click coordinates to grid coordinates
        x = event.x // self.tile_size
        y = event.y // self.tile_size

        # Check if click is within grid bounds
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.selected_x = x
            self.selected_y = y

            # Handle based on selected mode
            if self.mode_var.get() == "tile":
                # If we're placing a tile
                if self.tile_var.get() in [".", "#"]:
                    self.tiles[y][x] = self.tile_var.get()
                    self.status_var.set(f"Placed tile: {self.tile_var.get()} at ({x}, {y})")
            elif self.mode_var.get() == "entity":
                # If we're placing an entity
                selected_char = self.entity_var.get()
                if selected_char:
                    # Check if this entity type is unique
                    is_unique_entity = False
                    for entity_type in ENTITY_TYPES:
                        if entity_type["char"] == selected_char:
                            is_unique_entity = entity_type["unique"]
                            break

                    # For unique entities, remove any existing ones
                    if is_unique_entity:
                        self.entities = [e for e in self.entities if e["char"] != selected_char]

                    # Remove existing entity at this position (if any)
                    self.entities = [e for e in self.entities if not (e["x"] == x and e["y"] == y)]

                    # Add new entity
                    self.entities.append({
                        "x": x,
                        "y": y,
                        "char": selected_char
                    })

                    # Find entity name for status message
                    entity_name = selected_char
                    for entity_type in ENTITY_TYPES:
                        if entity_type["char"] == selected_char:
                            entity_name = entity_type["name"]
                            break

                    self.status_var.set(f"Placed entity: {entity_name} ({selected_char}) at ({x}, {y})")

            self.draw_grid()

    def run_level(self):
        """Run the current level in the game."""
        try:
            # Check if we need to save the current level
            selected_name = self.level_var.get()

            # If it's a custom level and has unsaved changes, ask to save
            if selected_name and selected_name.startswith("custom_"):
                # Check if current level has been modified since last save
                # For simplicity, we'll just ask to save
                if messagebox.askyesno("Save Changes", "Do you want to save changes to the current level before running it?"):
                    self.save_level()
            else:
                # If it's a default level, save as custom level
                if messagebox.askyesno("Save Level", "Do you want to save this level as a custom level before running it?"):
                    self.save_level_as()
                else:
                    # If user doesn't want to save, we'll still save to temp file for running
                    pass

            # Create a temporary level file in the levels directory
            import tempfile
            import os

            # Create a temporary file name
            temp_file = os.path.join("levels", "temp_run_level.json")

            # Save current level to temp file
            data = {
                "name": "Temp Run Level",
                "tiles": ["".join(row) for row in self.tiles],
                "entities": self.entities,
            }

            with open(temp_file, 'w') as f:
                import json
                json.dump(data, f, indent=2)

            self.status_var.set(f"Running level: temp_run_level.json")

            # Run the game with the temp level
            import subprocess
            import sys

            # Launch game in a separate process with level name as argument
            game_process = subprocess.Popen([
                sys.executable, "game.py", "temp_run_level.json"
            ], cwd=os.getcwd())

            self.status_var.set("Game running... (close window to return)")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to run level: {str(e)}")
            self.status_var.set("Error running level")

def main():
    root = tk.Tk()
    editor = LevelEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()