"""
King - Character role class for kings
"""
import random
from game.characters.character import Character

class King(Character):
    """Character role class for kings."""
    
    def __init__(self, name, gender, birth_year=None):
        """Initialize a King character.
        
        Args:
            name: The character's name.
            gender: The character's gender.
            birth_year: The character's birth year (optional).
        """
        super().__init__(name, gender, "king", birth_year)
        
        # Set role-specific properties
        self.role = "King"
        self.wealth = 5000
        self.kingdom = "Your Kingdom"
        self.court = []
        self.taxes = 10  # Tax rate as a percentage
        self.popularity = 50  # 0-100 scale
        
        # New properties for enhanced gameplay
        self.treasury_reserves = 5000  # Royal treasury separate from personal wealth
        self.military_strength = 70  # 0-100 scale
        self.at_war_with = []  # List of kingdom names currently at war with
        
        # Royal advisors and their competence (0-100 scale)
        self.advisors = {
            "Chancellor": random.randint(40, 70),  # Diplomacy
            "Treasurer": random.randint(40, 70),   # Finance
            "Marshal": random.randint(40, 70),     # Military
            "Spymaster": random.randint(40, 70),   # Intelligence
            "Court Chaplain": random.randint(40, 70)  # Religious affairs
        }
        
        # Adjust skills for role
        self._adjust_skills_for_role()
    
    def _adjust_skills_for_role(self):
        """Adjust skills based on character role."""
        # Kings are better at diplomacy and stewardship
        self.skills["diplomacy"] += random.randint(10, 30)
        self.skills["stewardship"] += random.randint(10, 30)
        self.skills["combat"] += random.randint(0, 20)
        
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
        
        # Add king-specific actions
        actions.extend([
            "Adjust Taxes",
            "Hold Court",
            "Declare War",
            "Make Peace",
            "Build Monument",
            "Host Feast",
            "Manage Advisors"
        ])
        
        return actions
    
    def perform_action(self, action, game_manager):
        """Perform an action.
        
        Args:
            action: The name of the action to perform.
            game_manager: The game manager.
        """
        if action == "Adjust Taxes":
            self._adjust_taxes(game_manager)
        elif action == "Hold Court":
            self._hold_court(game_manager)
        elif action == "Declare War":
            self._declare_war(game_manager)
        elif action == "Make Peace":
            self._make_peace(game_manager)
        elif action == "Build Monument":
            self._build_monument(game_manager)
        elif action == "Host Feast":
            self._host_feast(game_manager)
        elif action == "Manage Advisors":
            self._manage_advisors(game_manager)
        else:
            # Use base class implementation for common actions
            super().perform_action(action, game_manager)
    
    def _adjust_taxes(self, game_manager):
        """Adjust the tax rate for the kingdom.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Adjust Taxes ===")
        interface.display_message(f"Current Tax Rate: {self.taxes}%")
        interface.display_message(f"Current Popularity: {self.popularity}/100")
        interface.display_message(f"Treasury Reserves: {self.treasury_reserves} coins")
        
        # Show estimated income
        estimated_income = int(self.taxes * 100)  # Simple calculation
        treasurer_bonus = int((self.advisors["Treasurer"] - 50) / 10)  # -5 to +5
        if treasurer_bonus != 0:
            treasurer_effect = estimated_income * treasurer_bonus // 10
            estimated_income += treasurer_effect
            
            if treasurer_bonus > 0:
                interface.display_message(f"Your Treasurer's competence increases tax efficiency by {treasurer_bonus * 10}%")
            else:
                interface.display_message(f"Your Treasurer's incompetence decreases tax efficiency by {abs(treasurer_bonus) * 10}%")
        
        interface.display_message(f"Estimated Annual Income: {estimated_income} coins")
        
        # Tax policy options
        tax_options = [
            "Increase taxes by 5%",
            "Increase taxes by 2%",
            "Increase taxes by 1%",
            "Keep current tax rate",
            "Decrease taxes by 1%",
            "Decrease taxes by 2%",
            "Decrease taxes by 5%",
            "Back"
        ]
        
        choice = interface.display_menu("Choose a tax policy:", tax_options)
        
        # Apply tax change
        tax_change = 0
        if choice == 0:  # Increase by 5%
            tax_change = 5
        elif choice == 1:  # Increase by 2%
            tax_change = 2
        elif choice == 2:  # Increase by 1%
            tax_change = 1
        elif choice == 3:  # Keep current
            tax_change = 0
        elif choice == 4:  # Decrease by 1%
            tax_change = -1
        elif choice == 5:  # Decrease by 2%
            tax_change = -2
        elif choice == 6:  # Decrease by 5%
            tax_change = -5
        else:  # Back
            return
        
        # Apply the change
        old_tax_rate = self.taxes
        self.taxes = max(1, min(30, self.taxes + tax_change))
        
        interface.display_message(f"Tax rate changed from {old_tax_rate}% to {self.taxes}%")
        
        # Popularity effects
        if tax_change > 0:
            # Tax increases are unpopular
            popularity_change = -tax_change * 2
            self.popularity += popularity_change
            interface.display_message(f"Popularity decreased by {abs(popularity_change)} points due to tax increase.")
        elif tax_change < 0:
            # Tax decreases are popular
            popularity_change = abs(tax_change)
            self.popularity += popularity_change
            interface.display_message(f"Popularity increased by {popularity_change} points due to tax decrease.")
        else:
            interface.display_message("Keeping the current tax rate has no effect on popularity.")
        
        # Ensure popularity stays within bounds
        self.popularity = max(0, min(100, self.popularity))
        
        # Show new estimated income
        new_estimated_income = int(self.taxes * 100)
        if treasurer_bonus != 0:
            treasurer_effect = new_estimated_income * treasurer_bonus // 10
            new_estimated_income += treasurer_effect
        
        income_change = new_estimated_income - estimated_income
        if income_change > 0:
            interface.display_message(f"Estimated annual income increased by {income_change} coins.")
        elif income_change < 0:
            interface.display_message(f"Estimated annual income decreased by {abs(income_change)} coins.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _hold_court(self, game_manager):
        """Hold court to hear petitions and make judgments.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Hold Court ===")
        interface.display_message("You sit upon your throne as subjects bring their petitions.")
        
        # Number of petitions based on kingdom size (simplified)
        num_petitions = random.randint(3, 5)
        
        # Chancellor's competence affects petition quality
        chancellor_bonus = (self.advisors["Chancellor"] - 50) / 100  # -0.5 to +0.5
        
        for i in range(num_petitions):
            interface.display_message(f"\nPetition {i+1} of {num_petitions}:")
            
            # Generate a random petition
            petition_type = random.choice([
                "Land Dispute",
                "Criminal Case",
                "Tax Exemption Request",
                "Noble Title Request",
                "Trade Agreement Proposal",
                "Religious Matter",
                "Military Request"
            ])
            
            # Generate petitioners
            if petition_type in ["Land Dispute", "Tax Exemption Request", "Noble Title Request"]:
                petitioner = f"Noble {random.choice(['Lord', 'Lady'])} {random.choice(['Smith', 'Jones', 'Williams', 'Brown', 'Taylor'])}"
            elif petition_type == "Criminal Case":
                petitioner = f"Sheriff of {random.choice(['Northshire', 'Westfall', 'Redridge', 'Duskwood'])}"
            elif petition_type == "Trade Agreement Proposal":
                petitioner = f"Guild Master {random.choice(['Thomas', 'Richard', 'Harold', 'Elizabeth', 'Catherine'])}"
            elif petition_type == "Religious Matter":
                petitioner = f"Bishop {random.choice(['John', 'Peter', 'Matthew', 'Luke', 'Mark'])}"
            else:  # Military Request
                petitioner = f"Captain {random.choice(['James', 'Robert', 'William', 'Edward', 'Henry'])}"
            
            # Generate petition details
            if petition_type == "Land Dispute":
                details = f"A dispute over land boundaries between {petitioner} and another noble."
                options = ["Rule in favor of the petitioner", "Rule against the petitioner", "Propose a compromise"]
            elif petition_type == "Criminal Case":
                crime = random.choice(["theft", "assault", "treason", "tax evasion"])
                details = f"A case of {crime} brought by {petitioner}."
                options = ["Harsh punishment", "Lenient punishment", "Pardon the accused"]
            elif petition_type == "Tax Exemption Request":
                details = f"{petitioner} requests exemption from taxes for three years, citing service to the crown."
                options = ["Grant full exemption", "Grant partial exemption", "Deny exemption"]
            elif petition_type == "Noble Title Request":
                details = f"{petitioner} requests elevation to a higher title."
                options = ["Grant the title", "Deny the request", "Offer a different honor"]
            elif petition_type == "Trade Agreement Proposal":
                details = f"{petitioner} proposes a new trade agreement that could increase treasury income."
                options = ["Accept the proposal", "Reject the proposal", "Negotiate better terms"]
            elif petition_type == "Religious Matter":
                details = f"{petitioner} requests funding for a new cathedral."
                options = ["Provide full funding", "Provide partial funding", "Deny funding"]
            else:  # Military Request
                details = f"{petitioner} requests additional resources for the army."
                options = ["Grant the request", "Partially grant the request", "Deny the request"]
            
            # Display petition
            interface.display_message(f"Petitioner: {petitioner}")
            interface.display_message(f"Matter: {petition_type}")
            interface.display_message(f"Details: {details}")
            
            # Get player's judgment
            choice = interface.display_menu("Your judgment:", options)
            
            # Determine outcome based on petition type and choice
            if petition_type == "Land Dispute":
                if choice == 0:  # Rule in favor
                    interface.display_message(f"You rule in favor of {petitioner}.")
                    interface.display_message("They are pleased with your judgment.")
                    # Gain favor with one noble, lose with another
                    self.popularity += random.randint(-3, 3)
                elif choice == 1:  # Rule against
                    interface.display_message(f"You rule against {petitioner}.")
                    interface.display_message("They are displeased with your judgment.")
                    # Lose favor with one noble, gain with another
                    self.popularity += random.randint(-3, 3)
                else:  # Compromise
                    interface.display_message("You propose a compromise that partially satisfies both parties.")
                    # Small popularity gain for wisdom
                    self.popularity += random.randint(1, 3)
            
            elif petition_type == "Criminal Case":
                if choice == 0:  # Harsh
                    interface.display_message("You order a harsh punishment.")
                    # Deterrent effect, but may seem cruel
                    self.popularity += random.randint(-5, 5)
                elif choice == 1:  # Lenient
                    interface.display_message("You order a lenient punishment.")
                    # Seen as merciful, but may seem weak
                    self.popularity += random.randint(-3, 5)
                else:  # Pardon
                    interface.display_message("You pardon the accused.")
                    # Could be seen as very merciful or very weak
                    self.popularity += random.randint(-10, 10)
            
            elif petition_type == "Tax Exemption Request":
                if choice == 0:  # Full exemption
                    interface.display_message("You grant a full tax exemption.")
                    # Noble is happy, but treasury suffers
                    self.popularity += random.randint(1, 5)
                    self.treasury_reserves -= random.randint(100, 300)
                elif choice == 1:  # Partial exemption
                    interface.display_message("You grant a partial tax exemption.")
                    # Balanced approach
                    self.popularity += random.randint(0, 3)
                    self.treasury_reserves -= random.randint(50, 150)
                else:  # Deny
                    interface.display_message("You deny the tax exemption request.")
                    # Treasury intact, but noble is unhappy
                    self.popularity -= random.randint(1, 5)
            
            elif petition_type == "Noble Title Request":
                if choice == 0:  # Grant title
                    interface.display_message("You grant the requested title.")
                    # Noble is very happy, but others may be jealous
                    self.popularity += random.randint(-2, 8)
                elif choice == 1:  # Deny
                    interface.display_message("You deny the title request.")
                    # Noble is unhappy
                    self.popularity -= random.randint(1, 5)
                else:  # Different honor
                    interface.display_message("You offer a different honor instead of the requested title.")
                    # Compromise
                    self.popularity += random.randint(-1, 5)
            
            elif petition_type == "Trade Agreement Proposal":
                if choice == 0:  # Accept
                    interface.display_message("You accept the trade agreement proposal.")
                    # Economic benefit, but terms might not be ideal
                    self.treasury_reserves += random.randint(200, 500)
                elif choice == 1:  # Reject
                    interface.display_message("You reject the trade agreement proposal.")
                    # No economic benefit, guild master unhappy
                    self.popularity -= random.randint(1, 3)
                else:  # Negotiate
                    interface.display_message("You negotiate for better terms.")
                    # Better economic benefit if successful
                    if random.random() < 0.6 + chancellor_bonus:
                        interface.display_message("Negotiations are successful!")
                        self.treasury_reserves += random.randint(300, 700)
                        self.popularity += random.randint(1, 3)
                    else:
                        interface.display_message("Negotiations fail and the deal falls through.")
                        self.popularity -= random.randint(1, 5)
            
            elif petition_type == "Religious Matter":
                if choice == 0:  # Full funding
                    interface.display_message("You provide full funding for the cathedral.")
                    # Church is very happy, treasury suffers
                    self.popularity += random.randint(5, 10)
                    self.treasury_reserves -= random.randint(500, 1000)
                elif choice == 1:  # Partial funding
                    interface.display_message("You provide partial funding for the cathedral.")
                    # Balanced approach
                    self.popularity += random.randint(2, 5)
                    self.treasury_reserves -= random.randint(200, 500)
                else:  # Deny funding
                    interface.display_message("You deny funding for the cathedral.")
                    # Church is unhappy
                    self.popularity -= random.randint(3, 8)
            
            else:  # Military Request
                if choice == 0:  # Grant
                    interface.display_message("You grant the military request.")
                    # Military is strengthened, treasury suffers
                    self.military_strength = min(100, self.military_strength + random.randint(3, 8))
                    self.treasury_reserves -= random.randint(300, 700)
                elif choice == 1:  # Partial
                    interface.display_message("You partially grant the military request.")
                    # Balanced approach
                    self.military_strength = min(100, self.military_strength + random.randint(1, 4))
                    self.treasury_reserves -= random.randint(100, 300)
                else:  # Deny
                    interface.display_message("You deny the military request.")
                    # Military is unhappy
                    self.military_strength = max(1, self.military_strength - random.randint(1, 3))
            
            # Pause between petitions
            interface.get_input("\nPress Enter to continue to the next petition...")
        
        # Court session complete
        interface.display_message("\nThe court session is complete.")
        
        # Chancellor's competence affects overall court effectiveness
        if self.advisors["Chancellor"] >= 70:
            interface.display_message("Your Chancellor managed the proceedings expertly.")
            self.popularity += random.randint(1, 3)
        elif self.advisors["Chancellor"] <= 30:
            interface.display_message("Your Chancellor struggled to maintain order in court.")
            self.popularity -= random.randint(1, 3)
        
        # Ensure values stay within bounds
        self.popularity = max(0, min(100, self.popularity))
        
        interface.get_input("\nPress Enter to continue...")
    
    def _declare_war(self, game_manager):
        """Declare war on another kingdom.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Declare War ===")
        
        # Check if treasury can support a war
        if self.treasury_reserves < 2000:
            interface.display_message("Your treasury does not have sufficient funds to wage war.")
            interface.display_message("You need at least 2000 coins in the royal treasury.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Check if already at war with too many kingdoms
        if len(self.at_war_with) >= 2:
            interface.display_message("Your kingdom is already engaged in multiple wars.")
            interface.display_message("Your military is stretched too thin to declare another war.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Get list of kingdoms
        kingdoms = game_manager.world.kingdoms
        
        # Filter out kingdoms already at war with
        available_kingdoms = [k for k in kingdoms if k.name not in self.at_war_with]
        
        if not available_kingdoms:
            interface.display_message("There are no kingdoms available to declare war on.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Create list of kingdom names with their relative strength
        kingdom_options = []
        for kingdom in available_kingdoms:
            # Estimate kingdom strength (would be a property of Kingdom in a full implementation)
            kingdom_strength = random.randint(40, 100)
            strength_comparison = ""
            
            if kingdom_strength > self.military_strength + 20:
                strength_comparison = "(Much Stronger)"
            elif kingdom_strength > self.military_strength:
                strength_comparison = "(Stronger)"
            elif kingdom_strength < self.military_strength - 20:
                strength_comparison = "(Much Weaker)"
            elif kingdom_strength < self.military_strength:
                strength_comparison = "(Weaker)"
            else:
                strength_comparison = "(Equal Strength)"
            
            kingdom_options.append(f"{kingdom.name} {strength_comparison}")
        
        kingdom_options.append("Cancel")
        
        # Display menu
        choice = interface.display_menu("Choose a kingdom to declare war on:", kingdom_options)
        
        if choice < len(available_kingdoms):
            target_kingdom = available_kingdoms[choice]
            
            # Get war justification
            justifications = [
                "Border Dispute",
                "Dynastic Claim",
                "Religious Differences",
                "Trade Conflict",
                "Personal Insult"
            ]
            
            justification_choice = interface.display_menu("Choose a justification for war:", justifications)
            justification = justifications[justification_choice]
            
            # Confirm war declaration
            confirm = interface.display_menu(
                f"Declare war on {target_kingdom.name} citing {justification}?\nThis will cost 2000 coins from the treasury initially.",
                ["Yes", "No"]
            )
            
            if confirm == 0:  # Yes
                # Add to war list
                self.at_war_with.append(target_kingdom.name)
                
                # Initial war costs
                self.treasury_reserves -= 2000
                
                # Popularity effects based on justification
                if justification in ["Border Dispute", "Trade Conflict"]:
                    # Practical reasons are moderately popular
                    self.popularity += random.randint(-5, 10)
                elif justification == "Personal Insult":
                    # Personal reasons are unpopular
                    self.popularity -= random.randint(5, 15)
                elif justification == "Dynastic Claim":
                    # Dynastic reasons are popular with nobles
                    self.popularity += random.randint(0, 5)
                else:  # Religious Differences
                    # Religious reasons can be divisive
                    self.popularity += random.randint(-10, 15)
                
                # Marshal's competence affects initial military preparation
                marshal_bonus = int((self.advisors["Marshal"] - 50) / 10)  # -5 to +5
                self.military_strength = min(100, self.military_strength + marshal_bonus)
                
                interface.display_message(f"You have declared war on {target_kingdom.name}, citing {justification}!")
                interface.display_message("Your armies are being mobilized and your generals are preparing battle plans.")
                
                if marshal_bonus > 0:
                    interface.display_message(f"Your Marshal's competence has improved your military preparation by {marshal_bonus} points.")
                elif marshal_bonus < 0:
                    interface.display_message(f"Your Marshal's incompetence has hindered your military preparation by {abs(marshal_bonus)} points.")
            else:
                interface.display_message("You decided not to declare war at this time.")
        else:
            interface.display_message("You decided not to declare war.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _make_peace(self, game_manager):
        """Make peace with another kingdom.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Make Peace ===")
        
        # Check if at war with any kingdoms
        if not self.at_war_with:
            interface.display_message("Your kingdom is not currently at war with anyone.")
            interface.get_input("\nPress Enter to continue...")
            return
        
        # Create list of kingdoms at war with
        war_options = []
        for enemy in self.at_war_with:
            war_options.append(enemy)
        
        war_options.append("Cancel")
        
        # Display menu
        choice = interface.display_menu("Choose a kingdom to make peace with:", war_options)
        
        if choice < len(self.at_war_with):
            target_kingdom = self.at_war_with[choice]
            
            # Peace terms
            terms = [
                "White Peace (No Concessions)",
                "Favorable Terms (Demand Tribute)",
                "Unfavorable Terms (Pay Tribute)"
            ]
            
            terms_choice = interface.display_menu("Choose peace terms:", terms)
            chosen_terms = terms[terms_choice]
            
            # Chancellor's competence affects negotiation success
            chancellor_bonus = (self.advisors["Chancellor"] - 50) / 100  # -0.5 to +0.5
            
            # Base success chance depends on terms
            if chosen_terms == "White Peace (No Concessions)":
                success_chance = 0.7 + chancellor_bonus
            elif chosen_terms == "Favorable Terms (Demand Tribute)":
                success_chance = 0.4 + chancellor_bonus
            else:  # Unfavorable Terms
                success_chance = 0.9 + chancellor_bonus
            
            # Cap success chance
            success_chance = max(0.1, min(0.95, success_chance))
            
            # Determine outcome
            if random.random() < success_chance:
                # Peace negotiation successful
                interface.display_message(f"Peace negotiations with {target_kingdom} are successful!")
                
                # Remove from war list
                self.at_war_with.remove(target_kingdom)
                
                # Effects based on terms
                if chosen_terms == "White Peace (No Concessions)":
                    interface.display_message("The war ends with no territorial changes or reparations.")
                    self.popularity += random.randint(5, 10)
                
                elif chosen_terms == "Favorable Terms (Demand Tribute)":
                    tribute = random.randint(1000, 3000)
                    self.treasury_reserves += tribute
                    interface.display_message(f"You secure a tribute of {tribute} coins from {target_kingdom}.")
                    self.popularity += random.randint(10, 20)
                
                else:  # Unfavorable Terms
                    tribute = random.randint(1000, 3000)
                    self.treasury_reserves -= tribute
                    interface.display_message(f"You agree to pay {tribute} coins to {target_kingdom} as reparations.")
                    self.popularity -= random.randint(5, 15)
                
                # Military recovery
                recovery = random.randint(5, 15)
                self.military_strength = min(100, self.military_strength + recovery)
                interface.display_message(f"Your military begins to recover, gaining {recovery} strength points.")
            
            else:
                # Peace negotiation failed
                interface.display_message(f"Peace negotiations with {target_kingdom} have failed!")
                interface.display_message("The war continues...")
                
                # Diplomatic penalty
                chancellor_penalty = random.randint(1, 5)
                self.advisors["Chancellor"] = max(1, self.advisors["Chancellor"] - chancellor_penalty)
                interface.display_message(f"Your Chancellor's reputation suffers, losing {chancellor_penalty} competence points.")
        else:
            interface.display_message("You decided not to pursue peace at this time.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def _build_monument(self, game_manager):
        """Build a monument to increase prestige.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Build Monument ===")
        interface.display_message("You can build a monument to increase your prestige and legacy.")
        interface.display_message(f"Treasury Reserves: {self.treasury_reserves} coins")
        
        # Monument options with costs and benefits
        monuments = [
            {
                "name": "Statue",
                "description": "A statue of yourself in the town square.",
                "cost": 1000,
                "popularity_gain": random.randint(5, 10),
                "time_to_build": 1  # years
            },
            {
                "name": "Triumphal Arch",
                "description": "A grand arch celebrating your military victories.",
                "cost": 2000,
                "popularity_gain": random.randint(8, 15),
                "time_to_build": 2  # years
            },
            {
                "name": "Royal Gardens",
                "description": "Extensive gardens open to the public.",
                "cost": 3000,
                "popularity_gain": random.randint(10, 20),
                "time_to_build": 2  # years
            },
            {
                "name": "Cathedral",
                "description": "A magnificent cathedral to demonstrate your piety.",
                "cost": 5000,
                "popularity_gain": random.randint(15, 25),
                "time_to_build": 3  # years
            },
            {
                "name": "Palace",
                "description": "A grand palace to showcase your wealth and power.",
                "cost": 8000,
                "popularity_gain": random.randint(20, 30),
                "time_to_build": 4  # years
            }
        ]
        
        # Create menu options
        monument_options = []
        for monument in monuments:
            monument_options.append(f"{monument['name']} - Cost: {monument['cost']} coins, Build Time: {monument['time_to_build']} years")
        
        monument_options.append("Cancel")
        
        # Display menu
        choice = interface.display_menu("Choose a monument to build:", monument_options)
        
        if choice < len(monuments):
            selected_monument = monuments[choice]
            
            # Check if player can afford it
            if self.treasury_reserves < selected_monument["cost"]:
                interface.display_message(f"You cannot afford to build this monument. It costs {selected_monument['cost']} coins.")
                interface.display_message(f"Your treasury only has {self.treasury_reserves} coins.")
                interface.get_input("\nPress Enter to continue...")
                return
            
            # Confirm construction
            confirm = interface.display_menu(
                f"Begin construction of {selected_monument['name']} for {selected_monument['cost']} coins?",
                ["Yes", "No"]
            )
            
            if confirm == 0:  # Yes
                # Pay cost
                self.treasury_reserves -= selected_monument["cost"]
                
                # Treasurer's competence affects cost efficiency
                treasurer_bonus = int((self.advisors["Treasurer"] - 50) / 10)  # -5 to +5
                if treasurer_bonus > 0:
                    savings = selected_monument["cost"] * treasurer_bonus // 20
                    self.treasury_reserves += savings
                    interface.display_message(f"Your Treasurer's efficiency saved you {savings} coins on the project.")
                
                # Add monument to construction projects
                if not hasattr(self, "construction_projects"):
                    self.construction_projects = []
                
                self.construction_projects.append({
                    "name": selected_monument["name"],
                    "years_remaining": selected_monument["time_to_build"],
                    "popularity_gain": selected_monument["popularity_gain"]
                })
                
                interface.display_message(f"Construction of {selected_monument['name']} has begun!")
                interface.display_message(f"Estimated completion time: {selected_monument['time_to_build']} years.")
                
                # Immediate small popularity boost for starting project
                popularity_boost = random.randint(1, 5)
                self.popularity += popularity_boost
                interface.display_message(f"Your subjects are excited about the new project! Popularity increased by {popularity_boost}.")
            else:
                interface.display_message("You decided not to build a monument at this time.")
        else:
            interface.display_message("You decided not to build a monument at this time.")
        
        # Ensure popularity stays within bounds
        self.popularity = max(0, min(100, self.popularity))
        
        interface.get_input("\nPress Enter to continue...")
    
    def _host_feast(self, game_manager):
        """Host a feast to increase popularity.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Host Feast ===")
        interface.display_message("You can host a feast to increase your popularity and build relationships.")
        interface.display_message(f"Treasury Reserves: {self.treasury_reserves} coins")
        
        # Feast options with costs and benefits
        feast_options = [
            {
                "name": "Small Banquet",
                "description": "A modest banquet for local nobles.",
                "cost": 500,
                "popularity_gain": random.randint(3, 8),
                "guests": "Local Nobles"
            },
            {
                "name": "Royal Feast",
                "description": "A grand feast for nobles from across the kingdom.",
                "cost": 1000,
                "popularity_gain": random.randint(5, 12),
                "guests": "Kingdom Nobles"
            },
            {
                "name": "Festival",
                "description": "A public festival for all your subjects.",
                "cost": 1500,
                "popularity_gain": random.randint(8, 15),
                "guests": "All Subjects"
            },
            {
                "name": "Grand Tournament",
                "description": "A tournament with feasting and entertainment.",
                "cost": 2500,
                "popularity_gain": random.randint(10, 20),
                "guests": "Nobles and Knights"
            },
            {
                "name": "Royal Wedding",
                "description": "A celebration of a royal marriage (requires an unmarried royal).",
                "cost": 3000,
                "popularity_gain": random.randint(15, 25),
                "guests": "Royalty and Nobility"
            }
        ]
        
        # Create menu options
        menu_options = []
        for option in feast_options:
            menu_options.append(f"{option['name']} - Cost: {option['cost']} coins, Guests: {option['guests']}")
        
        menu_options.append("Cancel")
        
        # Display menu
        choice = interface.display_menu("Choose a feast to host:", menu_options)
        
        if choice < len(feast_options):
            selected_feast = feast_options[choice]
            
            # Check if player can afford it
            if self.treasury_reserves < selected_feast["cost"]:
                interface.display_message(f"You cannot afford this feast. It costs {selected_feast['cost']} coins.")
                interface.display_message(f"Your treasury only has {self.treasury_reserves} coins.")
                interface.get_input("\nPress Enter to continue...")
                return
            
            # Special case for Royal Wedding
            if selected_feast["name"] == "Royal Wedding":
                interface.display_message("A royal wedding requires an unmarried royal family member.")
                interface.display_message("Since this is a simplified simulation, we'll assume one is available.")
            
            # Confirm feast
            confirm = interface.display_menu(
                f"Host a {selected_feast['name']} for {selected_feast['cost']} coins?",
                ["Yes", "No"]
            )
            
            if confirm == 0:  # Yes
                # Pay cost
                self.treasury_reserves -= selected_feast["cost"]
                
                # Base popularity gain
                popularity_gain = selected_feast["popularity_gain"]
                
                # Chancellor's competence affects feast success
                chancellor_bonus = int((self.advisors["Chancellor"] - 50) / 10)  # -5 to +5
                
                # Determine feast quality
                feast_quality_roll = random.random() + (chancellor_bonus / 20)  # -0.25 to +0.25 modifier
                
                if feast_quality_roll > 0.8:
                    feast_quality = "exceptional"
                    popularity_multiplier = 1.5
                elif feast_quality_roll > 0.5:
                    feast_quality = "good"
                    popularity_multiplier = 1.0
                elif feast_quality_roll > 0.2:
                    feast_quality = "adequate"
                    popularity_multiplier = 0.7
                else:
                    feast_quality = "poor"
                    popularity_multiplier = 0.4
                
                # Calculate final popularity gain
                final_popularity_gain = int(popularity_gain * popularity_multiplier)
                self.popularity += final_popularity_gain
                
                # Display results
                interface.display_message(f"You host a {feast_quality} {selected_feast['name']}!")
                
                if feast_quality == "exceptional":
                    interface.display_message("The feast is a tremendous success! Your guests are thoroughly impressed.")
                    interface.display_message("Stories of your generosity spread throughout the kingdom.")
                elif feast_quality == "good":
                    interface.display_message("The feast is well-received. Your guests enjoy themselves.")
                    interface.display_message("Your reputation for hospitality is enhanced.")
                elif feast_quality == "adequate":
                    interface.display_message("The feast is acceptable, though not particularly memorable.")
                    interface.display_message("Your guests are satisfied, but not impressed.")
                else:
                    interface.display_message("The feast is disappointing. There are complaints about the food and entertainment.")
                    interface.display_message("Some guests leave early, which is noted by others.")
                
                interface.display_message(f"Your popularity increases by {final_popularity_gain} points.")
                
                # Special effects based on feast type
                if selected_feast["name"] == "Grand Tournament":
                    military_boost = random.randint(1, 5)
                    self.military_strength = min(100, self.military_strength + military_boost)
                    interface.display_message(f"The tournament attracts skilled warriors to your service. Military strength increased by {military_boost}.")
                
                elif selected_feast["name"] == "Royal Wedding":
                    # Diplomatic benefits
                    interface.display_message("The royal wedding creates a new alliance with another kingdom.")
                    interface.display_message("This may provide diplomatic advantages in the future.")
                
                # Chancellor effect
                if chancellor_bonus >= 3:
                    interface.display_message("Your Chancellor's excellent management made the event even more successful.")
                elif chancellor_bonus <= -3:
                    interface.display_message("Your Chancellor's poor management detracted from the event's success.")
            else:
                interface.display_message("You decided not to host a feast at this time.")
        else:
            interface.display_message("You decided not to host a feast at this time.")
        
        # Ensure popularity stays within bounds
        self.popularity = max(0, min(100, self.popularity))
        
        interface.get_input("\nPress Enter to continue...")
    
    def _manage_advisors(self, game_manager):
        """Manage royal advisors.
        
        Args:
            game_manager: The game manager.
        """
        interface = game_manager.interface
        
        interface.display_message("=== Manage Advisors ===")
        interface.display_message("Your royal council advises you on matters of state.")
        
        # Display current advisors
        interface.display_message("\nCurrent Advisors:")
        for position, competence in self.advisors.items():
            interface.display_message(f"  {position}: {competence}/100")
        
        # Advisor positions
        positions = list(self.advisors.keys())
        positions.append("Back")
        
        # Display menu
        choice = interface.display_menu("Which advisor position would you like to manage?", positions)
        
        if choice < len(positions) - 1:
            position = positions[choice]
            current_competence = self.advisors[position]
            
            interface.display_message(f"\n{position} - Current Competence: {current_competence}/100")
            
            # Advisor management options
            options = [
                f"Replace Advisor (Cost: {200 + current_competence * 5} coins)",
                f"Train Advisor (Cost: {100 + current_competence * 2} coins)",
                "Back"
            ]
            
            action_choice = interface.display_menu("What would you like to do?", options)
            
            if action_choice == 0:  # Replace
                # Calculate cost based on current competence
                cost = 200 + current_competence * 5
                
                # Check if player can afford it
                if self.treasury_reserves < cost:
                    interface.display_message(f"You cannot afford to replace this advisor. Cost: {cost} coins.")
                    interface.display_message(f"Treasury: {self.treasury_reserves} coins.")
                    interface.get_input("\nPress Enter to continue...")
                    return
                
                # Confirm replacement
                confirm = interface.display_menu(
                    f"Replace your {position} for {cost} coins?",
                    ["Yes", "No"]
                )
                
                if confirm == 0:  # Yes
                    # Pay cost
                    self.treasury_reserves -= cost
                    
                    # Generate new advisor competence
                    # Higher cost means better chance of high competence
                    min_competence = max(30, current_competence - 20)
                    max_competence = min(100, current_competence + 40)
                    new_competence = random.randint(min_competence, max_competence)
                    
                    # Update advisor
                    self.advisors[position] = new_competence
                    
                    interface.display_message(f"You have replaced your {position}.")
                    interface.display_message(f"New {position} Competence: {new_competence}/100")
                    
                    # Temporary popularity effect
                    if new_competence > current_competence + 10:
                        self.popularity += random.randint(1, 5)
                        interface.display_message("Your subjects approve of the new appointment.")
                    elif new_competence < current_competence - 10:
                        self.popularity -= random.randint(1, 5)
                        interface.display_message("Your subjects question your judgment in this appointment.")
                else:
                    interface.display_message("You decided not to replace your advisor.")
            
            elif action_choice == 1:  # Train
                # Calculate cost based on current competence
                cost = 100 + current_competence * 2
                
                # Check if player can afford it
                if self.treasury_reserves < cost:
                    interface.display_message(f"You cannot afford to train this advisor. Cost: {cost} coins.")
                    interface.display_message(f"Treasury: {self.treasury_reserves} coins.")
                    interface.get_input("\nPress Enter to continue...")
                    return
                
                # Confirm training
                confirm = interface.display_menu(
                    f"Invest {cost} coins in training your {position}?",
                    ["Yes", "No"]
                )
                
                if confirm == 0:  # Yes
                    # Pay cost
                    self.treasury_reserves -= cost
                    
                    # Calculate improvement
                    improvement = random.randint(3, 8)
                    new_competence = min(100, current_competence + improvement)
                    
                    # Update advisor
                    self.advisors[position] = new_competence
                    
                    interface.display_message(f"You have invested in training your {position}.")
                    interface.display_message(f"Their competence has improved by {improvement} points.")
                    interface.display_message(f"New {position} Competence: {new_competence}/100")
                else:
                    interface.display_message("You decided not to train your advisor.")
        
        interface.get_input("\nPress Enter to continue...")
    
    def update_for_new_year(self):
        """Update character stats for a new year."""
        super().update_for_new_year()
        
        # Base tax income
        tax_income = int(self.taxes * 100)  # Simple calculation
        self.treasury_reserves += tax_income
        
        # Advisor effects
        treasurer_bonus = int((self.advisors["Treasurer"] - 50) / 10)  # -5 to +5
        if treasurer_bonus != 0:
            treasurer_effect = tax_income * treasurer_bonus // 10
            self.treasury_reserves += treasurer_effect
        
        # War effects
        for enemy in self.at_war_with:
            # Wars are costly
            war_cost = random.randint(500, 1500)
            self.treasury_reserves -= war_cost
            
            # Wars affect popularity
            self.popularity -= random.randint(3, 8)
            
            # Wars affect military strength
            battle_outcome = random.random()
            if battle_outcome < 0.4:  # Victory
                self.military_strength = min(100, self.military_strength + random.randint(1, 5))
                self.popularity += random.randint(5, 10)
            elif battle_outcome < 0.7:  # Stalemate
                self.military_strength = max(1, self.military_strength - random.randint(1, 3))
            else:  # Defeat
                self.military_strength = max(1, self.military_strength - random.randint(5, 10))
                self.popularity -= random.randint(5, 15)
        
        # Military maintenance costs
        military_upkeep = int(self.military_strength * 20)
        self.treasury_reserves -= military_upkeep
        
        # Update construction projects
        self.completed_monuments = []
        if hasattr(self, "construction_projects") and self.construction_projects:
            remaining_projects = []
            for project in self.construction_projects:
                project["years_remaining"] -= 1
                
                if project["years_remaining"] <= 0:
                    # Project completed
                    self.popularity += project["popularity_gain"]
                    self.completed_monuments.append(project["name"])
                else:
                    # Project still in progress
                    remaining_projects.append(project)
            
            self.construction_projects = remaining_projects
        
        # Random events
        event_roll = random.random()
        if event_roll < 0.1:
            # Scandal
            self.popularity -= random.randint(5, 15)
        elif event_roll < 0.2:
            # Good harvest
            self.treasury_reserves += random.randint(500, 1000)
            self.popularity += random.randint(3, 8)
        
        # Ensure values stay within bounds
        self.popularity = max(0, min(100, self.popularity))
        
        # If treasury is negative, take debt penalties
        if self.treasury_reserves < 0:
            self.popularity -= random.randint(5, 15)
            # In a real game, you might add more severe consequences
    
    def display_status(self, interface):
        """Display the character's status.
        
        Args:
            interface: The game interface.
        """
        interface.display_message(f"=== {self.name}, {self.role} of {self.kingdom} ===")
        interface.display_message(f"Age: {self.age}")
        interface.display_message(f"Personal Wealth: {self.wealth} coins")
        interface.display_message(f"Royal Treasury: {self.treasury_reserves} coins")
        interface.display_message(f"Tax Rate: {self.taxes}%")
        interface.display_message(f"Popularity: {self.popularity}/100")
        interface.display_message(f"Military Strength: {self.military_strength}/100")
        
        # Display completed monuments
        if hasattr(self, "completed_monuments") and self.completed_monuments:
            interface.display_message("\nCompleted Monuments:")
            for monument in self.completed_monuments:
                interface.display_message(f"  - {monument} has been completed!")
            # Clear the list after displaying
            self.completed_monuments = []
        
        # Display ongoing construction projects
        if hasattr(self, "construction_projects") and self.construction_projects:
            interface.display_message("\nOngoing Construction:")
            for project in self.construction_projects:
                interface.display_message(f"  - {project['name']} - {project['years_remaining']} years remaining")
        
        if self.at_war_with:
            interface.display_message("\nCurrently at War with:")
            for enemy in self.at_war_with:
                interface.display_message(f"  - {enemy}")
        
        interface.display_message("\nRoyal Advisors:")
        for position, competence in self.advisors.items():
            rating = "Excellent" if competence >= 80 else "Good" if competence >= 60 else "Average" if competence >= 40 else "Poor"
            interface.display_message(f"  {position}: {rating} ({competence}/100)") 