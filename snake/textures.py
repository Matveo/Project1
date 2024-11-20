"""
textures.py

This module handles loading and updating textures (images) for the game. It allows changing the
paths for the snake, apple, and background textures via a configuration file (`config.json`).
"""
import json
import os
import pygame
from settings import SIZE, RES

CONFIG_FILE = "config.json"


def load_texture(path, size=(SIZE, SIZE)):
    """
    Loads an image texture from a given path and scales it to a given size.

    Args:
        path (str): Path to the image file.
        size (tuple): Desired (width, height) of the image.

    Returns:
        pygame.Surface: Scaled image surface.
    """
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading texture from {path}: {e}")
        return pygame.Surface(size)  # Return empty surface as fallback


# load_config() written by chat gpt
def load_config():
    """
    Loads texture configuration from a JSON file.

    Returns:
        dict: Dictionary containing paths to textures.
    """
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "background": "assets/default/background.png",
            "snake_head": "assets/default/player.png",
            "apple": "assets/default/apple.png"
        }


def save_config(config):
    """
    Saves the updated texture configuration to a JSON file.

    Args:
        config (dict): Configuration dictionary to save.
    """
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


def update_config():
    """
    Allows the user to update texture paths via console input.
    """
    config = load_config()
    print("Current texture paths:")
    for key, value in config.items():
        print(f"{key}: {value}")

    change = input(
        "Do you want to change textures? (yes/no): ").lower()
    if change in ["yes", "y"]:
        for key in config:
            new_path = input(
                f"Enter new path for {key} (or press Enter to keep current): ")
            if new_path:
                if os.path.exists(new_path):
                    config[key] = new_path
                else:
                    print(
                        f"File not found: {new_path}. Keeping the current texture.")
        save_config(config)
        print("Texture paths updated. RESTART to play with new textures.")


# Load texture paths from config.json
config = load_config()

# Load textures
BACKGROUND_IMG = load_texture(config["background"], (RES, RES))
SNAKE_HEAD_IMG = load_texture(config["snake_head"])
SNAKE_BODY_IMG = load_texture(config["snake"])
APPLE_IMG = load_texture(config["apple"])
