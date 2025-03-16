"""
Priest - Character role class for priests
"""
import random
from game.characters.character import Character

class Priest(Character):
    """Character role class for priests."""
    
    def __init__(self, name, gender, birth_year=None):
        """Initialize a new priest character.
        
        Args:
            name: The character's name.
            gender: The character's gender.
            birth_year: The character's birth year (optional).
        """
        super().__init__(name, gender, "priest", birth_year)
        
        # Priests start with modest wealth
        self.wealth = random.randint(20, 100)
        
        # Priest-specific properties
        self.church_rank = 1  # 1=Novice, 2=Priest, 3=Bishop, 4=Archbishop
        self.piety = random.randint(40, 80)  # Religious devotion (0-100)
        self.congregation_size = random.randint(20, 100)  # Size of congregation
        self.church_influence = random.randint(10, 30)  # Influence in church hierarchy (0-100)
        self.religious_knowledge = random.randint(30, 70)  # Knowledge of religious texts (0-100)
        self.promotion_message = None  # Message to display when promoted
        
        # Adjust skills for role
        self._adjust_skills_for_role()
    
    def _adjust_skills_for_role(self):
        """Adjust skills based on character role."""
        # Priests are better at wisdom
        self.attributes["wisdom"] += random.randint(20, 40)
        
        # Priests also have some charisma
        self.attributes["charisma"] += random.randint(5, 15)
        
        # Ensure attributes stay within bounds
        for attr in self.attributes:
            self.attributes[attr] = min(100, self.attributes[attr])
    
    def get_actions(self):
        """Get the list of actions available to this character.
        
        Returns:
            A list of action names.
        """
        # Get base actions
        actions = super().get_actions()
        
        # Add priest-specific actions
        priest_actions = ["Pray", "Perform Ceremony", "Study Scriptures"]
        
        # Add conditional actions
        if self.church_rank >= 2:  # Full Priest or higher
            priest_actions.append("Counsel Nobles")
        
        if self.congregation_size >= 50:
            priest_actions.append("Collect Tithes")
        
        if self.church_rank >= 3:  # Bishop or higher
            priest_actions.append("Manage Diocese")
        
        actions.extend(priest_actions)
        return actions
    
    def perform_action(self, action, game_manager):
        """Perform an action.
        
        Args:
            action: The name of the action to perform.
            game_manager: The game manager.
        """
        if action == "Pray":
            self._pray(game_manager)
        elif action == "Perform Ceremony":
            self._perform_ceremony(game_manager)
        elif action == "Study Scriptures":
            self._study_scriptures(game_manager)
        elif action == "Counsel Nobles":
            self._counsel_nobles(game_manager)
        elif action == "Collect Tithes":
            self._collect_tithes(game_manager)
        elif action == "Manage Diocese":
            self._manage_diocese(game_manager)
        else:
            # Use base class implementation for common actions
            super().perform_action(action, game_manager)
    
    def _pray(self, game_manager):
        """Pray to increase piety and wisdom.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Pray ===")
        interface.display_message("You spend time in prayer and meditation.")
        
        # Prayer types
        prayer_types = [
            "Personal Meditation",
            "Group Prayer",
            "Fasting and Prayer",
            "Night Vigil"
        ]
        
        choice = interface.display_menu("What type of prayer would you like to engage in?", prayer_types)
        
        # Calculate prayer effectiveness based on wisdom and random factors
        wisdom_factor = self.attributes["wisdom"] / 100  # 0-1 based on wisdom
        random_factor = random.uniform(0.7, 1.3)  # Random fluctuation
        
        if choice == 0:  # Personal Meditation
            # Moderate piety gain, high wisdom gain
            piety_gain = int(5 * wisdom_factor * random_factor)
            wisdom_gain = int(3 * random_factor)
            health_cost = random.randint(0, 2)
            
            interface.display_message("You spend time in quiet meditation, reflecting on sacred texts.")
        
        elif choice == 1:  # Group Prayer
            # High piety gain, moderate wisdom gain, chance for congregation growth
            piety_gain = int(8 * wisdom_factor * random_factor)
            wisdom_gain = int(2 * random_factor)
            health_cost = random.randint(1, 3)
            
            interface.display_message("You lead a group in prayer, strengthening your community bonds.")
            
            # Chance to increase congregation
            if random.random() < 0.3:  # 30% chance
                congregation_gain = random.randint(1, 5)
                self.congregation_size += congregation_gain
                interface.display_message(f"Your inspiring prayers attract {congregation_gain} new members to your congregation.")
        
        elif choice == 2:  # Fasting and Prayer
            # Very high piety gain, moderate wisdom gain, higher health cost
            piety_gain = int(12 * wisdom_factor * random_factor)
            wisdom_gain = int(2 * random_factor)
            health_cost = random.randint(5, 10)
            
            interface.display_message("You fast and pray intensely, denying yourself food to focus on spiritual matters.")
        
        else:  # Night Vigil
            # High piety gain, high wisdom gain, high health cost
            piety_gain = int(10 * wisdom_factor * random_factor)
            wisdom_gain = int(4 * random_factor)
            health_cost = random.randint(8, 15)
            
            interface.display_message("You stay awake through the night in prayer and contemplation.")
        
        # Apply gains and costs
        self.piety = min(100, self.piety + piety_gain)
        self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
        self.health = max(1, self.health - health_cost)
        
        # Display results
        interface.display_message(f"Your piety increased by {piety_gain} points.")
        interface.display_message(f"Your wisdom increased by {wisdom_gain} points.")
        if health_cost > 0:
            interface.display_message(f"The spiritual exertion cost you {health_cost} health points.")
        
        interface.display_message(f"Current piety: {self.piety}/100")
        interface.display_message(f"Current wisdom: {self.attributes['wisdom']}/100")
        interface.display_message(f"Current health: {self.health}/100")
        
        # Chance for church influence gain based on piety
        if self.piety > 70 and random.random() < 0.2:  # 20% chance if piety > 70
            influence_gain = random.randint(1, 3)
            self.church_influence = min(100, self.church_influence + influence_gain)
            interface.display_message(f"Your devotion is noticed by church superiors. Your church influence increases by {influence_gain} points.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _perform_ceremony(self, game_manager):
        """Perform a religious ceremony.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Perform Ceremony ===")
        
        # Ceremony types
        ceremony_types = [
            "Sunday Service",
            "Wedding",
            "Funeral",
            "Baptism",
            "Special Holiday Service"
        ]
        
        choice = interface.display_menu("What type of ceremony would you like to perform?", ceremony_types)
        
        # Calculate ceremony effectiveness based on charisma, wisdom, and random factors
        charisma_factor = self.attributes["charisma"] / 100  # 0-1 based on charisma
        wisdom_factor = self.attributes["wisdom"] / 100  # 0-1 based on wisdom
        random_factor = random.uniform(0.7, 1.3)  # Random fluctuation
        
        # Base success chance
        success_chance = 0.5 + (charisma_factor * 0.3) + (wisdom_factor * 0.2)  # 0.5-1.0
        success_chance = min(0.95, success_chance * random_factor)  # Apply random factor, cap at 95%
        
        # Determine ceremony outcome
        ceremony_success = random.random() < success_chance
        
        # Ceremony-specific effects
        if choice == 0:  # Sunday Service
            if ceremony_success:
                interface.display_message("Your Sunday service is well-received by the congregation.")
                
                # Moderate congregation growth
                congregation_gain = random.randint(1, 5)
                self.congregation_size += congregation_gain
                interface.display_message(f"Your inspiring service attracts {congregation_gain} new members to your congregation.")
                
                # Moderate wealth gain from offerings
                wealth_gain = int(self.congregation_size * 0.2 * random_factor)
                self.wealth += wealth_gain
                interface.display_message(f"The congregation's offerings amount to {wealth_gain} coins.")
            else:
                interface.display_message("Your Sunday service is poorly received. Your sermon fails to inspire the congregation.")
                
                # Small congregation loss
                congregation_loss = random.randint(1, 3)
                self.congregation_size = max(0, self.congregation_size - congregation_loss)
                interface.display_message(f"{congregation_loss} members leave your congregation, disappointed.")
        
        elif choice == 1:  # Wedding
            # Weddings are usually paid services
            fee = random.randint(20, 50)
            self.wealth += fee
            
            if ceremony_success:
                interface.display_message(f"You perform a beautiful wedding ceremony and receive {fee} coins as payment.")
                
                # Chance for reputation boost
                if random.random() < 0.3:  # 30% chance
                    influence_gain = random.randint(1, 3)
                    self.church_influence = min(100, self.church_influence + influence_gain)
                    interface.display_message(f"The noble families involved in the wedding speak highly of you. Your church influence increases by {influence_gain} points.")
            else:
                interface.display_message(f"The wedding ceremony has some awkward moments, but you still receive {fee} coins as payment.")
        
        elif choice == 2:  # Funeral
            # Funerals are usually paid services
            fee = random.randint(15, 40)
            self.wealth += fee
            
            if ceremony_success:
                interface.display_message(f"You perform a solemn and moving funeral service and receive {fee} coins as payment.")
                
                # Wisdom gain from contemplating mortality
                wisdom_gain = random.randint(1, 3)
                self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
                interface.display_message(f"Contemplating mortality increases your wisdom by {wisdom_gain} points.")
            else:
                interface.display_message(f"The funeral service is adequate but not particularly moving. You receive {fee} coins as payment.")
        
        elif choice == 3:  # Baptism
            if ceremony_success:
                interface.display_message("You perform a joyful baptism ceremony that touches the hearts of all present.")
                
                # Small congregation growth
                congregation_gain = random.randint(1, 3)
                self.congregation_size += congregation_gain
                interface.display_message(f"The ceremony attracts {congregation_gain} new members to your congregation.")
                
                # Small piety gain
                piety_gain = random.randint(1, 5)
                self.piety = min(100, self.piety + piety_gain)
                interface.display_message(f"Your piety increases by {piety_gain} points.")
            else:
                interface.display_message("The baptism ceremony proceeds without incident, but fails to inspire those present.")
        
        else:  # Special Holiday Service
            if ceremony_success:
                interface.display_message("Your special holiday service is magnificent, drawing a large crowd and much acclaim.")
                
                # Large congregation growth
                congregation_gain = random.randint(3, 10)
                self.congregation_size += congregation_gain
                interface.display_message(f"Your inspiring service attracts {congregation_gain} new members to your congregation.")
                
                # Large wealth gain from offerings
                wealth_gain = int(self.congregation_size * 0.3 * random_factor)
                self.wealth += wealth_gain
                interface.display_message(f"The generous holiday offerings amount to {wealth_gain} coins.")
                
                # Church influence gain
                influence_gain = random.randint(2, 5)
                self.church_influence = min(100, self.church_influence + influence_gain)
                interface.display_message(f"Your church influence increases by {influence_gain} points due to the successful service.")
            else:
                interface.display_message("Your special holiday service falls short of expectations, disappointing many attendees.")
                
                # Congregation loss
                congregation_loss = random.randint(2, 6)
                self.congregation_size = max(0, self.congregation_size - congregation_loss)
                interface.display_message(f"{congregation_loss} members leave your congregation, disappointed by the service.")
        
        # Common effects for all ceremonies
        
        # Charisma improvement from public speaking
        charisma_gain = random.randint(1, 2)
        self.attributes["charisma"] = min(100, self.attributes["charisma"] + charisma_gain)
        interface.display_message(f"Your public speaking practice improves your charisma by {charisma_gain} points.")
        
        # Health cost from exertion
        health_cost = random.randint(2, 5)
        self.health = max(1, self.health - health_cost)
        interface.display_message(f"The ceremony was tiring. You lost {health_cost} health points.")
        
        # Display current stats
        interface.display_message(f"Current congregation size: {self.congregation_size}")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        interface.display_message(f"Current health: {self.health}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _study_scriptures(self, game_manager):
        """Study religious texts to increase knowledge and wisdom.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Study Scriptures ===")
        interface.display_message("You spend time studying religious texts and scriptures.")
        
        # Study focus options
        study_options = [
            "Basic Texts (Easy)",
            "Theological Treatises (Moderate)",
            "Ancient Manuscripts (Difficult)",
            "Mystical Texts (Very Difficult)"
        ]
        
        choice = interface.display_menu("What would you like to study?", study_options)
        
        # Calculate study effectiveness based on intelligence, wisdom, and random factors
        intelligence_factor = self.attributes["intelligence"] / 100  # 0-1 based on intelligence
        wisdom_factor = self.attributes["wisdom"] / 100  # 0-1 based on wisdom
        random_factor = random.uniform(0.7, 1.3)  # Random fluctuation
        
        # Difficulty and rewards based on choice
        if choice == 0:  # Basic Texts
            difficulty = 30
            knowledge_gain_base = 3
            wisdom_gain_base = 1
            health_cost = random.randint(1, 3)
        elif choice == 1:  # Theological Treatises
            difficulty = 50
            knowledge_gain_base = 5
            wisdom_gain_base = 2
            health_cost = random.randint(2, 5)
        elif choice == 2:  # Ancient Manuscripts
            difficulty = 70
            knowledge_gain_base = 8
            wisdom_gain_base = 3
            health_cost = random.randint(3, 8)
        else:  # Mystical Texts
            difficulty = 90
            knowledge_gain_base = 12
            wisdom_gain_base = 5
            health_cost = random.randint(5, 10)
        
        # Calculate success chance
        success_factor = (intelligence_factor * 0.6) + (wisdom_factor * 0.4)  # 0-1 weighted toward intelligence
        success_chance = 0.5 + (success_factor - (difficulty / 100))  # Adjust for difficulty
        success_chance = max(0.1, min(0.9, success_chance * random_factor))  # Apply random factor, bound between 10-90%
        
        # Determine study outcome
        if random.random() < success_chance:
            # Success
            interface.display_message("Your studies are fruitful! You gain new insights and understanding.")
            
            # Knowledge gain
            knowledge_gain = int(knowledge_gain_base * random_factor)
            self.religious_knowledge = min(100, self.religious_knowledge + knowledge_gain)
            interface.display_message(f"Your religious knowledge increased by {knowledge_gain} points.")
            
            # Wisdom gain
            wisdom_gain = int(wisdom_gain_base * random_factor)
            self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
            interface.display_message(f"Your wisdom increased by {wisdom_gain} points.")
            
            # Piety gain
            piety_gain = random.randint(1, 3)
            self.piety = min(100, self.piety + piety_gain)
            interface.display_message(f"Your piety increased by {piety_gain} points.")
            
            # Chance for church influence gain based on knowledge
            if self.religious_knowledge > 70 and random.random() < 0.2:  # 20% chance if knowledge > 70
                influence_gain = random.randint(1, 3)
                self.church_influence = min(100, self.church_influence + influence_gain)
                interface.display_message(f"Your scholarly insights are noticed by church superiors. Your church influence increases by {influence_gain} points.")
        else:
            # Failure
            interface.display_message("You struggle to understand the texts. Your studies yield little insight.")
            
            # Small knowledge gain
            knowledge_gain = random.randint(0, 1)
            if knowledge_gain > 0:
                self.religious_knowledge = min(100, self.religious_knowledge + knowledge_gain)
                interface.display_message(f"Your religious knowledge increased by only {knowledge_gain} point.")
            
            # Small wisdom gain
            wisdom_gain = random.randint(0, 1)
            if wisdom_gain > 0:
                self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
                interface.display_message(f"Your wisdom increased by {wisdom_gain} point.")
        
        # Apply health cost
        self.health = max(1, self.health - health_cost)
        interface.display_message(f"The intense study was tiring. You lost {health_cost} health points.")
        
        # Display current stats
        interface.display_message(f"Current religious knowledge: {self.religious_knowledge}/100")
        interface.display_message(f"Current wisdom: {self.attributes['wisdom']}/100")
        interface.display_message(f"Current health: {self.health}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def update_for_new_year(self):
        """Update character stats for a new year."""
        # Call base class method
        super().update_for_new_year()
        
        # Chance for promotion based on church influence and piety
        if self.church_rank < 4:  # Not yet at maximum rank
            promotion_chance = (self.church_influence / 200) + (self.piety / 200)  # 0-1 based on influence and piety
            
            if random.random() < promotion_chance:
                self.church_rank += 1
                
                # Rank titles
                rank_titles = ["Novice", "Priest", "Bishop", "Archbishop"]
                
                # Store promotion message for next status display
                self.promotion_message = f"You have been promoted to {rank_titles[self.church_rank - 1]}!"
                
                # Increase influence with promotion
                influence_gain = random.randint(10, 20)
                self.church_influence = min(100, self.church_influence + influence_gain)
    
    def display_status(self, interface):
        """Display the character's status.
        
        Args:
            interface: The user interface.
        """
        # Rank titles
        rank_titles = ["Novice", "Priest", "Bishop", "Archbishop"]
        
        # Display promotion message if there is one
        if self.promotion_message:
            interface.display_message(self.promotion_message)
            self.promotion_message = None  # Clear the message after displaying it
        
        interface.display_message(f"Rank: {rank_titles[self.church_rank - 1]}")
        interface.display_message(f"Piety: {self.piety}/100")
        interface.display_message(f"Congregation Size: {self.congregation_size}")
        interface.display_message(f"Church Influence: {self.church_influence}/100")
        interface.display_message(f"Religious Knowledge: {self.religious_knowledge}/100")
        interface.display_message(f"Wisdom: {self.attributes['wisdom']}/100")
    
    def _counsel_nobles(self, game_manager):
        """Provide spiritual counsel to nobles for influence and wealth.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Counsel Nobles ===")
        interface.display_message("You offer spiritual guidance to the nobility.")
        
        # Counsel types
        counsel_types = [
            "Personal Spiritual Guidance",
            "Political Advice",
            "Family Matters",
            "Moral Dilemmas"
        ]
        
        choice = interface.display_menu("What type of counsel will you provide?", counsel_types)
        
        # Calculate counsel effectiveness based on wisdom, charisma, and random factors
        wisdom_factor = self.attributes["wisdom"] / 100  # 0-1 based on wisdom
        charisma_factor = self.attributes["charisma"] / 100  # 0-1 based on charisma
        random_factor = random.uniform(0.7, 1.3)  # Random fluctuation
        
        # Base success chance
        success_chance = 0.4 + (wisdom_factor * 0.3) + (charisma_factor * 0.3)  # 0.4-1.0
        success_chance = min(0.95, success_chance * random_factor)  # Apply random factor, cap at 95%
        
        # Determine counsel outcome
        if random.random() < success_chance:
            # Success
            interface.display_message("Your counsel is well-received and greatly appreciated.")
            
            # Common rewards for successful counsel
            # Wealth gain (donation)
            wealth_gain = random.randint(20, 50)
            self.wealth += wealth_gain
            interface.display_message(f"The noble offers a donation of {wealth_gain} coins in gratitude.")
            
            # Church influence gain
            influence_gain = random.randint(2, 5)
            self.church_influence = min(100, self.church_influence + influence_gain)
            interface.display_message(f"Your church influence increases by {influence_gain} points.")
            
            # Counsel-specific effects
            if choice == 0:  # Personal Spiritual Guidance
                # Piety gain
                piety_gain = random.randint(3, 8)
                self.piety = min(100, self.piety + piety_gain)
                interface.display_message(f"Your piety increases by {piety_gain} points.")
                
                # Wisdom gain
                wisdom_gain = random.randint(1, 3)
                self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
                interface.display_message(f"Your wisdom increases by {wisdom_gain} points.")
            
            elif choice == 1:  # Political Advice
                # Higher church influence gain
                extra_influence = random.randint(2, 5)
                self.church_influence = min(100, self.church_influence + extra_influence)
                interface.display_message(f"Your political insight earns you an additional {extra_influence} points of church influence.")
                
                # Chance for congregation growth
                if random.random() < 0.3:  # 30% chance
                    congregation_gain = random.randint(3, 8)
                    self.congregation_size += congregation_gain
                    interface.display_message(f"The noble's public support brings {congregation_gain} new members to your congregation.")
            
            elif choice == 2:  # Family Matters
                # Charisma gain
                charisma_gain = random.randint(1, 3)
                self.attributes["charisma"] = min(100, self.attributes["charisma"] + charisma_gain)
                interface.display_message(f"Your interpersonal skills improve, increasing your charisma by {charisma_gain} points.")
                
                # Higher wealth gain
                extra_wealth = random.randint(10, 30)
                self.wealth += extra_wealth
                interface.display_message(f"The grateful family provides an additional gift of {extra_wealth} coins.")
            
            else:  # Moral Dilemmas
                # Wisdom gain
                wisdom_gain = random.randint(2, 5)
                self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
                interface.display_message(f"Wrestling with complex moral issues increases your wisdom by {wisdom_gain} points.")
                
                # Piety gain
                piety_gain = random.randint(2, 5)
                self.piety = min(100, self.piety + piety_gain)
                interface.display_message(f"Your moral guidance increases your piety by {piety_gain} points.")
        
        else:
            # Failure
            interface.display_message("Your counsel fails to resonate with the noble.")
            
            # Small wealth gain (token donation)
            wealth_gain = random.randint(5, 15)
            self.wealth += wealth_gain
            interface.display_message(f"The noble offers a token donation of {wealth_gain} coins out of obligation.")
            
            # Possible negative effects based on counsel type
            if choice == 1:  # Political Advice (most risky)
                # Church influence loss
                influence_loss = random.randint(1, 5)
                self.church_influence = max(0, self.church_influence - influence_loss)
                interface.display_message(f"Your poor political advice costs you {influence_loss} points of church influence.")
            
            # Small wisdom gain (learning from mistakes)
            wisdom_gain = random.randint(0, 1)
            if wisdom_gain > 0:
                self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
                interface.display_message(f"Despite the setback, your wisdom increases by {wisdom_gain} point.")
        
        # Health cost
        health_cost = random.randint(1, 4)
        self.health = max(1, self.health - health_cost)
        interface.display_message(f"The counseling session was mentally taxing. You lost {health_cost} health points.")
        
        # Display current stats
        interface.display_message(f"Current wealth: {self.wealth} coins")
        interface.display_message(f"Current church influence: {self.church_influence}/100")
        interface.display_message(f"Current health: {self.health}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _collect_tithes(self, game_manager):
        """Collect tithes from the congregation.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Collect Tithes ===")
        interface.display_message(f"You collect tithes from your congregation of {self.congregation_size} members.")
        
        # Tithe collection approaches
        approach_options = [
            "Standard Collection (Safe)",
            "Emphasize Charity (Moderate)",
            "Emphasize Obligation (Risky)",
            "Special Collection for Project (Very Risky)"
        ]
        
        choice = interface.display_menu("How would you like to approach the tithe collection?", approach_options)
        
        # Calculate base tithe amount
        base_tithe = self.congregation_size * random.uniform(0.8, 1.2)  # Average 1 coin per member with some randomness
        
        # Calculate collection effectiveness based on charisma and random factors
        charisma_factor = self.attributes["charisma"] / 100  # 0-1 based on charisma
        random_factor = random.uniform(0.7, 1.3)  # Random fluctuation
        
        # Approach-specific modifiers and risks
        if choice == 0:  # Standard Collection
            # Moderate amount, low risk
            amount_modifier = 1.0
            risk_level = 0.1  # 10% chance of negative outcome
            interface.display_message("You conduct a standard tithe collection during services.")
        
        elif choice == 1:  # Emphasize Charity
            # Slightly higher amount, moderate risk
            amount_modifier = 1.2
            risk_level = 0.2  # 20% chance of negative outcome
            interface.display_message("You emphasize the charitable works of the church when collecting tithes.")
        
        elif choice == 2:  # Emphasize Obligation
            # Higher amount, higher risk
            amount_modifier = 1.5
            risk_level = 0.4  # 40% chance of negative outcome
            interface.display_message("You emphasize the religious obligation to tithe, pressing your congregation for more generous donations.")
        
        else:  # Special Collection
            # Highest amount, highest risk
            amount_modifier = 2.0
            risk_level = 0.6  # 60% chance of negative outcome
            interface.display_message("You announce a special collection for a church project, asking for exceptional generosity.")
        
        # Calculate success chance
        success_chance = 1.0 - (risk_level * (1.0 - charisma_factor))  # Charisma reduces risk
        
        # Determine collection outcome
        if random.random() < success_chance:
            # Success
            # Calculate tithe amount
            tithe_amount = int(base_tithe * amount_modifier * (1.0 + charisma_factor * 0.5) * random_factor)
            self.wealth += tithe_amount
            
            interface.display_message(f"Your tithe collection is successful, bringing in {tithe_amount} coins.")
            
            # Chance for congregation growth if approach was charitable
            if choice == 1 and random.random() < 0.3:  # 30% chance with charitable approach
                congregation_gain = random.randint(1, 5)
                self.congregation_size += congregation_gain
                interface.display_message(f"Your charitable focus attracts {congregation_gain} new members to your congregation.")
            
            # Piety gain
            piety_gain = random.randint(1, 3)
            self.piety = min(100, self.piety + piety_gain)
            interface.display_message(f"Your piety increases by {piety_gain} points.")
        
        else:
            # Failure
            # Calculate reduced tithe amount
            tithe_amount = int(base_tithe * 0.5 * random_factor)  # Half the base amount
            self.wealth += tithe_amount
            
            interface.display_message(f"Your tithe collection is poorly received, bringing in only {tithe_amount} coins.")
            
            # Congregation loss
            congregation_loss = random.randint(2, 8)
            self.congregation_size = max(0, self.congregation_size - congregation_loss)
            interface.display_message(f"{congregation_loss} members leave your congregation, unhappy with your approach to tithes.")
            
            # Church influence loss if approach was demanding
            if choice >= 2:  # Obligation or Special Collection
                influence_loss = random.randint(1, 5)
                self.church_influence = max(0, self.church_influence - influence_loss)
                interface.display_message(f"Your demanding approach costs you {influence_loss} points of church influence.")
        
        # Health cost
        health_cost = random.randint(2, 5)
        self.health = max(1, self.health - health_cost)
        interface.display_message(f"The collection process was tiring. You lost {health_cost} health points.")
        
        # Display current stats
        interface.display_message(f"Current wealth: {self.wealth} coins")
        interface.display_message(f"Current congregation size: {self.congregation_size}")
        interface.display_message(f"Current health: {self.health}/100")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _manage_diocese(self, game_manager):
        """Manage your diocese as a Bishop or Archbishop.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Manage Diocese ===")
        
        # Rank titles
        rank_titles = ["Novice", "Priest", "Bishop", "Archbishop"]
        
        # Diocese size based on church rank
        if self.church_rank == 3:  # Bishop
            diocese_size = "small diocese"
            num_parishes = random.randint(5, 15)
        else:  # Archbishop
            diocese_size = "large archdiocese"
            num_parishes = random.randint(15, 30)
        
        interface.display_message(f"As a {rank_titles[self.church_rank - 1]}, you oversee a {diocese_size} with {num_parishes} parishes.")
        
        # Management options
        management_options = [
            "Visit Parishes",
            "Train Clergy",
            "Manage Church Finances",
            "Address Religious Disputes"
        ]
        
        choice = interface.display_menu("How would you like to manage your diocese?", management_options)
        
        # Calculate management effectiveness based on wisdom, charisma, and random factors
        wisdom_factor = self.attributes["wisdom"] / 100  # 0-1 based on wisdom
        charisma_factor = self.attributes["charisma"] / 100  # 0-1 based on charisma
        random_factor = random.uniform(0.7, 1.3)  # Random fluctuation
        
        # Base success chance
        success_chance = 0.5 + (wisdom_factor * 0.25) + (charisma_factor * 0.25)  # 0.5-1.0
        success_chance = min(0.95, success_chance * random_factor)  # Apply random factor, cap at 95%
        
        # Determine management outcome
        if random.random() < success_chance:
            # Success
            interface.display_message("Your diocesan management is effective and well-received.")
            
            # Common rewards for successful management
            # Church influence gain
            influence_gain = random.randint(3, 8)
            self.church_influence = min(100, self.church_influence + influence_gain)
            interface.display_message(f"Your church influence increases by {influence_gain} points.")
            
            # Management-specific effects
            if choice == 0:  # Visit Parishes
                # Congregation growth
                congregation_gain = random.randint(5, 15)
                self.congregation_size += congregation_gain
                interface.display_message(f"Your parish visits inspire {congregation_gain} new members to join your congregation.")
                
                # Charisma gain
                charisma_gain = random.randint(1, 3)
                self.attributes["charisma"] = min(100, self.attributes["charisma"] + charisma_gain)
                interface.display_message(f"Your public speaking improves, increasing your charisma by {charisma_gain} points.")
            
            elif choice == 1:  # Train Clergy
                # Religious knowledge gain
                knowledge_gain = random.randint(2, 5)
                self.religious_knowledge = min(100, self.religious_knowledge + knowledge_gain)
                interface.display_message(f"Teaching others deepens your own understanding. Your religious knowledge increases by {knowledge_gain} points.")
                
                # Wisdom gain
                wisdom_gain = random.randint(1, 3)
                self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
                interface.display_message(f"Your wisdom increases by {wisdom_gain} points.")
            
            elif choice == 2:  # Manage Church Finances
                # Wealth gain
                wealth_gain = num_parishes * random.randint(5, 15)
                self.wealth += wealth_gain
                interface.display_message(f"Your effective financial management brings in {wealth_gain} coins.")
                
                # Intelligence gain
                intelligence_gain = random.randint(1, 2)
                self.attributes["intelligence"] = min(100, self.attributes["intelligence"] + intelligence_gain)
                interface.display_message(f"Your intelligence increases by {intelligence_gain} points.")
            
            else:  # Address Religious Disputes
                # Piety gain
                piety_gain = random.randint(3, 8)
                self.piety = min(100, self.piety + piety_gain)
                interface.display_message(f"Your piety increases by {piety_gain} points.")
                
                # Wisdom gain
                wisdom_gain = random.randint(2, 4)
                self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
                interface.display_message(f"Resolving complex disputes increases your wisdom by {wisdom_gain} points.")
                
                # Extra church influence
                extra_influence = random.randint(2, 5)
                self.church_influence = min(100, self.church_influence + extra_influence)
                interface.display_message(f"Your fair judgments earn you an additional {extra_influence} points of church influence.")
        
        else:
            # Failure
            interface.display_message("Your diocesan management encounters significant challenges.")
            
            # Church influence loss
            influence_loss = random.randint(2, 6)
            self.church_influence = max(0, self.church_influence - influence_loss)
            interface.display_message(f"Your church influence decreases by {influence_loss} points.")
            
            # Management-specific negative effects
            if choice == 0:  # Visit Parishes
                # Congregation loss
                congregation_loss = random.randint(3, 8)
                self.congregation_size = max(0, self.congregation_size - congregation_loss)
                interface.display_message(f"{congregation_loss} members leave your congregation, disappointed by your parish visits.")
            
            elif choice == 1:  # Train Clergy
                # No specific negative effects beyond influence loss
                interface.display_message("Your clergy training program fails to produce results.")
            
            elif choice == 2:  # Manage Church Finances
                # Wealth loss
                wealth_loss = num_parishes * random.randint(2, 8)
                self.wealth = max(0, self.wealth - wealth_loss)
                interface.display_message(f"Your poor financial management costs the church {wealth_loss} coins.")
            
            else:  # Address Religious Disputes
                # Piety loss
                piety_loss = random.randint(2, 5)
                self.piety = max(0, self.piety - piety_loss)
                interface.display_message(f"Your piety decreases by {piety_loss} points as your judgments are questioned.")
            
            # Small wisdom gain (learning from mistakes)
            wisdom_gain = random.randint(1, 2)
            self.attributes["wisdom"] = min(100, self.attributes["wisdom"] + wisdom_gain)
            interface.display_message(f"Despite the setback, your wisdom increases by {wisdom_gain} points from the experience.")
        
        # Health cost
        health_cost = random.randint(5, 10)
        self.health = max(1, self.health - health_cost)
        interface.display_message(f"Managing the diocese is exhausting. You lost {health_cost} health points.")
        
        # Display current stats
        interface.display_message(f"Current church influence: {self.church_influence}/100")
        interface.display_message(f"Current wealth: {self.wealth} coins")
        interface.display_message(f"Current health: {self.health}/100")
        
        interface.get_input("\nPress Enter to continue...") 