"""
World - Manages the game world, including locations, resources, and NPCs
"""
import random

class World:
    """Represents the game world."""
    
    def __init__(self):
        """Initialize the game world."""
        self.kingdoms = []
        self.settlements = []
        self.resources = {}
        
        # Create initial world
        self._generate_world()
    
    def _generate_world(self):
        """Generate the initial world state."""
        # Create kingdoms
        kingdom_names = ["Westria", "Eastmark", "Northland", "Southvale", "Midreach"]
        for name in kingdom_names:
            self.kingdoms.append(Kingdom(name))
        
        # Create settlements
        settlement_types = ["city", "town", "village", "hamlet", "castle"]
        settlement_names = [
            "Oakvale", "Riverrun", "Highgarden", "Winterfell", "Sunspear",
            "Casterly", "Dragonstone", "Blackwater", "Ironhold", "Goldcrest",
            "Silvermine", "Copperfield", "Bronzehall", "Steelport", "Ironforge"
        ]
        
        for i in range(15):
            name = settlement_names[i]
            settlement_type = random.choice(settlement_types)
            kingdom = random.choice(self.kingdoms)
            
            settlement = Settlement(name, settlement_type, kingdom)
            self.settlements.append(settlement)
            kingdom.add_settlement(settlement)
        
        # Generate resources
        resource_types = ["food", "wood", "stone", "iron", "gold", "cloth"]
        for resource_type in resource_types:
            self.resources[resource_type] = random.randint(1000, 5000)
    
    def get_kingdom_by_name(self, name):
        """Get a kingdom by name.
        
        Args:
            name: The name of the kingdom.
            
        Returns:
            The kingdom with the specified name, or None if not found.
        """
        for kingdom in self.kingdoms:
            if kingdom.name.lower() == name.lower():
                return kingdom
        return None
    
    def get_settlement_by_name(self, name):
        """Get a settlement by name.
        
        Args:
            name: The name of the settlement.
            
        Returns:
            The settlement with the specified name, or None if not found.
        """
        for settlement in self.settlements:
            if settlement.name.lower() == name.lower():
                return settlement
        return None
    
    def update_for_new_year(self):
        """Update the world for a new year."""
        # Update kingdoms
        for kingdom in self.kingdoms:
            kingdom.update_for_new_year()
        
        # Update settlements
        for settlement in self.settlements:
            settlement.update_for_new_year()
        
        # Update resources
        for resource_type in self.resources:
            # Random fluctuation in resources
            change = random.randint(-500, 1000)
            self.resources[resource_type] = max(0, self.resources[resource_type] + change)

class Kingdom:
    """Represents a kingdom in the game world."""
    
    def __init__(self, name):
        """Initialize a new kingdom.
        
        Args:
            name: The name of the kingdom.
        """
        self.name = name
        self.ruler = None
        self.settlements = []
        self.wealth = random.randint(5000, 20000)
        self.military_strength = random.randint(1000, 5000)
        self.stability = random.randint(50, 100)
        self.relations = {}  # Other kingdoms -> relation value (-100 to 100)
    
    def add_settlement(self, settlement):
        """Add a settlement to the kingdom.
        
        Args:
            settlement: The settlement to add.
        """
        self.settlements.append(settlement)
    
    def update_for_new_year(self):
        """Update the kingdom for a new year."""
        # Random events and changes
        self.wealth += random.randint(-1000, 2000)
        self.military_strength += random.randint(-200, 500)
        self.stability += random.randint(-10, 5)
        
        # Ensure values stay within bounds
        self.wealth = max(0, self.wealth)
        self.military_strength = max(0, self.military_strength)
        self.stability = max(0, min(100, self.stability))
        
        # Update relations with other kingdoms
        for kingdom, relation in self.relations.items():
            change = random.randint(-5, 5)
            self.relations[kingdom] = max(-100, min(100, relation + change))

class Settlement:
    """Represents a settlement in the game world."""
    
    def __init__(self, name, settlement_type, kingdom):
        """Initialize a new settlement.
        
        Args:
            name: The name of the settlement.
            settlement_type: The type of settlement (e.g., 'city', 'town').
            kingdom: The kingdom the settlement belongs to.
        """
        self.name = name
        self.type = settlement_type
        self.kingdom = kingdom
        self.population = self._initial_population()
        self.wealth = self._initial_wealth()
        self.buildings = self._initial_buildings()
    
    def _initial_population(self):
        """Determine the initial population based on settlement type."""
        if self.type == "city":
            return random.randint(5000, 10000)
        elif self.type == "town":
            return random.randint(1000, 5000)
        elif self.type == "village":
            return random.randint(200, 1000)
        elif self.type == "hamlet":
            return random.randint(50, 200)
        elif self.type == "castle":
            return random.randint(100, 500)
        else:
            return random.randint(50, 100)
    
    def _initial_wealth(self):
        """Determine the initial wealth based on settlement type."""
        if self.type == "city":
            return random.randint(5000, 10000)
        elif self.type == "town":
            return random.randint(1000, 5000)
        elif self.type == "village":
            return random.randint(200, 1000)
        elif self.type == "hamlet":
            return random.randint(50, 200)
        elif self.type == "castle":
            return random.randint(1000, 3000)
        else:
            return random.randint(50, 100)
    
    def _initial_buildings(self):
        """Determine the initial buildings based on settlement type."""
        buildings = {}
        
        # Common buildings
        buildings["houses"] = self.population // 4  # Assume 4 people per house
        
        # Type-specific buildings
        if self.type == "city":
            buildings["market"] = random.randint(3, 5)
            buildings["church"] = random.randint(2, 4)
            buildings["tavern"] = random.randint(5, 10)
            buildings["blacksmith"] = random.randint(3, 6)
            buildings["barracks"] = random.randint(1, 3)
        elif self.type == "town":
            buildings["market"] = random.randint(1, 3)
            buildings["church"] = random.randint(1, 2)
            buildings["tavern"] = random.randint(2, 5)
            buildings["blacksmith"] = random.randint(1, 3)
            buildings["barracks"] = random.randint(0, 1)
        elif self.type == "village":
            buildings["market"] = random.randint(0, 1)
            buildings["church"] = 1
            buildings["tavern"] = random.randint(1, 2)
            buildings["blacksmith"] = 1
        elif self.type == "hamlet":
            buildings["church"] = random.randint(0, 1)
            buildings["tavern"] = 1
        elif self.type == "castle":
            buildings["barracks"] = random.randint(2, 4)
            buildings["church"] = 1
            buildings["blacksmith"] = 1
        
        return buildings
    
    def update_for_new_year(self):
        """Update the settlement for a new year."""
        # Population growth
        growth_rate = random.uniform(-0.05, 0.1)  # -5% to 10% growth
        self.population = int(self.population * (1 + growth_rate))
        
        # Wealth changes
        wealth_change = random.uniform(-0.1, 0.2)  # -10% to 20% change
        self.wealth = int(self.wealth * (1 + wealth_change))
        
        # Update buildings
        if random.random() < 0.2:  # 20% chance of new building
            building_types = ["houses", "market", "church", "tavern", "blacksmith", "barracks"]
            building_type = random.choice(building_types)
            
            if building_type in self.buildings:
                self.buildings[building_type] += 1
            else:
                self.buildings[building_type] = 1 