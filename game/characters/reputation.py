"""
Reputation System - Tracks player standing with different social groups
"""

class ReputationManager:
    """Manages reputation with different social groups."""
    
    def __init__(self):
        """Initialize reputation manager."""
        self.reputations = {
            "nobility": 50,      # Standing with noble houses
            "clergy": 50,        # Standing with the church
            "merchants": 50,     # Standing with merchant guilds
            "peasants": 50,      # Standing with common folk
            "military": 50,      # Standing with knights and soldiers
            "criminals": 0       # Standing with the criminal underworld
        }
        
        # Track specific houses/guilds/organizations
        self.specific_reputations = {}
        
        # Define opposing groups where gaining reputation with one loses it with another
        self.opposing_groups = {
            "nobility": "peasants",
            "clergy": "criminals",
            "merchants": "nobility",
            "military": "criminals"
        }
    
    def adjust_reputation(self, group, amount):
        """Adjust reputation with a group.
        
        Args:
            group: The social group to adjust reputation with.
            amount: The amount to adjust by (positive or negative).
        """
        if group in self.reputations:
            old_rep = self.reputations[group]
            self.reputations[group] = max(0, min(100, old_rep + amount))
            
            # Adjust opposing group reputation
            if group in self.opposing_groups:
                opposing = self.opposing_groups[group]
                # Smaller opposite effect
                self.reputations[opposing] = max(0, min(100, 
                    self.reputations[opposing] - amount * 0.5))
    
    def add_specific_reputation(self, category, name):
        """Add reputation tracking for a specific organization.
        
        Args:
            category: The type of organization (e.g., "noble_house", "guild")
            name: The name of the organization
        """
        key = f"{category}_{name}"
        if key not in self.specific_reputations:
            self.specific_reputations[key] = 50
    
    def adjust_specific_reputation(self, category, name, amount):
        """Adjust reputation with a specific organization.
        
        Args:
            category: The type of organization
            name: The name of the organization
            amount: The amount to adjust by
        """
        key = f"{category}_{name}"
        if key in self.specific_reputations:
            self.specific_reputations[key] = max(0, min(100, 
                self.specific_reputations[key] + amount))
    
    def get_reputation_level(self, group):
        """Get the reputation level description for a group.
        
        Args:
            group: The social group.
            
        Returns:
            A tuple of (level_name, effects_description)
        """
        rep = self.reputations.get(group, 0)
        
        if rep >= 90:
            return ("Legendary", "Maximum benefits and special opportunities")
        elif rep >= 75:
            return ("Honored", "Significant benefits and opportunities")
        elif rep >= 60:
            return ("Respected", "Notable benefits")
        elif rep >= 40:
            return ("Neutral", "No special effects")
        elif rep >= 25:
            return ("Distrusted", "Minor penalties")
        elif rep >= 10:
            return ("Disliked", "Significant penalties")
        else:
            return ("Hated", "Maximum penalties and hostile reactions")
    
    def get_reputation_effects(self, group):
        """Get the current effects of reputation with a group.
        
        Args:
            group: The social group.
            
        Returns:
            A dictionary of effects based on current reputation.
        """
        rep = self.reputations.get(group, 0)
        effects = {}
        
        if group == "nobility":
            effects["tax_rate"] = 1.0 - (rep * 0.003)  # Up to 30% tax reduction
            effects["invite_chance"] = rep * 0.01  # % chance of noble invitations
        
        elif group == "clergy":
            effects["blessing_power"] = 1.0 + (rep * 0.005)  # Up to 50% stronger
            effects["tithe_reduction"] = rep * 0.003  # Up to 30% tithe reduction
        
        elif group == "merchants":
            effects["buy_discount"] = rep * 0.002  # Up to 20% discount
            effects["sell_bonus"] = rep * 0.002    # Up to 20% better prices
        
        elif group == "peasants":
            effects["food_cost"] = 1.0 - (rep * 0.002)  # Up to 20% food discount
            effects["labor_cost"] = 1.0 - (rep * 0.002) # Up to 20% labor discount
        
        elif group == "military":
            effects["recruit_quality"] = 1.0 + (rep * 0.005)  # Up to 50% better
            effects["training_cost"] = 1.0 - (rep * 0.003)   # Up to 30% discount
        
        elif group == "criminals":
            effects["fence_rate"] = 0.5 + (rep * 0.003)     # Up to 80% value
            effects["contract_chance"] = rep * 0.01         # % chance of jobs
        
        return effects 