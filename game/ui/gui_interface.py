"""
GUI Interface - Handles the graphical user interface for the game using Pygame
"""
import os
import time
import pygame
import pygame.freetype
import random

class GUIInterface:
    """Graphical user interface for the game using Pygame."""
    
    def __init__(self):
        """Initialize the GUI interface."""
        pygame.init()
        
        # Screen dimensions
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Medieval Life Simulator")
        
        # Game manager reference (will be set later)
        self.game_manager = None
        
        # Colors - define these first so they can be used by other initialization code
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (150, 150, 150)
        self.LIGHT_GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.BROWN = (139, 69, 19)
        self.LIGHT_BROWN = (160, 82, 45)
        self.DARK_BROWN = (101, 67, 33)
        self.GOLD = (212, 175, 55)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 128, 0)
        self.BLUE = (0, 0, 255)
        
        # Updated medieval color palette
        self.PARCHMENT = (255, 252, 220)
        self.ROYAL_BLUE = (65, 105, 225)
        self.ROYAL_PURPLE = (120, 81, 169)
        self.DARK_RED = (139, 0, 0)
        self.FOREST_GREEN = (34, 139, 34)
        self.GOLD_HIGHLIGHT = (255, 215, 0)
        self.STONE_GRAY = (169, 169, 169)
        self.WOOD_BROWN = (133, 94, 66)
        
        # Create a simple medieval-themed icon
        icon_size = 32
        icon = pygame.Surface((icon_size, icon_size))
        icon.fill(self.ROYAL_BLUE)
        
        # Draw a simple crown
        crown_color = (255, 215, 0)  # Gold
        # Base of crown
        pygame.draw.rect(icon, crown_color, (4, 20, 24, 8))
        # Crown spikes
        pygame.draw.polygon(icon, crown_color, [(4, 20), (8, 10), (12, 20)])
        pygame.draw.polygon(icon, crown_color, [(12, 20), (16, 5), (20, 20)])
        pygame.draw.polygon(icon, crown_color, [(20, 20), (24, 10), (28, 20)])
        # Crown jewels
        pygame.draw.circle(icon, (255, 0, 0), (8, 15), 2)  # Ruby
        pygame.draw.circle(icon, (0, 0, 255), (16, 12), 2)  # Sapphire
        pygame.draw.circle(icon, (0, 255, 0), (24, 15), 2)  # Emerald
        
        pygame.display.set_icon(icon)
        
        # Fonts
        self.font_small = pygame.freetype.SysFont("Times New Roman", 16)
        self.font_medium = pygame.freetype.SysFont("Times New Roman", 24)
        self.font_large = pygame.freetype.SysFont("Times New Roman", 32)
        self.font_title = pygame.freetype.SysFont("Times New Roman", 48)
        
        # Load background image
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(self.PARCHMENT)
        
        # Create a parchment texture effect
        for i in range(2000):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            radius = random.randint(1, 3)
            shade = random.randint(0, 20)
            color = (255 - shade, 252 - shade, 220 - shade)
            pygame.draw.circle(self.background, color, (x, y), radius)
        
        # Message log
        self.message_log = []
        self.max_messages = 10
        
        # Input field
        self.input_text = ""
        self.input_active = False
        
        # Menu options
        self.menu_options = []
        self.menu_title = ""
        self.menu_active = False
        self.selected_option = 0
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Game state
        self.running = True
        self.waiting_for_input = False
        self.waiting_for_menu = False
        self.input_result = None
        self.menu_result = None
    
    def clear_screen(self):
        """Clear the screen."""
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
    
    def display_message(self, message):
        """Display a message on the screen.
        
        Args:
            message: The message to display.
        """
        # Add message to log
        self.message_log.append(message)
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
        
        # Update display
        self._update_display()
    
    def get_input(self, prompt):
        """Get input from the user.
        
        Args:
            prompt: The prompt to display to the user.
            
        Returns:
            The user's input.
        """
        # Display prompt
        self.display_message(prompt)
        
        # Set up input field
        self.input_text = ""
        self.input_active = True
        self.waiting_for_input = True
        
        # Wait for input
        while self.waiting_for_input and self.running:
            self._handle_events()
            self._update_display()
            self.clock.tick(self.fps)
        
        # Return input
        return self.input_result
    
    def display_menu(self, title, options):
        """Display a menu with options.
        
        Args:
            title: The menu title.
            options: A list of options to display.
            
        Returns:
            The index of the chosen option, or None if the menu was closed.
        """
        # Add message to log
        self.message_log.append(f">>> {title}")
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
        
        # Set up menu
        self.menu_title = title
        self.menu_options = options
        self.menu_active = True
        self.waiting_for_menu = True
        self.selected_option = 0
        self.menu_result = None
        
        # Update display
        self._update_display()
        
        # Wait for menu selection
        while self.waiting_for_menu and self.running:
            self._handle_events()
            self.clock.tick(self.fps)
        
        # Clean up
        self.menu_active = False
        
        # Return result
        return self.menu_result
    
    def display_character_sheet(self, character):
        """Display the character sheet.
        
        Args:
            character: The character to display.
        """
        # Clear screen
        self.clear_screen()
        
        # Draw decorative border
        border_width = 5
        border_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.screen, self.WOOD_BROWN, border_rect, border_width)
        
        # Draw main panel
        main_panel = pygame.Rect(20, 20, self.width - 40, self.height - 40)
        pygame.draw.rect(self.screen, self.PARCHMENT, main_panel, 0, 10)
        pygame.draw.rect(self.screen, self.WOOD_BROWN, main_panel, 2, 10)
        
        # Draw title
        title_rect = pygame.Rect(30, 30, main_panel.width - 20, 60)
        pygame.draw.rect(self.screen, self.ROYAL_BLUE, title_rect, 0, 5)
        pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, title_rect, 2, 5)
        
        # Character name and role
        name_text = f"{character.name} the {character.role.capitalize()}"
        self.font_large.render_to(self.screen, (self.width // 2 - len(name_text) * 8, 45), name_text, self.WHITE)
        
        # Create a tabbed interface
        tab_y = title_rect.bottom + 20
        tab_height = 40
        tab_width = 200
        tab_padding = 5
        
        tabs = ["Basic Info", "Attributes", "Skills", "Family"]
        active_tab = 0
        
        # Draw tabs
        tab_buttons = []
        tab_x = 30
        for i, tab in enumerate(tabs):
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            
            # Active tab has different color
            if i == active_tab:
                pygame.draw.rect(self.screen, self.ROYAL_PURPLE, tab_rect, 0, 5)
                text_color = self.WHITE
            else:
                pygame.draw.rect(self.screen, self.DARK_BROWN, tab_rect, 0, 5)
                text_color = self.LIGHT_GRAY
            
            pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, tab_rect, 2, 5)
            
            # Center text in tab
            text_rect = self.font_medium.get_rect(tab)
            text_x = tab_rect.centerx - text_rect.width // 2
            text_y = tab_rect.centery - text_rect.height // 2
            self.font_medium.render_to(self.screen, (text_x, text_y), tab, text_color)
            
            tab_buttons.append(tab_rect)
            tab_x += tab_width + tab_padding
        
        # Content area
        content_y = tab_y + tab_height + 10
        content_height = main_panel.height - (content_y - main_panel.top) - 70  # Leave space for back button
        content_rect = pygame.Rect(30, content_y, main_panel.width - 60, content_height)
        pygame.draw.rect(self.screen, self.WHITE, content_rect, 0, 5)
        pygame.draw.rect(self.screen, self.WOOD_BROWN, content_rect, 2, 5)
        
        # Display content based on active tab
        if active_tab == 0:  # Basic Info
            self._display_basic_info(character, content_rect)
        elif active_tab == 1:  # Attributes
            self._display_attributes(character, content_rect)
        elif active_tab == 2:  # Skills
            self._display_skills(character, content_rect)
        elif active_tab == 3:  # Family
            self._display_family(character, content_rect)
        
        # Draw back button
        back_button = pygame.Rect(self.width // 2 - 100, self.height - 80, 200, 50)
        pygame.draw.rect(self.screen, self.ROYAL_BLUE, back_button, 0, 10)
        pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, back_button, 2, 10)
        self.font_medium.render_to(self.screen, (self.width // 2 - 30, self.height - 65), "Back", self.WHITE)
        
        # Update display
        pygame.display.flip()
        
        # Wait for tab selection or back button
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a tab was clicked
                    for i, tab_rect in enumerate(tab_buttons):
                        if tab_rect.collidepoint(event.pos):
                            active_tab = i
                            # Redraw the screen with the new active tab
                            self.display_character_sheet(character)
                            break
                    
                    # Check if back button was clicked
                    if back_button.collidepoint(event.pos):
                        waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                    # Allow number keys for quick tab selection
                    elif pygame.K_1 <= event.key <= pygame.K_4:
                        active_tab = event.key - pygame.K_1
                        # Redraw the screen with the new active tab
                        self.display_character_sheet(character)
            
            self.clock.tick(self.fps)
    
    def _display_basic_info(self, character, content_rect):
        """Display basic character information.
        
        Args:
            character: The character to display.
            content_rect: The rectangle to draw in.
        """
        x = content_rect.left + 20
        y = content_rect.top + 20
        line_height = 30
        
        # Basic stats
        self.font_medium.render_to(self.screen, (x, y), f"Age: {character.age}", self.DARK_BROWN)
        y += line_height
        
        self.font_medium.render_to(self.screen, (x, y), f"Gender: {character.gender.capitalize()}", self.DARK_BROWN)
        y += line_height
        
        self.font_medium.render_to(self.screen, (x, y), f"Birth Year: {character.birth_year}", self.DARK_BROWN)
        y += line_height
        
        # Health with bar
        health_text = f"Health: {character.health}/100"
        self.font_medium.render_to(self.screen, (x, y), health_text, self.DARK_BROWN)
        
        # Health bar
        bar_x = x + 200
        bar_width = 200
        bar_height = 20
        health_bar_bg = pygame.Rect(bar_x, y, bar_width, bar_height)
        health_bar_fill = pygame.Rect(bar_x, y, int(bar_width * character.health / 100), bar_height)
        
        # Color the health bar based on health level
        if character.health > 70:
            health_color = self.FOREST_GREEN
        elif character.health > 30:
            health_color = self.GOLD_HIGHLIGHT
        else:
            health_color = self.DARK_RED
        
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, health_bar_bg)
        pygame.draw.rect(self.screen, health_color, health_bar_fill)
        pygame.draw.rect(self.screen, self.DARK_BROWN, health_bar_bg, 1)
        y += line_height
        
        # Wealth
        self.font_medium.render_to(self.screen, (x, y), f"Wealth: {character.wealth} coins", self.DARK_BROWN)
        y += line_height * 2
        
        # Role-specific status
        self.font_large.render_to(self.screen, (x, y), f"{character.role.capitalize()} Status:", self.DARK_BROWN)
        y += line_height * 1.5
        
        # Get role-specific status
        status_lines = []
        
        # Create a temporary text interface to capture status lines
        class TempInterface:
            def display_message(self, message):
                status_lines.append(message)
        
        temp_interface = TempInterface()
        character.display_status(temp_interface)
        
        # Display role-specific status
        for line in status_lines:
            self.font_small.render_to(self.screen, (x + 20, y), line, self.DARK_BROWN)
            y += line_height
    
    def _display_attributes(self, character, content_rect):
        """Display character attributes.
        
        Args:
            character: The character to display.
            content_rect: The rectangle to draw in.
        """
        x = content_rect.left + 20
        y = content_rect.top + 20
        line_height = 40
        bar_width = 300
        bar_height = 25
        
        self.font_large.render_to(self.screen, (x, y), "Attributes", self.DARK_BROWN)
        y += line_height * 1.5
        
        # Display each attribute with a bar
        for attr, value in character.attributes.items():
            # Attribute name
            self.font_medium.render_to(self.screen, (x, y), f"{attr.capitalize()}:", self.DARK_BROWN)
            
            # Attribute bar
            bar_x = x + 150
            bar_bg = pygame.Rect(bar_x, y, bar_width, bar_height)
            bar_fill = pygame.Rect(bar_x, y, int(bar_width * value / 100), bar_height)
            
            # Color based on value
            if value > 70:
                color = self.FOREST_GREEN
            elif value > 40:
                color = self.GOLD_HIGHLIGHT
            else:
                color = self.DARK_RED
            
            pygame.draw.rect(self.screen, self.LIGHT_GRAY, bar_bg)
            pygame.draw.rect(self.screen, color, bar_fill)
            pygame.draw.rect(self.screen, self.DARK_BROWN, bar_bg, 1)
            
            # Value text
            self.font_small.render_to(self.screen, (bar_x + bar_width + 10, y + 5), str(value), self.DARK_BROWN)
            
            y += line_height
    
    def _display_skills(self, character, content_rect):
        """Display character skills.
        
        Args:
            character: The character to display.
            content_rect: The rectangle to draw in.
        """
        x = content_rect.left + 20
        y = content_rect.top + 20
        line_height = 40
        bar_width = 300
        bar_height = 25
        
        self.font_large.render_to(self.screen, (x, y), "Skills", self.DARK_BROWN)
        y += line_height * 1.5
        
        # Display each skill with a bar
        for skill, value in character.skills.items():
            # Skill name
            self.font_medium.render_to(self.screen, (x, y), f"{skill.capitalize()}:", self.DARK_BROWN)
            
            # Skill bar
            bar_x = x + 150
            bar_bg = pygame.Rect(bar_x, y, bar_width, bar_height)
            bar_fill = pygame.Rect(bar_x, y, int(bar_width * value / 100), bar_height)
            
            # Color based on value
            if value > 70:
                color = self.FOREST_GREEN
            elif value > 40:
                color = self.GOLD_HIGHLIGHT
            else:
                color = self.DARK_RED
            
            pygame.draw.rect(self.screen, self.LIGHT_GRAY, bar_bg)
            pygame.draw.rect(self.screen, color, bar_fill)
            pygame.draw.rect(self.screen, self.DARK_BROWN, bar_bg, 1)
            
            # Value text
            self.font_small.render_to(self.screen, (bar_x + bar_width + 10, y + 5), str(value), self.DARK_BROWN)
            
            y += line_height
    
    def _display_family(self, character, content_rect):
        """Display character family information.
        
        Args:
            character: The character to display.
            content_rect: The rectangle to draw in.
        """
        x = content_rect.left + 20
        y = content_rect.top + 20
        line_height = 30
        
        self.font_large.render_to(self.screen, (x, y), "Family", self.DARK_BROWN)
        y += line_height * 1.5
        
        # Spouse
        if hasattr(character, 'spouse') and character.spouse:
            self.font_medium.render_to(self.screen, (x, y), "Spouse:", self.DARK_BROWN)
            y += line_height
            
            spouse_info = f"{character.spouse.name}, {character.spouse.age} years old, {character.spouse.role.capitalize()}"
            self.font_small.render_to(self.screen, (x + 20, y), spouse_info, self.DARK_BROWN)
            y += line_height * 1.5
        else:
            self.font_medium.render_to(self.screen, (x, y), "Spouse: None", self.DARK_BROWN)
            y += line_height * 1.5
        
        # Children
        if hasattr(character, 'children') and character.children:
            self.font_medium.render_to(self.screen, (x, y), "Children:", self.DARK_BROWN)
            y += line_height
            
            for child in character.children:
                child_info = f"{child.name}, {child.age} years old, {child.gender.capitalize()}"
                self.font_small.render_to(self.screen, (x + 20, y), child_info, self.DARK_BROWN)
                y += line_height
        else:
            self.font_medium.render_to(self.screen, (x, y), "Children: None", self.DARK_BROWN)
    
    def display_game_status(self, game_year, player, actions, month=None, season=None):
        """Display the game status screen.
        
        Args:
            game_year: The current game year.
            player: The player character.
            actions: A list of available actions.
            month: The current month name (optional).
            season: The current season name (optional).
            
        Returns:
            The index of the chosen action, or None if the window was closed.
        """
        # Clear the screen
        self.clear_screen()
        
        # Set up the layout
        header_height = 80
        footer_height = 50
        content_height = self.height - header_height - footer_height
        
        # Draw the header
        header_rect = pygame.Rect(0, 0, self.width, header_height)
        pygame.draw.rect(self.screen, (50, 50, 80), header_rect)
        
        # Draw the year and character info
        self.font_large.render_to(self.screen, (20, 20), f"Year: {game_year}", self.WHITE)
        
        # Add month and season if provided
        if month and season:
            self.font_medium.render_to(self.screen, (20, 50), f"Month: {month} ({season})", self.WHITE)
        
        # Draw character info
        char_text = f"{player.name} the {player.role.capitalize()}"
        char_rect = self.font_large.get_rect(char_text)
        self.font_large.render_to(self.screen, (self.width - char_rect.width - 20, 20), char_text, self.WHITE)
        
        age_text = f"Age: {player.age}"
        age_rect = self.font_medium.get_rect(age_text)
        self.font_medium.render_to(self.screen, (self.width - age_rect.width - 20, 50), age_text, self.WHITE)
        
        # Draw the content area
        content_rect = pygame.Rect(0, header_height, self.width, content_height)
        pygame.draw.rect(self.screen, (30, 30, 50), content_rect)
        
        # Draw the character status
        status_width = self.width // 3
        status_rect = pygame.Rect(0, header_height, status_width, content_height)
        pygame.draw.rect(self.screen, (40, 40, 60), status_rect)
        
        # Draw status title
        status_title = "Status"
        status_rect = self.font_medium.get_rect(status_title)
        self.font_medium.render_to(self.screen, (status_width // 2 - status_rect.width // 2, header_height + 10), status_title, self.WHITE)
        
        # Draw health and wealth
        self.font_small.render_to(self.screen, (20, header_height + 50), f"Health: {player.health}/100", self.WHITE)
        self.font_small.render_to(self.screen, (20, header_height + 80), f"Wealth: {player.wealth} coins", self.WHITE)
        
        # Draw role-specific status
        status_lines = []
        
        # Create a temporary text interface to capture status lines
        class TempInterface:
            def __init__(self):
                self.status_lines = []
            
            def display_message(self, message):
                self.status_lines.append(message)
        
        temp_interface = TempInterface()
        player.display_status(temp_interface)
        
        # Display role-specific status
        y = header_height + 110
        for line in temp_interface.status_lines:
            self.font_small.render_to(self.screen, (20, y), line, self.WHITE)
            y += 25
        
        # Draw the actions
        actions_width = self.width - status_width
        actions_rect = pygame.Rect(status_width, header_height, actions_width, content_height)
        pygame.draw.rect(self.screen, (30, 30, 50), actions_rect)
        
        # Draw actions title
        actions_title = "Actions"
        actions_rect = self.font_medium.get_rect(actions_title)
        self.font_medium.render_to(self.screen, (status_width + actions_width // 2 - actions_rect.width // 2, header_height + 10), actions_title, self.WHITE)
        
        # Draw action buttons
        button_height = 40
        button_margin = 10
        button_width = actions_width - 2 * button_margin
        
        # Calculate how many buttons can fit in the content area
        max_buttons = (content_height - 50) // (button_height + button_margin)
        
        # If we have more actions than can fit, add pagination
        start_idx = 0
        end_idx = min(len(actions), max_buttons)
        
        # Clear buttons dictionary
        self.buttons = {}
        
        # Draw the action buttons
        for i in range(start_idx, end_idx):
            button_rect = pygame.Rect(
                status_width + button_margin,
                header_height + 50 + i * (button_height + button_margin),
                button_width,
                button_height
            )
            
            # Draw the button
            pygame.draw.rect(self.screen, (60, 60, 90), button_rect)
            pygame.draw.rect(self.screen, (100, 100, 140), button_rect, 2)
            
            # Draw the button text
            text_rect = self.font_small.get_rect(actions[i])
            text_x = button_rect.centerx - text_rect.width // 2
            text_y = button_rect.centery - text_rect.height // 2
            self.font_small.render_to(self.screen, (text_x, text_y), actions[i], self.WHITE)
            
            # Store the button rect for click detection
            self.buttons[i] = button_rect
        
        # Draw the footer
        footer_rect = pygame.Rect(0, self.height - footer_height, self.width, footer_height)
        pygame.draw.rect(self.screen, (50, 50, 80), footer_rect)
        
        # Update the display
        self._update_display()
        
        # Wait for user input
        self.menu_result = None
        while self.menu_result is None and self.running:
            self._handle_events()
        
        return self.menu_result
    
    def display_event(self, event_title, event_description):
        """Display an event with title and description.
        
        Args:
            event_title: The title of the event.
            event_description: The description of the event.
        """
        # Clear screen
        self.clear_screen()
        
        # Draw decorative border
        border_width = 5
        border_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.screen, self.WOOD_BROWN, border_rect, border_width)
        
        # Draw main panel
        main_panel = pygame.Rect(20, 20, self.width - 40, self.height - 40)
        pygame.draw.rect(self.screen, self.PARCHMENT, main_panel, 0, 10)
        pygame.draw.rect(self.screen, self.WOOD_BROWN, main_panel, 2, 10)
        
        # Draw title
        title_rect = pygame.Rect(30, 30, main_panel.width - 20, 60)
        pygame.draw.rect(self.screen, self.ROYAL_BLUE, title_rect, 0, 5)
        pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, title_rect, 2, 5)
        
        # Center title text
        title_text_rect = self.font_large.get_rect(event_title)
        title_x = title_rect.centerx - title_text_rect.width // 2
        title_y = title_rect.centery - title_text_rect.height // 2
        self.font_large.render_to(self.screen, (title_x, title_y), event_title, self.WHITE)
        
        # Content area
        content_y = title_rect.bottom + 20
        content_height = main_panel.height - (content_y - main_panel.top) - 80  # Leave space for continue button
        content_rect = pygame.Rect(30, content_y, main_panel.width - 60, content_height)
        pygame.draw.rect(self.screen, self.WHITE, content_rect, 0, 5)
        pygame.draw.rect(self.screen, self.WOOD_BROWN, content_rect, 2, 5)
        
        # Word wrap the description
        words = event_description.split()
        lines = []
        current_line = ""
        max_width = content_rect.width - 40
        
        for word in words:
            test_line = current_line + word + " "
            text_width = self.font_medium.get_rect(test_line).width
            
            if text_width < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)
        
        # Draw the wrapped text
        x = content_rect.left + 20
        y = content_rect.top + 20
        line_height = 30
        
        for line in lines:
            self.font_medium.render_to(self.screen, (x, y), line, self.DARK_BROWN)
            y += line_height
        
        # Draw continue button
        button_rect = pygame.Rect(self.width // 2 - 100, self.height - 80, 200, 50)
        pygame.draw.rect(self.screen, self.ROYAL_BLUE, button_rect, 0, 10)
        pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, button_rect, 2, 10)
        
        # Center button text
        button_text = "Continue"
        button_text_rect = self.font_medium.get_rect(button_text)
        button_x = button_rect.centerx - button_text_rect.width // 2
        button_y = button_rect.centery - button_text_rect.height // 2
        self.font_medium.render_to(self.screen, (button_x, button_y), button_text, self.WHITE)
        
        # Update display
        pygame.display.flip()
        
        # Wait for button click or key press
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        waiting = False
            
            self.clock.tick(self.fps)
    
    def display_notification(self, message):
        """Display a notification message.
        
        Args:
            message: The notification message to display.
        """
        # Create notification surface
        notification_width = min(len(message) * 12 + 40, self.width - 100)
        notification_height = 60
        notification = pygame.Surface((notification_width, notification_height), pygame.SRCALPHA)
        
        # Draw notification background with rounded corners and semi-transparency
        notification_rect = pygame.Rect(0, 0, notification_width, notification_height)
        pygame.draw.rect(notification, (self.ROYAL_BLUE[0], self.ROYAL_BLUE[1], self.ROYAL_BLUE[2], 230), 
                        notification_rect, 0, 15)
        pygame.draw.rect(notification, (self.GOLD_HIGHLIGHT[0], self.GOLD_HIGHLIGHT[1], self.GOLD_HIGHLIGHT[2], 255), 
                        notification_rect, 2, 15)
        
        # Add a decorative icon
        icon_radius = 15
        pygame.draw.circle(notification, self.GOLD_HIGHLIGHT, (icon_radius + 10, notification_height // 2), icon_radius)
        
        # Draw an exclamation mark or info icon
        pygame.draw.rect(notification, self.ROYAL_BLUE, 
                        (icon_radius + 7, notification_height // 2 - 10, 6, 15))
        pygame.draw.circle(notification, self.ROYAL_BLUE, 
                          (icon_radius + 10, notification_height // 2 + 10), 3)
        
        # Render message text with shadow for better readability
        font = pygame.freetype.SysFont("Times New Roman", 20)
        font.render_to(notification, (icon_radius * 2 + 12, notification_height // 2 - 10), message, self.BLACK)
        font.render_to(notification, (icon_radius * 2 + 10, notification_height // 2 - 12), message, self.WHITE)
        
        # Display notification at the top of the screen
        self.screen.blit(notification, (self.width // 2 - notification_width // 2, 20))
        pygame.display.update(pygame.Rect(self.width // 2 - notification_width // 2, 20, 
                                         notification_width, notification_height))
        
        # Pause briefly
        time.sleep(1.5)
    
    def display_start_screen(self):
        """Display the game start screen.
        
        Returns:
            bool: True if the user chose to start/load a game, False if they chose to quit.
        """
        # Clear screen and draw background
        self.screen.blit(self.background, (0, 0))
        
        # Title
        title_surface = pygame.Surface((600, 100))
        title_surface.fill(self.ROYAL_BLUE)
        title_rect = title_surface.get_rect(center=(self.width // 2, 100))
        pygame.draw.rect(self.screen, self.ROYAL_BLUE, title_rect, 0, 15)
        pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, title_rect, 3, 15)
        self.font_title.render_to(self.screen, (self.width // 2 - 250, 80), "Medieval Life Simulator", self.WHITE)
        
        # Button dimensions
        button_width = 300
        button_height = 60
        button_spacing = 100
        start_y = 400
        
        # New Game button
        new_game_button = pygame.Rect(self.width // 2 - button_width//2, start_y, button_width, button_height)
        pygame.draw.rect(self.screen, self.ROYAL_BLUE, new_game_button, 0, 15)
        pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, new_game_button, 3, 15)
        self.font_large.render_to(self.screen, (self.width // 2 - 100, start_y + 15), "New Game", self.WHITE)
        
        # Load Game button
        load_game_button = pygame.Rect(self.width // 2 - button_width//2, start_y + button_spacing, button_width, button_height)
        pygame.draw.rect(self.screen, self.ROYAL_BLUE, load_game_button, 0, 15)
        pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, load_game_button, 3, 15)
        self.font_large.render_to(self.screen, (self.width // 2 - 100, start_y + button_spacing + 15), "Load Game", self.WHITE)
        
        # Quit button
        quit_button = pygame.Rect(self.width // 2 - button_width//2, start_y + button_spacing * 2, button_width, button_height)
        pygame.draw.rect(self.screen, self.DARK_RED, quit_button, 0, 15)
        pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, quit_button, 3, 15)
        self.font_large.render_to(self.screen, (self.width // 2 - 50, start_y + button_spacing * 2 + 15), "Quit", self.WHITE)
        
        # Update display
        pygame.display.flip()
        
        # Wait for button click
        waiting = True
        start_game = False
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_button.collidepoint(event.pos):
                        start_game = True
                        waiting = False
                    elif load_game_button.collidepoint(event.pos):
                        # Show load game menu
                        save_files = self.game_manager.save_system.get_save_files()
                        if save_files:
                            save_idx = self.display_menu("Choose a save file to load:", save_files + ["Cancel"])
                            if save_idx < len(save_files):  # Not Cancel
                                if self.game_manager.load_game(save_files[save_idx]):
                                    start_game = True
                                    waiting = False
                        else:
                            self.display_event("Load Game", "No save files found.")
                    elif quit_button.collidepoint(event.pos):
                        start_game = False
                        waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start_game = True
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        start_game = False
                        waiting = False
            
            self.clock.tick(self.fps)
        
        return start_game
    
    def _update_display(self):
        """Update the display."""
        # Clear screen
        self.screen.blit(self.background, (0, 0))
        
        # Draw decorative border
        border_width = 5
        border_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.screen, self.WOOD_BROWN, border_rect, border_width)
        
        # Draw message log with scroll-like appearance
        log_rect = pygame.Rect(20, 20, self.width - 40, 300)
        pygame.draw.rect(self.screen, self.PARCHMENT, log_rect, 0, 10)
        pygame.draw.rect(self.screen, self.WOOD_BROWN, log_rect, 2, 10)
        
        # Add scroll ends
        scroll_end_height = 30
        scroll_end_width = log_rect.width
        
        # Top scroll end
        pygame.draw.ellipse(self.screen, self.PARCHMENT, 
                           (log_rect.left, log_rect.top - scroll_end_height//2, 
                            scroll_end_width, scroll_end_height))
        pygame.draw.ellipse(self.screen, self.WOOD_BROWN, 
                           (log_rect.left, log_rect.top - scroll_end_height//2, 
                            scroll_end_width, scroll_end_height), 2)
        
        # Bottom scroll end
        pygame.draw.ellipse(self.screen, self.PARCHMENT, 
                           (log_rect.left, log_rect.bottom - scroll_end_height//2, 
                            scroll_end_width, scroll_end_height))
        pygame.draw.ellipse(self.screen, self.WOOD_BROWN, 
                           (log_rect.left, log_rect.bottom - scroll_end_height//2, 
                            scroll_end_width, scroll_end_height), 2)
        
        # Draw messages with improved styling
        y_pos = 30
        for message in self.message_log:
            self.font_small.render_to(self.screen, (30, y_pos), message, self.DARK_BROWN)
            y_pos += 25
        
        # Draw input field if active with improved styling
        if self.input_active:
            input_rect = pygame.Rect(20, 340, self.width - 40, 40)
            pygame.draw.rect(self.screen, self.WHITE, input_rect, 0, 5)
            pygame.draw.rect(self.screen, self.ROYAL_BLUE, input_rect, 2, 5)
            self.font_medium.render_to(self.screen, (30, 350), self.input_text, self.BLACK)
            
            # Add blinking cursor
            if pygame.time.get_ticks() % 1000 < 500:  # Blink every half second
                cursor_pos = self.font_medium.get_rect(self.input_text).width + 30
                pygame.draw.line(self.screen, self.BLACK, 
                                (cursor_pos, 350), 
                                (cursor_pos, 370), 2)
        
        # Draw menu if active with improved styling
        if self.menu_active:
            menu_rect = pygame.Rect(20, 400, self.width - 40, 300)
            pygame.draw.rect(self.screen, self.ROYAL_BLUE, menu_rect, 0, 10)
            pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, menu_rect, 2, 10)
            
            # Draw title with decorative header
            title_rect = pygame.Rect(30, 410, menu_rect.width - 20, 40)
            pygame.draw.rect(self.screen, self.DARK_BROWN, title_rect, 0, 5)
            pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, title_rect, 2, 5)
            self.font_medium.render_to(self.screen, (40, 420), self.menu_title, self.WHITE)
            
            # Draw options with improved styling
            y_pos = 470
            for i, option in enumerate(self.menu_options):
                option_rect = pygame.Rect(50, y_pos - 5, menu_rect.width - 100, 30)
                
                # Highlight selected option with better visual feedback
                if i == self.selected_option:
                    pygame.draw.rect(self.screen, self.ROYAL_PURPLE, option_rect, 0, 5)
                    pygame.draw.rect(self.screen, self.GOLD_HIGHLIGHT, option_rect, 2, 5)
                    text_color = self.WHITE
                    # Add arrow indicator
                    pygame.draw.polygon(self.screen, self.GOLD_HIGHLIGHT, 
                                       [(35, y_pos + 10), (45, y_pos + 5), (45, y_pos + 15)])
                else:
                    text_color = self.WHITE
                
                self.font_small.render_to(self.screen, (60, y_pos), f"{i+1}. {option}", text_color)
                y_pos += 35  # Increased spacing between options
        
        # Update display
        pygame.display.flip()
    
    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                # Also exit any waiting loops
                self.waiting_for_input = False
                self.waiting_for_menu = False
                pygame.quit()
                return
            
            # Handle key events
            if event.type == pygame.KEYDOWN:
                if self.input_active and self.waiting_for_input:
                    if event.key == pygame.K_RETURN:
                        self.input_result = self.input_text
                        self.input_text = ""
                        self.input_active = False
                        self.waiting_for_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        # Add character to input text
                        if len(event.unicode) > 0 and ord(event.unicode) >= 32:
                            self.input_text += event.unicode
                    
                    # Update display
                    self._update_display()
                
                elif self.menu_active and self.waiting_for_menu:
                    if event.key == pygame.K_UP:
                        self.selected_option = max(0, self.selected_option - 1)
                        self._update_display()
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = min(len(self.menu_options) - 1, self.selected_option + 1)
                        self._update_display()
                    elif event.key == pygame.K_RETURN:
                        self.menu_result = self.selected_option
                        self.menu_active = False
                        self.waiting_for_menu = False
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel menu
                        self.menu_result = None
                        self.menu_active = False
                        self.waiting_for_menu = False
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        option_idx = event.key - pygame.K_1
                        if option_idx < len(self.menu_options):
                            self.menu_result = option_idx
                            self.menu_active = False
                            self.waiting_for_menu = False
                    
                    # Update display
                    self._update_display()
            
            # Handle mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_active:
                    # Check if clicked on a menu option
                    y_pos = 450
                    for i in range(len(self.menu_options)):
                        option_rect = pygame.Rect(50, y_pos - 5, self.width - 140, 30)
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = i
                            self.menu_result = i
                            self.menu_active = False
                            self.waiting_for_menu = False
                        y_pos += 30 