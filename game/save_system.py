"""
Save System - Handles saving and loading game states
"""
import os
import json
import time
from pathlib import Path

class SaveSystem:
    """Handles saving and loading game states."""
    
    def __init__(self):
        """Initialize the save system."""
        self.save_dir = Path("saves")
        self.save_dir.mkdir(exist_ok=True)
    
    def save_game(self, game_manager):
        """Save the current game state.
        
        Args:
            game_manager: The game manager containing the game state.
            
        Returns:
            bool: True if save was successful, False otherwise.
        """
        try:
            # Create save data dictionary
            save_data = {
                "game_year": game_manager.game_year,
                "player": self._serialize_character(game_manager.player),
                "achievements": game_manager.achievements
            }
            
            # Save to file
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_file = self.save_dir / f"save_{timestamp}.json"
            
            with open(save_file, "w") as f:
                json.dump(save_data, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, game_manager, save_file):
        """Load a saved game state.
        
        Args:
            game_manager: The game manager to load the state into.
            save_file: The save file to load.
            
        Returns:
            bool: True if load was successful, False otherwise.
        """
        try:
            with open(save_file, "r") as f:
                save_data = json.load(f)
            
            # Load game year
            game_manager.game_year = save_data["game_year"]
            
            # Load player character
            player_data = save_data["player"]
            game_manager.player = self._deserialize_character(player_data)
            
            # Load achievements
            game_manager.achievements = save_data["achievements"]
            
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def _serialize_character(self, character):
        """Serialize a character object to a dictionary.
        
        Args:
            character: The character to serialize.
            
        Returns:
            A dictionary containing the character's data.
        """
        data = {
            "name": character.name,
            "role": character.role,
            "gender": character.gender,
            "age": character.age,
            "birth_year": character.birth_year,
            "health": character.health,
            "wealth": character.wealth,
            "happiness": character.happiness,
            "skills": character.skills,
            "attributes": character.attributes,
            "traits": character.traits,
            "is_alive": character.is_alive,
            "reputations": character.reputation.reputations
        }
        
        # Serialize spouse if exists
        if character.spouse:
            data["spouse"] = self._serialize_character(character.spouse)
        else:
            data["spouse"] = None
        
        # Serialize children
        data["children"] = [self._serialize_character(child) for child in character.children]
        
        # Serialize relationships
        data["relationships"] = [
            {
                "person": self._serialize_character(person),
                "level": rel.level,
                "status": rel.status
            }
            for person, rel in character.relationships.items()
        ]
        
        return data
    
    def _deserialize_character(self, data):
        """Deserialize a character from a dictionary.
        
        Args:
            data: The dictionary containing character data.
            
        Returns:
            A Character object.
        """
        from game.characters.character import Character, Relationship
        
        # Create base character
        character = Character(
            data["name"],
            data["gender"],
            data["role"],
            data["birth_year"]
        )
        
        # Set basic attributes
        character.age = data["age"]
        character.health = data["health"]
        character.wealth = data["wealth"]
        character.happiness = data["happiness"]
        character.skills = data["skills"]
        character.attributes = data["attributes"]
        character.traits = data["traits"]
        character.is_alive = data["is_alive"]
        
        # Set reputations
        character.reputation.reputations = data["reputations"]
        
        # Deserialize spouse if exists
        if data["spouse"]:
            character.spouse = self._deserialize_character(data["spouse"])
        
        # Deserialize children
        character.children = [self._deserialize_character(child) for child in data["children"]]
        
        # Deserialize relationships
        character.relationships = {}
        for rel_data in data["relationships"]:
            person = self._deserialize_character(rel_data["person"])
            relationship = Relationship(person, rel_data["status"], rel_data["level"])
            character.relationships[person] = relationship
        
        return character
    
    def get_save_files(self):
        """Get a list of available save files.
        
        Returns:
            A list of save file paths.
        """
        return list(self.save_dir.glob("save_*.json")) 