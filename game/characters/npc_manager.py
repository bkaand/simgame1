"""
NPC Manager - Manages persistent NPCs in the game world
"""
import random
from game.characters.character import Character, Relationship

class NPCManager:
    """Manages persistent NPCs in the game world."""
    
    def __init__(self, game_manager):
        """Initialize the NPC manager.
        
        Args:
            game_manager: The game manager.
        """
        self.game_manager = game_manager
        self.npcs = {}  # Maps NPC ID to NPC character
        self.npc_locations = {}  # Maps NPC ID to location
        self.npc_relationships = {}  # Maps (NPC ID, NPC ID) to relationship level
        self.next_npc_id = 1
        
        # Generate initial NPCs
        self._generate_initial_npcs()
    
    def _generate_initial_npcs(self):
        """Generate initial NPCs for the game world."""
        # Generate a mix of NPCs for each role
        roles = ["noble", "knight", "merchant", "farmer", "craftsman", "priest"]
        
        for role in roles:
            # Generate 3-5 NPCs for each role
            num_npcs = random.randint(3, 5)
            for _ in range(num_npcs):
                self.generate_npc(role=role)
    
    def generate_npc(self, name=None, gender=None, role=None, age=None, location=None):
        """Generate a new NPC.
        
        Args:
            name: The NPC's name (optional, will be generated if None).
            gender: The NPC's gender (optional, will be randomly chosen if None).
            role: The NPC's role (optional, will be randomly chosen if None).
            age: The NPC's age (optional, will be randomly chosen if None).
            location: The NPC's location (optional).
            
        Returns:
            The generated NPC.
        """
        # Generate gender if not provided
        if gender is None:
            gender = random.choice(["male", "female"])
        
        # Generate name if not provided
        if name is None:
            if gender == "male":
                name = random.choice([
                    "John", "William", "Robert", "Thomas", "Henry", "Edward", "Richard",
                    "James", "Walter", "Hugh", "Geoffrey", "Simon", "Peter", "Nicholas",
                    "Roger", "Adam", "Stephen", "Philip", "Gilbert", "Martin"
                ])
            else:
                name = random.choice([
                    "Mary", "Elizabeth", "Catherine", "Anne", "Margaret", "Eleanor", "Alice",
                    "Matilda", "Joan", "Isabella", "Agnes", "Cecily", "Emma", "Beatrice",
                    "Edith", "Maud", "Juliana", "Rose", "Lucy", "Avice"
                ])
        
        # Generate role if not provided
        if role is None:
            role = random.choice(["noble", "knight", "merchant", "farmer", "craftsman", "priest"])
        
        # Generate age if not provided
        if age is None:
            # Age range depends on role
            if role in ["noble", "knight"]:
                age = random.randint(20, 60)
            elif role == "priest":
                age = random.randint(25, 70)
            else:
                age = random.randint(16, 70)
        
        # Calculate birth year
        birth_year = self.game_manager.game_year - age
        
        # Create the NPC
        npc = Character(name, gender, role, birth_year)
        npc.age = age
        
        # Add some randomization to attributes and skills
        for attr in npc.attributes:
            # Adjust attributes based on role
            base_value = npc.attributes[attr]
            if role == "noble" and attr in ["charisma", "intelligence"]:
                base_value += random.randint(5, 15)
            elif role == "knight" and attr in ["strength", "endurance"]:
                base_value += random.randint(5, 15)
            elif role == "merchant" and attr in ["charisma", "cunning"]:
                base_value += random.randint(5, 15)
            elif role == "farmer" and attr in ["strength", "endurance"]:
                base_value += random.randint(5, 15)
            elif role == "craftsman" and attr in ["dexterity", "intelligence"]:
                base_value += random.randint(5, 15)
            elif role == "priest" and attr in ["intelligence", "wisdom"]:
                base_value += random.randint(5, 15)
            
            # Add some randomness
            base_value += random.randint(-10, 10)
            
            # Ensure within bounds
            npc.attributes[attr] = max(1, min(100, base_value))
        
        # Assign an ID to the NPC
        npc_id = self.next_npc_id
        self.next_npc_id += 1
        
        # Store the NPC
        self.npcs[npc_id] = npc
        
        # Store the NPC's location
        if location is None:
            # Default to the player's location
            location = "town"  # Simple default
        
        self.npc_locations[npc_id] = location
        
        # Add some personality traits
        npc.personality_traits = []
        num_traits = random.randint(1, 3)
        all_traits = [
            "Kind", "Cruel", "Ambitious", "Lazy", "Honest", "Deceitful", "Brave", "Cowardly",
            "Generous", "Greedy", "Patient", "Impatient", "Humble", "Proud", "Loyal", "Treacherous",
            "Pious", "Cynical", "Lustful", "Chaste", "Temperate", "Gluttonous", "Trusting", "Suspicious"
        ]
        npc.personality_traits = random.sample(all_traits, num_traits)
        
        # Add some background details
        backgrounds = {
            "noble": [
                "From an ancient noble family",
                "Recently elevated to nobility",
                "From a family known for military service",
                "From a family known for scholarship",
                "From a family with a scandalous past"
            ],
            "knight": [
                "Knighted for valor in battle",
                "From a family of knights",
                "Rose from common origins",
                "Served as a squire to a famous knight",
                "Won fame in tournaments"
            ],
            "merchant": [
                "Inherited a trading business",
                "Started as a peddler",
                "Specializes in exotic goods",
                "Has trading connections abroad",
                "Known for fair dealing"
            ],
            "farmer": [
                "Owns a small plot of land",
                "Works on a noble's estate",
                "Known for quality produce",
                "Struggling with recent harvests",
                "Experimenting with new crops"
            ],
            "craftsman": [
                "Master of their craft",
                "Apprenticed under a famous artisan",
                "Creates goods for nobility",
                "Innovator in their field",
                "Struggling to compete with imports"
            ],
            "priest": [
                "From a noble family",
                "Rose from humble origins",
                "Known for scholarly work",
                "Known for charitable works",
                "Has political ambitions"
            ]
        }
        
        npc.background = random.choice(backgrounds.get(role, ["Unknown background"]))
        
        # Add marital status
        if age >= 16:
            marital_status_chances = {
                "single": 0.3,
                "married": 0.6,
                "widowed": 0.1
            }
            
            # Adjust based on age
            if age < 20:
                marital_status_chances["single"] = 0.8
                marital_status_chances["married"] = 0.2
                marital_status_chances["widowed"] = 0.0
            elif age > 50:
                marital_status_chances["single"] = 0.2
                marital_status_chances["married"] = 0.5
                marital_status_chances["widowed"] = 0.3
            
            # Adjust based on role
            if role == "priest":
                marital_status_chances["single"] = 1.0
                marital_status_chances["married"] = 0.0
                marital_status_chances["widowed"] = 0.0
            
            # Determine marital status
            rand = random.random()
            if rand < marital_status_chances["single"]:
                npc.marital_status = "single"
            elif rand < marital_status_chances["single"] + marital_status_chances["married"]:
                npc.marital_status = "married"
            else:
                npc.marital_status = "widowed"
        else:
            npc.marital_status = "single"
        
        return npc
    
    def get_npc(self, npc_id):
        """Get an NPC by ID.
        
        Args:
            npc_id: The ID of the NPC.
            
        Returns:
            The NPC, or None if not found.
        """
        return self.npcs.get(npc_id)
    
    def get_npcs_by_role(self, role):
        """Get all NPCs with a specific role.
        
        Args:
            role: The role to filter by.
            
        Returns:
            A list of (npc_id, npc) tuples for NPCs with the specified role.
        """
        return [(npc_id, npc) for npc_id, npc in self.npcs.items() if npc.role == role]
    
    def get_npcs_by_location(self, location):
        """Get all NPCs at a specific location.
        
        Args:
            location: The location to filter by.
            
        Returns:
            A list of (npc_id, npc) tuples for NPCs at the specified location.
        """
        return [(npc_id, self.npcs[npc_id]) for npc_id in self.npc_locations 
                if self.npc_locations[npc_id] == location and npc_id in self.npcs]
    
    def get_random_npcs(self, count=3, exclude_ids=None):
        """Get a random selection of NPCs.
        
        Args:
            count: The number of NPCs to return.
            exclude_ids: A list of NPC IDs to exclude.
            
        Returns:
            A list of (npc_id, npc) tuples.
        """
        exclude_ids = exclude_ids or []
        eligible_npcs = [(npc_id, npc) for npc_id, npc in self.npcs.items() if npc_id not in exclude_ids]
        
        if len(eligible_npcs) <= count:
            return eligible_npcs
        
        return random.sample(eligible_npcs, count)
    
    def get_suitable_npcs_for_arc(self, arc_id, count=1, role=None, gender=None, age_min=None, age_max=None, marital_status=None):
        """Get NPCs suitable for a specific story arc.
        
        Args:
            arc_id: The ID of the story arc.
            count: The number of NPCs to return.
            role: Filter by role (optional).
            gender: Filter by gender (optional).
            age_min: Filter by minimum age (optional).
            age_max: Filter by maximum age (optional).
            marital_status: Filter by marital status (optional).
            
        Returns:
            A list of (npc_id, npc) tuples.
        """
        # Filter NPCs based on criteria
        eligible_npcs = []
        
        for npc_id, npc in self.npcs.items():
            # Skip NPCs already involved in this arc
            if arc_id in self.game_manager.story_arc_manager.arc_npcs and npc_id in self.game_manager.story_arc_manager.arc_npcs[arc_id]:
                continue
            
            # Apply filters
            if role is not None and npc.role != role:
                continue
            
            if gender is not None and npc.gender != gender:
                continue
            
            if age_min is not None and npc.age < age_min:
                continue
            
            if age_max is not None and npc.age > age_max:
                continue
            
            if marital_status is not None and getattr(npc, "marital_status", "single") != marital_status:
                continue
            
            eligible_npcs.append((npc_id, npc))
        
        # If we don't have enough eligible NPCs, generate some new ones
        if len(eligible_npcs) < count:
            for _ in range(count - len(eligible_npcs)):
                new_npc = self.generate_npc(role=role, gender=gender, age=random.randint(age_min or 16, age_max or 70))
                if marital_status is not None:
                    new_npc.marital_status = marital_status
                npc_id = self.next_npc_id - 1  # The ID assigned in generate_npc
                eligible_npcs.append((npc_id, new_npc))
        
        # Return a random selection
        if len(eligible_npcs) <= count:
            return eligible_npcs
        
        return random.sample(eligible_npcs, count)
    
    def update_for_new_year(self):
        """Update NPCs for a new year."""
        # Age all NPCs
        for npc_id, npc in list(self.npcs.items()):
            npc.age += 1
            
            # Random chance for life events
            if random.random() < 0.1:  # 10% chance per year
                event_type = random.choice(["marriage", "death", "relocation", "career"])
                
                if event_type == "marriage" and getattr(npc, "marital_status", "single") == "single" and npc.age >= 16:
                    npc.marital_status = "married"
                
                elif event_type == "death":
                    # Chance of death increases with age
                    death_chance = 0.01  # Base 1% chance
                    if npc.age > 60:
                        death_chance += (npc.age - 60) * 0.01  # +1% per year over 60
                    
                    if random.random() < death_chance:
                        # NPC dies
                        del self.npcs[npc_id]
                        if npc_id in self.npc_locations:
                            del self.npc_locations[npc_id]
                        continue
                
                elif event_type == "relocation":
                    # NPC moves to a new location
                    locations = ["town", "village", "castle", "monastery", "market"]
                    current_location = self.npc_locations.get(npc_id, "town")
                    new_location = random.choice([loc for loc in locations if loc != current_location])
                    self.npc_locations[npc_id] = new_location
                
                elif event_type == "career" and random.random() < 0.3:  # 30% chance of career event
                    # Possible career changes based on role
                    if npc.role == "farmer" and random.random() < 0.2:
                        npc.role = "merchant"  # Farmer becomes merchant
                    elif npc.role == "craftsman" and random.random() < 0.1:
                        npc.role = "merchant"  # Craftsman becomes merchant
                    elif npc.role == "merchant" and random.random() < 0.05:
                        npc.role = "noble"  # Very rare: merchant becomes noble
        
        # Generate new NPCs to replace those who died
        current_count = len(self.npcs)
        target_count = 30  # Maintain around 30 NPCs
        
        if current_count < target_count:
            for _ in range(target_count - current_count):
                self.generate_npc()
    
    def get_npc_description(self, npc_id):
        """Get a description of an NPC.
        
        Args:
            npc_id: The ID of the NPC.
            
        Returns:
            A string description of the NPC.
        """
        npc = self.npcs.get(npc_id)
        if not npc:
            return "Unknown NPC"
        
        marital_status = getattr(npc, "marital_status", "single")
        traits = getattr(npc, "personality_traits", [])
        background = getattr(npc, "background", "Unknown background")
        
        description = f"{npc.name}, {npc.age} years old, {npc.role.capitalize()}"
        
        if marital_status != "single":
            description += f", {marital_status}"
        
        if traits:
            description += f"\nTraits: {', '.join(traits)}"
        
        description += f"\nBackground: {background}"
        
        return description 