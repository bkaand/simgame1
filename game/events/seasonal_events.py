"""
Seasonal Events - Events that occur based on the season of the year
"""
import random

def get_season(month):
    """Get the season based on the month.
    
    Args:
        month: The month (1-12).
        
    Returns:
        The season name ("winter", "spring", "summer", or "autumn").
    """
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:  # 9, 10, 11
        return "autumn"

def get_seasonal_events():
    """Get the seasonal events.
    
    Returns:
        A dictionary of seasonal events.
    """
    seasonal_events = {
        # Winter events
        "winter_frost": {
            "title": "Winter Frost",
            "description": "A severe frost has affected the region.",
            "season": "winter",
            "probability": 0.3,
            "effects": {"health": -5},
            "role_specific": False
        },
        "winter_feast": {
            "title": "Winter Feast",
            "description": "You attend a winter feast celebrating the solstice.",
            "season": "winter",
            "probability": 0.4,
            "effects": {"health": 5, "wealth": -10},
            "role_specific": False
        },
        "winter_illness": {
            "title": "Winter Illness",
            "description": "The cold weather has brought illness to the region.",
            "season": "winter",
            "probability": 0.2,
            "effects": {"health": -10},
            "role_specific": False
        },
        
        # Spring events
        "spring_planting": {
            "title": "Spring Planting",
            "description": "The fields are being prepared for planting.",
            "season": "spring",
            "probability": 0.3,
            "effects": {},
            "role_specific": True,
            "roles": ["farmer"]
        },
        "spring_festival": {
            "title": "Spring Festival",
            "description": "A festival celebrating the return of spring is held.",
            "season": "spring",
            "probability": 0.4,
            "effects": {"wealth": -5, "health": 5},
            "role_specific": False
        },
        "spring_floods": {
            "title": "Spring Floods",
            "description": "Heavy rains have caused flooding in the region.",
            "season": "spring",
            "probability": 0.2,
            "effects": {"wealth": -20},
            "role_specific": True,
            "roles": ["farmer", "merchant"]
        },
        
        # Summer events
        "summer_heat": {
            "title": "Summer Heat",
            "description": "A heatwave has struck the region.",
            "season": "summer",
            "probability": 0.3,
            "effects": {"health": -5},
            "role_specific": False
        },
        "summer_fair": {
            "title": "Summer Fair",
            "description": "A fair is held in the town, attracting visitors from all around.",
            "season": "summer",
            "probability": 0.4,
            "effects": {"wealth": 15},
            "role_specific": True,
            "roles": ["merchant", "craftsman"]
        },
        "summer_tournament": {
            "title": "Summer Tournament",
            "description": "A tournament is held, attracting knights from all around.",
            "season": "summer",
            "probability": 0.3,
            "effects": {"wealth": 50},
            "role_specific": True,
            "roles": ["knight"]
        },
        
        # Autumn events
        "autumn_harvest": {
            "title": "Autumn Harvest",
            "description": "The harvest season has arrived.",
            "season": "autumn",
            "probability": 0.3,
            "effects": {"wealth": 30},
            "role_specific": True,
            "roles": ["farmer"]
        },
        "autumn_hunt": {
            "title": "Autumn Hunt",
            "description": "A grand hunt is organized in the nearby forest.",
            "season": "autumn",
            "probability": 0.3,
            "effects": {"health": 5},
            "role_specific": True,
            "roles": ["noble", "knight", "king"]
        },
        "autumn_taxes": {
            "title": "Autumn Taxes",
            "description": "It's time to pay the annual taxes.",
            "season": "autumn",
            "probability": 0.4,
            "effects": {"wealth": -50},
            "role_specific": False,
            "roles_exempt": ["king", "noble"]  # These roles don't pay taxes
        }
    }
    
    return seasonal_events 