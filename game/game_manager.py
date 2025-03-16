"""
Game Manager - Handles the core game logic and state
"""
import random
import time
from game.characters.character_factory import CharacterFactory
from game.world.world import World
from game.events.event_manager import EventManager
from game.events.story_arc import StoryArcManager
from game.characters.npc_manager import NPCManager
from game.events.seasonal_events import get_season
from game.save_system import SaveSystem
from game.family.family_manager import FamilyManager
from game.mechanics.historical_constraints import HistoricalConstraints

class GameManager:
    """Manages the game state and core game loop."""
    
    def __init__(self, interface):
        """Initialize the game manager.
        
        Args:
            interface: The user interface to use for the game.
        """
        self.interface = interface
        self.character_factory = CharacterFactory()
        self.world = None
        self.player = None
        self.event_manager = None
        self.story_arc_manager = None
        self.npc_manager = None
        self.family_manager = None
        self.game_year = 1200
        self.game_running = True
        self.tutorial_shown = False
        self.achievements = []
        self.save_system = SaveSystem()
        self.historical_constraints = HistoricalConstraints()
        
    def start_new_game(self, player_name, gender, role, birth_year=None):
        """Start a new game with the given player details."""
        # Validate role based on gender before creating character
        allowed_roles = self.historical_constraints.get_allowed_roles(gender)
        if role.lower() not in allowed_roles:
            self.interface.display_message(f"That role is not available for your gender. Available roles: {', '.join(allowed_roles)}")
            return False
            
        self.interface.display_message("Starting new game...")
        
        # Create the world
        self.world = World()
        self.interface.display_message("World created.")
        
        # Create managers
        self.event_manager = EventManager(self)
        self.story_arc_manager = StoryArcManager(self)
        self.npc_manager = NPCManager(self)
        self.family_manager = FamilyManager(self)
        
        # Create player character
        self._create_player(player_name, gender, role, birth_year)
        
        # Show tutorial for new players
        if not self.tutorial_shown:
            self._show_tutorial()
            self.tutorial_shown = True
        
        # Start the game loop
        self.game_running = True
        self.game_loop()
    
    def _create_player(self, player_name, gender, role, birth_year=None):
        """Create a new character based on player choices."""
        self.interface.display_message("\n=== Character Creation ===")
        
        # Set starting age and calculate birth year if not provided
        starting_age = 20
        if birth_year is None:
            birth_year = self.game_year - starting_age
        
        # Create the character
        character = self.character_factory.create_character(role.lower(), player_name, gender, birth_year)
        character.age = starting_age
        
        # Initialize basic attributes
        character.health = 100
        character.happiness = 50
        
        # Initialize starting wealth based on role
        if role == "noble":
            character.wealth = random.randint(500, 1000)
        elif role == "knight":
            character.wealth = random.randint(200, 400)
        elif role == "merchant":
            character.wealth = random.randint(300, 600)
        elif role == "priest":
            character.wealth = random.randint(100, 200)
        else:  # farmer or craftsman
            character.wealth = random.randint(50, 150)
        
        # Initialize skills based on role
        character._adjust_skills_for_role()
        
        # Initialize reputation based on role
        character._adjust_starting_reputation()
        
        # Initialize random traits
        character._initialize_traits()
        
        self.interface.display_message(f"\nWelcome, {player_name} the {role.capitalize()}!")
        self.interface.display_message(f"You were born in the year {birth_year}.")
        
        # Display initial character stats
        self.interface.display_message("\nYour starting attributes:")
        for attr, value in character.attributes.items():
            self.interface.display_message(f"{attr.capitalize()}: {value}")
        
        self.interface.display_message("\nYour starting skills:")
        for skill, value in character.skills.items():
            self.interface.display_message(f"{skill.capitalize()}: {value}")
        
        if character.traits:
            self.interface.display_message("\nYour traits:")
            for trait in character.traits:
                self.interface.display_message(f"- {trait.capitalize()}")
        
        self.interface.get_input("\nPress Enter to continue...")
        
        self.player = character
    
    def game_loop(self):
        """Main game loop."""
        while self.game_running and self.player.is_alive() and self.interface.running:
            # Display current status
            action = self._display_status()
            
            # If the player chose to advance the year
            if action == "Advance Year":
                # Process events
                self._process_events()
                
                # Advance time
                self._advance_time()
                
                # Display notification about the new year
                self.interface.display_notification(f"The year is now {self.game_year}")
            
            # Check if the interface is still running (user might have closed the window)
            if not self.interface.running:
                break
        
        # Game over
        if not self.player.is_alive() and self.interface.running:
            self._handle_death()
    
    def _display_status(self):
        """Display the current game status.
        
        Returns:
            The action chosen by the player.
        """
        # Get available actions
        actions = self._get_available_actions()
        
        # Get current month and season
        current_month = self.event_manager.current_month
        month_name = self._get_month_name(current_month)
        current_season = get_season(current_month)
        
        # Display game status screen
        choice_idx = self.interface.display_game_status(
            self.game_year, 
            self.player, 
            actions,
            month=month_name,
            season=current_season.capitalize()
        )
        
        # Handle action choice
        if choice_idx is not None:
            action = actions[choice_idx]
            self._perform_action(action)
            return action
        
        return None
    
    def _get_available_actions(self):
        """Get the list of available actions.
        
        Returns:
            A list of action names.
        """
        # Get base actions
        actions = ["View Character Details", "View Family", "View Relationships"]
        
        # Add role-specific actions
        role_actions = self.player.get_actions()
        actions.extend(role_actions)
        
        # Add general actions
        actions.extend(["Advance Year", "Save Game", "Quit"])
        
        return actions
    
    def _perform_action(self, action):
        """Perform the selected action.
        
        Args:
            action: The name of the action to perform.
        """
        if action == "View Character Details":
            self._view_character_details()
        elif action == "View Family":
            self._view_family()
        elif action == "View Relationships":
            self._view_relationships()
        elif action == "Advance Year":
            # This is now handled in the game loop
            pass
        elif action == "Save Game":
            self._save_game()
        elif action == "Quit":
            self._quit_game()
        else:
            # Must be a role-specific action
            self.player.perform_action(action, self)
        
        # After action is completed, check for social mobility
        self._check_social_mobility()
    
    def _view_character_details(self):
        """Display detailed character information."""
        self.interface.display_character_sheet(self.player)
    
    def _view_family(self):
        """Display family information."""
        family_info = []
        
        # Basic family info
        if self.player.spouse:
            spouse_traits = getattr(self.player.spouse, 'traits', [])
            spouse_info = f"Spouse: {self.player.spouse.name}, Age: {self.player.spouse.age}"
            if spouse_traits:
                spouse_info += f"\nTraits: {', '.join(spouse_traits)}"
            family_info.append(spouse_info)
        else:
            family_info.append("You are not married.")
        
        # Children info
        if self.player.children:
            family_info.append("\nChildren:")
            for child in self.player.children:
                child_info = [f"- {child.name}, Age: {child.age}"]
                
                # Add traits if any
                if hasattr(child, 'traits') and child.traits:
                    child_info.append(f"  Traits: {', '.join(child.traits)}")
                
                # Add interests or career path for older children
                if child.age >= 12:
                    if hasattr(child, 'role') and child.role != "child":
                        child_info.append(f"  Role: {child.role.capitalize()}")
                    else:
                        child_info.append("  Still deciding their path in life")
                
                family_info.append("\n".join(child_info))
        else:
            family_info.append("\nYou have no children.")
        
        # Display family info as an event
        self.interface.display_event("Family", "\n".join(family_info))
        
        # Display any active family events
        if self.family_manager:
            current_events = self.family_manager.check_family_events()
            if current_events:
                self.interface.display_message("\nCurrent Family Matters:")
                for event in current_events:
                    self.interface.display_message(f"- {event['description']}")
        
        self.interface.get_input("\nPress Enter to continue...")
    
    def _view_relationships(self):
        """Display relationship information."""
        relationship_info = []
        
        if self.player.relationships:
            for person, relation in self.player.relationships.items():
                relationship_info.append(f"{person.name}: {relation.level}/100 ({relation.status})")
        else:
            relationship_info.append("You have no significant relationships.")
        
        # Display relationship info as an event
        self.interface.display_event("Relationships", "\n".join(relationship_info))
    
    def _save_game(self):
        """Save the current game state."""
        if self.save_system.save_game(self):
            self.interface.display_event("Save Game", "Game saved successfully!")
        else:
            self.interface.display_event("Save Game", "Failed to save game.")
        
        self.interface.get_input("Press Enter to continue...")
    
    def _quit_game(self):
        """Quit the current game."""
        confirm = self.interface.display_menu("Are you sure you want to quit?", ["Yes", "No"])
        if confirm == 0:  # Yes
            self.game_running = False
            # Also set interface.running to False to ensure clean exit
            self.interface.running = False
    
    def _get_month_name(self, month):
        """Get the name of a month.
        
        Args:
            month: The month number (1-12).
            
        Returns:
            The name of the month.
        """
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return month_names[month - 1]
    
    def _process_events(self):
        """Process random events for the current year."""
        # Get the current month and season
        current_month = self.event_manager.current_month
        month_name = self._get_month_name(current_month)
        current_season = get_season(current_month)
        
        # Display the current month and season
        self.interface.display_notification(f"It is now {month_name}, {self.game_year} ({current_season.capitalize()})")
        
        # Process regular random events
        events = self.event_manager.get_events_for_year()
        for event in events:
            event.execute(self.player, self.interface)
        
        # Process story arc events
        story_events = self.story_arc_manager.update_for_new_year()
        for arc, event in story_events:
            # Display the event
            event.execute(self.player, self.interface)
            
            # If there are choices, handle the outcome
            if event.choices:
                # The choice_idx is set by the event's execute method
                choice_idx = self.interface.menu_result
                self.story_arc_manager.handle_event_outcome(arc, choice_idx)
        
        # Process family events
        family_events = self.family_manager.update_family_for_new_year()
        for event in family_events:
            self.interface.display_event(event["title"], event["description"])
            
            # Apply effects
            if "effects" in event:
                for stat, value in event["effects"].items():
                    if stat == "wealth":
                        self.player.wealth = max(0, self.player.wealth + value)
                    elif stat == "happiness":
                        # Happiness affects health
                        health_change = value // 2
                        self.player.health = max(1, min(100, self.player.health + health_change))
        
        # Update NPCs
        self.npc_manager.update_for_new_year()
        
        # Age the player
        self.player.age += 1
        
        # Check for death
        if self._check_death():
            self.game_running = False
            return
        
        # Update achievements
        self._update_achievements()
        
        # Advance year
        self.game_year += 1
    
    def _advance_time(self):
        """Advance the game time by one year."""
        self.game_year += 1
        self.player.age += 1
        
        # Update character stats based on age
        self.player.update_for_new_year()
        
        # Update NPCs
        if self.npc_manager:
            self.npc_manager.update_for_new_year()
        
        # Update the world
        if self.world:
            self.world.update_for_new_year()
        
        # Check for natural death due to old age
        if self.player.age > 60:
            death_chance = (self.player.age - 60) * 5  # 5% per year after 60
            if random.randint(1, 100) <= death_chance:
                self.player.health = 0
    
    def _handle_death(self):
        """Handle player character death."""
        death_message = f"{self.player.name} the {self.player.role.capitalize()} has died at the age of {self.player.age}."
        self.interface.display_event("You Have Died", death_message)
        
        # Check for heirs
        heirs = [child for child in self.player.children if child.age >= 16]
        
        if heirs:
            heir_names = [f"{heir.name}, {heir.age} years old, {heir.role.capitalize()}" for heir in heirs]
            heir_idx = self.interface.display_menu("Choose your heir:", heir_names)
            
            # Continue as heir
            self.player = heirs[heir_idx]
            self.interface.display_event("New Heir", f"You now continue as {self.player.name} the {self.player.role.capitalize()}.")
            self.game_running = True
        else:
            self.interface.display_event("Game Over", "You have no eligible heirs. Your legacy ends here.")
            self.game_running = False
    
    def _show_tutorial(self):
        """Show the tutorial for new players."""
        tutorial_pages = [
            {
                "title": "Welcome to Medieval Life Simulator",
                "content": "In this game, you'll live the life of a medieval character, making decisions that affect your wealth, health, and relationships. This tutorial will guide you through the basics of gameplay."
            },
            {
                "title": "Game Basics",
                "content": "Each turn represents one year in your character's life. You can perform one major action per year, such as planting crops, finding a spouse, or engaging in trade. Choose your actions wisely to build a successful life!"
            },
            {
                "title": f"Your Role: {self.player.role.capitalize()}",
                "content": self._get_role_tutorial(self.player.role)
            },
            {
                "title": "Character Stats",
                "content": "Your character has various attributes and skills that affect their success in different activities. Health decreases with age, and wealth is needed for many actions. Build relationships to gain advantages in society."
            },
            {
                "title": "Events",
                "content": "Random events will occur throughout your life, bringing opportunities and challenges. These events can affect your health, wealth, and relationships. Respond to them wisely!"
            },
            {
                "title": "Family",
                "content": "Finding a spouse and having children is an important aspect of the game. When your character dies, you can continue playing as your heir, building a dynasty that spans generations."
            },
            {
                "title": "Ready to Begin",
                "content": "You're now ready to begin your medieval life! Remember, each decision shapes your character's future. Good luck on your journey!"
            }
        ]
        
        for page in tutorial_pages:
            self.interface.display_event(page["title"], page["content"])
    
    def _get_role_tutorial(self, role):
        """Get role-specific tutorial content.
        
        Args:
            role: The character role.
            
        Returns:
            Role-specific tutorial text.
        """
        tutorials = {
            "king": "As a King, you rule over a kingdom. You can adjust taxes, hold court, declare war, and build monuments. Balance keeping your subjects happy with maintaining your treasury and power.",
            
            "noble": "As a Noble, you manage estates and engage in politics. Build alliances with other nobles and the king to increase your influence and wealth.",
            
            "knight": "As a Knight, you serve your lord in battle and tournaments. Improve your combat skills to win glory and rewards. You can participate in tournaments, go on quests, and serve in wars.",
            
            "merchant": "As a Merchant, you buy and sell goods for profit. Establish trade routes, negotiate deals, and build a commercial empire. Your success depends on your trading skill and business acumen.",
            
            "farmer": "As a Farmer, you work the land to produce crops and raise livestock. Plant crops, tend animals, and sell your produce at market. Expand your farm by buying more land and hiring workers.",
            
            "craftsman": "As a Craftsman, you create goods with your skilled hands. Fulfill commissions, improve your workshop, and train apprentices. Your crafting skill determines the quality and value of your products.",
            
            "priest": "As a Priest, you serve the church and provide spiritual guidance. Perform religious ceremonies, help the poor, and increase your influence within the church hierarchy."
        }
        
        return tutorials.get(role, "Your role gives you unique actions and opportunities. Explore them to find the best strategy!")

    def load_game(self, save_file):
        """Load a saved game state.
        
        Args:
            save_file: The name of the save file to load.
            
        Returns:
            bool: True if load was successful, False otherwise.
        """
        if self.save_system.load_game(save_file, self):
            self.interface.display_event("Load Game", "Game loaded successfully!")
            return True
        else:
            self.interface.display_event("Load Game", "Failed to load game.")
            return False

    def _check_death(self):
        """Check if the player character is dead."""
        return not self.player.is_alive()

    def _update_achievements(self):
        """Update player achievements based on current game state."""
        # Implementation of updating achievements based on the game state
        pass

    def _advance_year(self):
        """Advance the game by one year."""
        self.game_year += 1
        self.player.age += 1
        
        # Process random events
        self._process_events()
        
        # Update character status
        self._update_character_status()
        
        # Check for game over conditions
        if not self._check_game_over():
            self.interface.display_message(f"\nYear {self.game_year} begins...")
            self.interface.get_input("Press Enter to continue...")
    
    def _update_character_status(self):
        """Update the character's status for the new year."""
        # Natural health recovery
        if self.player.health < 100:
            self.player.health = min(100, self.player.health + 10)
        
        # Apply age effects
        if self.player.age > 50:
            health_loss = (self.player.age - 50) // 10
            self.player.health = max(1, self.player.health - health_loss)
    
    def _check_game_over(self):
        """Check if the game should end.
        
        Returns:
            bool: True if the game should end, False otherwise.
        """
        if self.player.health <= 0:
            self.interface.display_message("\nYou have died!")
            return True
        elif self.player.age >= 80:
            self.interface.display_message("\nYou have reached old age and retire from active life.")
            return True
        return False

    def handle_action(self, action):
        """Handle a player action."""
        if not self.player:
            return
            
        # Check if action is allowed based on historical constraints
        allowed, reason = self.historical_constraints.can_perform_action(self.player, action)
        if not allowed:
            self.interface.display_message(reason)
            self.interface.get_input("Press Enter to continue...")
            return
            
        if action == "Find Spouse":
            self.player._find_spouse(self)
        elif action == "Socialize":
            self.player._socialize(self)
        elif action == "Family Activities":
            self.player._family_activities(self)
        elif action == "Rest and Recover":
            self.player._rest_and_recover(self)
        elif action == "Train Skills":
            self._handle_training()
        elif action == "Travel":
            self.player._travel(self)
        elif action == "Trade":
            outcome_message = self.player._trade()
            self.interface.display_message(outcome_message)
            self.interface.get_input("Press Enter to continue...")
        elif action == "Combat":
            outcome_message = self.player._combat()
            self.interface.display_message(outcome_message)
            self.interface.get_input("Press Enter to continue...")
        elif action == "Diplomacy":
            outcome_message = self.player._diplomacy()
            self.interface.display_message(outcome_message)
            self.interface.get_input("Press Enter to continue...")
        elif action == "Craft":
            outcome_message = self.player._craft()
            self.interface.display_message(outcome_message)
            self.interface.get_input("Press Enter to continue...")
        elif action == "Study":
            outcome_message = self.player._study()
            self.interface.display_message(outcome_message)
            self.interface.get_input("Press Enter to continue...")
        elif action == "Farm":
            outcome_message = self.player._farm()
            self.interface.display_message(outcome_message)
            self.interface.get_input("Press Enter to continue...")
        elif action == "Prayer":
            outcome_message = self.player._prayer()
            self.interface.display_message(outcome_message)
            self.interface.get_input("Press Enter to continue...")
        else:
            self.interface.display_message(f"Action '{action}' not implemented.")
            self.interface.get_input("Press Enter to continue...")
        
        # After action is completed, check for social mobility
        self._check_social_mobility()
    
    def _handle_training(self):
        """Handle skill training action."""
        # Display available skills
        skills = list(self.player.skills.keys())
        self.interface.display_message("\nAvailable skills to train:")
        for i, skill in enumerate(skills, 1):
            self.interface.display_message(f"{i}. {skill.capitalize()}: {self.player.skills[skill]}")
        
        # Get skill choice
        choice = self.interface.get_input("\nChoose a skill to train (number) or 0 to cancel: ")
        if not choice.isdigit() or int(choice) == 0:
            return
        
        skill_index = int(choice) - 1
        if 0 <= skill_index < len(skills):
            skill = skills[skill_index]
            message, rewards = self.player.perform_action("study", difficulty_modifier=0)
            self.interface.display_message(f"\n{message}")
            if "gold" in rewards:
                self.interface.display_message(f"Cost: {rewards['gold']} gold")
            self.interface.get_input("\nPress Enter to continue...")
        else:
            self.interface.display_message("Invalid choice.")
            self.interface.get_input("Press Enter to continue...")
    
    def _check_social_mobility(self):
        """Check and handle potential social mobility opportunities."""
        potential_class, chance = self.historical_constraints.calculate_social_mobility(self.player)
        current_class = self.historical_constraints._determine_social_class(self.player)
        
        if potential_class != current_class and random.randint(1, 100) <= chance:
            # Character has opportunity to move up in society
            message = f"Your actions and success have drawn attention. "
            
            if potential_class == "nobility":
                message += "A noble has taken notice of your achievements and offers to sponsor your elevation to the nobility."
                new_roles = ["noble", "knight"]
            elif potential_class == "clergy":
                message += "The Church recognizes your devotion and learning. You are offered a position in the clergy."
                new_roles = ["priest", "monk"]
            elif potential_class == "merchants":
                message += "Your business acumen has impressed the merchant guild. They offer you membership."
                new_roles = ["merchant", "craftsman"]
            else:
                return  # No downward mobility
                
            self.interface.display_message(message)
            
            # Filter roles based on gender
            allowed_roles = self.historical_constraints.get_allowed_roles(self.player.gender)
            new_roles = [role for role in new_roles if role in allowed_roles]
            
            if not new_roles:
                return
                
            new_roles.append("Keep current role")
            choice = self.interface.display_menu("Choose your new path:", new_roles)
            
            if choice < len(new_roles) - 1:  # If not "Keep current role"
                old_role = self.player.role
                self.player.role = new_roles[choice]
                
                # Update skills based on new role
                if self.player.role == "noble":
                    self.player.skills["diplomacy"] = max(self.player.skills.get("diplomacy", 0), 40)
                    self.player.skills["etiquette"] = max(self.player.skills.get("etiquette", 0), 40)
                elif self.player.role == "knight":
                    self.player.skills["combat"] = max(self.player.skills.get("combat", 0), 40)
                    self.player.skills["leadership"] = max(self.player.skills.get("leadership", 0), 30)
                elif self.player.role == "priest":
                    self.player.skills["theology"] = max(self.player.skills.get("theology", 0), 40)
                    self.player.skills["literacy"] = max(self.player.skills.get("literacy", 0), 40)
                elif self.player.role == "merchant":
                    self.player.skills["commerce"] = max(self.player.skills.get("commerce", 0), 40)
                    self.player.skills["negotiation"] = max(self.player.skills.get("negotiation", 0), 30)
                
                self.interface.display_message(f"You have advanced from {old_role} to {self.player.role}!")
                
                # Reputation boost with new social class
                self.player.reputation.adjust_reputation(potential_class, 20)
                
                # Achievement for social advancement
                self.achievements["social_climber"] = True
            
    def display_status(self):
        """Display the player's current status."""
        if not self.player:
            return
            
        # Get social class info
        social_class = self.historical_constraints._determine_social_class(self.player)
        potential_class, mobility_chance = self.historical_constraints.calculate_social_mobility(self.player)
        
        status_text = [
            f"Name: {self.player.name}",
            f"Age: {self.player.age}",
            f"Role: {self.player.role.capitalize()}",
            f"Social Class: {social_class.capitalize()}",
            f"Year: {self.game_year}",
            f"Wealth: {self.player.wealth} coins",
            f"Happiness: {self.player.happiness}",
            "",
            "Skills:",
        ]
        
        # Add skills
        for skill, value in sorted(self.player.skills.items()):
            status_text.append(f"  {skill.capitalize()}: {value}")
        
        # Add reputation info
        status_text.extend([
            "",
            "Reputation:",
            f"  Nobility: {self.player.reputation.get_reputation('nobility')}",
            f"  Clergy: {self.player.reputation.get_reputation('clergy')}",
            f"  Merchants: {self.player.reputation.get_reputation('merchants')}",
            f"  Commoners: {self.player.reputation.get_reputation('commoners')}",
        ])
        
        # Add social mobility info if there's a chance
        if potential_class != social_class and mobility_chance > 0:
            status_text.extend([
                "",
                f"Social Mobility: {mobility_chance}% chance to advance to {potential_class.capitalize()}"
            ])
        
        # Add family info
        if self.player.spouse:
            status_text.extend([
                "",
                "Family:",
                f"  Spouse: {self.player.spouse.name} ({self.player.spouse.role.capitalize()})"
            ])
            if self.player.children:
                status_text.append("  Children:")
                for child in self.player.children:
                    status_text.append(f"    - {child.name} (Age: {child.age})")
        
        self.interface.display_message("\n".join(status_text))
        self.interface.get_input("Press Enter to continue...") 