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
        self.game_year = 1200
        self.game_running = True
        self.tutorial_shown = False
        self.achievements = {
            "married": False,
            "first_child": False,
            "wealthy": False,
            "old_age": False,
            "skilled_master": False
        }
        
    def start_new_game(self):
        """Start a new game."""
        self.interface.display_message("Starting new game...")
        
        # Create the world
        self.world = World()
        self.interface.display_message("World created.")
        
        # Character creation
        self.player = self._create_character()
        
        # Create event manager
        self.event_manager = EventManager(self)
        
        # Create story arc manager
        self.story_arc_manager = StoryArcManager(self)
        
        # Create NPC manager
        self.npc_manager = NPCManager(self)
        
        # Show tutorial for new players
        if not self.tutorial_shown:
            self._show_tutorial()
            self.tutorial_shown = True
        
        # Start the game loop
        self.game_running = True
        self.game_loop()
    
    def _create_character(self):
        """Create a new character based on player choices."""
        self.interface.display_message("\n=== Character Creation ===")
        
        # Get character name
        name = self.interface.get_input("Enter your character's name: ")
        
        # Choose character role
        roles = ["King", "Noble", "Knight", "Merchant", "Farmer", "Craftsman", "Priest"]
        role_idx = self.interface.display_menu("Choose your role:", roles)
        role = roles[role_idx]
        
        # Choose gender
        gender_idx = self.interface.display_menu("Choose your gender:", ["Male", "Female"])
        gender = "male" if gender_idx == 0 else "female"
        
        # Set starting age and calculate birth year
        starting_age = 20
        birth_year = self.game_year - starting_age
        
        # Create the character
        character = self.character_factory.create_character(role.lower(), name, gender, birth_year)
        character.age = starting_age
        
        self.interface.display_message(f"\nWelcome, {name} the {role}!")
        self.interface.display_message(f"You were born in the year {birth_year}.")
        
        return character
    
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
    
    def _view_character_details(self):
        """Display detailed character information."""
        self.interface.display_character_sheet(self.player)
    
    def _view_family(self):
        """Display family information."""
        family_info = []
        
        if self.player.spouse:
            family_info.append(f"Spouse: {self.player.spouse.name}, Age: {self.game_year - self.player.spouse.birth_year}")
        else:
            family_info.append("You are not married.")
        
        if self.player.children:
            family_info.append("\nChildren:")
            for child in self.player.children:
                family_info.append(f"- {child.name}, Age: {self.game_year - child.birth_year}")
        else:
            family_info.append("\nYou have no children.")
        
        # Display family info as an event
        self.interface.display_event("Family", "\n".join(family_info))
    
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
        self.interface.display_event("Save Game", "Saving game... (Not implemented yet)")
    
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