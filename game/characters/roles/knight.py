"""
Knight - Character role class for knights
"""
import random
from game.characters.character import Character

class Knight(Character):
    """Character role class for knights."""
    
    def __init__(self, name, gender, birth_year=None):
        """Initialize a new knight character.
        
        Args:
            name: The character's name.
            gender: The character's gender.
            birth_year: The character's birth year (optional).
        """
        super().__init__(name, gender, "knight", birth_year)
        
        # Knights start with moderate wealth
        self.wealth = random.randint(100, 500)
        
        # Knight-specific properties
        self.lord = None  # The knight's lord (if any)
        self.reputation = random.randint(30, 70)  # Reputation among peers (0-100)
        self.tournament_wins = 0  # Number of tournament wins
        self.tournament_losses = 0  # Number of tournament losses
        self.equipment_quality = random.randint(30, 70)  # Quality of armor and weapons (0-100)
        
        # Adjust skills for role
        self._adjust_skills_for_role()
    
    def _adjust_skills_for_role(self):
        """Adjust skills based on character role."""
        # Knights are better at combat
        self.skills["combat"] += random.randint(20, 40)
        
        # Knights also have some diplomacy skills
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
        
        # Add knight-specific actions
        knight_actions = ["Train Combat"]
        
        # Add conditional actions
        if self.wealth >= 50:
            knight_actions.append("Participate in Tournament")
        
        if self.lord is None:
            knight_actions.append("Seek Lord to Serve")
        else:
            knight_actions.append("Serve Lord")
        
        if self.wealth >= 100:
            knight_actions.append("Improve Equipment")
        
        actions.extend(knight_actions)
        return actions
    
    def perform_action(self, action, game_manager):
        """Perform an action.
        
        Args:
            action: The name of the action to perform.
            game_manager: The game manager.
        """
        if action == "Train Combat":
            self._train_combat(game_manager)
        elif action == "Participate in Tournament":
            self._participate_in_tournament(game_manager)
        elif action == "Seek Lord to Serve":
            self._seek_lord(game_manager)
        elif action == "Serve Lord":
            self._serve_lord(game_manager)
        elif action == "Improve Equipment":
            self._improve_equipment(game_manager)
        else:
            # Use base class implementation for common actions
            super().perform_action(action, game_manager)
    
    def _train_combat(self, game_manager):
        """Train to improve combat skills.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Train Combat ===")
        interface.display_message("You spend time training your combat skills.")
        
        # Calculate training effectiveness based on attributes and random chance
        strength_factor = self.attributes["strength"] / 100  # 0-1 based on strength
        dexterity_factor = self.attributes["dexterity"] / 100  # 0-1 based on dexterity
        
        base_improvement = 3
        improvement = base_improvement + int(strength_factor * 3) + int(dexterity_factor * 3) + random.randint(0, 2)
        
        # Apply improvement
        old_skill = self.skills["combat"]
        self.skills["combat"] = min(100, self.skills["combat"] + improvement)
        actual_improvement = self.skills["combat"] - old_skill
        
        # Health cost of training
        health_cost = random.randint(3, 8)
        self.health = max(1, self.health - health_cost)
        
        # Display results
        interface.display_message(f"Your combat skill improved by {actual_improvement} points.")
        interface.display_message(f"Current combat skill: {self.skills['combat']}/100")
        interface.display_message(f"The training was tiring. You lost {health_cost} health points.")
        interface.display_message(f"Current health: {self.health}/100")
        
        # Chance to improve strength or dexterity
        if random.random() < 0.2:  # 20% chance
            attribute = random.choice(["strength", "dexterity"])
            gain = random.randint(1, 2)
            self.attributes[attribute] = min(100, self.attributes[attribute] + gain)
            interface.display_message(f"Your {attribute} improved by {gain} points from the training.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _participate_in_tournament(self, game_manager):
        """Participate in a tournament.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Tournament ===")
        
        # Check if player has enough money for entry fee
        entry_fee = 50
        if self.wealth < entry_fee:
            interface.display_message(f"You don't have enough money to pay the tournament entry fee of {entry_fee} coins.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Pay entry fee
        self.wealth -= entry_fee
        interface.display_message(f"You pay the entry fee of {entry_fee} coins to participate in the tournament.")
        
        # Determine tournament difficulty (1-5)
        tournament_tier = random.randint(1, 5)
        tier_names = ["local", "regional", "kingdom", "grand", "royal"]
        tournament_name = f"{tier_names[tournament_tier-1]} tournament"
        
        interface.display_message(f"You are participating in a {tournament_name}.")
        
        # Simulate tournament rounds
        rounds = tournament_tier + 1
        current_round = 1
        eliminated = False
        
        while current_round <= rounds and not eliminated:
            # Opponent skill increases with rounds and tournament tier
            opponent_base_skill = 30 + (tournament_tier * 10) + (current_round * 5)
            opponent_skill = max(10, min(95, opponent_base_skill + random.randint(-10, 10)))
            
            interface.display_message(f"\nRound {current_round}:")
            interface.display_message(f"You face an opponent with combat skill of approximately {opponent_skill}.")
            
            # Calculate success chance based on combat skill, equipment, and attributes
            player_effective_skill = self.skills["combat"] + (self.equipment_quality / 10)
            player_attribute_bonus = (self.attributes["strength"] + self.attributes["dexterity"]) / 40
            
            success_chance = 0.5 + ((player_effective_skill - opponent_skill) / 100) + player_attribute_bonus
            success_chance = max(0.1, min(0.9, success_chance))  # Bound between 10% and 90%
            
            # Determine outcome
            if random.random() < success_chance:
                # Win the round
                interface.display_message("You defeat your opponent and advance to the next round!")
                
                # Small health cost
                health_cost = random.randint(1, 5)
                self.health = max(1, self.health - health_cost)
                
                # Small combat skill improvement
                skill_gain = random.randint(1, 2)
                self.skills["combat"] = min(100, self.skills["combat"] + skill_gain)
                
                current_round += 1
            else:
                # Lose the round
                interface.display_message("Your opponent defeats you. You are eliminated from the tournament.")
                
                # Larger health cost from defeat
                health_cost = random.randint(5, 15)
                self.health = max(1, self.health - health_cost)
                
                eliminated = True
                self.tournament_losses += 1
        
        # Tournament results
        if not eliminated:
            # Won the tournament
            interface.display_message("\nCongratulations! You have won the tournament!")
            
            # Calculate prize money based on tournament tier
            prize = entry_fee * (tournament_tier * 3)
            self.wealth += prize
            interface.display_message(f"You receive a prize of {prize} coins.")
            
            # Reputation gain
            rep_gain = tournament_tier * 5
            self.reputation = min(100, self.reputation + rep_gain)
            interface.display_message(f"Your reputation increases by {rep_gain} points.")
            
            # Record win
            self.tournament_wins += 1
        else:
            # Consolation for participating
            interface.display_message("\nDespite not winning, you gained valuable experience in the tournament.")
            
            # Small reputation gain just for participating
            rep_gain = random.randint(1, 3)
            self.reputation = min(100, self.reputation + rep_gain)
            interface.display_message(f"Your reputation increases slightly by {rep_gain} points.")
        
        interface.display_message(f"\nTournament record: {self.tournament_wins} wins, {self.tournament_losses} losses")
        interface.display_message(f"Current health: {self.health}/100")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        interface.display_message(f"Current reputation: {self.reputation}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _seek_lord(self, game_manager):
        """Seek a lord to serve.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Seek Lord to Serve ===")
        interface.display_message("You search for a noble lord who might accept your service.")
        
        # List of potential lords with their wealth and prestige
        potential_lords = [
            {"name": "Baron Harwick", "wealth": 3, "prestige": 2},
            {"name": "Count Blackwood", "wealth": 4, "prestige": 3},
            {"name": "Duke Montfort", "wealth": 5, "prestige": 4},
            {"name": "Lord Eastley", "wealth": 2, "prestige": 2},
            {"name": "Viscount Redfield", "wealth": 3, "prestige": 3}
        ]
        
        # Filter lords based on player's reputation
        available_lords = []
        for lord in potential_lords:
            required_reputation = (lord["prestige"] * 15) + 10
            if self.reputation >= required_reputation:
                available_lords.append(lord)
        
        if not available_lords:
            interface.display_message("Unfortunately, no lords are willing to accept your service at this time.")
            interface.display_message("You should improve your reputation by winning tournaments or performing other honorable deeds.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Display available lords
        interface.display_message("\nThe following lords might accept your service:")
        lord_options = []
        for i, lord in enumerate(available_lords):
            wealth_stars = "★" * lord["wealth"]
            prestige_stars = "★" * lord["prestige"]
            lord_desc = f"{lord['name']} (Wealth: {wealth_stars}, Prestige: {prestige_stars})"
            lord_options.append(lord_desc)
            interface.display_message(f"{i+1}. {lord_desc}")
        
        # Add option to decline all
        lord_options.append("Decline all offers")
        
        # Let player choose
        choice = interface.display_menu("Which lord would you like to serve?", lord_options)
        
        if choice < len(available_lords):
            # Player chose a lord
            chosen_lord = available_lords[choice]
            self.lord = chosen_lord["name"]
            
            interface.display_message(f"You pledge your service to {self.lord}.")
            interface.display_message("You are now a sworn knight in their service.")
            
            # Reputation gain
            rep_gain = chosen_lord["prestige"] * 2
            self.reputation = min(100, self.reputation + rep_gain)
            interface.display_message(f"Your reputation increases by {rep_gain} points.")
            
            # Initial payment
            payment = chosen_lord["wealth"] * 20
            self.wealth += payment
            interface.display_message(f"You receive an initial payment of {payment} coins.")
        else:
            # Player declined all offers
            interface.display_message("You decide not to enter anyone's service for now.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _serve_lord(self, game_manager):
        """Serve your lord by performing duties.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Serve Lord ===")
        interface.display_message(f"You are currently serving {self.lord}.")
        
        # List of possible duties
        duties = [
            "Guard duty",
            "Escort mission",
            "Training recruits",
            "Border patrol",
            "Hunt bandits"
        ]
        
        # Let player choose a duty
        choice = interface.display_menu("What duty would you like to perform?", duties)
        chosen_duty = duties[choice]
        
        interface.display_message(f"You perform {chosen_duty} for your lord.")
        
        # Calculate success chance based on relevant skills and attributes
        if chosen_duty == "Guard duty":
            relevant_skill = self.skills["combat"]
            relevant_attribute = self.attributes["strength"]
            difficulty = 30  # Relatively easy
        elif chosen_duty == "Escort mission":
            relevant_skill = (self.skills["combat"] + self.skills["diplomacy"]) / 2
            relevant_attribute = self.attributes["dexterity"]
            difficulty = 50  # Moderate
        elif chosen_duty == "Training recruits":
            relevant_skill = self.skills["combat"]
            relevant_attribute = self.attributes["charisma"]
            difficulty = 40  # Moderate
        elif chosen_duty == "Border patrol":
            relevant_skill = self.skills["combat"]
            relevant_attribute = self.attributes["dexterity"]
            difficulty = 60  # Challenging
        elif chosen_duty == "Hunt bandits":
            relevant_skill = self.skills["combat"]
            relevant_attribute = (self.attributes["strength"] + self.attributes["dexterity"]) / 2
            difficulty = 70  # Very challenging
        
        # Calculate success chance
        success_chance = 0.5 + ((relevant_skill - difficulty) / 100) + (relevant_attribute / 200)
        success_chance = max(0.1, min(0.9, success_chance))  # Bound between 10% and 90%
        
        # Determine outcome
        if random.random() < success_chance:
            # Success
            interface.display_message("You successfully complete your duty!")
            
            # Calculate rewards based on duty difficulty
            base_payment = 20 + (difficulty / 2)
            payment = int(base_payment + random.randint(-5, 5))
            self.wealth += payment
            interface.display_message(f"You receive a payment of {payment} coins.")
            
            # Reputation gain
            rep_gain = int(difficulty / 10) + random.randint(1, 3)
            self.reputation = min(100, self.reputation + rep_gain)
            interface.display_message(f"Your reputation increases by {rep_gain} points.")
            
            # Skill improvement
            if chosen_duty in ["Guard duty", "Border patrol", "Hunt bandits"]:
                skill_gain = random.randint(1, 2)
                self.skills["combat"] = min(100, self.skills["combat"] + skill_gain)
                interface.display_message(f"Your combat skill improved by {skill_gain} points.")
            elif chosen_duty == "Escort mission":
                skill_gain = random.randint(1, 2)
                self.skills["diplomacy"] = min(100, self.skills["diplomacy"] + skill_gain)
                interface.display_message(f"Your diplomacy skill improved by {skill_gain} points.")
            elif chosen_duty == "Training recruits":
                skill_gain = random.randint(1, 2)
                if random.random() < 0.5:
                    self.skills["combat"] = min(100, self.skills["combat"] + skill_gain)
                    interface.display_message(f"Your combat skill improved by {skill_gain} points.")
                else:
                    self.attributes["charisma"] = min(100, self.attributes["charisma"] + skill_gain)
                    interface.display_message(f"Your charisma improved by {skill_gain} points.")
        else:
            # Failure
            interface.display_message("Unfortunately, you fail to complete your duty satisfactorily.")
            
            # Small payment
            payment = int((20 + (difficulty / 2)) / 2)
            self.wealth += payment
            interface.display_message(f"You receive a reduced payment of {payment} coins.")
            
            # Reputation loss
            rep_loss = random.randint(1, 5)
            self.reputation = max(0, self.reputation - rep_loss)
            interface.display_message(f"Your reputation decreases by {rep_loss} points.")
        
        # Health cost based on duty
        if chosen_duty in ["Guard duty", "Training recruits"]:
            health_cost = random.randint(1, 5)  # Light duty
        elif chosen_duty in ["Escort mission", "Border patrol"]:
            health_cost = random.randint(3, 8)  # Moderate duty
        else:  # Hunt bandits
            health_cost = random.randint(5, 15)  # Heavy duty
        
        self.health = max(1, self.health - health_cost)
        interface.display_message(f"The duty was tiring. You lost {health_cost} health points.")
        
        interface.display_message(f"Current health: {self.health}/100")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        interface.display_message(f"Current reputation: {self.reputation}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _improve_equipment(self, game_manager):
        """Improve equipment quality by purchasing upgrades or maintaining gear.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Improve Equipment ===")
        interface.display_message(f"Current equipment quality: {self.equipment_quality}/100")
        
        # Options for improvement
        options = [
            "Basic maintenance (Cost: 20 coins, Small improvement)",
            "Purchase new armor pieces (Cost: 50 coins, Moderate improvement)",
            "Commission custom equipment (Cost: 100 coins, Large improvement)"
        ]
        
        # Let player choose an option
        choice = interface.display_menu("How would you like to improve your equipment?", options)
        
        # Calculate costs and improvements based on choice
        if choice == 0:  # Basic maintenance
            cost = 20
            base_improvement = 3
        elif choice == 1:  # New armor pieces
            cost = 50
            base_improvement = 8
        else:  # Custom equipment
            cost = 100
            base_improvement = 15
        
        # Check if player has enough money
        if self.wealth < cost:
            interface.display_message(f"You don't have enough money. This option costs {cost} coins.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Pay for improvement
        self.wealth -= cost
        interface.display_message(f"You spend {cost} coins on equipment improvements.")
        
        # Calculate actual improvement with some randomness
        improvement = base_improvement + random.randint(-2, 2)
        improvement = max(1, improvement)  # Ensure at least some improvement
        
        # Apply improvement
        old_quality = self.equipment_quality
        self.equipment_quality = min(100, self.equipment_quality + improvement)
        actual_improvement = self.equipment_quality - old_quality
        
        # Display results
        interface.display_message(f"Your equipment quality improved by {actual_improvement} points.")
        interface.display_message(f"New equipment quality: {self.equipment_quality}/100")
        interface.display_message(f"Remaining wealth: {self.wealth} coins")
        
        # Explain benefits
        interface.display_message("\nBetter equipment will improve your performance in tournaments and duties.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def display_status(self, interface):
        """Display the character's status.
        
        Args:
            interface: The user interface.
        """
        interface.display_message(f"Combat Skill: {self.skills['combat']}/100")
        interface.display_message(f"Equipment Quality: {self.equipment_quality}/100")
        interface.display_message(f"Reputation: {self.reputation}/100")
        interface.display_message(f"Tournament Record: {self.tournament_wins} wins, {self.tournament_losses} losses")
        
        if self.lord:
            interface.display_message(f"Serving: {self.lord}")
        else:
            interface.display_message("Not currently serving any lord") 