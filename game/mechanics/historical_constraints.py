"""
Historical Constraints - Manages historical accuracy and social barriers in the game
"""
from dataclasses import dataclass
from typing import Dict, List, Set

@dataclass
class SocialClass:
    """Represents a social class with its constraints and privileges."""
    name: str
    allowed_roles: Set[str]
    allowed_actions: Set[str]
    marriage_classes: Set[str]
    education_level: int  # 0-100
    wealth_range: tuple  # (min, max)
    mobility_chance: int  # 0-100, chance to move up in society per year

class HistoricalConstraints:
    """Manages historical accuracy and social barriers."""
    
    def __init__(self):
        """Initialize historical constraints."""
        self.social_classes = self._initialize_social_classes()
        self.gender_restrictions = self._initialize_gender_restrictions()
        self.education_requirements = self._initialize_education_requirements()
        
    def _initialize_social_classes(self) -> Dict[str, SocialClass]:
        """Initialize social class definitions."""
        return {
            "nobility": SocialClass(
                name="nobility",
                allowed_roles={"king", "noble"},
                allowed_actions={"Diplomacy", "Study", "Combat", "Travel", "Prayer"},
                marriage_classes={"nobility", "royalty"},
                education_level=80,
                wealth_range=(1000, 100000),
                mobility_chance=0
            ),
            "clergy": SocialClass(
                name="clergy",
                allowed_roles={"priest", "monk"},
                allowed_actions={"Prayer", "Study", "Diplomacy", "Travel"},
                marriage_classes=set(),  # Clergy cannot marry
                education_level=70,
                wealth_range=(100, 1000),
                mobility_chance=20
            ),
            "merchants": SocialClass(
                name="merchants",
                allowed_roles={"merchant", "craftsman"},
                allowed_actions={"Trade", "Craft", "Travel", "Study"},
                marriage_classes={"merchants", "craftsmen", "peasants"},
                education_level=50,
                wealth_range=(200, 5000),
                mobility_chance=30
            ),
            "peasants": SocialClass(
                name="peasants",
                allowed_roles={"farmer", "craftsman"},
                allowed_actions={"Farm", "Craft", "Trade"},
                marriage_classes={"peasants", "craftsmen"},
                education_level=20,
                wealth_range=(0, 200),
                mobility_chance=10
            )
        }
    
    def _initialize_gender_restrictions(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize gender-specific restrictions."""
        return {
            "male": {
                "allowed_roles": ["king", "noble", "knight", "merchant", "farmer", "craftsman", "priest"],
                "restricted_actions": [],
                "education_penalty": 0
            },
            "female": {
                "allowed_roles": ["noble", "merchant", "farmer"],  # Limited roles for historical accuracy
                "restricted_actions": ["Combat", "Prayer"],  # Some actions restricted
                "education_penalty": -20  # Historical education disadvantage
            }
        }
    
    def _initialize_education_requirements(self) -> Dict[str, Dict[str, int]]:
        """Initialize education requirements for different actions."""
        return {
            "Study": {
                "base_requirement": 30,
                "nobility_bonus": 20,
                "clergy_bonus": 30,
                "merchant_bonus": 10
            },
            "Diplomacy": {
                "base_requirement": 40,
                "nobility_bonus": 30,
                "clergy_bonus": 20,
                "merchant_bonus": 0
            },
            "Trade": {
                "base_requirement": 20,
                "nobility_bonus": 0,
                "clergy_bonus": 0,
                "merchant_bonus": 20
            }
        }
    
    def can_perform_action(self, character, action: str) -> tuple[bool, str]:
        """Check if a character can perform an action based on historical constraints.
        
        Args:
            character: The character attempting the action
            action: The action being attempted
            
        Returns:
            A tuple of (allowed, reason)
        """
        # Get character's social class
        social_class = self._determine_social_class(character)
        
        # Check gender restrictions
        gender_restrictions = self.gender_restrictions[character.gender]
        if action in gender_restrictions["restricted_actions"]:
            return False, f"As a {character.gender}, you cannot perform this action in medieval times."
        
        # Check social class restrictions
        if action not in self.social_classes[social_class].allowed_actions:
            return False, f"Your social class ({social_class}) does not permit this action."
        
        # Check education requirements
        if action in self.education_requirements:
            req = self.education_requirements[action]
            base_req = req["base_requirement"]
            class_bonus = req.get(f"{social_class}_bonus", 0)
            
            # Calculate effective education level
            education_level = self._calculate_education_level(character)
            if education_level < (base_req - class_bonus):
                return False, f"You lack the education to perform this action. (Required: {base_req - class_bonus})"
        
        return True, "Action permitted."
    
    def can_marry(self, character1, character2) -> tuple[bool, str]:
        """Check if two characters can marry based on historical constraints.
        
        Args:
            character1: First character
            character2: Second character
            
        Returns:
            A tuple of (allowed, reason)
        """
        # Get social classes
        class1 = self._determine_social_class(character1)
        class2 = self._determine_social_class(character2)
        
        # Check if either class is clergy
        if class1 == "clergy" or class2 == "clergy":
            return False, "Clergy members cannot marry."
        
        # Check if marriage is allowed between these classes
        if class2 not in self.social_classes[class1].marriage_classes:
            return False, f"Marriage between {class1} and {class2} is not permitted."
        
        return True, "Marriage permitted."
    
    def calculate_social_mobility(self, character) -> tuple[str, int]:
        """Calculate chances of social mobility for a character.
        
        Args:
            character: The character to check
            
        Returns:
            A tuple of (potential_new_class, chance_percentage)
        """
        current_class = self._determine_social_class(character)
        social_class = self.social_classes[current_class]
        
        # Base chance from social class
        base_chance = social_class.mobility_chance
        
        # Modify based on wealth
        if character.wealth > social_class.wealth_range[1]:
            base_chance += 10
        
        # Modify based on education
        education_level = self._calculate_education_level(character)
        if education_level > social_class.education_level:
            base_chance += 5
        
        # Determine potential new class
        if current_class == "peasants":
            return "merchants", base_chance
        elif current_class == "merchants":
            return "nobility", base_chance // 2  # Harder to reach nobility
        
        return current_class, 0  # No mobility for nobility or clergy
    
    def _determine_social_class(self, character) -> str:
        """Determine a character's social class based on their role and wealth."""
        role_to_class = {
            "king": "nobility",
            "noble": "nobility",
            "priest": "clergy",
            "monk": "clergy",
            "merchant": "merchants",
            "craftsman": "merchants" if character.wealth >= 500 else "peasants",
            "farmer": "peasants"
        }
        return role_to_class.get(character.role, "peasants")
    
    def _calculate_education_level(self, character) -> int:
        """Calculate a character's effective education level."""
        # Base education from skills
        base_education = (
            character.skills.get("diplomacy", 0) +
            character.skills.get("stewardship", 0) +
            character.skills.get("medicine", 0)
        ) // 3
        
        # Modify based on attributes
        base_education += character.attributes.get("intelligence", 0) // 2
        base_education += character.attributes.get("wisdom", 0) // 2
        
        # Apply gender penalty if applicable
        gender_penalty = self.gender_restrictions[character.gender]["education_penalty"]
        base_education = max(0, base_education + gender_penalty)
        
        # Cap at 100
        return min(100, base_education)
    
    def get_allowed_roles(self, gender: str) -> List[str]:
        """Get the list of roles allowed for a given gender.
        
        Args:
            gender: The gender to check
            
        Returns:
            A list of allowed role names
        """
        return self.gender_restrictions[gender]["allowed_roles"] 