"""
Illicit Arcs - Story arcs involving illicit relationships and activities
"""
from game.events.story_arc_base import StoryArc

def get_illicit_arcs():
    """Get story arcs related to illicit relationships and activities.
    
    Returns:
        A dictionary of story arcs.
    """
    illicit_arcs = {
        # Adultery Arc
        "adultery": StoryArc(
            "adultery",
            "Forbidden Passion",
            "You find yourself drawn to someone who is already married.",
            [
                {
                    "title": "Temptation",
                    "description": "At a social gathering, you meet a married noble who shows interest in you. The attraction is mutual and powerful.",
                    "effects": {"attribute_charisma": 3},
                    "choices": [
                        {
                            "text": "Pursue the attraction discreetly",
                            "effects": {},
                            "outcome": "You decide to pursue the attraction, arranging a private meeting."
                        },
                        {
                            "text": "Flirt but maintain boundaries",
                            "effects": {},
                            "outcome": "You enjoy the flirtation but are careful not to cross any boundaries."
                        },
                        {
                            "text": "Reject the advances entirely",
                            "effects": {"attribute_honor": 5},
                            "outcome": "You politely but firmly reject the advances, respecting the sanctity of marriage."
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Secret Meetings",
                    "description": "Your relationship with the married noble has developed over the past year.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 0, "choice": 0},
                            "description": "You have been meeting in secret for months now. The passion is intoxicating, but the risk of discovery grows with each encounter.",
                            "effects": {"attribute_cunning": 5},
                            "choices": [
                                {
                                    "text": "Continue the affair",
                                    "effects": {"health": 5},  # The affair is exciting and invigorating
                                    "outcome": "You continue your secret affair, finding moments of passion amidst the danger."
                                },
                                {
                                    "text": "End the affair",
                                    "effects": {"attribute_willpower": 5},
                                    "outcome": "You decide to end the affair before it's discovered, prioritizing safety over passion."
                                },
                                {
                                    "text": "Suggest they leave their spouse",
                                    "effects": {},
                                    "outcome": "You suggest that your lover leave their spouse to be with you openly."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 1},
                            "description": "Your flirtation has continued, walking a dangerous line between propriety and scandal. The married noble has become more bold in their advances.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Give in to temptation",
                                    "effects": {},
                                    "outcome": "You finally give in to temptation and begin a secret affair."
                                },
                                {
                                    "text": "Continue the flirtation but maintain boundaries",
                                    "effects": {"attribute_willpower": 5},
                                    "outcome": "You continue to enjoy the flirtation but maintain your boundaries."
                                },
                                {
                                    "text": "End the flirtation entirely",
                                    "effects": {"attribute_honor": 5},
                                    "outcome": "You decide to end the flirtation entirely, removing yourself from temptation."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 2},
                            "description": "Despite your rejection, the married noble has continued to seek your attention, sending gifts and messages.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Reconsider and accept their advances",
                                    "effects": {},
                                    "outcome": "You reconsider your position and decide to accept their advances."
                                },
                                {
                                    "text": "Return the gifts and firmly reject them",
                                    "effects": {"attribute_honor": 5},
                                    "outcome": "You return all gifts and make it clear that you are not interested in an illicit relationship."
                                },
                                {
                                    "text": "Report their behavior to their spouse",
                                    "effects": {"attribute_honor": -5, "attribute_cunning": 5},
                                    "outcome": "You decide to inform their spouse of their inappropriate behavior."
                                }
                            ]
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Discovery",
                    "description": "The consequences of your choices regarding the married noble come to a head.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 1, "choice": 0},
                            "description": "Your affair has been discovered. The spouse of your lover has learned of your relationship and is publicly accusing you of adultery.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Deny everything",
                                    "effects": {"attribute_honor": -10, "attribute_cunning": 5},
                                    "outcome": "You deny the accusations vehemently. Some believe you, others don't, but the scandal damages your reputation regardless."
                                },
                                {
                                    "text": "Admit the affair and apologize",
                                    "effects": {"wealth": -200, "attribute_honor": -5},
                                    "outcome": "You admit to the affair and offer a sincere apology. You pay compensation to the wronged spouse, but your reputation suffers."
                                },
                                {
                                    "text": "Flee the area to escape scandal",
                                    "effects": {"wealth": -500},
                                    "outcome": "You flee to escape the scandal, leaving behind your home and many possessions."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 1, "choice": 1},
                            "description": "You ended the affair, but rumors have begun to circulate nonetheless. The spouse of your former lover has heard whispers and confronts you publicly.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Deny any impropriety",
                                    "effects": {"attribute_cunning": 5},
                                    "outcome": "You deny any impropriety, insisting that you maintained proper boundaries. Most believe you, but some doubt remains."
                                },
                                {
                                    "text": "Admit to flirtation but deny an affair",
                                    "effects": {"attribute_honor": 5},
                                    "outcome": "You admit to flirtation but insist that no affair took place. Your honesty is appreciated, though some still judge you."
                                },
                                {
                                    "text": "Apologize for any appearance of impropriety",
                                    "effects": {"attribute_diplomacy": 5},
                                    "outcome": "You apologize for any appearance of impropriety, smoothing over the situation with careful words."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 1, "choice": 2},
                            "description": "The spouse of the noble who pursued you has learned of their behavior and your rejection. They approach you privately to thank you for your honor.",
                            "effects": {"attribute_honor": 10},
                            "choices": [
                                {
                                    "text": "Accept their gratitude graciously",
                                    "effects": {"wealth": 100},
                                    "outcome": "You accept their gratitude graciously. They offer you a gift as a token of appreciation, which you accept."
                                },
                                {
                                    "text": "Downplay your actions",
                                    "effects": {"attribute_humility": 5},
                                    "outcome": "You downplay your actions, saying you simply did what any honorable person would do."
                                },
                                {
                                    "text": "Suggest they reconsider their marriage",
                                    "effects": {"attribute_wisdom": -5},
                                    "outcome": "You suggest they reconsider their marriage to someone who would pursue others. They are offended by your presumption."
                                }
                            ]
                        }
                    ]
                }
            ],
            role_specific=False,
            prerequisites={"age": 18}
        ),
        
        # Forbidden Love Arc (across social classes)
        "forbidden_love": StoryArc(
            "forbidden_love",
            "Love Across Boundaries",
            "You develop feelings for someone from a different social class.",
            [
                {
                    "title": "Chance Meeting",
                    "description": "Through an unusual circumstance, you meet someone from a vastly different social class. Despite the difference in your stations, you feel an immediate connection.",
                    "effects": {"attribute_charisma": 3},
                    "choices": [
                        {
                            "text": "Pursue the connection discreetly",
                            "effects": {},
                            "outcome": "You decide to pursue the connection, finding ways to meet in secret."
                        },
                        {
                            "text": "Maintain a proper distance",
                            "effects": {"attribute_willpower": 3},
                            "outcome": "You acknowledge the connection but maintain a proper distance appropriate to your different stations."
                        },
                        {
                            "text": "Dismiss the feelings entirely",
                            "effects": {},
                            "outcome": "You dismiss your feelings as inappropriate and impractical, focusing instead on suitable relationships."
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Growing Attachment",
                    "description": "A year has passed since your first meeting.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 0, "choice": 0},
                            "description": "Your secret meetings have led to a deep attachment. You've shared dreams, fears, and stolen moments of happiness, but the difference in your stations makes a future together seem impossible.",
                            "effects": {"attribute_charisma": 5},
                            "choices": [
                                {
                                    "text": "Continue the secret relationship",
                                    "effects": {"health": 5},
                                    "outcome": "You continue your secret relationship, treasuring each moment together despite the uncertainty."
                                },
                                {
                                    "text": "Make plans to overcome the social barriers",
                                    "effects": {"wealth": -100},
                                    "outcome": "You begin making plans to overcome the social barriers, perhaps through elevation of status or relocation."
                                },
                                {
                                    "text": "End the relationship before it becomes too painful",
                                    "effects": {"health": -5, "attribute_willpower": 5},
                                    "outcome": "With a heavy heart, you end the relationship, believing it can only lead to greater pain."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 1},
                            "description": "Though you've maintained a proper distance, your paths continue to cross, and each meeting strengthens your feelings. Others have begun to notice your interest in each other.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Acknowledge your feelings and pursue a relationship",
                                    "effects": {},
                                    "outcome": "You can no longer deny your feelings and decide to pursue a relationship despite the social barriers."
                                },
                                {
                                    "text": "Continue to maintain a proper distance",
                                    "effects": {"attribute_willpower": 5},
                                    "outcome": "You continue to maintain a proper distance, though it becomes increasingly difficult."
                                },
                                {
                                    "text": "Arrange to stop crossing paths",
                                    "effects": {"health": -3},
                                    "outcome": "You arrange to stop crossing paths, sacrificing potential happiness for social propriety."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 2},
                            "description": "Despite dismissing your feelings, you find yourself thinking of the person often. By chance, you encounter them again, and the connection is still there.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Reconsider and pursue the connection",
                                    "effects": {},
                                    "outcome": "You reconsider your previous decision and decide to pursue the connection after all."
                                },
                                {
                                    "text": "Maintain your resolve",
                                    "effects": {"attribute_willpower": 10},
                                    "outcome": "You maintain your resolve, acknowledging the feelings but choosing not to act on them."
                                },
                                {
                                    "text": "Seek a more suitable match",
                                    "effects": {},
                                    "outcome": "You actively seek a more suitable match to help forget the inappropriate connection."
                                }
                            ]
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Societal Pressure",
                    "description": "Your relationship faces increasing pressure from society.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 1, "choice": 0},
                            "description": "Your relationship has become known to others, and you face significant pressure from family and peers to end it. Your reputation is suffering, and your loved one faces even harsher consequences due to their station.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Defy society and continue the relationship openly",
                                    "effects": {"wealth": -300, "attribute_courage": 15},
                                    "outcome": "You defy societal expectations and continue your relationship openly. You face significant social and financial consequences, but gain respect from some for your courage."
                                },
                                {
                                    "text": "End the relationship due to societal pressure",
                                    "effects": {"health": -10, "attribute_conformity": 10},
                                    "outcome": "You succumb to societal pressure and end the relationship, prioritizing your position and reputation over love."
                                },
                                {
                                    "text": "Elope together to start a new life elsewhere",
                                    "effects": {"wealth": -500, "attribute_courage": 10},
                                    "outcome": "You decide to elope together to a place where you can start anew without the social barriers that kept you apart."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 1, "choice": 1},
                            "description": "Your continued propriety has not gone unnoticed. Your family is pleased with your restraint and has arranged a socially advantageous match for you. However, your heart still yearns for the one you've been denying yourself.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Reject the arranged match and pursue your true feelings",
                                    "effects": {"wealth": -200, "attribute_courage": 10},
                                    "outcome": "You reject the arranged match and finally pursue your true feelings, facing the social consequences."
                                },
                                {
                                    "text": "Accept the arranged match",
                                    "effects": {"wealth": 300, "health": -5},
                                    "outcome": "You accept the arranged match, gaining social and financial advantages but sacrificing the chance for true love."
                                },
                                {
                                    "text": "Delay the decision",
                                    "effects": {},
                                    "outcome": "You ask for time to consider the arranged match, hoping to find a way to follow your heart without sacrificing everything."
                                }
                            ]
                        }
                    ]
                }
            ],
            role_specific=False,
            prerequisites={"age": 16}
        ),
        
        # Secret Same-Sex Relationship Arc
        "same_sex_relationship": StoryArc(
            "same_sex_relationship",
            "Hidden Affections",
            "You develop feelings for someone of the same gender, a dangerous attraction in medieval society.",
            [
                {
                    "title": "Unexpected Feelings",
                    "description": "You find yourself developing feelings for someone of the same gender, a dangerous attraction in medieval society where such relationships are forbidden.",
                    "effects": {"attribute_cunning": 3},
                    "choices": [
                        {
                            "text": "Cautiously explore these feelings",
                            "effects": {},
                            "outcome": "You decide to cautiously explore these feelings, testing whether they are reciprocated."
                        },
                        {
                            "text": "Suppress these feelings entirely",
                            "effects": {"health": -3, "attribute_willpower": 5},
                            "outcome": "You suppress these feelings entirely, knowing the dangers they represent in society."
                        },
                        {
                            "text": "Seek spiritual guidance",
                            "effects": {"attribute_piety": 5},
                            "outcome": "You seek spiritual guidance to help you understand and address these feelings."
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Hidden Truth",
                    "description": "A year has passed since you first acknowledged your feelings.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 0, "choice": 0},
                            "description": "Your cautious exploration revealed that your feelings are reciprocated. You have begun a secret relationship, meeting in private and maintaining a careful facade in public.",
                            "effects": {"attribute_cunning": 5},
                            "choices": [
                                {
                                    "text": "Continue the secret relationship",
                                    "effects": {"health": 5, "attribute_cunning": 5},
                                    "outcome": "You continue your secret relationship, developing elaborate precautions to avoid discovery."
                                },
                                {
                                    "text": "End the relationship due to the risk",
                                    "effects": {"health": -5, "attribute_willpower": 5},
                                    "outcome": "Despite your feelings, you end the relationship, unwilling to risk the severe consequences of discovery."
                                },
                                {
                                    "text": "Consider relocating to a more tolerant region",
                                    "effects": {"wealth": -200},
                                    "outcome": "You begin making discreet inquiries about places where you might live more openly, though such places are rare in this era."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 1},
                            "description": "You have suppressed your feelings, but doing so has taken a toll on your well-being. The person who inspired these feelings remains in your life, unaware of your struggle.",
                            "effects": {"health": -3},
                            "choices": [
                                {
                                    "text": "Reconsider and cautiously reveal your feelings",
                                    "effects": {},
                                    "outcome": "You reconsider your decision and cautiously approach the person to reveal your feelings."
                                },
                                {
                                    "text": "Maintain your resolve and distance yourself",
                                    "effects": {"attribute_willpower": 10},
                                    "outcome": "You maintain your resolve and begin to distance yourself from the person to make suppressing your feelings easier."
                                },
                                {
                                    "text": "Seek a traditional marriage to help forget",
                                    "effects": {},
                                    "outcome": "You actively seek a traditional marriage, hoping it will help you forget these forbidden feelings."
                                }
                            ]
                        },
                        {
                            "condition": {"stage": 0, "choice": 2},
                            "description": "The spiritual guidance you sought has led to much reflection. The religious authorities counseled prayer and penance to overcome what they view as sinful temptation.",
                            "effects": {"attribute_piety": 5},
                            "choices": [
                                {
                                    "text": "Reject the religious counsel and embrace your feelings",
                                    "effects": {"attribute_piety": -10, "attribute_independence": 10},
                                    "outcome": "You reject the religious counsel, deciding to trust your own heart despite societal and religious condemnation."
                                },
                                {
                                    "text": "Accept the religious counsel and suppress your feelings",
                                    "effects": {"attribute_piety": 10, "health": -5},
                                    "outcome": "You accept the religious counsel and commit to suppressing your feelings, viewing them as a test of faith."
                                },
                                {
                                    "text": "Seek a middle path of private acceptance and public conformity",
                                    "effects": {"attribute_cunning": 10},
                                    "outcome": "You develop a nuanced approach, privately accepting your feelings while maintaining public conformity to religious expectations."
                                }
                            ]
                        }
                    ],
                    "years_until_next": 1
                },
                {
                    "title": "Moment of Truth",
                    "description": "Your situation has reached a critical point where significant decisions must be made.",
                    "effects": {},
                    "conditional_events": [
                        {
                            "condition": {"stage": 1, "choice": 0},
                            "description": "Someone has discovered your secret relationship and is threatening to expose you. The consequences could be severe, including imprisonment, public humiliation, or worse.",
                            "effects": {},
                            "choices": [
                                {
                                    "text": "Pay for their silence",
                                    "effects": {"wealth": -500, "attribute_cunning": 5},
                                    "outcome": "You pay a substantial sum for their silence, buying temporary safety at great cost."
                                },
                                {
                                    "text": "Deny everything and discredit the accuser",
                                    "effects": {"attribute_cunning": 10, "attribute_honor": -10},
                                    "outcome": "You vehemently deny everything and work to discredit your accuser, using your social standing to your advantage."
                                },
                                {
                                    "text": "Flee together to a distant land",
                                    "effects": {"wealth": -1000, "attribute_courage": 15},
                                    "outcome": "You decide to flee together to a distant land where you might live more freely, leaving behind everything familiar."
                                }
                            ]
                        }
                    ]
                }
            ],
            role_specific=False,
            prerequisites={"age": 16}
        )
    }
    
    return illicit_arcs 