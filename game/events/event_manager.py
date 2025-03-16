"""
Event Manager - Manages random events in the game
"""
import random
from game.events.event import Event
from game.events.seasonal_events import get_seasonal_events, get_season

class EventManager:
    """Manages random events in the game."""
    
    def __init__(self, game_manager):
        """Initialize the event manager.
        
        Args:
            game_manager: The game manager.
        """
        self.game_manager = game_manager
        self.event_types = self._initialize_event_types()
        self.seasonal_events = get_seasonal_events()
        self.current_month = 1  # Start in January
    
    def _initialize_event_types(self):
        """Initialize the available event types.
        
        Returns:
            A dictionary of event types.
        """
        event_types = {
            # Personal events
            "illness": {
                "title": "Illness",
                "description": "You have fallen ill.",
                "probability": 0.1,
                "effects": {"health": -10},
                "role_specific": False
            },
            "recovery": {
                "title": "Recovery",
                "description": "You have recovered from your illness.",
                "probability": 0.05,
                "effects": {"health": 10},
                "role_specific": False
            },
            "windfall": {
                "title": "Windfall",
                "description": "You have come into some unexpected wealth.",
                "probability": 0.05,
                "effects": {"wealth": 100},
                "role_specific": False
            },
            "robbery": {
                "title": "Robbery",
                "description": "You have been robbed.",
                "probability": 0.05,
                "effects": {"wealth": -50},
                "role_specific": False
            },
            
            # Role-specific events
            "good_harvest": {
                "title": "Good Harvest",
                "description": "Your fields have yielded a bountiful harvest.",
                "probability": 0.2,
                "effects": {"wealth": 50},
                "role_specific": True,
                "roles": ["farmer"]
            },
            "bad_harvest": {
                "title": "Bad Harvest",
                "description": "Your crops have failed this year.",
                "probability": 0.1,
                "effects": {"wealth": -30},
                "role_specific": True,
                "roles": ["farmer"]
            },
            "successful_trade": {
                "title": "Successful Trade",
                "description": "Your trading ventures have been successful.",
                "probability": 0.2,
                "effects": {"wealth": 100},
                "role_specific": True,
                "roles": ["merchant"]
            },
            "trade_loss": {
                "title": "Trade Loss",
                "description": "Your trading ventures have suffered losses.",
                "probability": 0.1,
                "effects": {"wealth": -50},
                "role_specific": True,
                "roles": ["merchant"]
            },
            "tournament_victory": {
                "title": "Tournament Victory",
                "description": "You have won a tournament.",
                "probability": 0.1,
                "effects": {"wealth": 200, "skills.combat": 5},
                "role_specific": True,
                "roles": ["knight"]
            },
            "battle_injury": {
                "title": "Battle Injury",
                "description": "You have been injured in battle.",
                "probability": 0.1,
                "effects": {"health": -20},
                "role_specific": True,
                "roles": ["knight"]
            },
            "royal_favor": {
                "title": "Royal Favor",
                "description": "You have gained the favor of the monarch.",
                "probability": 0.1,
                "effects": {"wealth": 300},
                "role_specific": True,
                "roles": ["noble", "knight"]
            },
            "royal_disfavor": {
                "title": "Royal Disfavor",
                "description": "You have fallen out of favor with the monarch.",
                "probability": 0.05,
                "effects": {"wealth": -100},
                "role_specific": True,
                "roles": ["noble", "knight"]
            },
            "successful_commission": {
                "title": "Successful Commission",
                "description": "You have completed a valuable commission.",
                "probability": 0.2,
                "effects": {"wealth": 80, "skills.crafting": 5},
                "role_specific": True,
                "roles": ["craftsman"]
            },
            "workshop_fire": {
                "title": "Workshop Fire",
                "description": "Your workshop has been damaged by fire.",
                "probability": 0.05,
                "effects": {"wealth": -100},
                "role_specific": True,
                "roles": ["craftsman"]
            },
            "religious_revelation": {
                "title": "Religious Revelation",
                "description": "You have experienced a religious revelation.",
                "probability": 0.1,
                "effects": {"skills.wisdom": 10},
                "role_specific": True,
                "roles": ["priest"]
            },
            "church_donation": {
                "title": "Church Donation",
                "description": "Your church has received a generous donation.",
                "probability": 0.2,
                "effects": {"wealth": 150},
                "role_specific": True,
                "roles": ["priest"]
            },
            "rebellion": {
                "title": "Rebellion",
                "description": "Your subjects have rebelled against your rule.",
                "probability": 0.05,
                "effects": {"wealth": -500},
                "role_specific": True,
                "roles": ["king"]
            },
            "diplomatic_success": {
                "title": "Diplomatic Success",
                "description": "Your diplomatic efforts have been successful.",
                "probability": 0.1,
                "effects": {"wealth": 300, "skills.diplomacy": 5},
                "role_specific": True,
                "roles": ["king"]
            }
        }
        
        return event_types
    
    def get_events_for_year(self):
        """Get the events for the current year.
        
        Returns:
            A list of events for the current year.
        """
        events = []
        
        # Check for each event type
        for event_type, event_data in self.event_types.items():
            # Skip role-specific events that don't apply to the player
            if event_data["role_specific"] and self.game_manager.player.role not in event_data["roles"]:
                continue
            
            # Check if the event occurs
            if random.random() < event_data["probability"]:
                # Create the event
                event = Event(
                    event_data["title"],
                    event_data["description"],
                    event_data["effects"]
                )
                events.append(event)
        
        # Get the current season based on the month
        current_season = get_season(self.current_month)
        
        # Check for seasonal events
        for event_type, event_data in self.seasonal_events.items():
            # Skip events that don't match the current season
            if event_data["season"] != current_season:
                continue
            
            # Skip role-specific events that don't apply to the player
            if event_data["role_specific"] and self.game_manager.player.role not in event_data["roles"]:
                continue
                
            # Skip events that the player's role is exempt from
            if "roles_exempt" in event_data and self.game_manager.player.role in event_data["roles_exempt"]:
                continue
            
            # Check if the event occurs
            if random.random() < event_data["probability"]:
                # Create the event
                event = Event(
                    event_data["title"],
                    event_data["description"],
                    event_data["effects"]
                )
                events.append(event)
        
        # Limit to a reasonable number of events per year
        if len(events) > 3:
            events = random.sample(events, 3)
        
        # Advance to the next month (for the next call)
        self.current_month = (self.current_month % 12) + 1
        
        return events 