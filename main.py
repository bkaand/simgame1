#!/usr/bin/env python3
"""
Medieval Life Simulator - A medieval life simulation game with a graphical interface
"""
import os
import sys
import time
import random
from game.game_manager import GameManager
from game.ui.gui_interface import GUIInterface

def main():
    """Main entry point for the game."""
    # Initialize the game with GUI interface
    interface = GUIInterface()
    
    try:
        # Create game manager and set reference
        game = GameManager(interface)
        interface.game_manager = game
        
        # Display start screen and handle game start/load
        if interface.display_start_screen():
            # Get character creation choices through GUI
            name = interface.get_input("Enter your character's name:")
            
            gender_choice = interface.display_menu("Choose your gender:", ["Male", "Female"])
            if gender_choice is None:
                sys.exit(0)
            gender = "male" if gender_choice == 0 else "female"
            
            roles = ["Noble", "Knight", "Merchant", "Farmer", "Craftsman", "Priest"]
            role_choice = interface.display_menu("Choose your role:", roles)
            if role_choice is None:
                sys.exit(0)
            role = roles[role_choice].lower()
            
            # Start new game with character details
            game.start_new_game(name, gender, role)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        interface.display_message("Exiting game. Farewell!")
        sys.exit(0)
    except Exception as e:
        interface.display_message(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
