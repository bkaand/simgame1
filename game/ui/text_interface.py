"""
Text Interface - Handles the text-based user interface for the game
"""
import os
import time

class TextInterface:
    """Text-based user interface for the game."""
    
    def __init__(self):
        """Initialize the text interface."""
        self.width = 80
        self.running = True
        self.game_manager = None
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_message(self, message):
        """Display a message to the user.
        
        Args:
            message: The message to display.
        """
        print(message)
    
    def get_input(self, prompt):
        """Get input from the user.
        
        Args:
            prompt: The prompt to display to the user.
            
        Returns:
            The user's input.
        """
        return input(prompt)
    
    def display_menu(self, title, options):
        """Display a menu and get the user's choice.
        
        Args:
            title: The title of the menu.
            options: A list of options to display.
            
        Returns:
            The index of the chosen option.
        """
        self.display_message(f"\n{title}")
        for i, option in enumerate(options, 1):
            self.display_message(f"{i}. {option}")
        
        while True:
            try:
                choice = int(self.get_input("\nEnter your choice (number): "))
                if 1 <= choice <= len(options):
                    return choice - 1
                self.display_message(f"Invalid choice. Please enter 1-{len(options)}.")
            except ValueError:
                self.display_message("Invalid input. Please enter a number.")
    
    def display_character_sheet(self, character):
        """Display detailed character information.
        
        Args:
            character: The character to display information for.
        """
        self.display_message("\n=== Character Sheet ===")
        character.display_details(self)
    
    def display_event(self, event_title, event_description):
        """Display an event to the user.
        
        Args:
            event_title: The title of the event.
            event_description: The description of the event.
        """
        border = "!" * self.width
        self.display_message(border)
        self.display_message(f"{event_title:^{self.width}}")
        self.display_message(border)
        self.display_message("")
        self.display_message(event_description)
        self.display_message("")
    
    def display_notification(self, message):
        """Display a notification to the user.
        
        Args:
            message: The notification message.
        """
        self.display_message(f"\n>>> {message} <<<\n")
        time.sleep(1.5)  # Pause briefly to let the user read the notification 