"""
Craftsman - Character role class for craftsmen (placeholder)
"""
import random
from game.characters.character import Character

class Craftsman(Character):
    """Character role class for craftsmen."""
    
    def __init__(self, name, gender, birth_year=None):
        """Initialize a new craftsman character.
        
        Args:
            name: The character's name.
            gender: The character's gender.
            birth_year: The character's birth year (optional).
        """
        super().__init__(name, gender, "craftsman", birth_year)
        
        # Craftsmen start with modest wealth
        self.wealth = random.randint(50, 200)
        
        # Adjust skills for role
        self._adjust_skills_for_role()
    
    def _adjust_skills_for_role(self):
        """Adjust skills based on character role."""
        # Craftsmen are better at crafting
        self.skills["crafting"] += random.randint(20, 40)
        
        # Ensure skills stay within bounds
        for skill in self.skills:
            self.skills[skill] = min(100, self.skills[skill])
    
    def get_actions(self):
        """Get the list of actions available to this character.
        
        Returns:
            A list of action names.
        """
        # Get base actions
        actions = super().get_actions()
        
        # Add craftsman-specific actions (to be implemented)
        actions.extend([
            "Craft Item"
        ])
        
        return actions
    
    def perform_action(self, action, game_manager):
        """Perform an action.
        
        Args:
            action: The name of the action to perform.
            game_manager: The game manager.
        """
        if action == "Craft Item":
            # Placeholder
            game_manager.interface.display_message("This action is not yet implemented.")
            game_manager.interface.get_input("Press Enter to continue...")
        else:
            # Use base class implementation for common actions
            super().perform_action(action, game_manager)
    
    def display_status(self, interface):
        """Display the character's status.
        
        Args:
            interface: The user interface.
        """
        interface.display_message("Crafting Skill: " + str(self.skills["crafting"]) + "/100") 