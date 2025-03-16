"""
Criminal Arcs - Story arcs involving criminal activities
"""
from game.events.story_arc_base import StoryArc

def get_criminal_arcs():
    """Get story arcs related to criminal activities.
    
    Returns:
        A dictionary of story arcs.
    """
    criminal_arcs = {
        # Smuggling Arc
        "smuggling": StoryArc(
            "smuggling",
            "Contraband Trade",
            "You become involved in smuggling illegal or untaxed goods.",
            [
                {
                    "title": "A Lucrative Proposition",
                    "description": "A merchant approaches you with a proposition to help move goods without paying the required taxes and tariffs.",
                    "effects": {},
                    "choices": [
                        {
                            "text": "Accept the proposition",
                            "effects": {"wealth": 100, "attribute_cunning": 3},
                            "outcome": "You agree to participate in the smuggling operation, seeing an opportunity for profit."
                        },
                        {
                            "text": "Decline but keep their secret",
                            "effects": {},
                            "outcome": "You decline to participate but agree to keep their activities secret."
                        },
                        {
                            "text": "Report them to the authorities",
                            "effects": {"attribute_honor": 5},
                            "outcome": "You report the smuggler to the local authorities, upholding the law."
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Deeper Involvement",
                    "description": "A year has passed since the smuggling proposition.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 0, "choice": 0},
                            "description": "Your smuggling activities have been profitable, but the operation is expanding and becoming more dangerous. The leader wants you to take on more responsibility.",
                            "effects": {"wealth": 200},
                            "choices": [
                                {
                                    "text": "Accept greater responsibility",
                                    "effects": {"wealth": 300, "attribute_cunning": 5},
                                    "outcome": "You accept a larger role in the smuggling operation, with greater risks and rewards."
                                },
                                {
                                    "text": "Maintain your current level of involvement",
                                    "effects": {"wealth": 100},
                                    "outcome": "You decide to maintain your current level of involvement, not wanting to take on more risk."
                                },
                                {
                                    "text": "Try to leave the operation",
                                    "effects": {},
                                    "outcome": "You try to distance yourself from the smuggling operation, concerned about the increasing risks."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 1},
                            "description": "The smuggler has returned, claiming they're in trouble and need your help with just one shipment. They offer a substantial payment.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Help them this one time",
                                    "effects": {"wealth": 200, "attribute_cunning": 3},
                                    "outcome": "You agree to help just this once, for a substantial payment."
                                },
                                {
                                    "text": "Refuse to get involved",
                                    "effects": {"attribute_willpower": 5},
                                    "outcome": "You refuse to get involved, maintaining your distance from illegal activities."
                                },
                                {
                                    "text": "Suggest a legal alternative",
                                    "effects": {"attribute_wisdom": 5},
                                    "outcome": "You suggest a legal alternative that might help them out of their trouble."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 2},
                            "description": "The authorities have arrested several smugglers based on your information. They now ask for your help in catching the ringleaders.",
                            "effects": {"attribute_honor": 5},
                            "choices": [
                                {
                                    "text": "Agree to help the authorities",
                                    "effects": {"attribute_courage": 5, "attribute_honor": 5},
                                    "outcome": "You agree to help the authorities catch the smuggling ringleaders."
                                },
                                {
                                    "text": "Decline further involvement",
                                    "effects": {},
                                    "outcome": "You decline further involvement, feeling you've done your civic duty."
                                },
                                {
                                    "text": "Warn the smugglers anonymously",
                                    "effects": {"attribute_honor": -10, "attribute_cunning": 5},
                                    "outcome": "For reasons of your own, you anonymously warn the smugglers about the authorities' plans."
                                }
                            ]
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "The Consequences",
                    "description": "Your involvement with smuggling reaches a critical point.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 1, "choice": 0},
                            "description": "Your expanded role in the smuggling operation has made you wealthy, but a recent shipment was seized by authorities. There's evidence that could lead back to you.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Bribe officials to destroy the evidence",
                                    "effects": {"wealth": -500, "attribute_cunning": 5},
                                    "outcome": "You use your wealth to bribe officials to destroy the evidence linking you to the smuggling operation."
                                },
                                {
                                    "text": "Flee to another region",
                                    "effects": {"wealth": -300},
                                    "outcome": "You flee to another region to escape potential prosecution, leaving behind your home but taking most of your wealth."
                                },
                                {
                                    "text": "Turn yourself in and cooperate",
                                    "effects": {"wealth": -1000, "attribute_honor": 10},
                                    "outcome": "You turn yourself in and cooperate with authorities. Your sentence is reduced, but you lose most of your ill-gotten gains."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 1, "choice": 1},
                            "description": "The 'one-time' shipment you helped with was intercepted. The smuggler was arrested and has implicated you under questioning.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Deny everything",
                                    "effects": {"attribute_cunning": 5},
                                    "outcome": "You deny any involvement. Without strong evidence, the authorities cannot prove your guilt, but suspicion remains."
                                },
                                {
                                    "text": "Flee before arrest",
                                    "effects": {"wealth": -200},
                                    "outcome": "You flee before you can be arrested, leaving behind your home and some possessions."
                                },
                                {
                                    "text": "Confess and seek leniency",
                                    "effects": {"wealth": -300, "attribute_honor": 5},
                                    "outcome": "You confess to your limited involvement and seek leniency. You pay a substantial fine but avoid imprisonment."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 1, "choice": 2},
                            "description": "With your help, the authorities have set a trap for the smuggling ringleaders. The operation is ready, but there's significant danger involved.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Participate in the trap",
                                    "effects": {"attribute_courage": 10, "wealth": 300},
                                    "outcome": "You participate in the trap, which successfully captures the ringleaders. You are rewarded for your service."
                                },
                                {
                                    "text": "Provide information but stay away",
                                    "effects": {"attribute_cunning": 5, "wealth": 100},
                                    "outcome": "You provide detailed information but stay away from the actual trap. The operation is successful, and you receive a modest reward."
                                },
                                {
                                    "text": "Back out at the last minute",
                                    "effects": {"attribute_honor": -5},
                                    "outcome": "You back out at the last minute, fearing for your safety. The operation proceeds without you but is less successful."
                                }
                            ]
                        }
                    ]
                }
            ],
            role_specific=False,
            prerequisites={"age": 18}
        ),
        
        # Theft Arc
        "theft": StoryArc(
            "theft",
            "Temptation of Theft",
            "You are presented with opportunities to steal valuable items.",
            [
                {
                    "title": "Easy Target",
                    "description": "You notice a wealthy merchant has left their purse unattended. No one is watching, and it would be easy to take it.",
                    "effects": {},
                    "choices": [
                        {
                            "text": "Take the purse",
                            "effects": {"wealth": 100, "attribute_honor": -5},
                            "outcome": "You take the purse, gaining a significant sum of money but compromising your honor."
                        },
                        {
                            "text": "Ignore the opportunity",
                            "effects": {"attribute_honor": 5},
                            "outcome": "You ignore the opportunity, maintaining your integrity."
                        },
                        {
                            "text": "Alert the merchant about their purse",
                            "effects": {"attribute_honor": 10},
                            "outcome": "You alert the merchant about their unattended purse. They are grateful for your honesty."
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Reputation and Opportunity",
                    "description": "A year has passed since the incident with the merchant's purse.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 0, "choice": 0},
                            "description": "Word has spread in certain circles about your light fingers. A professional thief approaches you with a proposition for a more organized theft.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Join the planned theft",
                                    "effects": {"wealth": 300, "attribute_cunning": 5, "attribute_honor": -10},
                                    "outcome": "You join the planned theft, which is successful and highly profitable."
                                },
                                {
                                    "text": "Decline but keep their secret",
                                    "effects": {},
                                    "outcome": "You decline to participate but agree to keep their activities secret."
                                },
                                {
                                    "text": "Report them to the authorities",
                                    "effects": {"attribute_honor": 5},
                                    "outcome": "You report the thief to the authorities, perhaps seeking to redeem yourself."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 1},
                            "description": "You've maintained your integrity, but times have become hard. You notice a valuable item poorly guarded in a wealthy home, and the temptation returns stronger than before.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Steal the valuable item",
                                    "effects": {"wealth": 200, "attribute_honor": -10},
                                    "outcome": "Driven by necessity, you steal the valuable item, compromising your previously maintained integrity."
                                },
                                {
                                    "text": "Resist the temptation again",
                                    "effects": {"attribute_willpower": 10, "attribute_honor": 5},
                                    "outcome": "You resist the temptation again, maintaining your integrity despite difficult circumstances."
                                },
                                {
                                    "text": "Seek honest work instead",
                                    "effects": {"wealth": 50, "attribute_honor": 10},
                                    "outcome": "Instead of stealing, you seek honest work to improve your situation, maintaining your integrity."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 2},
                            "description": "The merchant whose purse you saved has remembered your honesty. They seek you out to offer you a position of trust in their business.",
                            "effects": {"attribute_honor": 5},
                            "choices": [
                                {
                                    "text": "Accept the position",
                                    "effects": {"wealth": 150, "attribute_honor": 5},
                                    "outcome": "You accept the position, gaining stable income and building a reputation for trustworthiness."
                                },
                                {
                                    "text": "Decline politely",
                                    "effects": {},
                                    "outcome": "You decline politely, preferring to maintain your current path."
                                },
                                {
                                    "text": "Accept but plan to exploit their trust",
                                    "effects": {"attribute_cunning": 5, "attribute_honor": -15},
                                    "outcome": "You accept the position but secretly plan to exploit their trust for personal gain."
                                }
                            ]
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Consequences of Choices",
                    "description": "Your choices regarding theft have led to significant consequences.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 1, "choice": 0},
                            "description": "Your involvement in organized theft has been profitable, but authorities are investigating a string of thefts. A fellow thief has been caught and might reveal your involvement under questioning.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Silence the captured thief",
                                    "effects": {"wealth": -200, "attribute_honor": -20},
                                    "outcome": "You arrange to silence the captured thief through bribery or more sinister means, protecting yourself but sinking deeper into criminality."
                                },
                                {
                                    "text": "Flee the area",
                                    "effects": {"wealth": -100},
                                    "outcome": "You flee the area before you can be implicated, leaving behind your home but taking most of your ill-gotten gains."
                                },
                                {
                                    "text": "Turn yourself in and seek leniency",
                                    "effects": {"wealth": -500, "attribute_honor": 10},
                                    "outcome": "You turn yourself in and seek leniency. You pay restitution and face some punishment, but begin the path to redemption."
                                }
                            ]
                        }
                    ]
                }
            ],
            role_specific=False,
            prerequisites={"age": 16}
        ),
        
        # Corruption Arc (for officials)
        "corruption": StoryArc(
            "corruption",
            "Power and Corruption",
            "Your position of authority presents opportunities for corruption.",
            [
                {
                    "title": "Bribe Offer",
                    "description": "Someone offers you a bribe to use your position of authority in their favor.",
                    "effects": {},
                    "choices": [
                        {
                            "text": "Accept the bribe",
                            "effects": {"wealth": 200, "attribute_honor": -10},
                            "outcome": "You accept the bribe, using your position to favor the briber's interests."
                        },
                        {
                            "text": "Refuse the bribe",
                            "effects": {"attribute_honor": 10},
                            "outcome": "You refuse the bribe, maintaining your integrity and the trust placed in your position."
                        },
                        {
                            "text": "Pretend to accept but report them",
                            "effects": {"attribute_cunning": 5, "attribute_honor": 5},
                            "outcome": "You pretend to accept the bribe but report the briber to higher authorities."
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Reputation Spreads",
                    "description": "Your reputation regarding bribes has spread.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 0, "choice": 0},
                            "description": "Word has spread that you are open to bribes. More people approach you with larger offers, but there are whispers that could reach your superiors.",
                            "effects": {"wealth": 100},
                            "choices": [
                                {
                                    "text": "Continue accepting bribes more carefully",
                                    "effects": {"wealth": 300, "attribute_cunning": 5, "attribute_honor": -10},
                                    "outcome": "You continue accepting bribes but become more careful about it, developing a system to avoid detection."
                                },
                                {
                                    "text": "Stop accepting bribes",
                                    "effects": {"attribute_willpower": 10},
                                    "outcome": "You decide to stop accepting bribes, concerned about the growing risks and your deteriorating honor."
                                },
                                {
                                    "text": "Demand larger bribes from fewer people",
                                    "effects": {"wealth": 500, "attribute_honor": -15},
                                    "outcome": "You become more selective, demanding larger bribes from fewer people to reduce the risk of exposure."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 1},
                            "description": "Your reputation for integrity has grown. You are offered a promotion to a position with more authority and responsibility.",
                            "effects": {"attribute_honor": 5},
                            "choices": [
                                {
                                    "text": "Accept the promotion",
                                    "effects": {"wealth": 200, "attribute_honor": 5},
                                    "outcome": "You accept the promotion, gaining more authority and better compensation."
                                },
                                {
                                    "text": "Decline the promotion",
                                    "effects": {},
                                    "outcome": "You decline the promotion, preferring to remain in your current position."
                                },
                                {
                                    "text": "Accept and reconsider taking bribes",
                                    "effects": {"attribute_cunning": 5},
                                    "outcome": "You accept the promotion but begin to consider that your new position might offer more lucrative opportunities for corruption."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 2},
                            "description": "Your sting operation was successful. The would-be briber was punished, and your superiors have taken note of your integrity and cunning.",
                            "effects": {"attribute_honor": 5, "attribute_cunning": 5},
                            "choices": [
                                {
                                    "text": "Accept a promotion to anti-corruption unit",
                                    "effects": {"wealth": 150, "attribute_honor": 10},
                                    "outcome": "You accept a promotion to a unit specifically tasked with fighting corruption, using your experience to catch others."
                                },
                                {
                                    "text": "Continue in your current role",
                                    "effects": {"wealth": 50},
                                    "outcome": "You continue in your current role, maintaining your integrity and gaining a modest increase in compensation."
                                },
                                {
                                    "text": "Realize corruption's potential and start accepting bribes",
                                    "effects": {"wealth": 200, "attribute_honor": -20},
                                    "outcome": "Having seen how the system works from the inside, you ironically decide to start accepting bribes, using your knowledge to avoid detection."
                                }
                            ]
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Investigation",
                    "description": "Your activities have drawn attention, leading to significant consequences.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 1, "choice": 0},
                            "description": "An investigation into corruption has been launched, and evidence points to your activities. A witness is prepared to testify against you.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Bribe or threaten the witness",
                                    "effects": {"wealth": -300, "attribute_honor": -15},
                                    "outcome": "You use your wealth and influence to silence the witness, escaping immediate consequences but sinking deeper into corruption."
                                },
                                {
                                    "text": "Resign and flee",
                                    "effects": {"wealth": -200},
                                    "outcome": "You resign from your position and flee before the investigation can conclude, escaping punishment but losing your position and some wealth."
                                },
                                {
                                    "text": "Confess and cooperate",
                                    "effects": {"wealth": -500, "attribute_honor": 10},
                                    "outcome": "You confess to your corrupt activities and cooperate with the investigation. You lose your position and much of your wealth, but begin the path to redemption."
                                }
                            ]
                        }
                    ]
                }
            ],
            role_specific=True,
            roles=["king", "noble", "knight"],
            prerequisites={"age": 20}
        )
    }
    
    return criminal_arcs 