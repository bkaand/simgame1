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
        for i, option in enumerate(options):
            self.display_message(f"{i+1}. {option}")
        
        while True:
            try:
                choice = int(self.get_input("\nEnter your choice (number): "))
                if 1 <= choice <= len(options):
                    return choice - 1
                else:
                    self.display_message("Invalid choice. Please try again.")
            except ValueError:
                self.display_message("Please enter a number.")
    
    def display_character_sheet(self, character):
        """Display a character sheet.
        
        Args:
            character: The character to display.
        """
        self.clear_screen()
        self.display_message("=" * self.width)
        self.display_message(f"Character Sheet: {character.name}".center(self.width))
        self.display_message("=" * self.width)
        self.display_message(f"Role: {character.role.capitalize()}")
        self.display_message(f"Age: {character.age}")
        self.display_message(f"Gender: {character.gender.capitalize()}")
        self.display_message(f"Health: {character.health}/100")
        self.display_message(f"Wealth: {character.wealth} coins")
        
        # Display attributes
        self.display_message("\nAttributes:")
        for attr, value in character.attributes.items():
            self.display_message(f"  {attr.capitalize()}: {value}")
        
        # Display skills
        self.display_message("\nSkills:")
        for skill, value in character.skills.items():
            self.display_message(f"  {skill.capitalize()}: {value}")
        
        self.get_input("\nPress Enter to continue...")
    
    def display_event(self, event_title, event_description):
        """Display an event to the user.
        
        Args:
            event_title: The title of the event.
            event_description: The description of the event.
        """
        self.clear_screen()
        self.display_message("!" * self.width)
        self.display_message(f"EVENT: {event_title}".center(self.width))
        self.display_message("!" * self.width)
        self.display_message(f"\n{event_description}\n")
        self.get_input("Press Enter to continue...")
    
    def display_notification(self, message):
        """Display a notification to the user.
        
        Args:
            message: The notification message.
        """
        self.display_message(f"\n>>> {message}")
        time.sleep(1.5)  # Pause briefly to let the user read the notification 