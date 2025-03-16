"""
Farmer - Character role class for farmers
"""
import random
from game.characters.character import Character

class Farmer(Character):
    """Character role class for farmers."""
    
    def __init__(self, name, gender, birth_year=None):
        """Initialize a new farmer character.
        
        Args:
            name: The character's name.
            gender: The character's gender ('male' or 'female').
            birth_year: The year the character was born.
        """
        super().__init__(name, gender, "farmer", birth_year)
        
        # Set initial wealth
        self.wealth = random.randint(10, 50)
        
        # Farm properties
        self.land = random.randint(3, 10)  # Acres of land
        self.crops = {}  # Crop type -> acres
        self.livestock = {}  # Animal type -> count
        self.storage = {}  # Crop type -> amount
        self.helpers = 0  # Number of hired workers
        
        # Farm quality metrics
        self.soil_fertility = random.randint(40, 70)  # Quality of soil (0-100)
        self.harvest_quality = random.randint(40, 70)  # Quality of harvests (0-100)
        self.livestock_health = {}  # Animal type -> health (0-100)
        self.livestock_quality = {}  # Animal type -> quality (0-100)
        
        # Worker management
        self.worker_assignment = None  # Where workers are assigned
        self.worker_efficiency = 50  # Worker efficiency (0-100)
        self.worker_morale = 50  # Worker morale (0-100)
        
        # Initialize farm with some crops and livestock
        self._initialize_farm()
        
        # Adjust skills for role
        self._adjust_skills_for_role()
    
    def _initialize_farm(self):
        """Initialize the farm with crops and livestock."""
        # Initialize crops
        crop_types = ["wheat", "barley", "oats", "rye", "vegetables"]
        for _ in range(random.randint(1, 3)):
            crop_type = random.choice(crop_types)
            self.crops[crop_type] = random.randint(1, 3)  # Acres of each crop
        
        # Initialize livestock
        livestock_types = ["chickens", "pigs", "cows", "sheep", "goats"]
        for _ in range(random.randint(1, 3)):
            livestock_type = random.choice(livestock_types)
            self.livestock[livestock_type] = random.randint(1, 5)  # Number of each animal
    
    def _adjust_skills_for_role(self):
        """Adjust skills based on character role."""
        # Farmers are better at farming
        self.skills["farming"] += random.randint(20, 40)
        
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
        
        # Add farmer-specific actions
        farmer_actions = [
            "Plant Crops",
            "Tend Livestock",
            "Sell Produce"
        ]
        
        # Add conditional actions based on farm state
        if self.land > 0:
            farmer_actions.append("Harvest Crops")
        
        if sum(self.crops.values()) > 0:
            farmer_actions.append("Rotate Crops")
        
        if self.wealth >= 100:
            farmer_actions.append("Buy Land")
        
        if self.wealth >= 50:
            farmer_actions.append("Buy Livestock")
        
        if self.wealth >= 150 and self.land >= 10:
            farmer_actions.append("Hire Help")
        
        if self.helpers > 0:
            farmer_actions.append("Manage Workers")
        
        if self.livestock.get("horses", 0) > 0:
            farmer_actions.append("Breed Horses")
        
        if self.livestock.get("cattle", 0) > 3 or self.livestock.get("sheep", 0) > 5:
            farmer_actions.append("Improve Livestock")
        
        actions.extend(farmer_actions)
        
        return actions
    
    def perform_action(self, action, game_manager):
        """Perform an action.
        
        Args:
            action: The name of the action to perform.
            game_manager: The game manager.
        """
        if action == "Plant Crops":
            self._plant_crops(game_manager)
        elif action == "Tend Livestock":
            self._tend_livestock(game_manager)
        elif action == "Sell Produce":
            self._sell_produce(game_manager)
        elif action == "Buy Land":
            self._buy_land(game_manager)
        elif action == "Buy Livestock":
            self._buy_livestock(game_manager)
        elif action == "Hire Help":
            self._hire_help(game_manager)
        elif action == "Harvest Crops":
            self._harvest_crops(game_manager)
        elif action == "Rotate Crops":
            self._rotate_crops(game_manager)
        elif action == "Manage Workers":
            self._manage_workers(game_manager)
        elif action == "Breed Horses":
            self._breed_horses(game_manager)
        elif action == "Improve Livestock":
            self._improve_livestock(game_manager)
        else:
            # Use base class implementation for common actions
            super().perform_action(action, game_manager)
    
    def _plant_crops(self, game_manager):
        """Plant crops on the farm.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.clear_screen()
        interface.display_message("=== Plant Crops ===")
        
        # Check if player has land
        if self.land <= 0:
            interface.display_message("You don't have any land to plant crops on.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Display current crops
        interface.display_message("Current crops:")
        if self.crops:
            for crop_type, acres in self.crops.items():
                interface.display_message(f"  {crop_type.capitalize()}: {acres} acres")
        else:
            interface.display_message("  None")
        
        # Choose crop to plant
        crop_types = ["Wheat", "Barley", "Oats", "Rye", "Vegetables"]
        choice = interface.display_menu("What would you like to plant?", crop_types)
        
        crop_type = crop_types[choice].lower()
        
        # Choose amount to plant
        available_land = self.land - sum(self.crops.values())
        if available_land <= 0:
            interface.display_message("You don't have any available land. You need to clear some crops first.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        amount_options = [f"{i} acre(s)" for i in range(1, available_land + 1)]
        amount_choice = interface.display_menu(f"How many acres of {crop_type} would you like to plant?", amount_options)
        
        amount = amount_choice + 1  # Convert to 1-based
        
        # Plant the crop
        if crop_type in self.crops:
            self.crops[crop_type] += amount
        else:
            self.crops[crop_type] = amount
        
        interface.display_message(f"You planted {amount} acre(s) of {crop_type}.")
        
        # Skill check for planting quality
        planting_quality = min(100, self.skills["farming"] + random.randint(-20, 20))
        if planting_quality >= 70:
            interface.display_message("The planting went very well!")
            self.harvest_quality = min(100, self.harvest_quality + random.randint(5, 15))
        elif planting_quality >= 40:
            interface.display_message("The planting went reasonably well.")
            self.harvest_quality = min(100, self.harvest_quality + random.randint(-5, 10))
        else:
            interface.display_message("The planting didn't go very well.")
            self.harvest_quality = max(0, self.harvest_quality - random.randint(5, 15))
        
        interface.get_input("\nPress Enter to continue...")
    
    def _tend_livestock(self, game_manager):
        """Tend to livestock on the farm.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.clear_screen()
        interface.display_message("=== Tend Livestock ===")
        
        # Display current livestock
        interface.display_message("Current livestock:")
        if self.livestock:
            for animal_type, count in self.livestock.items():
                interface.display_message(f"  {animal_type.capitalize()}: {count}")
        else:
            interface.display_message("  None")
        
        if not self.livestock:
            # Option to buy livestock
            buy = interface.display_menu("You don't have any livestock. Would you like to buy some?", ["Yes", "No"])
            
            if buy == 0:  # Yes
                self._buy_livestock(game_manager)
            else:
                interface.display_message("You decided not to buy any livestock.")
                interface.get_input("\nPress Enter to continue...")
            return
        
        # Choose livestock to tend
        livestock_types = list(self.livestock.keys())
        livestock_types = [animal_type.capitalize() for animal_type in livestock_types]
        choice = interface.display_menu("Which animals would you like to tend to?", livestock_types)
        
        animal_type = livestock_types[choice].lower()
        
        # Tend to the livestock
        interface.display_message(f"You spend time tending to your {animal_type}.")
        
        # Skill check for tending quality
        tending_quality = min(100, self.skills["farming"] + random.randint(-20, 20))
        if tending_quality >= 70:
            interface.display_message("Your animals are thriving under your care!")
            # Chance for animal reproduction
            if random.random() < 0.3:
                new_animals = random.randint(1, 2)
                self.livestock[animal_type] += new_animals
                interface.display_message(f"Your {animal_type} have produced {new_animals} offspring!")
        elif tending_quality >= 40:
            interface.display_message("Your animals are doing well.")
        else:
            interface.display_message("Your animals aren't doing very well.")
            # Chance for animal loss
            if random.random() < 0.2:
                lost_animals = min(1, self.livestock[animal_type])
                self.livestock[animal_type] -= lost_animals
                if self.livestock[animal_type] <= 0:
                    del self.livestock[animal_type]
                    interface.display_message(f"Unfortunately, all your {animal_type} have died.")
                else:
                    interface.display_message(f"Unfortunately, {lost_animals} of your {animal_type} have died.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _buy_livestock(self, game_manager):
        """Buy livestock for the farm.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.clear_screen()
        interface.display_message("=== Buy Livestock ===")
        
        # Choose livestock type
        livestock_types = ["Chickens", "Pigs", "Cows", "Sheep", "Goats"]
        livestock_prices = {"chickens": 2, "pigs": 10, "cows": 30, "sheep": 15, "goats": 12}
        
        choice = interface.display_menu("What type of livestock would you like to buy?", livestock_types)
        
        animal_type = livestock_types[choice].lower()
        price = livestock_prices[animal_type]
        
        # Choose amount to buy
        max_affordable = self.wealth // price
        if max_affordable <= 0:
            interface.display_message(f"You can't afford any {animal_type}. Each costs {price} coins.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        amount_options = [f"{i} ({i * price} coins)" for i in range(1, min(10, max_affordable + 1))]
        amount_choice = interface.display_menu(f"How many {animal_type} would you like to buy?", amount_options)
        
        amount = amount_choice + 1  # Convert to 1-based
        total_cost = amount * price
        
        # Confirm purchase
        confirm = interface.display_menu(
            f"Buy {amount} {animal_type} for {total_cost} coins?",
            ["Yes", "No"]
        )
        
        if confirm == 0:  # Yes
            self.wealth -= total_cost
            
            if animal_type in self.livestock:
                self.livestock[animal_type] += amount
            else:
                self.livestock[animal_type] = amount
            
            interface.display_message(f"You bought {amount} {animal_type} for {total_cost} coins.")
        else:
            interface.display_message("You decided not to buy any livestock.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _sell_produce(self, game_manager):
        """Sell farm produce at the market.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.clear_screen()
        interface.display_message("=== Sell Produce ===")
        
        # Check if player has anything to sell
        if not self.crops and not self.livestock:
            interface.display_message("You don't have any produce to sell.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Choose what to sell
        sell_options = []
        if self.crops:
            sell_options.append("Crops")
        if self.livestock:
            sell_options.append("Livestock")
        
        sell_options.append("Cancel")
        
        choice = interface.display_menu("What would you like to sell?", sell_options)
        
        if choice == len(sell_options) - 1:  # Cancel
            interface.display_message("You decided not to sell anything.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        if sell_options[choice] == "Crops":
            self._sell_crops(game_manager)
        else:
            self._sell_livestock(game_manager)
    
    def _sell_crops(self, game_manager):
        """Sell crops at the market.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.clear_screen()
        interface.display_message("=== Sell Crops ===")
        
        # Display current crops
        interface.display_message("Current crops:")
        for crop_type, acres in self.crops.items():
            interface.display_message(f"  {crop_type.capitalize()}: {acres} acres")
        
        # Choose crop to sell
        crop_types = list(self.crops.keys())
        crop_types = [crop_type.capitalize() for crop_type in crop_types]
        crop_types.append("Cancel")
        
        choice = interface.display_menu("Which crop would you like to sell?", crop_types)
        
        if choice == len(crop_types) - 1:  # Cancel
            interface.display_message("You decided not to sell any crops.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        crop_type = crop_types[choice].lower()
        
        # Choose amount to sell
        max_amount = self.crops[crop_type]
        amount_options = [f"{i} acre(s)" for i in range(1, max_amount + 1)]
        amount_choice = interface.display_menu(f"How many acres of {crop_type} would you like to sell?", amount_options)
        
        amount = amount_choice + 1  # Convert to 1-based
        
        # Calculate sale price based on harvest quality and market conditions
        base_price = {"wheat": 10, "barley": 8, "oats": 7, "rye": 9, "vegetables": 15}[crop_type]
        price_modifier = self.harvest_quality / 50.0  # 0.0 to 2.0
        market_modifier = random.uniform(0.8, 1.2)
        
        price_per_acre = int(base_price * price_modifier * market_modifier)
        total_price = price_per_acre * amount
        
        # Confirm sale
        confirm = interface.display_menu(
            f"Sell {amount} acre(s) of {crop_type} for {total_price} coins ({price_per_acre} per acre)?",
            ["Yes", "No"]
        )
        
        if confirm == 0:  # Yes
            self.crops[crop_type] -= amount
            if self.crops[crop_type] <= 0:
                del self.crops[crop_type]
            
            self.wealth += total_price
            
            interface.display_message(f"You sold {amount} acre(s) of {crop_type} for {total_price} coins.")
            
            # Skill improvement
            self.skills["trade"] = min(100, self.skills["trade"] + random.randint(1, 3))
        else:
            interface.display_message("You decided not to sell your crops.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _sell_livestock(self, game_manager):
        """Sell livestock at the market.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.clear_screen()
        interface.display_message("=== Sell Livestock ===")
        
        # Display current livestock
        interface.display_message("Current livestock:")
        for animal_type, count in self.livestock.items():
            interface.display_message(f"  {animal_type.capitalize()}: {count}")
        
        # Choose livestock to sell
        animal_types = list(self.livestock.keys())
        animal_types = [animal_type.capitalize() for animal_type in animal_types]
        animal_types.append("Cancel")
        
        choice = interface.display_menu("Which animals would you like to sell?", animal_types)
        
        if choice == len(animal_types) - 1:  # Cancel
            interface.display_message("You decided not to sell any livestock.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        animal_type = animal_types[choice].lower()
        
        # Choose amount to sell
        max_amount = self.livestock[animal_type]
        amount_options = [f"{i}" for i in range(1, max_amount + 1)]
        amount_choice = interface.display_menu(f"How many {animal_type} would you like to sell?", amount_options)
        
        amount = amount_choice + 1  # Convert to 1-based
        
        # Calculate sale price
        base_price = {"chickens": 3, "pigs": 15, "cows": 40, "sheep": 20, "goats": 18}[animal_type]
        market_modifier = random.uniform(0.8, 1.2)
        
        price_per_animal = int(base_price * market_modifier)
        total_price = price_per_animal * amount
        
        # Confirm sale
        confirm = interface.display_menu(
            f"Sell {amount} {animal_type} for {total_price} coins ({price_per_animal} per animal)?",
            ["Yes", "No"]
        )
        
        if confirm == 0:  # Yes
            self.livestock[animal_type] -= amount
            if self.livestock[animal_type] <= 0:
                del self.livestock[animal_type]
            
            self.wealth += total_price
            
            interface.display_message(f"You sold {amount} {animal_type} for {total_price} coins.")
            
            # Skill improvement
            self.skills["trade"] = min(100, self.skills["trade"] + random.randint(1, 3))
        else:
            interface.display_message("You decided not to sell your livestock.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _buy_land(self, game_manager):
        """Buy additional land for the farm.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.clear_screen()
        interface.display_message("=== Buy Land ===")
        interface.display_message(f"Current land: {self.land} acres")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        
        # Land price
        land_price = random.randint(40, 60)
        interface.display_message(f"Current land price: {land_price} coins per acre")
        
        # Calculate maximum affordable
        max_affordable = self.wealth // land_price
        if max_affordable <= 0:
            interface.display_message("You can't afford to buy any land right now.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Choose amount to buy
        amount_options = [f"{i} acre(s) ({i * land_price} coins)" for i in range(1, min(10, max_affordable + 1))]
        amount_options.append("Cancel")
        
        choice = interface.display_menu("How much land would you like to buy?", amount_options)
        
        if choice == len(amount_options) - 1:  # Cancel
            interface.display_message("You decided not to buy any land.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        amount = choice + 1  # Convert to 1-based
        total_cost = amount * land_price
        
        # Confirm purchase
        confirm = interface.display_menu(
            f"Buy {amount} acre(s) of land for {total_cost} coins?",
            ["Yes", "No"]
        )
        
        if confirm == 0:  # Yes
            self.wealth -= total_cost
            self.land += amount
            
            interface.display_message(f"You bought {amount} acre(s) of land for {total_cost} coins.")
            interface.display_message(f"You now have {self.land} acres of land.")
        else:
            interface.display_message("You decided not to buy any land.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _hire_help(self, game_manager):
        """Hire help for the farm.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.clear_screen()
        interface.display_message("=== Hire Help ===")
        
        # Check if player has enough wealth
        if self.wealth < 20:
            interface.display_message("You don't have enough wealth to hire help.")
            interface.display_message("You need at least 20 coins.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Choose type of help
        help_types = ["Farmhand (20 coins)", "Skilled Worker (50 coins)", "Cancel"]
        choice = interface.display_menu("What type of help would you like to hire?", help_types)
        
        if choice == 2:  # Cancel
            interface.display_message("You decided not to hire any help.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        if choice == 0:  # Farmhand
            cost = 20
            benefit = random.randint(5, 15)
        else:  # Skilled Worker
            cost = 50
            benefit = random.randint(15, 30)
        
        # Check if player has enough wealth
        if self.wealth < cost:
            interface.display_message(f"You don't have enough wealth to hire a {help_types[choice].split(' ')[0].lower()}.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Hire the help
        self.wealth -= cost
        self.harvest_quality = min(100, self.harvest_quality + benefit)
        
        interface.display_message(f"You hired a {help_types[choice].split(' ')[0].lower()} for {cost} coins.")
        interface.display_message(f"Your harvest quality has improved to {self.harvest_quality}/100.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def update_for_new_year(self):
        """Update character stats for a new year."""
        # Call base class implementation
        super().update_for_new_year()
        
        # Farmer-specific updates
        
        # Harvest crops
        total_crop_value = 0
        for crop_type, acres in list(self.crops.items()):
            base_yield = {"wheat": 10, "barley": 8, "oats": 7, "rye": 9, "vegetables": 15}[crop_type]
            yield_modifier = self.harvest_quality / 50.0  # 0.0 to 2.0
            weather_modifier = random.uniform(0.5, 1.5)
            
            crop_yield = int(base_yield * yield_modifier * weather_modifier * acres)
            total_crop_value += crop_yield
            
            # Clear crops after harvest
            del self.crops[crop_type]
        
        # Add harvest value to wealth
        self.wealth += total_crop_value
        
        # Reset harvest quality
        self.harvest_quality = 50
        
        # Livestock reproduction
        for animal_type, count in list(self.livestock.items()):
            # Chance for reproduction
            if count >= 2 and random.random() < 0.4:
                new_animals = random.randint(1, max(1, count // 3))
                self.livestock[animal_type] += new_animals
    
    def display_status(self, interface):
        """Display the character's status.
        
        Args:
            interface: The user interface.
        """
        interface.display_message(f"Land: {self.land} acres")
        
        interface.display_message("\nCrops:")
        if self.crops:
            for crop_type, acres in self.crops.items():
                interface.display_message(f"  {crop_type.capitalize()}: {acres} acres")
        else:
            interface.display_message("  None")
        
        interface.display_message("\nLivestock:")
        if self.livestock:
            for animal_type, count in self.livestock.items():
                interface.display_message(f"  {animal_type.capitalize()}: {count}")
        else:
            interface.display_message("  None")
        
        interface.display_message(f"\nHarvest Quality: {self.harvest_quality}/100")
    
    def _harvest_crops(self, game_manager):
        """Harvest crops from the farm.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Harvest Crops ===")
        
        # Check if there are crops to harvest
        if not self.crops:
            interface.display_message("You don't have any crops to harvest.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Display current crops
        interface.display_message("Your crops:")
        for crop_type, acres in self.crops.items():
            interface.display_message(f"  {crop_type.capitalize()}: {acres} acres")
        
        # Choose crop to harvest
        crop_types = list(self.crops.keys())
        crop_display = [f"{crop.capitalize()} ({self.crops[crop]} acres)" for crop in crop_types]
        
        choice = interface.display_menu("Which crop would you like to harvest?", crop_display)
        crop_type = crop_types[choice]
        
        # Calculate harvest yield based on farming skill and random factors
        acres = self.crops[crop_type]
        base_yield = acres * 5  # Base yield per acre
        skill_bonus = self.skills["farming"] / 100  # 0-1 bonus based on skill
        weather_factor = random.uniform(0.7, 1.3)  # Random weather effect
        
        total_yield = int(base_yield * (1 + skill_bonus) * weather_factor)
        
        # Add to storage
        if crop_type in self.storage:
            self.storage[crop_type] += total_yield
        else:
            self.storage[crop_type] = total_yield
        
        # Remove harvested crop from field
        self.crops[crop_type] = 0
        if self.crops[crop_type] <= 0:
            del self.crops[crop_type]
        
        # Health cost of harvesting
        health_cost = random.randint(3, 8)
        self.health = max(1, self.health - health_cost)
        
        # Skill improvement
        skill_gain = random.randint(1, 3)
        self.skills["farming"] = min(100, self.skills["farming"] + skill_gain)
        
        # Display results
        if weather_factor > 1.1:
            interface.display_message("The weather has been favorable for your crops!")
        elif weather_factor < 0.9:
            interface.display_message("Poor weather has affected your harvest.")
        
        interface.display_message(f"You harvested {total_yield} units of {crop_type}.")
        interface.display_message(f"Your farming skill improved by {skill_gain} points.")
        interface.display_message(f"The work was tiring. You lost {health_cost} health points.")
        interface.display_message(f"Current health: {self.health}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _rotate_crops(self, game_manager):
        """Rotate crops to improve soil fertility.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Rotate Crops ===")
        interface.display_message("Rotating crops helps maintain soil fertility and can improve future yields.")
        
        # Check if there are crops to rotate
        if not self.crops:
            interface.display_message("You don't have any crops to rotate.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Display current crops
        interface.display_message("Your crops:")
        for crop_type, acres in self.crops.items():
            interface.display_message(f"  {crop_type.capitalize()}: {acres} acres")
        
        # Choose crop to rotate
        crop_types = list(self.crops.keys())
        crop_display = [f"{crop.capitalize()} ({self.crops[crop]} acres)" for crop in crop_types]
        
        choice = interface.display_menu("Which crop would you like to rotate?", crop_display)
        crop_type = crop_types[choice]
        
        # Choose new crop
        new_crop_types = ["Wheat", "Barley", "Oats", "Rye", "Vegetables", "Legumes", "Fallow (rest the soil)"]
        new_choice = interface.display_menu(f"What would you like to plant instead of {crop_type}?", new_crop_types)
        new_crop_type = new_crop_types[new_choice].lower()
        
        # Calculate effects
        acres = self.crops[crop_type]
        
        # Remove old crop
        del self.crops[crop_type]
        
        # Add new crop or leave fallow
        if new_crop_type != "fallow (rest the soil)":
            if new_crop_type in self.crops:
                self.crops[new_crop_type] += acres
            else:
                self.crops[new_crop_type] = acres
            
            interface.display_message(f"You rotated {acres} acres from {crop_type} to {new_crop_type}.")
        else:
            interface.display_message(f"You decided to let {acres} acres of land rest to restore fertility.")
            # Leaving land fallow improves future yields
            self.soil_fertility = min(100, self.soil_fertility + 10)
            interface.display_message("The soil fertility has improved.")
        
        # Skill improvement
        skill_gain = random.randint(1, 2)
        self.skills["farming"] = min(100, self.skills["farming"] + skill_gain)
        interface.display_message(f"Your farming skill improved by {skill_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _manage_workers(self, game_manager):
        """Manage farm workers.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Manage Workers ===")
        interface.display_message(f"You currently have {self.helpers} workers on your farm.")
        
        options = [
            "Assign to crop fields",
            "Assign to livestock",
            "Train workers",
            "Pay bonuses",
            "Dismiss workers"
        ]
        
        choice = interface.display_menu("What would you like to do with your workers?", options)
        
        if choice == 0:  # Assign to crop fields
            if not self.crops:
                interface.display_message("You don't have any crops for workers to tend.")
            else:
                interface.display_message("You assign workers to tend the crop fields.")
                interface.display_message("This will improve your harvest yields.")
                self.worker_assignment = "crops"
                
                # Skill improvement for workers
                skill_gain = random.randint(1, 2)
                interface.display_message(f"Your workers' farming skills improved by {skill_gain} points.")
        
        elif choice == 1:  # Assign to livestock
            if not self.livestock:
                interface.display_message("You don't have any livestock for workers to tend.")
            else:
                interface.display_message("You assign workers to tend the livestock.")
                interface.display_message("This will improve your animals' health and productivity.")
                self.worker_assignment = "livestock"
                
                # Livestock health improvement
                for animal in self.livestock:
                    self.livestock_health[animal] = min(100, self.livestock_health.get(animal, 50) + 10)
                interface.display_message("Your livestock's health has improved.")
        
        elif choice == 2:  # Train workers
            cost = 10 * self.helpers
            if self.wealth < cost:
                interface.display_message(f"You don't have enough money to train your workers. Cost: {cost} coins.")
            else:
                self.wealth -= cost
                interface.display_message(f"You spend {cost} coins to train your workers.")
                interface.display_message("Their efficiency has improved, which will benefit your farm.")
                self.worker_efficiency = min(100, self.worker_efficiency + 5)
        
        elif choice == 3:  # Pay bonuses
            cost = 20 * self.helpers
            if self.wealth < cost:
                interface.display_message(f"You don't have enough money to pay bonuses. Cost: {cost} coins.")
            else:
                self.wealth -= cost
                interface.display_message(f"You spend {cost} coins on bonuses for your workers.")
                interface.display_message("Their morale has improved, which will benefit your farm.")
                self.worker_morale = min(100, self.worker_morale + 10)
        
        elif choice == 4:  # Dismiss workers
            if self.helpers <= 0:
                interface.display_message("You don't have any workers to dismiss.")
            else:
                dismiss_options = [f"{i+1} worker(s)" for i in range(self.helpers)]
                dismiss_choice = interface.display_menu("How many workers would you like to dismiss?", dismiss_options)
                dismiss_count = dismiss_choice + 1
                
                self.helpers -= dismiss_count
                interface.display_message(f"You dismissed {dismiss_count} worker(s).")
                interface.display_message(f"You now have {self.helpers} worker(s) on your farm.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _breed_horses(self, game_manager):
        """Breed horses for profit or farm use.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Breed Horses ===")
        
        # Check if player has enough horses
        if self.livestock.get("horses", 0) < 2:
            interface.display_message("You need at least 2 horses to breed them.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        interface.display_message(f"You currently have {self.livestock['horses']} horses.")
        
        # Calculate breeding success based on farming skill and random chance
        skill_factor = self.skills["farming"] / 100  # 0-1 based on farming skill
        success_chance = 0.3 + (skill_factor * 0.4)  # 30-70% chance based on skill
        
        if random.random() < success_chance:
            # Successful breeding
            foals = random.randint(1, 2)
            self.livestock["horses"] += foals
            
            interface.display_message(f"Your breeding efforts were successful! You have {foals} new foal(s).")
            interface.display_message(f"You now have {self.livestock['horses']} horses.")
            
            # Skill improvement
            skill_gain = random.randint(2, 4)
            self.skills["farming"] = min(100, self.skills["farming"] + skill_gain)
            interface.display_message(f"Your farming skill improved by {skill_gain} points.")
            
            # Wealth potential
            potential_value = foals * 50
            interface.display_message(f"The new foal(s) could be worth up to {potential_value} coins when grown.")
        else:
            # Unsuccessful breeding
            interface.display_message("Unfortunately, your breeding efforts were unsuccessful this time.")
            
            # Small skill improvement
            skill_gain = random.randint(1, 2)
            self.skills["farming"] = min(100, self.skills["farming"] + skill_gain)
            interface.display_message(f"Your farming skill still improved by {skill_gain} points from the experience.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _improve_livestock(self, game_manager):
        """Improve the quality of livestock through selective breeding and better care.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Improve Livestock ===")
        
        # Check if player has livestock
        if not self.livestock:
            interface.display_message("You don't have any livestock to improve.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Display current livestock
        interface.display_message("Your livestock:")
        for animal, count in self.livestock.items():
            quality = self.livestock_quality.get(animal, 50)
            interface.display_message(f"  {animal.capitalize()}: {count} (Quality: {quality}/100)")
        
        # Choose livestock to improve
        livestock_types = list(self.livestock.keys())
        livestock_display = [f"{animal.capitalize()} ({self.livestock[animal]} head)" for animal in livestock_types]
        
        choice = interface.display_menu("Which livestock would you like to improve?", livestock_display)
        animal_type = livestock_types[choice]
        
        # Calculate improvement based on farming skill and random factors
        skill_factor = self.skills["farming"] / 100  # 0-1 based on farming skill
        base_improvement = 5
        improvement = base_improvement + int(skill_factor * 10) + random.randint(-2, 5)
        
        # Cost of improvement
        cost = self.livestock[animal_type] * 5
        
        if self.wealth < cost:
            interface.display_message(f"You don't have enough money to improve your {animal_type}. Cost: {cost} coins.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Apply improvement
        self.wealth -= cost
        current_quality = self.livestock_quality.get(animal_type, 50)
        self.livestock_quality[animal_type] = min(100, current_quality + improvement)
        
        # Skill improvement
        skill_gain = random.randint(1, 3)
        self.skills["farming"] = min(100, self.skills["farming"] + skill_gain)
        
        interface.display_message(f"You spend {cost} coins on better feed, care, and selective breeding for your {animal_type}.")
        interface.display_message(f"Their quality improved by {improvement} points.")
        interface.display_message(f"Current {animal_type} quality: {self.livestock_quality[animal_type]}/100")
        interface.display_message(f"Your farming skill improved by {skill_gain} points.")
        interface.display_message("Higher quality livestock will produce more and better products.")
        
        interface.get_input("\nPress Enter to continue...") 