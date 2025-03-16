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
        self.wealth = random.randint(100, 300)
        
        # Merchant-specific properties
        self.inventory = {}  # Type -> quantity
        self.trade_routes = []
        self.shop_level = 1
        self.employees = 0
        self.last_trade_result = None
        
        # Initialize starting inventory
        self.inventory = {
            "food": random.randint(5, 15),
            "cloth": random.randint(3, 8),
            "tools": random.randint(2, 5)
        }
        
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
        merchant_actions = ["Trade Goods", "Hire Employee", "Upgrade Shop"]
        
        actions.extend(merchant_actions)
        return actions
    
    def perform_action(self, action, game_manager):
        """Perform an action.
        
        Args:
            action: The name of the action to perform.
            game_manager: The game manager.
        """
        if action == "Trade Goods":
            self._trade(game_manager)
        elif action == "Hire Employee":
            self._hire_employee(game_manager)
        elif action == "Upgrade Shop":
            self._upgrade_shop(game_manager)
        else:
            # Use base class implementation for common actions
            super().perform_action(action, game_manager)
    
    def _trade(self, game_manager):
        """Conduct trade with consideration for reputation effects."""
        # Get reputation modifiers
        merchant_mod = self.reputation.get_reputation_effects("merchants").get("buy_discount", 1.0)
        noble_mod = self.reputation.get_reputation_effects("nobility").get("trade_profit", 1.0)
        
        base_success_chance = 0.6 + (self.skills["trade"] / 200)  # 60-85% base chance
        success_chance = min(0.95, base_success_chance * merchant_mod)
        
        if random.random() < success_chance:
            # Successful trade
            base_profit = random.randint(20, 50) * self.shop_level
            profit = int(base_profit * noble_mod)
            
            self.wealth += profit
            self.skills["trade"] = min(100, self.skills["trade"] + random.randint(1, 3))
            
            # Improve reputation with merchants and nobility
            self.reputation.adjust_reputation("merchants", random.randint(1, 3))
            if profit > 30:
                self.reputation.adjust_reputation("nobility", 1)
            
            self.last_trade_result = f"Trade successful! Earned {profit} coins."
            return True
        else:
            # Failed trade
            loss = random.randint(10, 30) * self.shop_level
            self.wealth = max(0, self.wealth - loss)
            
            # Small reputation loss
            self.reputation.adjust_reputation("merchants", -1)
            
            self.last_trade_result = f"Trade failed. Lost {loss} coins."
            return False
    
    def _hire_employee(self, game_manager):
        """Hire an employee with reputation effects."""
        cost = 50 * (self.employees + 1)
        
        if self.wealth >= cost:
            # Reputation affects employee quality
            peasant_mod = self.reputation.get_reputation_effects("peasants").get("worker_quality", 1.0)
            merchant_mod = self.reputation.get_reputation_effects("merchants").get("hire_discount", 1.0)
            
            # Adjust cost based on merchant reputation
            final_cost = int(cost * merchant_mod)
            
            self.wealth -= final_cost
            self.employees += 1
            
            # Employee quality affects skill gain
            skill_gain = int(random.randint(2, 5) * peasant_mod)
            self.skills["trade"] = min(100, self.skills["trade"] + skill_gain)
            
            # Improve reputation with peasants
            self.reputation.adjust_reputation("peasants", 2)
            
            return f"Hired employee for {final_cost} coins. Trade skill increased by {skill_gain}."
        return "Not enough money to hire an employee."
    
    def _upgrade_shop(self, game_manager):
        """Upgrade shop with reputation effects."""
        base_cost = 200 * self.shop_level
        
        # Reputation affects upgrade costs
        merchant_mod = self.reputation.get_reputation_effects("merchants").get("upgrade_discount", 1.0)
        cost = int(base_cost * merchant_mod)
        
        if self.wealth >= cost:
            self.wealth -= cost
            self.shop_level += 1
            
            # Significant reputation gain with merchants
            self.reputation.adjust_reputation("merchants", 5)
            
            # Small reputation gain with nobility due to improved establishment
            self.reputation.adjust_reputation("nobility", 2)
            
            return f"Shop upgraded to level {self.shop_level}!"
        return "Not enough money to upgrade shop."
    
    def display_status(self, interface):
        """Display merchant status with reputation effects."""
        super().display_status(interface)
        
        interface.display_message(f"\nShop Level: {self.shop_level}")
        interface.display_message(f"Employees: {self.employees}")
        
        if self.last_trade_result:
            interface.display_message(f"\nLast Trade Result: {self.last_trade_result}")
        
        interface.display_message("\nInventory:")
        for item, amount in self.inventory.items():
            interface.display_message(f"{item.capitalize()}: {amount}")
        
        # Display relevant reputation bonuses
        merchant_effects = self.reputation.get_reputation_effects("merchants")
        noble_effects = self.reputation.get_reputation_effects("nobility")
        
        trade_bonus = (merchant_effects.get("buy_discount", 1.0) - 1) * 100
        profit_bonus = (noble_effects.get("trade_profit", 1.0) - 1) * 100
        
        if trade_bonus != 0 or profit_bonus != 0:
            interface.display_message("\nTrade Bonuses:")
            if trade_bonus != 0:
                interface.display_message(f"Purchase Discount: {trade_bonus:+.1f}%")
            if profit_bonus != 0:
                interface.display_message(f"Profit Bonus: {profit_bonus:+.1f}%") 