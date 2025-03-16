#!/usr/bin/env python3
"""
Medieval Life Simulator - A medieval life simulation game with a graphical interface
"""
import os
import sys
import time
import random
import pygame
from game.game_manager import GameManager
from game.ui.gui_interface import GUIInterface

def main():
    """Main entry point for the game."""
    # Initialize the game
    interface = GUIInterface()
    
    try:
        # Show start screen
        if not interface.display_start_screen():
            return  # User chose to quit
        
        # Create game manager
        game = GameManager(interface)
        
        # Start new game
        game.start_new_game()
    finally:
        # Ensure pygame is properly quit
        pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting game. Farewell!")
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit(1)
