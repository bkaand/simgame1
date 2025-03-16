"""
Noble - Character role class for nobles
"""
import random
from game.characters.character import Character

class Noble(Character):
    """Character role class for nobles."""
    
    def __init__(self, name, gender, birth_year=None):
        """Initialize a new noble character.
        
        Args:
            name: The character's name.
            gender: The character's gender.
            birth_year: The character's birth year (optional).
        """
        super().__init__(name, gender, "noble", birth_year)
        
        # Nobles start with more wealth than commoners
        self.wealth = random.randint(500, 2000)
        
        # Noble-specific properties
        self.estate_size = random.randint(1, 3)  # 1=Small, 2=Medium, 3=Large
        self.estate_income = self.estate_size * random.randint(30, 50)  # Annual income
        self.prestige = random.randint(30, 70)  # Social standing (0-100)
        self.vassals = random.randint(0, self.estate_size)  # Number of vassals
        self.court_influence = random.randint(10, 40)  # Influence at court (0-100)
        
        # Adjust skills for role
        self._adjust_skills_for_role()
    
    def _adjust_skills_for_role(self):
        """Adjust skills based on character role."""
        # Nobles are better at diplomacy
        self.skills["diplomacy"] += random.randint(10, 30)
        
        # Nobles also have some stewardship skills
        self.skills["stewardship"] += random.randint(5, 15)
        
        # Ensure skills stay within bounds
        for skill in self.skills:
            self.skills[skill] = min(100, self.skills[skill])
    
    def get_actions(self):
        """Get the list of actions available to this character.
        
        Returns:
            A list of action names.
        """
        # Get base actions
        actions = super().get_actions()
        
        # Add noble-specific actions
        noble_actions = ["Manage Estate", "Attend Court"]
        
        actions.extend(noble_actions)
        return actions
    
    def perform_action(self, action, game_manager):
        """Perform an action.
        
        Args:
            action: The name of the action to perform.
            game_manager: The game manager.
        """
        if action == "Manage Estate":
            self._manage_estate(game_manager)
        elif action == "Attend Court":
            self._attend_court(game_manager)
        else:
            # Use base class implementation for common actions
            super().perform_action(action, game_manager)
    
    def _manage_estate(self, game_manager):
        """Manage your estate.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Manage Estate ===")
        
        # Display estate information
        estate_sizes = ["Small Manor", "Medium Estate", "Large Estate"]
        interface.display_message(f"Estate: {estate_sizes[self.estate_size - 1]}")
        interface.display_message(f"Annual Income: {self.estate_income} coins")
        interface.display_message(f"Vassals: {self.vassals}")
        
        # Management options
        options = [
            "Collect Taxes",
            "Improve Estate",
            "Host Feast",
            "Back"
        ]
        
        choice = interface.display_menu("What would you like to do?", options)
        
        if choice == 0:  # Collect Taxes
            self._collect_taxes(game_manager)
        elif choice == 1:  # Improve Estate
            self._improve_estate(game_manager)
        elif choice == 2:  # Host Feast
            self._host_feast(game_manager)
        else:  # Back
            return
    
    def _collect_taxes(self, game_manager):
        """Collect taxes from your estate.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Collect Taxes ===")
        
        # Calculate tax collection based on estate size, stewardship skill, and random factors
        base_amount = self.estate_income
        stewardship_bonus = self.skills["stewardship"] / 100  # 0-1 bonus
        random_factor = random.uniform(0.8, 1.2)  # Random fluctuation
        
        collected_amount = int(base_amount * (1 + stewardship_bonus) * random_factor)
        
        # Add to wealth
        self.wealth += collected_amount
        
        # Display results
        interface.display_message(f"You collect {collected_amount} coins in taxes from your estate.")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        
        # Skill improvement
        skill_gain = random.randint(1, 2)
        self.skills["stewardship"] = min(100, self.skills["stewardship"] + skill_gain)
        interface.display_message(f"Your stewardship skill improved by {skill_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _improve_estate(self, game_manager):
        """Improve your estate.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Improve Estate ===")
        
        # Calculate improvement costs based on current estate size
        improvement_cost = self.estate_size * 200
        
        # Check if player can afford improvement
        if self.wealth < improvement_cost:
            interface.display_message(f"You need {improvement_cost} coins to improve your estate.")
            interface.display_message(f"Current wealth: {self.wealth} coins")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Confirm improvement
        estate_sizes = ["Small Manor", "Medium Estate", "Large Estate", "Grand Estate"]
        current_size = estate_sizes[self.estate_size - 1]
        
        if self.estate_size >= 3:
            interface.display_message("Your estate is already at its maximum size.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        next_size = estate_sizes[self.estate_size]
        confirm = interface.display_menu(f"Improve from {current_size} to {next_size} for {improvement_cost} coins?", ["Yes", "No"])
        
        if confirm == 1:  # No
            interface.display_message("You decide not to improve your estate at this time.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Apply improvement
        self.wealth -= improvement_cost
        self.estate_size += 1
        
        # Increase estate income
        old_income = self.estate_income
        self.estate_income = self.estate_size * random.randint(30, 50)
        income_increase = self.estate_income - old_income
        
        # Increase prestige
        prestige_gain = random.randint(5, 15)
        self.prestige = min(100, self.prestige + prestige_gain)
        
        # Display results
        interface.display_message(f"You have improved your estate from {current_size} to {next_size}!")
        interface.display_message(f"Estate income increased by {income_increase} coins per year.")
        interface.display_message(f"Your prestige increased by {prestige_gain} points.")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _host_feast(self, game_manager):
        """Host a feast at your estate.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Host Feast ===")
        
        # Calculate feast cost based on estate size
        base_cost = 100
        estate_multiplier = self.estate_size
        feast_cost = base_cost * estate_multiplier
        
        # Check if player can afford feast
        if self.wealth < feast_cost:
            interface.display_message(f"You need {feast_cost} coins to host a feast.")
            interface.display_message(f"Current wealth: {self.wealth} coins")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Confirm feast
        confirm = interface.display_menu(f"Host a feast for {feast_cost} coins?", ["Yes", "No"])
        
        if confirm == 1:  # No
            interface.display_message("You decide not to host a feast at this time.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Apply cost
        self.wealth -= feast_cost
        
        # Calculate feast success based on diplomacy skill and random factors
        diplomacy_factor = self.skills["diplomacy"] / 100  # 0-1 bonus
        random_factor = random.uniform(0.7, 1.3)  # Random fluctuation
        success_level = (0.5 + diplomacy_factor) * random_factor  # 0.35-1.3
        
        # Determine outcome based on success level
        if success_level < 0.6:  # Poor feast
            interface.display_message("Your feast is poorly received. The food is mediocre, and few notable guests attend.")
            
            # Small prestige gain
            prestige_gain = random.randint(1, 3)
            self.prestige = min(100, self.prestige + prestige_gain)
            interface.display_message(f"Your prestige increased by only {prestige_gain} points.")
            
            # Small influence gain
            influence_gain = random.randint(0, 2)
            self.court_influence = min(100, self.court_influence + influence_gain)
            if influence_gain > 0:
                interface.display_message(f"Your court influence increased by {influence_gain} points.")
            else:
                interface.display_message("Your court influence remains unchanged.")
        
        elif success_level < 1.0:  # Decent feast
            interface.display_message("Your feast is well-received. The food is good, and several notable guests attend.")
            
            # Moderate prestige gain
            prestige_gain = random.randint(3, 8)
            self.prestige = min(100, self.prestige + prestige_gain)
            interface.display_message(f"Your prestige increased by {prestige_gain} points.")
            
            # Moderate influence gain
            influence_gain = random.randint(2, 5)
            self.court_influence = min(100, self.court_influence + influence_gain)
            interface.display_message(f"Your court influence increased by {influence_gain} points.")
        
        else:  # Excellent feast
            interface.display_message("Your feast is a tremendous success! The food is exquisite, and many important guests attend.")
            
            # Large prestige gain
            prestige_gain = random.randint(8, 15)
            self.prestige = min(100, self.prestige + prestige_gain)
            interface.display_message(f"Your prestige increased by {prestige_gain} points.")
            
            # Large influence gain
            influence_gain = random.randint(5, 10)
            self.court_influence = min(100, self.court_influence + influence_gain)
            interface.display_message(f"Your court influence increased by {influence_gain} points.")
            
            # Chance to gain a vassal
            if self.vassals < self.estate_size * 2 and random.random() < 0.3:  # 30% chance
                self.vassals += 1
                interface.display_message("A minor noble is so impressed that they offer to become your vassal!")
                interface.display_message(f"You now have {self.vassals} vassals.")
        
        # Skill improvement
        diplomacy_gain = random.randint(1, 3)
        self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
        interface.display_message(f"Your diplomacy skill improved by {diplomacy_gain} points.")
        
        interface.display_message(f"Current wealth: {self.wealth} coins")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _attend_court(self, game_manager):
        """Attend the royal court to gain influence and prestige.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Attend Court ===")
        interface.display_message("You attend the royal court to engage in politics and intrigue.")
        
        # Court activities
        activities = [
            "Engage in Politics",
            "Seek Royal Favor",
            "Spread Rumors",
            "Form Alliances"
        ]
        
        choice = interface.display_menu("What would you like to do at court?", activities)
        
        # Calculate base success chance based on diplomacy skill and court influence
        diplomacy_factor = self.skills["diplomacy"] / 100  # 0-1 based on diplomacy
        influence_factor = self.court_influence / 200  # 0-0.5 based on current influence
        base_success_chance = 0.3 + diplomacy_factor + influence_factor  # 0.3-1.5
        
        if choice == 0:  # Engage in Politics
            self._engage_in_politics(game_manager, base_success_chance)
        elif choice == 1:  # Seek Royal Favor
            self._seek_royal_favor(game_manager, base_success_chance)
        elif choice == 2:  # Spread Rumors
            self._spread_rumors(game_manager, base_success_chance)
        elif choice == 3:  # Form Alliances
            self._form_alliances(game_manager, base_success_chance)
    
    def _engage_in_politics(self, game_manager, base_success_chance):
        """Engage in court politics.
        
        Args:
            game_manager: The game manager.
            base_success_chance: Base chance of success.
        """
        interface = game_manager.interface
        
        interface.display_message("You engage in political discussions and debates at court.")
        
        # Adjust success chance based on random factors
        random_factor = random.uniform(0.7, 1.3)
        success_chance = base_success_chance * random_factor
        
        # Determine outcome
        if random.random() < success_chance:
            # Success
            interface.display_message("Your political maneuvering is successful!")
            
            # Influence gain
            influence_gain = random.randint(3, 8)
            self.court_influence = min(100, self.court_influence + influence_gain)
            interface.display_message(f"Your court influence increased by {influence_gain} points.")
            
            # Prestige gain
            prestige_gain = random.randint(1, 4)
            self.prestige = min(100, self.prestige + prestige_gain)
            interface.display_message(f"Your prestige increased by {prestige_gain} points.")
            
            # Skill improvement
            diplomacy_gain = random.randint(1, 3)
            self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
            interface.display_message(f"Your diplomacy skill improved by {diplomacy_gain} points.")
        else:
            # Failure
            interface.display_message("Your political maneuvering is unsuccessful.")
            
            # Influence loss
            influence_loss = random.randint(1, 5)
            self.court_influence = max(0, self.court_influence - influence_loss)
            interface.display_message(f"Your court influence decreased by {influence_loss} points.")
            
            # Small skill improvement (learning from mistakes)
            diplomacy_gain = random.randint(0, 1)
            if diplomacy_gain > 0:
                self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
                interface.display_message(f"Despite the setback, your diplomacy skill improved by {diplomacy_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _seek_royal_favor(self, game_manager, base_success_chance):
        """Seek favor from the monarch.
        
        Args:
            game_manager: The game manager.
            base_success_chance: Base chance of success.
        """
        interface = game_manager.interface
        
        interface.display_message("You attempt to gain the monarch's favor through flattery and service.")
        
        # Adjust success chance based on random factors and prestige
        prestige_factor = self.prestige / 200  # 0-0.5 based on prestige
        random_factor = random.uniform(0.7, 1.3)
        success_chance = (base_success_chance + prestige_factor) * random_factor
        
        # Determine outcome
        if random.random() < success_chance:
            # Success
            interface.display_message("The monarch looks upon you with favor!")
            
            # Influence gain
            influence_gain = random.randint(5, 12)
            self.court_influence = min(100, self.court_influence + influence_gain)
            interface.display_message(f"Your court influence increased by {influence_gain} points.")
            
            # Prestige gain
            prestige_gain = random.randint(3, 8)
            self.prestige = min(100, self.prestige + prestige_gain)
            interface.display_message(f"Your prestige increased by {prestige_gain} points.")
            
            # Possible wealth gain (royal gift)
            if random.random() < 0.3:  # 30% chance
                wealth_gain = random.randint(50, 200)
                self.wealth += wealth_gain
                interface.display_message(f"The monarch grants you a gift of {wealth_gain} coins!")
            
            # Skill improvement
            diplomacy_gain = random.randint(1, 3)
            self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
            interface.display_message(f"Your diplomacy skill improved by {diplomacy_gain} points.")
        else:
            # Failure
            interface.display_message("The monarch ignores your attempts to gain favor.")
            
            # Small influence loss
            influence_loss = random.randint(0, 3)
            if influence_loss > 0:
                self.court_influence = max(0, self.court_influence - influence_loss)
                interface.display_message(f"Your court influence decreased by {influence_loss} points.")
            
            # Small skill improvement (learning from mistakes)
            diplomacy_gain = random.randint(0, 1)
            if diplomacy_gain > 0:
                self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
                interface.display_message(f"Despite the setback, your diplomacy skill improved by {diplomacy_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _spread_rumors(self, game_manager, base_success_chance):
        """Spread rumors to undermine rivals.
        
        Args:
            game_manager: The game manager.
            base_success_chance: Base chance of success.
        """
        interface = game_manager.interface
        
        interface.display_message("You carefully spread rumors to undermine your rivals at court.")
        
        # Adjust success chance based on random factors
        random_factor = random.uniform(0.7, 1.3)
        success_chance = base_success_chance * random_factor
        
        # Determine outcome
        if random.random() < success_chance:
            # Success
            interface.display_message("Your rumors successfully undermine your rivals!")
            
            # Influence gain
            influence_gain = random.randint(4, 10)
            self.court_influence = min(100, self.court_influence + influence_gain)
            interface.display_message(f"Your court influence increased by {influence_gain} points.")
            
            # Skill improvement
            diplomacy_gain = random.randint(1, 3)
            self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
            interface.display_message(f"Your diplomacy skill improved by {diplomacy_gain} points.")
        else:
            # Failure - rumors traced back to you
            interface.display_message("Your rumors are traced back to you, damaging your reputation!")
            
            # Influence loss
            influence_loss = random.randint(5, 15)
            self.court_influence = max(0, self.court_influence - influence_loss)
            interface.display_message(f"Your court influence decreased by {influence_loss} points.")
            
            # Prestige loss
            prestige_loss = random.randint(3, 8)
            self.prestige = max(0, self.prestige - prestige_loss)
            interface.display_message(f"Your prestige decreased by {prestige_loss} points.")
            
            # Small skill improvement (learning from mistakes)
            diplomacy_gain = random.randint(0, 1)
            if diplomacy_gain > 0:
                self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
                interface.display_message(f"Despite the setback, your diplomacy skill improved by {diplomacy_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _form_alliances(self, game_manager, base_success_chance):
        """Form alliances with other nobles.
        
        Args:
            game_manager: The game manager.
            base_success_chance: Base chance of success.
        """
        interface = game_manager.interface
        
        interface.display_message("You attempt to form alliances with other nobles at court.")
        
        # Adjust success chance based on random factors and prestige
        prestige_factor = self.prestige / 200  # 0-0.5 based on prestige
        random_factor = random.uniform(0.7, 1.3)
        success_chance = (base_success_chance + prestige_factor) * random_factor
        
        # Determine outcome
        if random.random() < success_chance:
            # Success
            interface.display_message("You successfully form valuable alliances with other nobles!")
            
            # Influence gain
            influence_gain = random.randint(5, 10)
            self.court_influence = min(100, self.court_influence + influence_gain)
            interface.display_message(f"Your court influence increased by {influence_gain} points.")
            
            # Prestige gain
            prestige_gain = random.randint(2, 5)
            self.prestige = min(100, self.prestige + prestige_gain)
            interface.display_message(f"Your prestige increased by {prestige_gain} points.")
            
            # Chance to gain a vassal
            if self.vassals < self.estate_size * 2 and random.random() < 0.2:  # 20% chance
                self.vassals += 1
                interface.display_message("A minor noble agrees to become your vassal as part of the alliance!")
                interface.display_message(f"You now have {self.vassals} vassals.")
            
            # Skill improvement
            diplomacy_gain = random.randint(2, 4)
            self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
            interface.display_message(f"Your diplomacy skill improved by {diplomacy_gain} points.")
        else:
            # Failure
            interface.display_message("Your attempts to form alliances are rebuffed.")
            
            # Small influence loss
            influence_loss = random.randint(1, 4)
            self.court_influence = max(0, self.court_influence - influence_loss)
            interface.display_message(f"Your court influence decreased by {influence_loss} points.")
            
            # Small skill improvement (learning from mistakes)
            diplomacy_gain = random.randint(0, 2)
            if diplomacy_gain > 0:
                self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + diplomacy_gain)
                interface.display_message(f"Despite the setback, your diplomacy skill improved by {diplomacy_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def update_for_new_year(self):
        """Update character stats for a new year."""
        # Call base class method
        super().update_for_new_year()
        
        # Collect estate income
        self.wealth += self.estate_income
        
        # Income from vassals
        vassal_income = self.vassals * random.randint(10, 30)
        if vassal_income > 0:
            self.wealth += vassal_income
    
    def display_status(self, interface):
        """Display the character's status.
        
        Args:
            interface: The user interface.
        """
        estate_sizes = ["Small Manor", "Medium Estate", "Large Estate"]
        interface.display_message(f"Estate: {estate_sizes[self.estate_size - 1]}")
        interface.display_message(f"Annual Income: {self.estate_income} coins")
        interface.display_message(f"Vassals: {self.vassals}")
        interface.display_message(f"Prestige: {self.prestige}/100")
        interface.display_message(f"Court Influence: {self.court_influence}/100") 