"""
Story Arc Base - Base class for story arcs
"""
import random
from game.events.event import Event

class StoryArc:
    """Represents a multi-year story arc with cascading consequences."""
    
    def __init__(self, arc_id, title, description, stages, role_specific=False, roles=None, prerequisites=None):
        """Initialize a new story arc.
        
        Args:
            arc_id: Unique identifier for the story arc.
            title: The story arc title.
            description: The story arc description.
            stages: A list of stages, each with its own events and choices.
            role_specific: Whether the story arc is specific to certain roles.
            roles: A list of roles that can experience this story arc.
            prerequisites: A dictionary of prerequisites for this story arc.
        """
        self.arc_id = arc_id
        self.title = title
        self.description = description
        self.stages = stages
        self.role_specific = role_specific
        self.roles = roles or []
        self.prerequisites = prerequisites or {}
        self.current_stage = 0
        self.active = False
        self.completed = False
        self.player_choices = []
        self.years_since_last_stage = 0
        self.state = {}  # For tracking arc-specific state
    
    def start(self):
        """Start the story arc."""
        self.active = True
        self.current_stage = 0
        self.years_since_last_stage = 0
        self.player_choices = []
    
    def check_prerequisites(self, player):
        """Check if the prerequisites for this story arc are met.
        
        Args:
            player: The player character.
            
        Returns:
            True if the prerequisites are met, False otherwise.
        """
        if not self.prerequisites:
            return True
            
        for stat, value in self.prerequisites.items():
            if stat == "age" and player.age < value:
                return False
            elif stat == "wealth" and player.wealth < value:
                return False
            elif stat == "health" and player.health < value:
                return False
            elif stat.startswith("skill_") and stat[6:] in player.skills:
                if player.skills[stat[6:]] < value:
                    return False
            elif stat.startswith("attribute_") and stat[10:] in player.attributes:
                if player.attributes[stat[10:]] < value:
                    return False
            elif stat == "role" and player.role != value:
                return False
            elif stat == "gender" and player.gender != value:
                return False
            elif stat == "previous_arc" and value not in player.completed_arcs:
                return False
        
        return True
    
    def get_current_event(self, player):
        """Get the current event for this story arc.
        
        Args:
            player: The player character.
            
        Returns:
            An Event object for the current stage, or None if the arc is complete.
        """
        if not self.active or self.completed or self.current_stage >= len(self.stages):
            return None
        
        stage = self.stages[self.current_stage]
        
        # Check if there are conditional events based on previous choices
        if "conditional_events" in stage and self.player_choices:
            for condition in stage["conditional_events"]:
                if self._check_condition(condition["condition"]):
                    # Create an event based on the conditional event
                    return Event(
                        f"{self.title}: {stage['title']}",
                        condition["description"],
                        condition["effects"],
                        condition.get("choices", [])
                    )
        
        # Create an event based on the current stage
        return Event(
            f"{self.title}: {stage['title']}",
            stage["description"],
            stage["effects"],
            stage.get("choices", [])
        )
    
    def advance_stage(self, choice_idx=None):
        """Advance to the next stage of the story arc.
        
        Args:
            choice_idx: The index of the player's choice, if applicable.
        """
        if choice_idx is not None:
            self.player_choices.append(choice_idx)
        
        self.current_stage += 1
        self.years_since_last_stage = 0
        
        if self.current_stage >= len(self.stages):
            self.completed = True
            self.active = False
    
    def update_for_new_year(self):
        """Update the story arc for a new year.
        
        Returns:
            True if a new stage is ready, False otherwise.
        """
        if not self.active or self.completed:
            return False
        
        self.years_since_last_stage += 1
        
        # Check if it's time for the next stage
        stage = self.stages[self.current_stage]
        years_until_next = stage.get("years_until_next", 1)
        
        return self.years_since_last_stage >= years_until_next
    
    def _check_condition(self, condition):
        """Check if a condition is met based on player choices.
        
        Args:
            condition: A dictionary describing the condition.
            
        Returns:
            True if the condition is met, False otherwise.
        """
        if "choice" in condition:
            stage_idx = condition["stage"]
            choice_idx = condition["choice"]
            
            if stage_idx < len(self.player_choices):
                return self.player_choices[stage_idx] == choice_idx
        
        return False 