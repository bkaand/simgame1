"""
Event - Represents a game event
"""
import random

class Event:
    """Represents a game event."""
    
    def __init__(self, title, description, effects, choices=None):
        """Initialize a new event.
        
        Args:
            title: The event title.
            description: The event description.
            effects: A dictionary of effects (e.g., {'health': -10}).
            choices: A list of choices for the player, each with its own effects.
        """
        self.title = title
        self.description = description
        self.effects = effects
        self.choices = choices or []
    
    def execute(self, player, interface):
        """Execute the event.
        
        Args:
            player: The player character.
            interface: The user interface.
        """
        # Display the event
        interface.display_event(self.title, self.description)
        
        # If there are choices, let the player choose
        if self.choices:
            choice_options = [choice["text"] for choice in self.choices]
            choice_idx = interface.display_menu("What will you do?", choice_options)
            
            # Apply effects of the chosen option
            chosen_effects = self.choices[choice_idx]["effects"]
            outcome_text = self.choices[choice_idx]["outcome"]
            
            # Apply the effects
            self._apply_effects(player, chosen_effects)
            
            # Display the outcome
            interface.display_event(f"Outcome: {self.title}", outcome_text)
        else:
            # Apply the default effects
            self._apply_effects(player, self.effects)
    
    def _apply_effects(self, player, effects):
        """Apply the event effects to the player.
        
        Args:
            player: The player character.
            effects: A dictionary of effects to apply.
        """
        for stat, value in effects.items():
            if stat == "health":
                player.health = max(0, min(100, player.health + value))
            elif stat == "wealth":
                player.wealth = max(0, player.wealth + value)
            elif stat.startswith("skill_"):
                skill_name = stat[6:]  # Remove 'skill_' prefix
                if skill_name in player.skills:
                    player.skills[skill_name] = max(0, min(100, player.skills[skill_name] + value))
            elif stat.startswith("attribute_"):
                attr_name = stat[10:]  # Remove 'attribute_' prefix
                if attr_name in player.attributes:
                    player.attributes[attr_name] = max(0, min(100, player.attributes[attr_name] + value))
            elif stat == "random_skill":
                # Improve a random skill
                skill_name = random.choice(list(player.skills.keys()))
                player.skills[skill_name] = max(0, min(100, player.skills[skill_name] + value))
            elif stat == "random_attribute":
                # Improve a random attribute
                attr_name = random.choice(list(player.attributes.keys()))
                player.attributes[attr_name] = max(0, min(100, player.attributes[attr_name] + value)) 