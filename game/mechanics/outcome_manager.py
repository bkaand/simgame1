"""
Outcome Manager - Handles variable outcomes and critical success/failure mechanics
"""
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class ActionOutcome:
    """Represents the outcome of an action."""
    success: bool
    is_critical: bool
    message: str
    rewards: Dict[str, int]
    reputation_changes: Dict[str, int]
    skill_gains: Dict[str, int]

class OutcomeManager:
    """Manages variable outcomes for character actions."""
    
    def __init__(self):
        """Initialize the outcome manager."""
        self.critical_threshold = 95  # Threshold for critical success/failure (95% or 5%)
        
        # Define base success chances for different action types
        self.base_success_rates = {
            "trade": 70,
            "combat": 60,
            "diplomacy": 65,
            "craft": 75,
            "study": 80,
            "farm": 70,
            "prayer": 90,
            "social": 75
        }
        
        # Initialize outcome templates
        self._initialize_outcome_templates()
    
    def _initialize_outcome_templates(self):
        """Initialize templates for different outcome types."""
        self.outcome_templates = {
            "trade": {
                "critical_success": {
                    "messages": [
                        "Your exceptional bargaining leads to an incredible deal!",
                        "You discover a rare and valuable item during the trade!",
                        "Your reputation as a shrewd trader spreads far and wide!"
                    ],
                    "reward_multiplier": 2.0,
                    "reputation_gain": {"merchants": 5, "nobility": 2}
                },
                "success": {
                    "messages": [
                        "The trade is completed successfully.",
                        "Both parties are satisfied with the deal.",
                        "You make a modest profit from the trade."
                    ],
                    "reward_multiplier": 1.0,
                    "reputation_gain": {"merchants": 1}
                },
                "failure": {
                    "messages": [
                        "The trade falls through.",
                        "You fail to reach an agreement.",
                        "The deal wasn't profitable enough."
                    ],
                    "reward_multiplier": 0.5,
                    "reputation_loss": {"merchants": -1}
                },
                "critical_failure": {
                    "messages": [
                        "Your goods are discovered to be defective!",
                        "You're accused of attempting to cheat in the trade!",
                        "You make a terrible miscalculation, resulting in significant losses!"
                    ],
                    "reward_multiplier": 0.0,
                    "reputation_loss": {"merchants": -5, "nobility": -2}
                }
            },
            "combat": {
                "critical_success": {
                    "messages": [
                        "Your exceptional combat prowess leads to a legendary victory!",
                        "Your perfect technique becomes the talk of the realm!",
                        "Songs will be sung of this glorious triumph!"
                    ],
                    "reward_multiplier": 2.0,
                    "reputation_gain": {"military": 5, "nobility": 3}
                },
                "success": {
                    "messages": [
                        "You emerge victorious from the battle.",
                        "Your combat training pays off.",
                        "You prove your worth in combat."
                    ],
                    "reward_multiplier": 1.0,
                    "reputation_gain": {"military": 1}
                },
                "failure": {
                    "messages": [
                        "You are defeated in combat.",
                        "Your opponent proves too skilled.",
                        "You fail to achieve victory."
                    ],
                    "reward_multiplier": 0.5,
                    "reputation_loss": {"military": -1}
                },
                "critical_failure": {
                    "messages": [
                        "You suffer a humiliating defeat!",
                        "Your poor performance becomes a cautionary tale!",
                        "Your reputation as a warrior takes a severe blow!"
                    ],
                    "reward_multiplier": 0.0,
                    "reputation_loss": {"military": -5, "nobility": -2}
                }
            },
            "diplomacy": {
                "critical_success": {
                    "messages": [
                        "Your masterful negotiation creates a lasting alliance!",
                        "Your diplomatic genius resolves a complex dispute!",
                        "Your words will be remembered as a triumph of diplomacy!"
                    ],
                    "reward_multiplier": 2.0,
                    "reputation_gain": {"nobility": 5, "clergy": 3}
                },
                "success": {
                    "messages": [
                        "Your diplomatic efforts bear fruit.",
                        "You successfully mediate the situation.",
                        "Your words help reach an agreement."
                    ],
                    "reward_multiplier": 1.0,
                    "reputation_gain": {"nobility": 2}
                },
                "failure": {
                    "messages": [
                        "Your diplomatic approach falls flat.",
                        "The negotiations break down.",
                        "You fail to reach an agreement."
                    ],
                    "reward_multiplier": 0.5,
                    "reputation_loss": {"nobility": -1}
                },
                "critical_failure": {
                    "messages": [
                        "Your diplomatic blunder causes an international incident!",
                        "Your words accidentally insult everyone involved!",
                        "Your failure at diplomacy will be remembered for years!"
                    ],
                    "reward_multiplier": 0.0,
                    "reputation_loss": {"nobility": -4, "clergy": -2}
                }
            },
            "craft": {
                "critical_success": {
                    "messages": [
                        "You create a masterpiece that will be admired for generations!",
                        "Your craftsmanship reaches new heights of excellence!",
                        "Your creation draws amazement from all who see it!"
                    ],
                    "reward_multiplier": 2.5,
                    "reputation_gain": {"merchants": 4, "peasants": 3}
                },
                "success": {
                    "messages": [
                        "Your crafting work is completed successfully.",
                        "The finished product meets expectations.",
                        "Your creation is well-made."
                    ],
                    "reward_multiplier": 1.0,
                    "reputation_gain": {"merchants": 1}
                },
                "failure": {
                    "messages": [
                        "The crafting attempt fails.",
                        "The materials are wasted.",
                        "The finished product is flawed."
                    ],
                    "reward_multiplier": 0.3,
                    "reputation_loss": {"merchants": -1}
                },
                "critical_failure": {
                    "messages": [
                        "Your workshop catches fire during the crafting attempt!",
                        "You completely destroy valuable materials!",
                        "Your spectacular failure becomes local gossip!"
                    ],
                    "reward_multiplier": 0.0,
                    "reputation_loss": {"merchants": -3, "peasants": -2}
                }
            },
            "study": {
                "critical_success": {
                    "messages": [
                        "You make a breakthrough in your studies!",
                        "Your dedication leads to exceptional understanding!",
                        "You master complex concepts with remarkable ease!"
                    ],
                    "reward_multiplier": 2.0,
                    "reputation_gain": {"clergy": 3, "nobility": 2}
                },
                "success": {
                    "messages": [
                        "Your studies progress well.",
                        "You learn new concepts successfully.",
                        "Your understanding grows steadily."
                    ],
                    "reward_multiplier": 1.0,
                    "reputation_gain": {"clergy": 1}
                },
                "failure": {
                    "messages": [
                        "You struggle to grasp the concepts.",
                        "Your studies yield little progress.",
                        "The material proves too challenging."
                    ],
                    "reward_multiplier": 0.5,
                    "reputation_loss": {}
                },
                "critical_failure": {
                    "messages": [
                        "You completely misunderstand fundamental concepts!",
                        "Your confusion leads to embarrassing mistakes!",
                        "Your studies leave you more confused than before!"
                    ],
                    "reward_multiplier": 0.0,
                    "reputation_loss": {"clergy": -2}
                }
            },
            "farm": {
                "critical_success": {
                    "messages": [
                        "Your crops yield an extraordinary harvest!",
                        "Your innovative farming methods produce amazing results!",
                        "Your farm becomes a model for the entire region!"
                    ],
                    "reward_multiplier": 2.0,
                    "reputation_gain": {"peasants": 5, "merchants": 2}
                },
                "success": {
                    "messages": [
                        "Your crops grow well.",
                        "The harvest is satisfactory.",
                        "Your farming efforts pay off."
                    ],
                    "reward_multiplier": 1.0,
                    "reputation_gain": {"peasants": 1}
                },
                "failure": {
                    "messages": [
                        "The crops yield poorly.",
                        "Pests damage your harvest.",
                        "The weather affects your crops negatively."
                    ],
                    "reward_multiplier": 0.4,
                    "reputation_loss": {"peasants": -1}
                },
                "critical_failure": {
                    "messages": [
                        "A devastating blight destroys your entire crop!",
                        "Severe weather ruins your farm!",
                        "Your farming mistakes lead to total crop failure!"
                    ],
                    "reward_multiplier": 0.0,
                    "reputation_loss": {"peasants": -3, "merchants": -2}
                }
            },
            "prayer": {
                "critical_success": {
                    "messages": [
                        "Your deep devotion brings divine inspiration!",
                        "Your prayers move the hearts of all present!",
                        "Your spiritual leadership inspires miraculous events!"
                    ],
                    "reward_multiplier": 2.0,
                    "reputation_gain": {"clergy": 5, "peasants": 3}
                },
                "success": {
                    "messages": [
                        "Your prayers are well-received.",
                        "Your devotion strengthens the faithful.",
                        "Your spiritual guidance helps others."
                    ],
                    "reward_multiplier": 1.0,
                    "reputation_gain": {"clergy": 1}
                },
                "failure": {
                    "messages": [
                        "Your prayers seem to go unanswered.",
                        "Your spiritual focus wavers.",
                        "Your message fails to resonate."
                    ],
                    "reward_multiplier": 0.5,
                    "reputation_loss": {}
                },
                "critical_failure": {
                    "messages": [
                        "You accidentally quote heretical texts!",
                        "Your spiritual guidance leads others astray!",
                        "Your religious mistakes cause a local scandal!"
                    ],
                    "reward_multiplier": 0.0,
                    "reputation_loss": {"clergy": -4, "nobility": -2}
                }
            },
            "social": {
                "critical_success": {
                    "messages": [
                        "Your charm and wit make you the star of the gathering!",
                        "You forge valuable new friendships and alliances!",
                        "Your social grace impresses everyone present!"
                    ],
                    "reward_multiplier": 2.0,
                    "reputation_gain": {"nobility": 3, "merchants": 2}
                },
                "success": {
                    "messages": [
                        "You make a good impression.",
                        "Your social interactions go well.",
                        "You strengthen your relationships."
                    ],
                    "reward_multiplier": 1.0,
                    "reputation_gain": {"nobility": 1}
                },
                "failure": {
                    "messages": [
                        "Your social attempts fall flat.",
                        "You struggle to connect with others.",
                        "The gathering proves awkward."
                    ],
                    "reward_multiplier": 0.5,
                    "reputation_loss": {"nobility": -1}
                },
                "critical_failure": {
                    "messages": [
                        "You cause a major social scandal!",
                        "Your behavior shocks and offends everyone!",
                        "Your social blunder becomes notorious gossip!"
                    ],
                    "reward_multiplier": 0.0,
                    "reputation_loss": {"nobility": -4, "merchants": -2}
                }
            }
        }
    
    def calculate_success_chance(self, character, action_type: str) -> int:
        """Calculate the success chance for an action based on character attributes and skills.
        
        Args:
            character: The character performing the action
            action_type: The type of action being performed
            
        Returns:
            The calculated success chance (0-100)
        """
        base_chance = self.base_success_rates.get(action_type, 50)
        
        # Add relevant skill bonus
        skill_bonus = 0
        if action_type in character.skills:
            skill_bonus = character.skills[action_type] // 10  # Every 10 points gives +1%
        
        # Add relevant attribute bonus
        attribute_bonus = 0
        if action_type == "trade":
            attribute_bonus = (character.attributes.get("charisma", 0) + 
                            character.attributes.get("intelligence", 0)) // 4
        elif action_type == "combat":
            attribute_bonus = (character.attributes.get("strength", 0) + 
                            character.attributes.get("dexterity", 0)) // 4
        
        # Calculate final chance
        success_chance = base_chance + skill_bonus + attribute_bonus
        
        # Ensure chance stays within 5-95 range (leaving room for critical outcomes)
        return max(5, min(95, success_chance))
    
    def get_outcome(self, character, action_type: str, difficulty_modifier: int = 0) -> ActionOutcome:
        """Determine the outcome of an action.
        
        Args:
            character: The character performing the action
            action_type: The type of action being performed
            difficulty_modifier: Modifier to success chance (-20 to +20)
            
        Returns:
            An ActionOutcome object containing the result
        """
        # Calculate success chance
        success_chance = self.calculate_success_chance(character, action_type)
        success_chance += difficulty_modifier
        
        # Roll for outcome
        roll = random.randint(1, 100)
        
        # Determine outcome type
        if roll <= 5:  # Critical failure
            success = False
            is_critical = True
            outcome_type = "critical_failure"
        elif roll >= 95:  # Critical success
            success = True
            is_critical = True
            outcome_type = "critical_success"
        elif roll <= success_chance:  # Normal success
            success = True
            is_critical = False
            outcome_type = "success"
        else:  # Normal failure
            success = False
            is_critical = False
            outcome_type = "failure"
        
        # Get outcome template
        template = self.outcome_templates.get(action_type, {}).get(outcome_type, {})
        
        # Generate outcome
        message = random.choice(template.get("messages", ["The action is completed."]))
        reward_multiplier = template.get("reward_multiplier", 1.0)
        reputation_changes = template.get("reputation_gain", {}) if success else template.get("reputation_loss", {})
        
        # Calculate skill gains (more on critical success, less on failure)
        skill_gains = {}
        if action_type in character.skills:
            base_gain = 1
            if is_critical and success:
                base_gain = 3
            elif success:
                base_gain = 2
            elif not success:
                base_gain = 1
            skill_gains[action_type] = base_gain
        
        return ActionOutcome(
            success=success,
            is_critical=is_critical,
            message=message,
            rewards={"gold": int(10 * reward_multiplier)},  # Example reward
            reputation_changes=reputation_changes,
            skill_gains=skill_gains
        ) 