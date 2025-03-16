"""
Family Manager - Handles family relationships and dynamics
"""
import random
from game.characters.character import Character, Relationship

class FamilyManager:
    """Manages family relationships and dynamics."""
    
    def __init__(self, game_manager):
        """Initialize the family manager.
        
        Args:
            game_manager: The game manager.
        """
        self.game_manager = game_manager
        self.family_events = self._initialize_family_events()
        self.family_traits = self._initialize_family_traits()
        
    def _initialize_family_events(self):
        """Initialize family events.
        
        Returns:
            A dictionary of family events.
        """
        return {
            "child_birth": {
                "title": "Child Birth",
                "description": "Your family welcomes a new child.",
                "probability": 0.2,  # 20% chance per year for married couples
                "requirements": {"married": True, "spouse_age_min": 16, "spouse_age_max": 45}
            },
            "child_milestone": {
                "title": "Child Milestone",
                "description": "One of your children reaches a significant milestone.",
                "probability": 0.3,  # 30% chance per year per child
                "requirements": {"has_children": True}
            },
            "family_gathering": {
                "title": "Family Gathering",
                "description": "Your family gathers for a special occasion.",
                "probability": 0.4,  # 40% chance per year
                "requirements": {"family_size_min": 2}
            },
            "spouse_career": {
                "title": "Spouse Career Event",
                "description": "Your spouse experiences a significant career event.",
                "probability": 0.2,  # 20% chance per year
                "requirements": {"married": True}
            },
            "inheritance": {
                "title": "Family Inheritance",
                "description": "A family inheritance matter requires attention.",
                "probability": 0.1,  # 10% chance per year
                "requirements": {"age_min": 25}
            }
        }
    
    def _initialize_family_traits(self):
        """Initialize hereditary family traits.
        
        Returns:
            A dictionary of family traits.
        """
        return {
            "ambitious": {
                "description": "More likely to succeed in career endeavors",
                "effects": {"career_success": 1.2},
                "hereditary_chance": 0.6  # 60% chance to pass to children
            },
            "scholarly": {
                "description": "Faster skill learning",
                "effects": {"skill_gain": 1.2},
                "hereditary_chance": 0.5
            },
            "charismatic": {
                "description": "Better at social interactions",
                "effects": {"social_success": 1.2},
                "hereditary_chance": 0.5
            },
            "robust": {
                "description": "Better health and longevity",
                "effects": {"health_bonus": 10, "longevity": 1.1},
                "hereditary_chance": 0.7
            }
        }
    
    def check_family_events(self):
        """Check for family events.
        
        Returns:
            A list of family events that occur.
        """
        events = []
        player = self.game_manager.player
        
        for event_id, event_data in self.family_events.items():
            if self._meets_requirements(player, event_data["requirements"]):
                if random.random() < event_data["probability"]:
                    events.append(self._process_family_event(event_id, event_data))
        
        return events
    
    def _meets_requirements(self, player, requirements):
        """Check if player meets event requirements.
        
        Args:
            player: The player character.
            requirements: Dictionary of requirements.
            
        Returns:
            bool: Whether requirements are met.
        """
        if requirements.get("married") and not player.spouse:
            return False
            
        if requirements.get("has_children") and not player.children:
            return False
            
        if requirements.get("family_size_min"):
            family_size = 1  # Player
            if player.spouse:
                family_size += 1
            family_size += len(player.children)
            if family_size < requirements["family_size_min"]:
                return False
                
        if requirements.get("age_min") and player.age < requirements["age_min"]:
            return False
            
        if requirements.get("spouse_age_min") and player.spouse:
            if player.spouse.age < requirements["spouse_age_min"]:
                return False
                
        if requirements.get("spouse_age_max") and player.spouse:
            if player.spouse.age > requirements["spouse_age_max"]:
                return False
        
        return True
    
    def _process_family_event(self, event_id, event_data):
        """Process a family event.
        
        Args:
            event_id: The event identifier.
            event_data: The event data.
            
        Returns:
            A processed event with outcomes.
        """
        player = self.game_manager.player
        
        if event_id == "child_birth":
            # Create a new child
            child_gender = random.choice(["male", "female"])
            child = self._create_child(player, child_gender)
            player.children.append(child)
            
            # Update achievements
            if not self.game_manager.achievements["first_child"]:
                self.game_manager.achievements["first_child"] = True
            
            return {
                "title": event_data["title"],
                "description": f"Your spouse has given birth to a {child_gender} child named {child.name}!",
                "effects": {"wealth": -50}  # Children cost money
            }
            
        elif event_id == "child_milestone":
            child = random.choice(player.children)
            milestone = self._generate_child_milestone(child)
            return {
                "title": event_data["title"],
                "description": milestone["description"],
                "effects": milestone["effects"]
            }
            
        elif event_id == "family_gathering":
            outcome = self._generate_family_gathering()
            return {
                "title": event_data["title"],
                "description": outcome["description"],
                "effects": outcome["effects"]
            }
            
        elif event_id == "spouse_career":
            career_event = self._generate_spouse_career_event()
            return {
                "title": event_data["title"],
                "description": career_event["description"],
                "effects": career_event["effects"]
            }
            
        elif event_id == "inheritance":
            inheritance = self._generate_inheritance_event()
            return {
                "title": event_data["title"],
                "description": inheritance["description"],
                "effects": inheritance["effects"]
            }
    
    def _create_child(self, player, gender):
        """Create a new child character.
        
        Args:
            player: The parent character.
            gender: The child's gender.
            
        Returns:
            A new Character instance representing the child.
        """
        # Generate name based on gender and medieval setting
        if gender == "male":
            name = random.choice(["John", "William", "Robert", "Richard", "Henry", "Thomas"])
        else:
            name = random.choice(["Mary", "Elizabeth", "Margaret", "Alice", "Joan", "Catherine"])
        
        # Create child with current year as birth year
        child = Character(name, gender, "child", self.game_manager.game_year)
        child.age = 0
        
        # Inherit traits
        self._inherit_traits(child, player)
        
        return child
    
    def _inherit_traits(self, child, parent):
        """Have child inherit traits from parent.
        
        Args:
            child: The child character.
            parent: The parent character.
        """
        # Initialize child's traits
        child.traits = []
        
        # Check each parent trait for inheritance
        if hasattr(parent, 'traits'):
            for trait in parent.traits:
                if trait in self.family_traits:
                    # Check if trait is inherited
                    if random.random() < self.family_traits[trait]["hereditary_chance"]:
                        child.traits.append(trait)
        
        # Small chance for new traits
        if random.random() < 0.1:  # 10% chance
            possible_new_traits = [t for t in self.family_traits if t not in child.traits]
            if possible_new_traits:
                child.traits.append(random.choice(possible_new_traits))
    
    def _generate_child_milestone(self, child):
        """Generate a milestone event for a child.
        
        Args:
            child: The child character.
            
        Returns:
            A dictionary containing the milestone event details.
        """
        milestones = {
            0: {
                "description": f"{child.name} speaks their first words!",
                "effects": {"happiness": 5}
            },
            5: {
                "description": f"{child.name} begins their education.",
                "effects": {"wealth": -20}
            },
            12: {
                "description": f"{child.name} shows interest in following your footsteps as a {self.game_manager.player.role}.",
                "effects": {"happiness": 5}
            },
            16: {
                "description": f"{child.name} comes of age and must choose their path in life.",
                "effects": {}
            }
        }
        
        # Get milestone for child's age, or generate random event if no specific milestone
        if child.age in milestones:
            return milestones[child.age]
        else:
            return {
                "description": f"{child.name} continues to grow and develop.",
                "effects": {"happiness": 2}
            }
    
    def _generate_family_gathering(self):
        """Generate a family gathering event.
        
        Returns:
            A dictionary containing the event details.
        """
        gatherings = [
            {
                "description": "Your family gathers for a feast. The bonds between you grow stronger.",
                "effects": {"happiness": 5, "wealth": -20}
            },
            {
                "description": "A family celebration brings everyone together. Stories and laughter are shared.",
                "effects": {"happiness": 5, "wealth": -15}
            },
            {
                "description": "Your family meets for a solemn occasion, supporting each other through difficult times.",
                "effects": {"happiness": 3}
            }
        ]
        
        return random.choice(gatherings)
    
    def _generate_spouse_career_event(self):
        """Generate a career event for the spouse.
        
        Returns:
            A dictionary containing the event details.
        """
        events = [
            {
                "description": "Your spouse's business ventures bring additional income to the family.",
                "effects": {"wealth": 50}
            },
            {
                "description": "Your spouse gains recognition in their field of work.",
                "effects": {"happiness": 5}
            },
            {
                "description": "Your spouse faces challenges in their work but perseveres.",
                "effects": {"wealth": -20}
            }
        ]
        
        return random.choice(events)
    
    def _generate_inheritance_event(self):
        """Generate an inheritance event.
        
        Returns:
            A dictionary containing the event details.
        """
        events = [
            {
                "description": "A distant relative leaves you a small inheritance.",
                "effects": {"wealth": 100}
            },
            {
                "description": "Family inheritance matters cause some tension among relatives.",
                "effects": {"happiness": -3, "wealth": 50}
            },
            {
                "description": "You must decide how to handle a family heirloom.",
                "effects": {"wealth": 30}
            }
        ]
        
        return random.choice(events)
    
    def update_family_for_new_year(self):
        """Update family members for the new year.
        
        Returns:
            A list of significant family events that occurred.
        """
        events = []
        player = self.game_manager.player
        
        # Age children
        for child in player.children:
            child.age += 1
            
            # Check for milestones
            if child.age in [5, 12, 16]:
                milestone = self._generate_child_milestone(child)
                events.append(milestone)
        
        # Check for new family events
        family_events = self.check_family_events()
        events.extend(family_events)
        
        return events 