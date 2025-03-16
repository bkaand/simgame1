"""
Character - Base class for all character types in the game
"""
import random
from datetime import datetime
from game.characters.reputation import ReputationManager
from game.mechanics.outcome_manager import OutcomeManager
from game.mechanics.historical_constraints import HistoricalConstraints

class Character:
    """Base class for all characters in the game."""
    
    def __init__(self, name, gender, role, birth_year=None):
        """Initialize a new character.
        
        Args:
            name: The character's name.
            gender: The character's gender ('male' or 'female').
            role: The character's role (e.g., 'king', 'farmer').
            birth_year: The year the character was born.
        """
        self.name = name
        self.gender = gender.lower()
        
        # Initialize historical constraints
        self.historical_constraints = HistoricalConstraints()
        
        # Validate role based on gender
        allowed_roles = self.historical_constraints.get_allowed_roles(gender)
        if role not in allowed_roles:
            # Default to an allowed role if the chosen one isn't permitted
            role = allowed_roles[0]
        
        self.role = role.lower()
        self.birth_year = birth_year
        self.age = 0  # Will be calculated based on game year
        self.health = 100
        self.wealth = 0  # Will be set by specific role classes
        self.spouse = None
        self.children = []
        self.relationships = {}  # Person -> Relationship
        self.traits = []  # List of character traits
        self.happiness = 50  # Base happiness level (0-100)
        
        # Initialize reputation system
        self.reputation = ReputationManager()
        
        # Initialize outcome manager
        self.outcome_manager = OutcomeManager()
        
        # Base attributes (1-100)
        self.attributes = {
            'strength': random.randint(20, 80),
            'intelligence': random.randint(20, 80),
            'charisma': random.randint(20, 80),
            'wisdom': random.randint(20, 80),
            'dexterity': random.randint(20, 80)
        }
        
        # Base skills (1-100)
        self.skills = {
            'combat': random.randint(10, 50),
            'diplomacy': random.randint(10, 50),
            'stewardship': random.randint(10, 50),
            'trade': random.randint(10, 50),
            'farming': random.randint(10, 50),
            'crafting': random.randint(10, 50),
            'medicine': random.randint(10, 50)
        }
        
        # Adjust skills based on role
        self._adjust_skills_for_role()
        
        # Adjust starting reputation based on role
        self._adjust_starting_reputation()
        
        # Initialize random traits
        self._initialize_traits()
    
    def _adjust_skills_for_role(self):
        """Adjust skills based on character role."""
        if self.role == "merchant":
            self.skills["trade"] += 20
            self.skills["diplomacy"] += 10
        elif self.role == "knight":
            self.skills["combat"] += 20
            self.skills["diplomacy"] += 5
        elif self.role == "craftsman":
            self.skills["crafting"] += 20
            self.skills["trade"] += 10
        elif self.role == "farmer":
            self.skills["farming"] += 20
            self.skills["crafting"] += 5
        elif self.role == "priest":
            self.skills["diplomacy"] += 15
            self.skills["medicine"] += 10
        elif self.role == "noble":
            self.skills["diplomacy"] += 15
            self.skills["stewardship"] += 10
    
    def _adjust_starting_reputation(self):
        """Adjust starting reputation based on character role."""
        if self.role == "noble" or self.role == "king":
            self.reputation.adjust_reputation("nobility", 20)
            self.reputation.adjust_reputation("peasants", -10)
        
        elif self.role == "priest":
            self.reputation.adjust_reputation("clergy", 20)
            self.reputation.adjust_reputation("criminals", -10)
        
        elif self.role == "merchant":
            self.reputation.adjust_reputation("merchants", 20)
        
        elif self.role == "knight":
            self.reputation.adjust_reputation("military", 20)
            self.reputation.adjust_reputation("nobility", 10)
        
        elif self.role == "farmer":
            self.reputation.adjust_reputation("peasants", 20)
        
        elif self.role == "craftsman":
            self.reputation.adjust_reputation("merchants", 10)
            self.reputation.adjust_reputation("peasants", 10)
    
    def _initialize_traits(self):
        """Initialize random character traits."""
        possible_traits = {
            "ambitious": 0.1,  # 10% chance
            "scholarly": 0.1,
            "charismatic": 0.1,
            "robust": 0.1
        }
        
        for trait, chance in possible_traits.items():
            if random.random() < chance:
                self.traits.append(trait)
    
    def is_alive(self):
        """Check if the character is alive.
        
        Returns:
            True if the character is alive, False otherwise.
        """
        return self.health > 0
    
    def update_for_new_year(self):
        """Update character stats for a new year."""
        # Base health decline with age
        if self.age > 40:
            self.health -= random.randint(0, 2)
        
        # Ensure health stays within bounds
        self.health = max(0, min(100, self.health))
    
    def get_actions(self):
        """Get the list of actions available to this character.
        
        Returns:
            A list of action names.
        """
        # Base actions available to all characters
        actions = ["Find Spouse", "Socialize", "Family Activities"]
        
        # Add role-specific actions
        if self.role == "merchant":
            actions.extend(["Trade", "Diplomacy"])
        elif self.role == "knight":
            actions.extend(["Combat", "Train Skills"])
        elif self.role == "craftsman":
            actions.extend(["Craft", "Trade"])
        elif self.role == "farmer":
            actions.extend(["Farm", "Trade"])
        elif self.role == "priest":
            actions.extend(["Prayer", "Study"])
        elif self.role == "noble":
            actions.extend(["Diplomacy", "Study"])
        
        # Add health-related actions
        if self.health < 80:
            actions.append("Rest and Recover")
        
        # Add travel action
        actions.append("Travel")
        
        return actions
    
    def perform_action(self, action_type: str, difficulty_modifier: int = 0):
        """Perform an action and get its outcome.
        
        Args:
            action_type: The type of action to perform
            difficulty_modifier: Optional modifier to success chance
            
        Returns:
            The outcome message and any gained rewards, or (None, None) if action is not permitted
        """
        # Check historical constraints
        allowed, reason = self.historical_constraints.can_perform_action(self, action_type)
        if not allowed:
            return reason, None
        
        # Get action outcome
        outcome = self.outcome_manager.get_outcome(self, action_type, difficulty_modifier)
        
        # Apply outcome effects
        self.wealth += outcome.rewards.get("gold", 0)
        
        # Apply reputation changes
        for group, change in outcome.reputation_changes.items():
            self.reputation.adjust_reputation(group, change)
        
        # Apply skill gains
        for skill, gain in outcome.skill_gains.items():
            self.skills[skill] = min(100, self.skills.get(skill, 0) + gain)
        
        # Check for social mobility opportunity
        potential_class, chance = self.historical_constraints.calculate_social_mobility(self)
        if random.randint(1, 100) <= chance:
            # Character has opportunity to move up in society
            self.last_action_result = f"{outcome.message}\n\nYour success has opened up opportunities for social advancement!"
            # The actual class change would be handled by the game manager
        else:
            self.last_action_result = outcome.message
        
        return outcome.message, outcome.rewards
    
    def _trade(self):
        """Conduct a trade."""
        message, rewards = self.perform_action("trade")
        self.last_action_result = message
        return message
    
    def _combat(self):
        """Engage in combat."""
        message, rewards = self.perform_action("combat")
        self.last_action_result = message
        return message
    
    def _find_spouse(self, game_manager):
        """Try to find a spouse.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        if self.spouse:
            interface.display_message(f"You are already married to {self.spouse.name}.")
            interface.get_input("Press Enter to continue...")
            return
        
        if self.age < 16:
            interface.display_message("You are too young to marry.")
            interface.get_input("Press Enter to continue...")
            return
        
        # Get potential spouses from NPC manager
        potential_spouses = []
        if game_manager.npc_manager:
            potential_spouses = game_manager.npc_manager.get_suitable_npcs_for_arc(
                "marriage",
                count=3,
                gender="female" if self.gender == "male" else "male",
                age_min=16,
                age_max=min(40, self.age + 10),
                marital_status="single"
            )
        
        # If not enough NPCs, generate some random ones
        while len(potential_spouses) < 3:
            age = random.randint(16, min(40, self.age + 10))
            birth_year = game_manager.game_year - age
            gender = "female" if self.gender == "male" else "male"
            
            # Generate a random name based on gender
            if gender == "male":
                name = random.choice(["John", "William", "Robert", "Thomas", "Henry"])
            else:
                name = random.choice(["Mary", "Elizabeth", "Catherine", "Anne", "Margaret"])
            
            # Create a basic character with an appropriate role for their gender
            allowed_roles = self.historical_constraints.get_allowed_roles(gender)
            role = random.choice(allowed_roles)
            spouse = Character(name, gender, role, birth_year)
            spouse.age = age
            
            potential_spouses.append((-1, spouse))
        
        # Filter potential spouses based on historical constraints
        valid_spouses = []
        for npc_id, spouse in potential_spouses:
            allowed, _ = self.historical_constraints.can_marry(self, spouse)
            if allowed:
                valid_spouses.append((npc_id, spouse))
        
        if not valid_spouses:
            interface.display_message("No suitable marriage prospects are available for someone of your social standing.")
            interface.get_input("Press Enter to continue...")
            return
        
        # Display valid potential spouses
        spouse_descriptions = []
        for npc_id, spouse in valid_spouses:
            social_class = self.historical_constraints._determine_social_class(spouse)
            if npc_id != -1 and game_manager.npc_manager:
                description = game_manager.npc_manager.get_npc_description(npc_id)
                spouse_descriptions.append(f"{description} ({social_class.capitalize()})")
            else:
                traits_str = f", Traits: {', '.join(spouse.traits)}" if spouse.traits else ""
                spouse_descriptions.append(f"{spouse.name}, {spouse.age} years old, {spouse.role.capitalize()} ({social_class.capitalize()}){traits_str}")
        
        spouse_descriptions.append("None of these")
        
        choice = interface.display_menu("Choose a spouse:", spouse_descriptions)
        
        if choice < len(valid_spouses):
            # Marry the chosen spouse
            _, chosen_spouse = valid_spouses[choice]
            self.spouse = chosen_spouse
            interface.display_message(f"You are now married to {self.spouse.name}!")
            
            # Update achievements
            game_manager.achievements["married"] = True
            
            # Happiness boost from marriage
            happiness_gain = random.randint(10, 20)
            self.happiness = min(100, self.happiness + happiness_gain)
            
            interface.display_message(f"Your happiness increases by {happiness_gain} points.")
        else:
            interface.display_message("You decided not to marry anyone at this time.")
        
        interface.get_input("Press Enter to continue...")
    
    def _socialize(self, game_manager):
        """Socialize with others.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        # Get NPCs from the NPC manager
        if game_manager.npc_manager:
            # Get NPCs at the player's location (default to "town")
            location_npcs = game_manager.npc_manager.get_npcs_by_location("town")
            
            # If not enough NPCs at this location, get some random ones
            if len(location_npcs) < 3:
                additional_npcs = game_manager.npc_manager.get_random_npcs(3 - len(location_npcs))
                all_npcs = location_npcs + additional_npcs
            else:
                # Get a random selection if there are many NPCs at this location
                all_npcs = random.sample(location_npcs, min(3, len(location_npcs)))
            
            # Check if any NPCs are involved in active story arcs with the player
            arc_npcs = []
            for arc in game_manager.story_arc_manager.active_arcs:
                if arc.arc_id in game_manager.story_arc_manager.arc_npcs:
                    arc_npcs.extend(game_manager.story_arc_manager.arc_npcs[arc.arc_id])
            
            # Prioritize NPCs involved in story arcs
            story_arc_npcs = [(npc_id, npc) for npc_id, npc in all_npcs if npc_id in arc_npcs]
            other_npcs = [(npc_id, npc) for npc_id, npc in all_npcs if npc_id not in arc_npcs]
            
            # Combine the lists, prioritizing story arc NPCs
            npcs_to_show = story_arc_npcs + other_npcs
            if len(npcs_to_show) > 3:
                npcs_to_show = npcs_to_show[:3]
        else:
            # Fallback to generating random NPCs if NPC manager is not available
            npcs_to_show = []
            for _ in range(3):
                age = random.randint(16, 70)
                birth_year = game_manager.game_year - age
                gender = random.choice(["male", "female"])
                
                # Generate a random name based on gender
                if gender == "male":
                    name = random.choice(["John", "William", "Robert", "Thomas", "Henry", "Edward"])
                else:
                    name = random.choice(["Mary", "Elizabeth", "Catherine", "Anne", "Margaret", "Eleanor"])
                
                role = random.choice(["noble", "knight", "merchant", "farmer", "craftsman", "priest"])
                
                # Create a basic character
                person = Character(name, gender, role, birth_year)
                person.age = age
                
                npcs_to_show.append((-1, person))  # Use -1 as a placeholder ID
        
        # Display people to socialize with
        person_descriptions = []
        for npc_id, npc in npcs_to_show:
            if npc_id != -1 and game_manager.npc_manager:
                # Use the detailed description for persistent NPCs
                description = game_manager.npc_manager.get_npc_description(npc_id)
                person_descriptions.append(description)
            else:
                # Use a simple description for non-persistent NPCs
                person_descriptions.append(f"{npc.name}, {npc.age} years old, {npc.role.capitalize()}")
        
        person_descriptions.append("No one")
        
        interface.display_message("=== Socialize ===")
        interface.display_message("You look around for someone to talk to.")
        
        choice = interface.display_menu("Choose someone to socialize with:", person_descriptions)
        
        if choice < len(npcs_to_show):
            # Socialize with the chosen person
            npc_id, npc = npcs_to_show[choice]
            
            # Check if this NPC is involved in any active story arcs
            npc_in_arc = False
            for arc in game_manager.story_arc_manager.active_arcs:
                if npc_id in game_manager.story_arc_manager.get_arc_npcs(arc.arc_id):
                    npc_in_arc = True
                    
                    # Get the current event for this arc
                    event = arc.get_current_event(game_manager.player)
                    if event:
                        interface.display_message(f"You approach {npc.name} to talk.")
                        interface.display_message(f"Your conversation quickly turns to matters related to recent events...")
                        
                        # Execute the event
                        event.execute(game_manager.player, interface)
                        
                        # Handle the outcome
                        if event.choices:
                            choice_idx = interface.menu_result
                            game_manager.story_arc_manager.handle_event_outcome(arc, choice_idx)
                        
                        return
            
            # If not in a story arc, proceed with normal socialization
            # Determine outcome based on charisma
            success_chance = 50 + (self.attributes['charisma'] - 50) // 2
            success = random.randint(1, 100) <= success_chance
            
            if success:
                interface.display_message(f"You had a pleasant conversation with {npc.name}.")
                
                # Check if there's a potential for a new story arc with this NPC
                if game_manager.story_arc_manager and random.random() < 0.2:  # 20% chance
                    # Find eligible arcs for this NPC
                    eligible_arcs = []
                    for arc_id, arc in game_manager.story_arc_manager.story_arcs.items():
                        # Skip arcs that are already active or completed
                        if arc in game_manager.story_arc_manager.active_arcs or arc in game_manager.story_arc_manager.completed_arcs:
                            continue
                        
                        # Skip arcs that are on cooldown
                        if arc_id in game_manager.story_arc_manager.arc_cooldown and game_manager.story_arc_manager.arc_cooldown[arc_id] > 0:
                            continue
                        
                        # Skip role-specific arcs that don't apply to the player
                        if arc.role_specific and self.role not in arc.roles:
                            continue
                        
                        # Check prerequisites
                        if not arc.check_prerequisites(self):
                            continue
                        
                        # Check compatibility with NPC
                        if arc_id == "adultery" and getattr(npc, "marital_status", "single") == "married":
                            eligible_arcs.append((arc_id, arc))
                        elif arc_id == "forbidden_romance" and npc.role != self.role:
                            eligible_arcs.append((arc_id, arc))
                        elif arc_id == "same_sex_relationship" and npc.gender == self.gender:
                            eligible_arcs.append((arc_id, arc))
                        elif arc_id in ["smuggling", "theft", "corruption", "criminal_temptation"]:
                            eligible_arcs.append((arc_id, arc))
                    
                    # Start a new arc if eligible
                    if eligible_arcs and len(game_manager.story_arc_manager.active_arcs) < game_manager.story_arc_manager.max_active_arcs:
                        arc_id, arc = random.choice(eligible_arcs)
                        arc.start()
                        game_manager.story_arc_manager.active_arcs.append(arc)
                        game_manager.story_arc_manager.assign_npc_to_arc(arc_id, npc_id)
                        
                        # Get the first event from this arc
                        event = arc.get_current_event(self)
                        if event:
                            interface.display_message("As you talk, the conversation takes an interesting turn...")
                            
                            # Execute the event
                            event.execute(self, interface)
                            
                            # Handle the outcome
                            if event.choices:
                                choice_idx = interface.menu_result
                                game_manager.story_arc_manager.handle_event_outcome(arc, choice_idx)
                            
                            return
                
                # If no story arc was started, continue with normal socialization
                interface.display_message("You've made a new acquaintance!")
                
                # Add to relationships if this is a persistent NPC
                if npc_id != -1:
                    self.relationships[npc] = Relationship(npc, "acquaintance", 30)
            else:
                interface.display_message(f"Your conversation with {npc.name} didn't go well.")
                interface.display_message("They don't seem interested in further interaction.")
        else:
            interface.display_message("You decided not to socialize with anyone at this time.")
        
        interface.get_input("Press Enter to continue...")
    
    def _rest_and_recover(self, game_manager):
        """Rest to recover health.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Rest and Recover ===")
        interface.display_message("You take time to rest and focus on your health.")
        
        # Calculate health recovery based on attributes and random chance
        base_recovery = 10
        wisdom_bonus = self.attributes["wisdom"] // 20  # 0-5 bonus based on wisdom
        recovery = base_recovery + wisdom_bonus + random.randint(0, 5)
        
        # Apply recovery
        old_health = self.health
        self.health = min(100, self.health + recovery)
        actual_recovery = self.health - old_health
        
        interface.display_message(f"Your health improved by {actual_recovery} points.")
        interface.display_message(f"Current health: {self.health}/100")
        
        # Chance to improve wisdom
        if random.random() < 0.2:  # 20% chance
            wisdom_gain = random.randint(1, 3)
            self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
            interface.display_message(f"The time spent in reflection has improved your wisdom by {wisdom_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _train_skills(self, game_manager):
        """Train to improve skills.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Train Skills ===")
        
        # List available skills to train
        skill_options = list(self.skills.keys())
        skill_display = [f"{skill.capitalize()} (Current: {self.skills[skill]})" for skill in skill_options]
        
        choice = interface.display_menu("Which skill would you like to train?", skill_display)
        skill_to_train = skill_options[choice]
        
        # Calculate training effectiveness based on attributes and random chance
        intelligence_factor = self.attributes["intelligence"] / 100  # 0-1 based on intelligence
        base_improvement = 3
        improvement = base_improvement + int(intelligence_factor * 5) + random.randint(0, 2)
        
        # Apply improvement
        old_skill = self.skills[skill_to_train]
        self.skills[skill_to_train] = min(100, self.skills[skill_to_train] + improvement)
        actual_improvement = self.skills[skill_to_train] - old_skill
        
        # Health cost of training
        health_cost = random.randint(1, 5)
        self.health = max(1, self.health - health_cost)
        
        interface.display_message(f"You spend time training your {skill_to_train} skill.")
        interface.display_message(f"Your {skill_to_train} skill improved by {actual_improvement} points.")
        interface.display_message(f"Current {skill_to_train} skill: {self.skills[skill_to_train]}/100")
        interface.display_message(f"The training was tiring. You lost {health_cost} health points.")
        interface.display_message(f"Current health: {self.health}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _travel(self, game_manager):
        """Travel to another location.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Travel ===")
        
        # Get list of settlements from the world
        world = game_manager.world
        settlements = []
        for kingdom in world.kingdoms:
            for settlement in kingdom.settlements:
                settlements.append(settlement)
        
        # Create display list
        settlement_display = [f"{s.name} ({s.type.capitalize()}) - {s.kingdom.name}" for s in settlements]
        
        choice = interface.display_menu("Where would you like to travel?", settlement_display)
        destination = settlements[choice]
        
        # Calculate travel effects
        travel_distance = random.randint(1, 10)  # Simulated distance
        health_cost = travel_distance // 2
        self.health = max(1, self.health - health_cost)
        
        # Chance to gain experience from travel
        skill_gain = random.randint(1, 2)
        random_skill = random.choice(list(self.skills.keys()))
        self.skills[random_skill] = min(100, self.skills[random_skill] + skill_gain)
        
        # Chance to find wealth on the road
        wealth_chance = random.random()
        if wealth_chance < 0.1:  # 10% chance
            wealth_gain = random.randint(10, 50)
            self.wealth += wealth_gain
            interface.display_message(f"You travel to {destination.name} in the kingdom of {destination.kingdom.name}.")
            interface.display_message(f"On your journey, you find a small treasure worth {wealth_gain} coins!")
        elif wealth_chance < 0.3:  # 20% chance
            interface.display_message(f"You travel to {destination.name} in the kingdom of {destination.kingdom.name}.")
            interface.display_message(f"The journey was uneventful but pleasant.")
        else:  # 70% chance
            interface.display_message(f"You travel to {destination.name} in the kingdom of {destination.kingdom.name}.")
            interface.display_message(f"The journey was long and tiring.")
        
        interface.display_message(f"You lost {health_cost} health points from the journey.")
        interface.display_message(f"Your {random_skill} skill improved by {skill_gain} points from the experiences on the road.")
        interface.display_message(f"Current health: {self.health}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _family_activities(self, game_manager):
        """Spend time with family.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Family Activities ===")
        
        if not self.spouse and not self.children:
            interface.display_message("You have no family to spend time with.")
            interface.get_input("Press Enter to continue...")
            return
        
        activities = []
        
        if self.spouse:
            activities.append("Spend time with spouse")
        
        if self.children:
            activities.extend([
                "Play with children",
                "Teach children",
                "Family meal"
            ])
        
        activities.append("Cancel")
        
        choice = interface.display_menu("Choose an activity:", activities)
        
        if choice == len(activities) - 1:  # Cancel
            return
        
        activity = activities[choice]
        
        if activity == "Spend time with spouse":
            # Improve relationship with spouse
            happiness_gain = random.randint(3, 8)
            self.happiness = min(100, self.happiness + happiness_gain)
            
            # Random events
            events = [
                "You and your spouse take a pleasant walk together.",
                "You share stories and laughter with your spouse.",
                "You and your spouse discuss plans for the future.",
                "You help your spouse with their daily tasks."
            ]
            interface.display_message(random.choice(events))
            interface.display_message(f"Your happiness increases by {happiness_gain} points.")
        
        elif activity == "Play with children":
            # Improve relationships with children
            happiness_gain = random.randint(2, 6)
            self.happiness = min(100, self.happiness + happiness_gain)
            
            # Random events
            events = [
                "You spend time playing games with your children.",
                "You tell stories to your children.",
                "You teach your children a new game.",
                "Your children show you their latest achievements."
            ]
            interface.display_message(random.choice(events))
            interface.display_message(f"Your happiness increases by {happiness_gain} points.")
        
        elif activity == "Teach children":
            # Choose a skill to teach
            teachable_skills = ["diplomacy", "trade", "stewardship"]
            skill_names = [skill.capitalize() for skill in teachable_skills]
            skill_names.append("Cancel")
            
            skill_choice = interface.display_menu("What would you like to teach?", skill_names)
            
            if skill_choice < len(teachable_skills):
                skill = teachable_skills[skill_choice]
                
                # Teaching effectiveness based on your skill level
                effectiveness = self.skills[skill] / 100
                
                # Children learn and gain skills
                for child in self.children:
                    if hasattr(child, 'skills') and child.age >= 5:
                        skill_gain = random.randint(1, 3)
                        adjusted_gain = int(skill_gain * effectiveness)
                        if skill in child.skills:
                            child.skills[skill] = min(100, child.skills[skill] + adjusted_gain)
                
                interface.display_message(f"You spend time teaching your children about {skill}.")
                interface.display_message("They seem to learn from your experience.")
        
        elif activity == "Family meal":
            # Everyone gains happiness
            happiness_gain = random.randint(2, 5)
            self.happiness = min(100, self.happiness + happiness_gain)
            
            # Cost of the meal
            meal_cost = random.randint(5, 15)
            self.wealth = max(0, self.wealth - meal_cost)
            
            interface.display_message(f"You share a wonderful meal with your family. (Cost: {meal_cost} coins)")
            interface.display_message(f"Your happiness increases by {happiness_gain} points.")
        
        interface.get_input("Press Enter to continue...")
    
    def display_status(self, interface):
        """Display the character's status.
        
        Args:
            interface: The user interface.
        """
        # Display basic info
        interface.display_message(f"Health: {self.health}/100")
        interface.display_message(f"Wealth: {self.wealth} coins")
        interface.display_message(f"Happiness: {self.happiness}/100")
        
        # Display traits
        if self.traits:
            interface.display_message("\nTraits:")
            for trait in self.traits:
                interface.display_message(f"- {trait.capitalize()}")
        
        # Display reputation levels
        interface.display_message("\nReputation Levels:")
        for group in ["nobility", "clergy", "merchants", "peasants", "military"]:
            level, desc = self.reputation.get_reputation_level(group)
            interface.display_message(f"{group.capitalize()}: {level}")
        
        # Only show criminal reputation if it's above 0
        if self.reputation.reputations["criminals"] > 0:
            level, desc = self.reputation.get_reputation_level("criminals")
            interface.display_message(f"Criminal: {level}")
        
        # Display active effects
        significant_effects = []
        for group in self.reputation.reputations:
            effects = self.reputation.get_reputation_effects(group)
            for effect, value in effects.items():
                if abs(1 - value) >= 0.1:  # Only show significant effects (>= 10% change)
                    significant_effects.append(f"{group.capitalize()} - {effect}: {value:.2f}x")
        
        if significant_effects:
            interface.display_message("\nActive Effects:")
            for effect in significant_effects:
                interface.display_message(effect)
    
    def display_details(self, interface):
        """Display detailed character information.
        
        Args:
            interface: The user interface.
        """
        interface.display_message(f"Name: {self.name}")
        interface.display_message(f"Role: {self.role.capitalize()}")
        interface.display_message(f"Age: {self.age}")
        interface.display_message(f"Gender: {self.gender.capitalize()}")
        interface.display_message(f"Health: {self.health}/100")
        interface.display_message(f"Wealth: {self.wealth} coins")
        
        interface.display_message("\nAttributes:")
        for attr, value in self.attributes.items():
            interface.display_message(f"  {attr.capitalize()}: {value}")
        
        interface.display_message("\nSkills:")
        for skill, value in self.skills.items():
            interface.display_message(f"  {skill.capitalize()}: {value}")

    def _diplomacy(self):
        """Engage in diplomatic activities."""
        message, rewards = self.perform_action("diplomacy")
        self.last_action_result = message
        return message

    def _craft(self):
        """Perform crafting work."""
        message, rewards = self.perform_action("craft")
        self.last_action_result = message
        return message

    def _study(self):
        """Study to gain knowledge."""
        message, rewards = self.perform_action("study")
        self.last_action_result = message
        return message

    def _farm(self):
        """Work on farming activities."""
        message, rewards = self.perform_action("farm")
        self.last_action_result = message
        return message

    def _prayer(self):
        """Engage in religious activities."""
        message, rewards = self.perform_action("prayer")
        self.last_action_result = message
        return message

class Relationship:
    """Represents a relationship between two characters."""
    
    def __init__(self, person, status, level):
        """Initialize a new relationship.
        
        Args:
            person: The person this relationship is with.
            status: The status of the relationship (e.g., 'friend', 'enemy').
            level: The level of the relationship (1-100).
        """
        self.person = person
        self.status = status
        self.level = level
    
    def improve(self, amount):
        """Improve the relationship.
        
        Args:
            amount: The amount to improve the relationship by.
        """
        self.level = min(100, self.level + amount)
        self._update_status()
    
    def worsen(self, amount):
        """Worsen the relationship.
        
        Args:
            amount: The amount to worsen the relationship by.
        """
        self.level = max(0, self.level - amount)
        self._update_status()
    
    def _update_status(self):
        """Update the relationship status based on the level."""
        if self.level >= 80:
            self.status = "close friend"
        elif self.level >= 60:
            self.status = "friend"
        elif self.level >= 40:
            self.status = "acquaintance"
        elif self.level >= 20:
            self.status = "distant"
        else:
            self.status = "enemy" 