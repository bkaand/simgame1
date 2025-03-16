"""
Merchant - Character role class for merchants
"""
import random
from game.characters.character import Character

class Merchant(Character):
    """Character role class for merchants."""
    
    def __init__(self, name, gender, birth_year=None):
        """Initialize a new merchant character.
        
        Args:
            name: The character's name.
            gender: The character's gender.
            birth_year: The character's birth year (optional).
        """
        super().__init__(name, gender, "merchant", birth_year)
        
        # Merchants start with moderate wealth
        self.wealth = random.randint(100, 500)
        
        # Merchant-specific properties
        self.inventory = {}  # Type -> quantity
        self.trade_reputation = random.randint(30, 70)  # Reputation among merchants (0-100)
        
        # Initialize with some random goods
        self._initialize_inventory()
        
        # Adjust skills for role
        self._adjust_skills_for_role()
    
    def _initialize_inventory(self):
        """Initialize the merchant's inventory with some random goods."""
        possible_goods = ["cloth", "spices", "grain", "tools", "leather", "pottery", "wine"]
        
        # Add 2-4 random goods to inventory
        num_goods = random.randint(2, 4)
        for _ in range(num_goods):
            good = random.choice(possible_goods)
            quantity = random.randint(5, 20)
            
            if good in self.inventory:
                self.inventory[good] += quantity
            else:
                self.inventory[good] = quantity
    
    def _adjust_skills_for_role(self):
        """Adjust skills based on character role."""
        # Merchants are better at trade
        self.skills["trade"] += random.randint(20, 40)
        
        # Merchants also have some diplomacy skills
        self.skills["diplomacy"] += random.randint(5, 15)
        
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
        
        # Add merchant-specific actions
        merchant_actions = ["Trade Goods"]
        
        actions.extend(merchant_actions)
        return actions
    
    def perform_action(self, action, game_manager):
        """Perform an action.
        
        Args:
            action: The name of the action to perform.
            game_manager: The game manager.
        """
        if action == "Trade Goods":
            self._trade_goods(game_manager)
        else:
            # Use base class implementation for common actions
            super().perform_action(action, game_manager)
    
    def _trade_goods(self, game_manager):
        """Trade goods at a market.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Trade Goods ===")
        
        # Choose whether to buy or sell
        choice = interface.display_menu("Would you like to buy or sell goods?", ["Buy", "Sell"])
        
        if choice == 0:  # Buy
            self._buy_goods(game_manager)
        else:  # Sell
            self._sell_goods(game_manager)
    
    def _buy_goods(self, game_manager):
        """Buy goods at the market.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Buy Goods ===")
        
        # Available goods to buy
        available_goods = {
            "cloth": {"base_price": 10, "quantity": random.randint(10, 30)},
            "spices": {"base_price": 25, "quantity": random.randint(5, 15)},
            "grain": {"base_price": 5, "quantity": random.randint(20, 50)},
            "tools": {"base_price": 15, "quantity": random.randint(8, 20)},
            "leather": {"base_price": 12, "quantity": random.randint(10, 25)},
            "pottery": {"base_price": 8, "quantity": random.randint(15, 35)},
            "wine": {"base_price": 20, "quantity": random.randint(5, 20)}
        }
        
        # Display available goods
        interface.display_message("Available goods:")
        good_options = []
        for good, details in available_goods.items():
            # Apply random price fluctuation
            price_fluctuation = random.uniform(0.8, 1.2)
            price = int(details["base_price"] * price_fluctuation)
            
            # Apply trade skill discount
            trade_discount = 1.0 - (self.skills["trade"] / 200)  # 0-50% discount based on trade skill
            final_price = max(1, int(price * trade_discount))
            
            # Update price in available_goods
            available_goods[good]["price"] = final_price
            
            good_desc = f"{good.capitalize()} - {details['quantity']} available at {final_price} coins each"
            good_options.append(good_desc)
            interface.display_message(f"  {good_desc}")
        
        # Add option to cancel
        good_options.append("Cancel purchase")
        
        # Let player choose a good to buy
        choice = interface.display_menu("What would you like to buy?", good_options)
        
        if choice == len(good_options) - 1:  # Cancel option
            interface.display_message("You decide not to buy anything.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Get the chosen good
        chosen_good = list(available_goods.keys())[choice]
        good_details = available_goods[chosen_good]
        
        # Ask for quantity
        max_affordable = min(good_details["quantity"], self.wealth // good_details["price"])
        if max_affordable <= 0:
            interface.display_message(f"You cannot afford any {chosen_good} at the current price.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        quantity_options = [str(i+1) for i in range(max_affordable)]
        quantity_choice = interface.display_menu(f"How many {chosen_good} would you like to buy?", quantity_options)
        quantity = quantity_choice + 1  # Convert to 1-based
        
        # Calculate total cost
        total_cost = quantity * good_details["price"]
        
        # Confirm purchase
        confirm = interface.display_menu(f"Purchase {quantity} {chosen_good} for {total_cost} coins?", ["Yes", "No"])
        if confirm == 1:  # No
            interface.display_message("Purchase canceled.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Complete purchase
        self.wealth -= total_cost
        
        # Add to inventory
        if chosen_good in self.inventory:
            self.inventory[chosen_good] += quantity
        else:
            self.inventory[chosen_good] = quantity
        
        # Display results
        interface.display_message(f"You purchased {quantity} {chosen_good} for {total_cost} coins.")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        
        # Small trade skill improvement
        skill_gain = random.randint(1, 2)
        self.skills["trade"] = min(100, self.skills["trade"] + skill_gain)
        interface.display_message(f"Your trade skill improved by {skill_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _sell_goods(self, game_manager):
        """Sell goods at the market.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Sell Goods ===")
        
        # Check if player has goods to sell
        if not self.inventory:
            interface.display_message("You don't have any goods to sell.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Display inventory
        interface.display_message("Your inventory:")
        good_options = []
        for good, quantity in self.inventory.items():
            good_desc = f"{good.capitalize()} - {quantity} in stock"
            good_options.append(good_desc)
            interface.display_message(f"  {good_desc}")
        
        # Add option to cancel
        good_options.append("Cancel sale")
        
        # Let player choose a good to sell
        choice = interface.display_menu("What would you like to sell?", good_options)
        
        if choice == len(good_options) - 1:  # Cancel option
            interface.display_message("You decide not to sell anything.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Get the chosen good
        chosen_good = list(self.inventory.keys())[choice]
        quantity_in_stock = self.inventory[chosen_good]
        
        # Base prices for goods
        base_prices = {
            "cloth": 10,
            "spices": 25,
            "grain": 5,
            "tools": 15,
            "leather": 12,
            "pottery": 8,
            "wine": 20
        }
        
        # Calculate selling price with random fluctuation and trade skill bonus
        base_price = base_prices.get(chosen_good, 10)
        price_fluctuation = random.uniform(0.8, 1.2)
        trade_bonus = 1.0 + (self.skills["trade"] / 200)  # 0-50% bonus based on trade skill
        selling_price = max(1, int(base_price * price_fluctuation * trade_bonus))
        
        # Ask for quantity
        quantity_options = [str(i+1) for i in range(quantity_in_stock)]
        quantity_choice = interface.display_menu(f"How many {chosen_good} would you like to sell at {selling_price} coins each?", quantity_options)
        quantity = quantity_choice + 1  # Convert to 1-based
        
        # Calculate total earnings
        total_earnings = quantity * selling_price
        
        # Confirm sale
        confirm = interface.display_menu(f"Sell {quantity} {chosen_good} for {total_earnings} coins?", ["Yes", "No"])
        if confirm == 1:  # No
            interface.display_message("Sale canceled.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Complete sale
        self.wealth += total_earnings
        
        # Remove from inventory
        self.inventory[chosen_good] -= quantity
        if self.inventory[chosen_good] <= 0:
            del self.inventory[chosen_good]
        
        # Display results
        interface.display_message(f"You sold {quantity} {chosen_good} for {total_earnings} coins.")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        
        # Trade skill improvement
        skill_gain = random.randint(1, 2)
        self.skills["trade"] = min(100, self.skills["trade"] + skill_gain)
        interface.display_message(f"Your trade skill improved by {skill_gain} points.")
        
        # Trade reputation improvement
        rep_gain = random.randint(1, 2)
        self.trade_reputation = min(100, self.trade_reputation + rep_gain)
        interface.display_message(f"Your trade reputation improved by {rep_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def display_status(self, interface):
        """Display the character's status.
        
        Args:
            interface: The user interface.
        """
        interface.display_message(f"Trade Skill: {self.skills['trade']}/100")
        interface.display_message(f"Trade Reputation: {self.trade_reputation}/100")
        
        # Display inventory
        if self.inventory:
            interface.display_message("\nInventory:")
            for good, quantity in self.inventory.items():
                interface.display_message(f"  {good.capitalize()}: {quantity}")
        else:
            interface.display_message("\nInventory: Empty") 