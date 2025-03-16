"""
Character Factory - Creates different character types based on role
"""
from game.characters.character import Character
from game.characters.roles.king import King
from game.characters.roles.noble import Noble
from game.characters.roles.knight import Knight
from game.characters.roles.merchant import Merchant
from game.characters.roles.farmer import Farmer
from game.characters.roles.craftsman import Craftsman
from game.characters.roles.priest import Priest

class CharacterFactory:
    """Factory for creating characters of different roles."""
    
    def create_character(self, role, name, gender, birth_year=None):
        """Create a character of the specified role.
        
        Args:
            role: The role of the character.
            name: The name of the character.
            gender: The gender of the character.
            birth_year: The birth year of the character (optional).
            
        Returns:
            A character of the specified role.
        """
        # If birth_year is not provided, it will be set in the game_manager
        # when creating a new character
        if role == "king":
            character = King(name, gender, birth_year)
        elif role == "noble":
            character = Noble(name, gender, birth_year)
        elif role == "knight":
            character = Knight(name, gender, birth_year)
        elif role == "merchant":
            character = Merchant(name, gender, birth_year)
        elif role == "farmer":
            character = Farmer(name, gender, birth_year)
        elif role == "craftsman":
            character = Craftsman(name, gender, birth_year)
        elif role == "priest":
            character = Priest(name, gender, birth_year)
        else:
            # Default to base character
            character = Character(name, gender, role, birth_year)
        
        # Set birth year if provided
        if birth_year is not None:
            character.birth_year = birth_year
        
        return character 