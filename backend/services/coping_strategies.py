"""
Advanced Coping Strategies Library
Provides evidence-based coping techniques for various emotional states
"""

import random


def get_coping_strategy(emotion, intensity="low", situation_type=None):
    """
    Get tailored coping strategy based on emotion and context
    
    Args:
        emotion: Current emotion (anxiety, sadness, anger, fear, guilt, shame, positive)
        intensity: Intensity level (low, medium, high, critical)
        situation_type: Optional context (work, relationship, social, etc.)
    
    Returns:
        Coping strategy description
    """
    
    strategies = {
        'anxiety': get_anxiety_coping,
        'fear': get_fear_coping,
        'sadness': get_sadness_coping,
        'anger': get_anger_coping,
        'guilt': get_guilt_coping,
        'shame': get_shame_coping,
        'positive': get_positive_enhancement
    }
    
    strategy_func = strategies.get(emotion, get_general_coping)
    return strategy_func(intensity, situation_type)


def get_anxiety_coping(intensity, situation):
    """Anxiety-specific coping strategies"""
    
    if intensity in ['high', 'critical']:
        strategies = [
            {
                "name": "4-7-8 Breathing",
                "description": "Try this right now: Breathe in for 4 counts, hold for 7, out for 8. Repeat 4 times. This activates your parasympathetic nervous system and calms anxiety physiologically."
            },
            {
                "name": "5-4-3-2-1 Grounding",
                "description": "Ground yourself in the present: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. This breaks the anxiety spiral by anchoring you here and now."
            },
            {
                "name": "Progressive Muscle Relaxation",
                "description": "Tense each muscle group for 5 seconds then release: Start with your toes, move to calves, thighs, stomach, chest, arms, hands, neck, face. Notice the difference between tension and relaxation."
            },
            {
                "name": "TIPP Method (DBT)",
                "description": "Temperature (splash cold water on face), Intense exercise (jumping jacks for 1 min), Paced breathing (slow and steady), and Paired muscle relaxation. These rapidly reduce intense anxiety."
            }
        ]
    else:
        strategies = [
            {
                "name": "Worry Time Scheduling",
                "description": "Set aside 15 minutes later today just for worrying. When anxious thoughts come now, write them down and save them for 'worry time.' This contains anxiety instead of letting it run your day."
            },
            {
                "name": "Anxiety Exposure Ladder",
                "description": "Rate your fears 1-10. Start facing situations rated 3-4, not 10. Gradual exposure builds confidence and shows you that you can handle more than you think."
            },
            {
                "name": "Box Breathing",
                "description": "Breathe in for 4, hold for 4, out for 4, hold for 4. Repeat 5 times. This military technique quickly calms the nervous system."
            },
            {
                "name": "Challenge Anxious Predictions",
                "description": "Write down what you fear will happen, rate the probability (0-100%), then later check what actually happened. Anxiety makes us horrible fortune tellers - gathering evidence helps."
            }
        ]
    
    return random.choice(strategies)


def get_fear_coping(intensity, situation):
    """Fear-specific coping strategies"""
    
    strategies = [
        {
            "name": "Safety Planning",
            "description": "Create a concrete plan: What's the worst case? What resources do you have? Who can help? What's your first step? Fear shrinks when we have a plan."
        },
        {
            "name": "Courage Inventory",
            "description": "List 5 scary things you've already survived. You've been afraid before and made it through. Past courage predicts future courage."
        },
        {
            "name": "Fear Ladder",
            "description": "Rate scary situations 1-10. Practice facing level 3-4 fears first. Each success builds confidence for bigger challenges. You don't have to be fearless - just willing to try despite fear."
        },
        {
            "name": "Imaginal Exposure",
            "description": "Spend 10 minutes imagining your fear in detail while staying calm. Repeated exposure reduces the fear response over time. What we avoid grows stronger; what we face gets weaker."
        }
    ]
    
    return random.choice(strategies)


def get_sadness_coping(intensity, situation):
    """Sadness and depression coping strategies"""
    
    if intensity in ['high', 'critical']:
        strategies = [
            {
                "name": "Opposite Action (DBT)",
                "description": "When depression says 'stay in bed,' do the opposite: Get up, shower, go outside for 5 minutes. Action comes before motivation, not after. Start tiny."
            },
            {
                "name": "Behavioral Activation Schedule",
                "description": "Schedule one small activity each day that used to bring joy: 10 min music, 5 min walk, calling one friend. Do it whether you feel like it or not. Joy follows action."
            },
            {
                "name": "PLEASE Skills (DBT)",
                "description": "Treat Physical illness, balance Eating, Avoid mood-altering drugs, Sleep 7-8 hrs, get Exercise daily. Depression thrives in neglected bodies. Physical care is mental care."
            }
        ]
    else:
        strategies = [
            {
                "name": "Gratitude Practice",
                "description": "List 3 specific things you're grateful for today, and WHY. Not 'family' but 'My sister texted me a funny meme because she knows what I like.' Specific gratitude rewires the brain."
            },
            {
                "name": "Micro-Achievements",
                "description": "Set tiny, achievable goals: Take a shower. Make coffee. Read 1 page. Each small win builds momentum. Depression lies that nothing matters - prove it wrong one small step at a time."
            },
            {
                "name": "Pleasant Activity Scheduling",
                "description": "Plan one enjoyable activity for tomorrow. Even if you don't feel like it. Pleasure and accomplishment are antidotes to depression. Schedule it like a medical appointment."
            },
            {
                "name": "Social Connection (even tiny)",
                "description": "Text one person, even just 'Hi.' Depression isolates us, but connection heals. You don't need a party - one genuine interaction fights the loneliness."
            }
        ]
    
    return random.choice(strategies)


def get_anger_coping(intensity, situation):
    """Anger-specific coping strategies"""
    
    if intensity in ['high', 'critical']:
        strategies = [
            {
                "name": "Timeout Technique",
                "description": "Leave the situation for 20 minutes. Walk, breathe, cool down physically. Your brain needs time for the anger chemicals to metabolize. Responding while enraged rarely helps."
            },
            {
                "name": "Physical Release",
                "description": "Sprint, do pushups, punch a pillow, rip paper. Anger is physical energy - channel it safely. After physical release, the thinking brain can return."
            },
            {
                "name": "Opposite Action for Anger",
                "description": "Anger wants to attack. Do the opposite: gentle voice, relaxed posture, kind words. This interrupts the anger cycle and gives you back control."
            }
        ]
    else:
        strategies = [
            {
                "name": "Anger Log",
                "description": "Track: What triggered it? What was I thinking? Physical sensations? What did I do? Patterns emerge. Understanding patterns gives you power to change them."
            },
            {
                "name": "Assertive Communication",
                "description": "Use 'I' statements: 'I feel ___ when ___ because ___. I need ___.' This expresses anger productively without attacking. You deserve to express needs clearly."
            },
            {
                "name": "Temperature Change",
                "description": "Hold ice cubes, take a cold shower, step outside. Changing your body temperature interrupts the anger response. Simple but remarkably effective."
            },
            {
                "name": "Count Backwards from 100",
                "description": "Count backwards by 7s from 100. This engages your prefrontal cortex and reduces amygdala reactivity. It's hard to be enraged while doing mental math."
            }
        ]
    
    return random.choice(strategies)


def get_guilt_coping(intensity, situation):
    """Guilt-specific coping strategies"""
    
    strategies = [
        {
            "name": "Responsible vs. Blame",
            "description": "Ask: What percentage of this outcome is truly within my control? Often we blame ourselves for things outside our control. Take responsibility for your part only, not all of it."
        },
        {
            "name": "Make Amends",
            "description": "If you actually did something wrong: Acknowledge it, apologize sincerely, make concrete changes. Real guilt is resolved through action, not rumination."
        },
        {
            "name": "Self-Forgiveness Ritual",
            "description": "Write a letter to yourself: What happened? What would you tell a friend? Can you forgive yourself? Sometimes we need to hear our own forgiveness out loud."
        },
        {
            "name": "Distinguish Real vs. False Guilt",
            "description": "Real guilt: I hurt someone through my actions. False guilt: I exist, I have needs, I said no, I can't fix everything. Ask: Did I actually do something wrong, or is this shame pretending to be guilt?"
        },
        {
            "name": "Opposite Action for Guilt",
            "description": "If guilty about self-care: Do MORE self-care. If guilty about boundaries: Hold the boundary. When guilt is unjustified, do the opposite of what it demands."
        }
    ]
    
    return random.choice(strategies)


def get_shame_coping(intensity, situation):
    """Shame-specific coping strategies"""
    
    strategies = [
        {
            "name": "Shame Resilience (Brené Brown)",
            "description": "Name the shame. Talk about it with someone safe. Own your story - shame can't survive being spoken out loud. Connection is the antidote to shame."
        },
        {
            "name": "Separate Behavior from Identity",
            "description": "You're not a bad person. You did something you regret. There's a huge difference between 'I made a mistake' and 'I am a mistake.' You are worthy regardless of what you've done."
        },
        {
            "name": "Critical Voice vs. Compassionate Voice",
            "description": "Write what shame says. Then write what a loving friend would say. Shame lies. Practice speaking to yourself like someone who genuinely cares about you."
        },
        {
            "name": "Vulnerability Practice",
            "description": "Share one small imperfection with someone safe. Shame thrives in secrecy and dies in empathy. Let someone see you and still accept you - it's powerfully healing."
        },
        {
            "name": "Worthiness Inventory",
            "description": "List 10 things that make you worthy (hint: You're worthy because you exist. You don't have to earn it). Shame says you're defective. Evidence says otherwise."
        }
    ]
    
    return random.choice(strategies)


def get_positive_enhancement(intensity, situation):
    """Strategies to maintain and enhance positive states"""
    
    strategies = [
        {
            "name": "Savor the Moment",
            "description": "Really notice this good feeling. What does it feel like in your body? What made it happen? How can you create more moments like this? Positive emotions are just as important to process as difficult ones."
        },
        {
            "name": "Gratitude Amplification",
            "description": "Write down what's going well and why. Share your good news with someone who will be genuinely happy for you. Celebrating multiplies joy."
        },
        {
            "name": "Build on Momentum",
            "description": "When you're feeling good, that's the time to tackle something you've been avoiding. Positive energy is a resource - use it wisely."
        },
        {
            "name": "Positive Memory Bank",
            "description": "Store this feeling. Take a mental snapshot. When hard times come (and they will), you'll have evidence that good moments exist too."
        }
    ]
    
    return random.choice(strategies)


def get_general_coping(intensity, situation):
    """General coping strategies for any emotion"""
    
    strategies = [
        {
            "name": "Mindful Awareness",
            "description": "Notice this feeling without judgment. Name it. Where is it in your body? What triggered it? Observing emotions mindfully reduces their intensity."
        },
        {
            "name": "Self-Compassion Break",
            "description": "Say to yourself: This is hard. Many people feel this way. May I be kind to myself. These three elements (mindfulness, common humanity, self-kindness) are evidence-based."
        },
        {
            "name": "Wise Mind (DBT)",
            "description": "Emotion Mind says one thing. Rational Mind says another. Wise Mind integrates both. What does your deepest wisdom say right now?"
        }
    ]
    
    return random.choice(strategies)


def get_quick_intervention(emotion):
    """Get immediate, actionable intervention for any emotion (short version)"""
    
    quick_tips = {
        'anxiety': "Take 3 slow breaths right now. In for 4, out for 6. Longer exhale activates calm.",
        'fear': "Name what you're afraid of out loud. Fear loses power when we speak it.",
        'sadness': "Do one tiny kind thing for yourself in the next 60 seconds. What would that be?",
        'anger': "Step away for 5 minutes. Literally leave the room if you can. Cool down, then respond.",
        'guilt': "Ask: Did I actually do something wrong? If yes, how can I make amends? If no, let it go.",
        'shame': "Tell one person you trust. Shame dies in empathy and connection.",
        'positive': "Notice this feeling fully. What contributed to it? How can you create more of this?"
    }
    
    return quick_tips.get(emotion, "Pause. Breathe. Notice what you're feeling. You're doing the right thing by checking in with yourself.")
