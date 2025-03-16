"""
Story Arc - Represents a multi-year story arc with cascading consequences
"""
import random
from game.events.event import Event
from game.events.story_arc_base import StoryArc
from game.events.illicit_arcs import get_illicit_arcs
from game.events.criminal_arcs import get_criminal_arcs

class StoryArcManager:
    """Manages story arcs in the game."""
    
    def __init__(self, game_manager):
        """Initialize the story arc manager.
        
        Args:
            game_manager: The game manager.
        """
        self.game_manager = game_manager
        self.story_arcs = self._initialize_story_arcs()
        self.active_arcs = []
        self.completed_arcs = []
        self.arc_cooldown = {}  # To prevent the same arc from triggering too frequently
        self.max_active_arcs = 2  # Maximum number of active story arcs at once
        
        # Define incompatible arc types
        # Arcs in the same group cannot be active simultaneously
        self.incompatible_groups = {
            "romance": ["adultery", "forbidden_romance", "same_sex_relationship"],
            "crime": ["smuggling", "theft", "corruption", "criminal_temptation"],
            "politics": ["noble_conspiracy"]
        }
        
        # Track NPCs involved in story arcs
        self.arc_npcs = {}  # Maps arc_id to list of NPCs
    
    def _initialize_story_arcs(self):
        """Initialize the available story arcs.
        
        Returns:
            A dictionary of story arcs.
        """
        # Define story arcs here
        story_arcs = {
            # Noble Conspiracy Arc
            "noble_conspiracy": StoryArc(
                "noble_conspiracy",
                "Noble Conspiracy",
                "You discover a conspiracy among the nobility.",
                [
                    {
                        "title": "Whispers of Treason",
                        "description": "You overhear whispers of a plot against the crown. Several nobles appear to be involved in a conspiracy.",
                        "effects": {"attribute_cunning": 5},
                        "choices": [
                            {
                                "text": "Investigate discreetly",
                                "effects": {"wealth": -50},
                                "outcome": "You spend resources to investigate the conspiracy discreetly."
                            },
                            {
                                "text": "Report to the authorities immediately",
                                "effects": {},
                                "outcome": "You report what you've heard to the royal guards."
                            },
                            {
                                "text": "Ignore it as idle gossip",
                                "effects": {},
                                "outcome": "You dismiss the whispers as idle gossip and go about your business."
                            }
                        ],
                        "years_until_next": 1
                    },
                    {
                        "title": "Growing Evidence",
                        "description": "The conspiracy seems to be growing. You've gathered more evidence of the plot.",
                        "effects": {},
                        "conditional_events": [
                            {
                                "condition": {"stage": 0, "choice": 0},
                                "description": "Your discreet investigation has yielded valuable information. You've identified several key conspirators and learned some details of their plan.",
                                "effects": {"attribute_cunning": 5},
                                "choices": [
                                    {
                                        "text": "Continue investigating",
                                        "effects": {"wealth": -100},
                                        "outcome": "You delve deeper into the conspiracy, risking your own safety."
                                    },
                                    {
                                        "text": "Report to the authorities with evidence",
                                        "effects": {},
                                        "outcome": "You take your evidence to the royal guards."
                                    },
                                    {
                                        "text": "Confront one of the conspirators",
                                        "effects": {},
                                        "outcome": "You decide to confront one of the conspirators directly."
                                    }
                                ]
                            },
                            {
                                "condition": {"stage": 0, "choice": 1},
                                "description": "The authorities have been investigating based on your report. They've made some progress but need more evidence.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Offer to help the investigation",
                                        "effects": {},
                                        "outcome": "You volunteer to assist the royal investigators."
                                    },
                                    {
                                        "text": "Let the authorities handle it",
                                        "effects": {},
                                        "outcome": "You decide to let the authorities continue their investigation without your involvement."
                                    },
                                    {
                                        "text": "Warn the conspirators anonymously",
                                        "effects": {},
                                        "outcome": "You anonymously warn the conspirators that they are being investigated."
                                    }
                                ]
                            },
                            {
                                "condition": {"stage": 0, "choice": 2},
                                "description": "Despite your initial dismissal, evidence of the conspiracy has become impossible to ignore. A servant brings you a letter that was mistakenly delivered to you, containing details of the plot.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Begin investigating now",
                                        "effects": {"wealth": -75},
                                        "outcome": "Better late than never, you begin investigating the conspiracy."
                                    },
                                    {
                                        "text": "Report to the authorities with the letter",
                                        "effects": {},
                                        "outcome": "You take the incriminating letter to the royal guards."
                                    },
                                    {
                                        "text": "Destroy the letter and stay uninvolved",
                                        "effects": {},
                                        "outcome": "You burn the letter and try to stay out of the dangerous situation."
                                    }
                                ]
                            }
                        ],
                        "years_until_next": 1
                    },
                    {
                        "title": "The Plot Revealed",
                        "description": "The conspiracy has reached its critical point. The plotters are ready to act.",
                        "effects": {},
                        "conditional_events": [
                            # Many conditional events based on previous choices would go here
                            # This is a simplified example
                            {
                                "condition": {"stage": 1, "choice": 0},
                                "description": "Your thorough investigation has uncovered the full extent of the plot. The conspirators plan to assassinate the king during the upcoming festival.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Warn the king personally",
                                        "effects": {"wealth": 500, "attribute_courage": 10},
                                        "outcome": "You rush to warn the king personally. He is grateful for your loyalty and rewards you handsomely."
                                    },
                                    {
                                        "text": "Set a trap for the conspirators",
                                        "effects": {"wealth": 300, "attribute_cunning": 10},
                                        "outcome": "You work with the royal guards to set a trap for the conspirators. The plot is foiled and the conspirators are arrested."
                                    },
                                    {
                                        "text": "Join the conspiracy",
                                        "effects": {"wealth": -200, "attribute_cunning": 5},
                                        "outcome": "You decide to join the conspiracy, but your late entry makes the other conspirators suspicious. The plot fails and you barely escape with your life."
                                    }
                                ]
                            }
                        ]
                    }
                ],
                role_specific=True,
                roles=["noble", "knight", "king"],
                prerequisites={"age": 25, "wealth": 500}
            ),
            
            # Forbidden Romance Arc
            "forbidden_romance": StoryArc(
                "forbidden_romance",
                "Forbidden Romance",
                "You find yourself drawn into a forbidden romance.",
                [
                    {
                        "title": "A Chance Encounter",
                        "description": "At a social gathering, you meet someone who captivates your attention. However, there are social barriers that make any relationship inappropriate.",
                        "effects": {"attribute_charisma": 5},
                        "choices": [
                            {
                                "text": "Pursue the attraction discreetly",
                                "effects": {},
                                "outcome": "You decide to pursue the attraction, arranging discreet meetings."
                            },
                            {
                                "text": "Acknowledge the attraction but maintain distance",
                                "effects": {},
                                "outcome": "You acknowledge the mutual attraction but decide to maintain a respectful distance."
                            },
                            {
                                "text": "Ignore the attraction completely",
                                "effects": {},
                                "outcome": "You ignore the attraction and focus on your duties."
                            }
                        ],
                        "years_until_next": 1
                    },
                    {
                        "title": "Deepening Feelings",
                        "description": "A year has passed, and your feelings have only grown stronger.",
                        "effects": {},
                        "conditional_events": [
                            {
                                "condition": {"stage": 0, "choice": 0},
                                "description": "Your discreet relationship has blossomed into something deeper, but the risk of discovery grows with each meeting.",
                                "effects": {"attribute_charisma": 5},
                                "choices": [
                                    {
                                        "text": "Continue the secret relationship",
                                        "effects": {},
                                        "outcome": "You continue your secret meetings, finding moments of happiness amidst the danger."
                                    },
                                    {
                                        "text": "End the relationship for safety",
                                        "effects": {"health": -5},  # Heartbreak
                                        "outcome": "With a heavy heart, you end the relationship to protect both of you from the consequences of discovery."
                                    },
                                    {
                                        "text": "Plan to overcome the social barriers",
                                        "effects": {"wealth": -100},
                                        "outcome": "You begin making plans to overcome the social barriers that keep you apart."
                                    }
                                ]
                            },
                            {
                                "condition": {"stage": 0, "choice": 1},
                                "description": "Despite maintaining distance, your paths continue to cross, and the tension between you is palpable.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Give in to your feelings",
                                        "effects": {},
                                        "outcome": "You can no longer deny your feelings and begin a discreet relationship."
                                    },
                                    {
                                        "text": "Continue to maintain distance",
                                        "effects": {"attribute_willpower": 5},
                                        "outcome": "You strengthen your resolve and continue to maintain a respectful distance."
                                    },
                                    {
                                        "text": "Arrange to stop crossing paths",
                                        "effects": {},
                                        "outcome": "You make arrangements to ensure your paths no longer cross, ending the temptation."
                                    }
                                ]
                            },
                            {
                                "condition": {"stage": 0, "choice": 2},
                                "description": "Despite your efforts to ignore the attraction, you find yourself thinking about the person often.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Reconsider and pursue the attraction",
                                        "effects": {},
                                        "outcome": "You change your mind and decide to pursue the attraction after all."
                                    },
                                    {
                                        "text": "Maintain your distance",
                                        "effects": {"attribute_willpower": 10},
                                        "outcome": "You maintain your distance, focusing on your duties and responsibilities."
                                    },
                                    {
                                        "text": "Seek a socially acceptable partner",
                                        "effects": {},
                                        "outcome": "You decide to seek a more socially acceptable partner to help forget the attraction."
                                    }
                                ]
                            }
                        ],
                        "years_until_next": 1
                    },
                    {
                        "title": "Moment of Truth",
                        "description": "The relationship has reached a critical point where decisions must be made.",
                        "effects": {},
                        "conditional_events": [
                            # Many conditional events based on previous choices would go here
                            # This is a simplified example
                            {
                                "condition": {"stage": 1, "choice": 0},
                                "description": "Your secret relationship has been discovered. Rumors are spreading, and you face potential scandal and consequences.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Defy convention and publicly acknowledge the relationship",
                                        "effects": {"wealth": -200, "attribute_courage": 15},
                                        "outcome": "You defy social conventions and publicly acknowledge your relationship. You face significant social and financial consequences, but gain respect from some for your courage."
                                    },
                                    {
                                        "text": "Deny everything and end the relationship",
                                        "effects": {"health": -10, "attribute_cunning": 5},
                                        "outcome": "You deny the rumors and end the relationship. The scandal eventually dies down, but you are left with a broken heart."
                                    },
                                    {
                                        "text": "Flee together to start a new life elsewhere",
                                        "effects": {"wealth": -500, "attribute_courage": 10},
                                        "outcome": "You decide to flee together to a place where you can start anew without the social barriers that kept you apart."
                                    }
                                ]
                            }
                        ]
                    }
                ],
                role_specific=False,
                prerequisites={"age": 16}
            ),
            
            # Criminal Temptation Arc
            "criminal_temptation": StoryArc(
                "criminal_temptation",
                "Criminal Temptation",
                "You are presented with opportunities for illicit gain.",
                [
                    {
                        "title": "An Offer",
                        "description": "A shady character approaches you with an opportunity for easy money through illegal means.",
                        "effects": {},
                        "choices": [
                            {
                                "text": "Accept the offer",
                                "effects": {"wealth": 200, "attribute_cunning": 5},
                                "outcome": "You accept the offer and participate in the illegal activity, earning a tidy sum."
                            },
                            {
                                "text": "Decline politely",
                                "effects": {},
                                "outcome": "You decline the offer but maintain a cordial relationship with the shady character."
                            },
                            {
                                "text": "Report to the authorities",
                                "effects": {"attribute_honor": 5},
                                "outcome": "You report the offer to the local authorities."
                            }
                        ],
                        "years_until_next": 1
                    },
                    {
                        "title": "Deeper Involvement",
                        "description": "Your previous choices have led to new developments in your relationship with the criminal world.",
                        "effects": {},
                        "conditional_events": [
                            {
                                "condition": {"stage": 0, "choice": 0},
                                "description": "Having proven yourself reliable, you're offered a more significant role in the criminal operation with greater rewards and risks.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Accept the larger role",
                                        "effects": {"wealth": 500, "attribute_cunning": 10},
                                        "outcome": "You accept the larger role, becoming more deeply involved in the criminal world."
                                    },
                                    {
                                        "text": "Stay at your current level",
                                        "effects": {"wealth": 100},
                                        "outcome": "You decide to stay at your current level of involvement, not wanting to take on more risk."
                                    },
                                    {
                                        "text": "Try to leave the operation",
                                        "effects": {},
                                        "outcome": "You try to distance yourself from the criminal operation."
                                    }
                                ]
                            },
                            {
                                "condition": {"stage": 0, "choice": 1},
                                "description": "The shady character returns with a more tempting offer, suggesting that your skills would be particularly valuable.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Accept this time",
                                        "effects": {"wealth": 300, "attribute_cunning": 5},
                                        "outcome": "This time, you accept the offer and join the criminal operation."
                                    },
                                    {
                                        "text": "Decline again",
                                        "effects": {"attribute_willpower": 5},
                                        "outcome": "You decline again, firmly establishing your disinterest in criminal activities."
                                    },
                                    {
                                        "text": "Pretend to accept but inform authorities",
                                        "effects": {"attribute_cunning": 10, "attribute_honor": 5},
                                        "outcome": "You pretend to accept the offer but secretly inform the authorities, becoming an informant."
                                    }
                                ]
                            },
                            {
                                "condition": {"stage": 0, "choice": 2},
                                "description": "The authorities have been monitoring the criminal operation based on your information. They now ask for your help in a sting operation.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Agree to help with the sting",
                                        "effects": {"attribute_courage": 10, "attribute_honor": 10},
                                        "outcome": "You agree to help the authorities with their sting operation against the criminals."
                                    },
                                    {
                                        "text": "Decline further involvement",
                                        "effects": {},
                                        "outcome": "You decline further involvement, feeling you've done your civic duty by reporting the initial offer."
                                    },
                                    {
                                        "text": "Warn the criminals anonymously",
                                        "effects": {"attribute_honor": -10},
                                        "outcome": "For reasons of your own, you anonymously warn the criminals about the authorities' plans."
                                    }
                                ]
                            }
                        ],
                        "years_until_next": 1
                    },
                    {
                        "title": "The Reckoning",
                        "description": "Your involvement with the criminal world reaches a climax.",
                        "effects": {},
                        "conditional_events": [
                            # Many conditional events based on previous choices would go here
                            # This is a simplified example
                            {
                                "condition": {"stage": 1, "choice": 0},
                                "description": "Your criminal activities have made you wealthy, but the authorities are closing in. There's evidence linking you to the operation.",
                                "effects": {},
                                "choices": [
                                    {
                                        "text": "Flee with your ill-gotten gains",
                                        "effects": {"wealth": -1000},  # Cost of fleeing
                                        "outcome": "You flee with as much of your wealth as you can carry, leaving behind your old life to start anew elsewhere."
                                    },
                                    {
                                        "text": "Turn yourself in and cooperate",
                                        "effects": {"wealth": -2000, "attribute_honor": 15},
                                        "outcome": "You turn yourself in and cooperate with the authorities. Your sentence is reduced, but you lose most of your wealth."
                                    },
                                    {
                                        "text": "Use wealth to bribe officials",
                                        "effects": {"wealth": -1500, "attribute_cunning": 10},
                                        "outcome": "You use your wealth to bribe officials and destroy evidence. The investigation mysteriously stalls."
                                    }
                                ]
                            }
                        ]
                    }
                ],
                role_specific=False,
                prerequisites={"age": 18}
            )
        }
        
        # Add illicit relationship arcs
        illicit_arcs = get_illicit_arcs()
        story_arcs.update(illicit_arcs)
        
        # Add criminal activity arcs
        criminal_arcs = get_criminal_arcs()
        story_arcs.update(criminal_arcs)
        
        return story_arcs
    
    def update_for_new_year(self):
        """Update story arcs for a new year and check for new arcs to start.
        
        Returns:
            A list of events from active story arcs that are ready for this year.
        """
        events = []
        
        # Update active arcs
        for arc in self.active_arcs[:]:  # Copy the list to avoid modification issues during iteration
            if arc.update_for_new_year():
                # This arc is ready for its next stage
                event = arc.get_current_event(self.game_manager.player)
                if event:
                    events.append((arc, event))
        
        # Check if we can start new arcs
        if len(self.active_arcs) < self.max_active_arcs:
            # Check for new arcs to start
            player = self.game_manager.player
            
            # Get eligible arcs
            eligible_arcs = []
            for arc_id, arc in self.story_arcs.items():
                # Skip arcs that are already active or completed
                if arc in self.active_arcs or arc in self.completed_arcs:
                    continue
                
                # Skip arcs that are on cooldown
                if arc_id in self.arc_cooldown and self.arc_cooldown[arc_id] > 0:
                    self.arc_cooldown[arc_id] -= 1
                    continue
                
                # Skip role-specific arcs that don't apply to the player
                if arc.role_specific and player.role not in arc.roles:
                    continue
                
                # Check prerequisites
                if not arc.check_prerequisites(player):
                    continue
                
                # Check if this arc is incompatible with any active arcs
                incompatible = False
                for group, arc_types in self.incompatible_groups.items():
                    if arc_id in arc_types:
                        # Check if any active arc is in the same group
                        for active_arc in self.active_arcs:
                            if active_arc.arc_id in arc_types:
                                incompatible = True
                                break
                    if incompatible:
                        break
                
                if not incompatible:
                    eligible_arcs.append((arc_id, arc))
            
            # Randomly select one arc to start (if any are eligible)
            if eligible_arcs and random.random() < 0.3:  # 30% chance per year to start a new arc
                arc_id, arc = random.choice(eligible_arcs)
                arc.start()
                self.active_arcs.append(arc)
                
                # Add the first event from this arc
                event = arc.get_current_event(player)
                if event:
                    events.append((arc, event))
        
        # Limit the number of events per year to avoid overwhelming the player
        if len(events) > 1:
            # Prioritize events from arcs that have been active longer
            events.sort(key=lambda x: x[0].years_since_last_stage, reverse=True)
            events = events[:1]  # Only return the most urgent event
        
        return events
    
    def handle_event_outcome(self, arc, choice_idx):
        """Handle the outcome of an event in a story arc.
        
        Args:
            arc: The story arc.
            choice_idx: The index of the player's choice.
        """
        arc.advance_stage(choice_idx)
        
        if arc.completed:
            self.active_arcs.remove(arc)
            self.completed_arcs.append(arc)
            
            # Add to player's completed arcs
            if not hasattr(self.game_manager.player, "completed_arcs"):
                self.game_manager.player.completed_arcs = []
            
            self.game_manager.player.completed_arcs.append(arc.arc_id)
            
            # Set cooldown for this arc type
            self.arc_cooldown[arc.arc_id] = 10  # 10 years before this type of arc can happen again
            
            # Clean up any NPCs associated with this arc
            if arc.arc_id in self.arc_npcs:
                del self.arc_npcs[arc.arc_id]
    
    def assign_npc_to_arc(self, arc_id, npc):
        """Assign an NPC to a story arc.
        
        Args:
            arc_id: The ID of the story arc.
            npc: The NPC to assign to the arc.
        """
        if arc_id not in self.arc_npcs:
            self.arc_npcs[arc_id] = []
        
        self.arc_npcs[arc_id].append(npc)
    
    def get_arc_npcs(self, arc_id):
        """Get the NPCs assigned to a story arc.
        
        Args:
            arc_id: The ID of the story arc.
            
        Returns:
            A list of NPCs assigned to the arc.
        """
        return self.arc_npcs.get(arc_id, []) 