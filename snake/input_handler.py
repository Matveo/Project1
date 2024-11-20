"""
input_handler.py
Handles player input for controlling the snake. This module processes keyboard events
such as pressing arrow keys to change the snake's direction.
"""
import pygame
def handle_direction(dx, dy, dirs):
    """
    Updates the direction of movement based on keyboard input.
    Args:
        dx (int): Current x-axis direction.
        dy (int): Current y-axis direction.
        dirs (dict): Allowed directions.
    Returns:
        tuple: Updated dx, dy values.
    """
    key = pygame.key.get_pressed()
    if key[pygame.K_w] and dirs['W']:
        return 0, -1, {'W': True, 'S': False, 'A': True, 'D': True}
    elif key[pygame.K_s] and dirs['S']:
        return 0, 1, {'W': False, 'S': True, 'A': True, 'D': True}
    elif key[pygame.K_a] and dirs['A']:
        return -1, 0, {'W': True, 'S': True, 'A': True, 'D': False}
    elif key[pygame.K_d] and dirs['D']:
        return 1, 0, {'W': True, 'S': True, 'A': False, 'D': True}
    return dx, dy, dirs
