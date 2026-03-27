"""
Activity Spaces - Specialized conversational experiences for specific mental health topics
Each space provides focused, contextual support for different concerns
"""
import random

ACTIVITY_SPACES = {
    'stress': {
        'name': 'Stress Management',
        'icon': 'wind',
        'color': '#f59e0b',
        'gradient': 'linear-gradient(135deg, #d97706, #f59e0b)',
        'description': 'Find calm in chaos. Techniques for managing daily stress.',
        'greeting': "Welcome to your stress management space. This is where we work on finding calm in the chaos. What's feeling stressful today?",
        'prompts': [
            "I'm feeling overwhelmed with everything",
            "Work stress is getting to be too much",
            "I can't seem to relax anymore",
            "Everything feels urgent and pressing"
        ]
    },
    'anxiety': {
        'name': 'Anxiety Support',
        'icon': 'heart-pulse',
        'color': '#8b5cf6',
        'gradient': 'linear-gradient(135deg, #7c3aed, #a855f7)',
        'description': 'Ground yourself. Tools to manage anxious thoughts and feelings.',
        'greeting': "Welcome to your anxiety support space. Let's work together to understand and manage these anxious feelings. What's been on your mind?",
        'prompts': [
            "I can't stop worrying about the future",
            "My anxiety is making it hard to focus",
            "I'm having panic-like symptoms",
            "I feel anxious but don't know why"
        ]
    },
    'mood': {
        'name': 'Mood Boosting',
        'icon': 'sparkles',
        'color': '#10b981',
        'gradient': 'linear-gradient(135deg, #059669, #10b981)',
        'description': 'Lift your spirits. Activities and insights for better mood.',
        'greeting': "Welcome to your mood boosting space! Let's focus on what brings you joy and energy. How are you feeling today?",
        'prompts': [
            "I've been feeling down lately",
            "I want to feel more positive",
            "Nothing seems fun anymore",
            "Help me find motivation"
        ]
    },
    'fear': {
        'name': 'Fear Processing',
        'icon': 'shield',
        'color': '#f43f5e',
        'gradient': 'linear-gradient(135deg, #db2777, #f43f5e)',
        'description': 'Face your fears. A safe space to explore and process fear.',
        'greeting': "This is your safe space for working with fear. Let's explore what's feeling scary and figure out how to work through it together. What brings you here today?",
        'prompts': [
            "I'm scared something bad will happen",
            "A specific situation makes me really afraid",
            "I avoid things because of fear",
            "My fear feels irrational but won't go away"
        ]
    },
    'sleep': {
        'name': 'Sleep & Rest',
        'icon': 'moon',
        'color': '#06b6d4',
        'gradient': 'linear-gradient(135deg, #0891b2, #06b6d4)',
        'description': 'Rest well. Support for better sleep and evening wind-down.',
        'greeting': "Welcome to your sleep and rest space. Let's work on helping you get the quality rest you deserve. What's been going on with your sleep?",
        'prompts': [
            "I can't fall asleep at night",
            "I wake up tired even after sleeping",
            "My mind races when I try to sleep",
            "I need help with a bedtime routine"
        ]
    },
    'relationships': {
        'name': 'Relationship Support',
        'icon': 'users',
        'color': '#ec4899',
        'gradient': 'linear-gradient(135deg, #db2777, #ec4899)',
        'description': 'Connect better. Navigate relationship challenges with clarity.',
        'greeting': "Welcome to your relationship support space. Let's talk through what's happening in your relationships and find healthy ways forward. What's on your mind?",
        'prompts': [
            "I'm having issues with my partner",
            "A friendship is feeling strained",
            "I don't know how to communicate my needs",
            "I feel misunderstood by people close to me"
        ]
    },
    'confidence': {
        'name': 'Self-Confidence',
        'icon': 'star',
        'color': '#facc15',
        'gradient': 'linear-gradient(135deg, #eab308, #facc15)',
        'description': 'Believe in yourself. Build confidence and self-worth.',
        'greeting': "Welcome to your confidence-building space. Let's work on recognizing your strengths and building genuine self-worth. What would you like to work on?",
        'prompts': [
            "I don't feel good enough",
            "I struggle with self-doubt",
            "I want to be more confident",
            "I compare myself to others constantly"
        ]
    },
    'focus': {
        'name': 'Focus & Clarity',
        'icon': 'target',
        'color': '#14b8a6',
        'gradient': 'linear-gradient(135deg, #0d9488, #14b8a6)',
        'description': 'Clear your mind. Improve focus and mental clarity.',
        'greeting': "Welcome to your focus and clarity space. Let's work on clearing the mental fog and improving your concentration. What's making it hard to focus?",
        'prompts': [
            "I can't concentrate on anything",
            "My mind feels scattered",
            "I'm easily distracted",
            "I need help staying on task"
        ]
    }
}


def get_activity_greeting(activity_type):
    """Get the greeting message for a specific activity space"""
    activity = ACTIVITY_SPACES.get(activity_type, {})
    return activity.get('greeting', "Hello! How can I help you today?")


def get_activity_context(activity_type):
    """Get full context for an activity space"""
    return ACTIVITY_SPACES.get(activity_type, {})


def generate_activity_response(activity_type, user_message, emotion=None, intensity=None):
    """
    Generate responses tailored to specific activity spaces
    More conversational and focused on the activity's specific goals
    """
    msg_lower = user_message.lower()
    
    # Activity-specific response strategies
    if activity_type == 'stress':
        return generate_stress_response(msg_lower, emotion, intensity)
    elif activity_type == 'anxiety':
        return generate_anxiety_response(msg_lower, emotion, intensity)
    elif activity_type == 'mood':
        return generate_mood_response(msg_lower, emotion, intensity)
    elif activity_type == 'fear':
        return generate_fear_response(msg_lower, emotion, intensity)
    elif activity_type == 'sleep':
        return generate_sleep_response(msg_lower, emotion, intensity)
    elif activity_type == 'relationships':
        return generate_relationship_response(msg_lower, emotion, intensity)
    elif activity_type == 'confidence':
        return generate_confidence_response(msg_lower, emotion, intensity)
    elif activity_type == 'focus':
        return generate_focus_response(msg_lower, emotion, intensity)
    else:
        return "I'm here to help. Tell me what's on your mind."


def generate_stress_response(msg, emotion, intensity):
    """Generate stress management focused responses"""
    responses = []
    
    # Empathetic opening
    openings = [
        "I can hear that the stress is really piling up. That feeling of being overwhelmed is so real.",
        "Oof, stress has this way of making everything feel urgent, doesn't it? Take a breath - we'll work through this.",
        "When stress builds up like this, it affects everything. Let's break it down together.",
        "That sounds like a lot to carry. Stress thrives when we feel we can't handle it all.",
    ]
    responses.append(random.choice(openings))
    
    # Stress-specific insight
    insights = [
        "Here's something interesting: our stress response doesn't differentiate between real threats and perceived ones. Your body is reacting as if everything is urgent, even though not everything actually is.",
        "Stress often comes from feeling lack of control. What's one small thing you could actually influence right now?",
        "When we're stressed, our brain narrows its focus to 'threat detection mode.' It's why everything feels more intense. Let's widen that lens a bit.",
    ]
    responses.append(random.choice(insights))
    
    # Practical intervention
    interventions = [
        "Quick stress-buster: Try the 4-7-8 breathing technique. Inhale for 4, hold for 7, exhale for 8. It activates your parasympathetic nervous system.",
        "Sometimes the best thing for stress is a 'priority check.' If you had to pick just 3 things that actually need attention today, what would they be?",
        "Progressive muscle relaxation can help: tense each muscle group for 5 seconds, then release. Start with your toes and work up.",
    ]
    responses.append(random.choice(interventions))
    
    # Exploratory question
    questions = [
        "What's the biggest contributor to your stress right now? Sometimes naming it helps us tackle it.",
        "When you imagine feeling less stressed, what would that look like for you?",
        "Is this stress from external pressure, or are you putting pressure on yourself?",
    ]
    responses.append(random.choice(questions))
    
    return "\n\n".join(responses)


def generate_anxiety_response(msg, emotion, intensity):
    """Generate anxiety-focused responses"""
    responses = []
    
    # High intensity vs normal
    if intensity in ['high', 'critical']:
        responses.append("Okay, first things first - let's get you grounded. You're safe right now in this moment. Place your feet flat on the floor and feel that connection to the ground beneath you.")
        responses.append("Anxiety can make our thoughts race into the future, imagining all kinds of scenarios. Let's gently redirect: focus on what's real and present right now, not what might happen.")
    else:
        openings = [
            "Anxiety is like a smoke alarm going off when there's just burnt toast - overprotective but not always accurate. Let's see what's really going on.",
            "I hear you, and I want you to know that anxious thoughts aren't facts. They feel real, but they're not always telling us the truth.",
            "It makes sense that you'd feel anxious. That's your brain trying to protect you. But let's examine if the threat is as big as it feels.",
        ]
        responses.append(random.choice(openings))
    
    # CBT intervention
    cbt_techniques = [
        "Let's reality-test this worry: What's the evidence for this anxious thought? What's the evidence against it?",
        "Anxiety loves 'what if' questions. Let's counter with 'what is' - what's actually happening right now?",
        "When anxiety strikes, ask yourself: Is this thought helpful? Is it true? Is it kind? Usually anxiety fails all three.",
    ]
    responses.append(random.choice(cbt_techniques))
    
    # Grounding technique
    grounding = [
        "Try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. It pulls you back to now.",
        "Put your hand on your chest and focus on your heartbeat. Breathe slowly and deliberately. You're teaching your body that you're safe.",
        "Anxiety lives in the future. Every time you notice you're spiraling, say 'right now, I am safe' and name something real around you.",
    ]
    responses.append(random.choice(grounding))
    
    questions = [
        "What specific thought keeps looping in your mind? Sometimes naming it takes away some of its power.",
        "Has this feared outcome actually happened before, or is it your anxiety creating stories?",
        "What would you tell a friend who was feeling this way?",
    ]
    responses.append(random.choice(questions))
    
    return "\n\n".join(responses)


def generate_mood_response(msg, emotion, intensity):
    """Generate mood-boosting responses"""
    responses = []
    
    openings = [
        "I'm really glad you're here and wanting to work on lifting your mood. That intention itself is powerful.",
        "Mood can feel like something that just happens to us, but we actually have more influence over it than we think. Let's explore that together.",
        "Even when our mood is low, there are small things we can do to shift it. Let's find what works for you.",
    ]
    responses.append(random.choice(openings))
    
    behavioral_activation = [
        "Here's a mood hack: do something small that you used to enjoy, even if you don't feel like it. Often, action comes before motivation, not the other way around.",
        "What's one tiny thing that usually brings you even a moment of pleasure? Music? A walk? A favorite snack? Let's start there.",
        "Behavioral activation is powerful: movement, even a short walk, literally changes our brain chemistry and can improve mood within minutes.",
    ]
    responses.append(random.choice(behavioral_activation))
    
    perspective = [
        "Mood isn't permanent, even though it feels like it when we're in it. Like weather, it shifts and changes. You won't always feel this way.",
        "Sometimes we wait to feel better before doing things, but it works better the other way: do things, and feelings follow.",
        "Low mood often comes with thoughts like 'nothing matters' or 'nothing will help.' Those are symptoms of the mood, not facts about reality.",
    ]
    responses.append(random.choice(perspective))
    
    questions = [
        "What's something that made you smile recently, even briefly? Let's build on that.",
        "If your mood could shift even 10% better, what would need to happen?",
        "When you think of feeling 'good,' what does that actually look like for you?",
    ]
    responses.append(random.choice(questions))
    
    return "\n\n".join(responses)


def generate_fear_response(msg, emotion, intensity):
    """Generate fear processing responses"""
    responses = []
    
    validation = [
        "Fear is one of our most primal emotions, and it's here to protect us. But sometimes it's protecting us from things that aren't actual threats. Let's figure out which this is.",
        "Thank you for being brave enough to face this fear instead of running from it. That takes real courage.",
        "Fear can feel overwhelming, but here's the thing: by talking about it, you're already taking away some of its power.",
    ]
    responses.append(random.choice(validation))
    
    exploration = [
        "Let's get specific about this fear. When you imagine the thing you're afraid of, what's the worst part? What exactly are you picturing?",
        "Fear often has layers. There's the surface fear and then the deeper fear underneath. What do you think this is really about?",
        "Sometimes we avoid looking directly at our fears because that feels safer. But avoidance actually makes fear grow. Exposure, even just mentally, helps shrink it.",
    ]
    responses.append(random.choice(exploration))
    
    if intensity in ['high', 'critical']:
        techniques = [
            "Your fear response is in overdrive right now. Let's calm the alarm system: breathe in through your nose for 4, hold for 4, out through your mouth for 6. Do this a few times.",
            "When fear is this strong, we need to remind our brain we're safe. Place both feet on the ground. Feel that stability. You're here, you're okay right now in this moment.",
        ]
    else:
        techniques = [
            "Let's reality-check this fear: On a scale of 1-10, how likely is this feared outcome to actually happen? Then, on the same scale, how bad would it be if it did?",
            "Fear thrives on vagueness. The more specific we make it, the more we can actually address it. Can you describe exactly what you're afraid of?",
        ]
    responses.append(random.choice(techniques))
    
    questions = [
        "What would it take for you to feel safe regarding this situation?",
        "Has facing a fear in the past ever taught you something valuable?",
        "If this fear wasn't in control, what would you be doing differently?",
    ]
    responses.append(random.choice(questions))
    
    return "\n\n".join(responses)


def generate_sleep_response(msg, emotion, intensity):
    """Generate sleep support responses"""
    responses = []
    
    validation = [
        "Sleep issues are so frustrating because they create a vicious cycle - stress about not sleeping makes it harder to sleep.",
        "Good sleep is absolutely fundamental to our mental health, so I'm glad we're focusing on this. Let's figure out what's getting in the way.",
        "When we can't sleep, it feels like we've lost control over something really basic. That's incredibly stressful.",
    ]
    responses.append(random.choice(validation))
    
    # Check for specific sleep issues
    if 'fall asleep' in msg or 'insomnia' in msg:
        responses.append("Trouble falling asleep often ties to an overactive mind or being in 'alert mode.' We need to signal to your brain that it's time to wind down.")
        tips = [
            "Create a 'wind-down hour' before bed: dim lights, no screens, maybe reading or gentle stretching. You're training your brain to recognize the bedtime routine.",
            "Try the '4-7-8' breathing technique in bed: inhale for 4, hold for 7, exhale for 8. It activates rest mode in your nervous system.",
            "If you're not asleep in 20 minutes, get up and do something boring in low light until you feel sleepy. Don't let the bed become a place of frustration.",
        ]
        responses.append(random.choice(tips))
    elif 'wake' in msg or 'tired' in msg:
        responses.append("Waking up exhausted even after sleeping suggests the quality of sleep isn't there. This could be stress, light sleep, or even sleep disruptions.")
        tips = [
            "Keep your bedroom cool (65-68°F is ideal), completely dark, and quiet. Quality sleep happens when the environment supports it.",
            "Avoid caffeine after 2pm and alcohol close to bedtime - both mess with sleep cycles even though alcohol might make you feel sleepy initially.",
            "Consistent sleep schedule helps a lot: try to go to bed and wake up at the same time every day, even weekends.",
        ]
        responses.append(random.choice(tips))
    elif 'mind races' in msg or 'thinking' in msg or 'worry' in msg:
        responses.append("Racing thoughts at bedtime are super common, especially when we're stressed. Your mind uses quiet time to process, but we need to give it a better outlet.")
        tips = [
            "Try a 'thought download': spend 10 minutes before bed writing down everything on your mind. It clears the mental cache.",
            "When thoughts race, don't fight them. Instead, focus on your breath or do a body scan - systematically relax each body part from toes to head.",
            "Practice the '10-3-2-1-0' rule: no caffeine 10hrs before bed, no food 3hrs before, no work 2hrs before, no screens 1hr before, zero snoozes in the morning.",
        ]
        responses.append(random.choice(tips))
    else:
        general_tips = [
            "Sleep hygiene makes a huge difference: consistent schedule, cool dark room, no screens before bed, limit caffeine, regular exercise (but not close to bedtime).",
            "The bedroom should be for sleep and intimacy only - not work, not TV, not scrolling. Your brain needs to associate it with rest.",
        ]
        responses.append(random.choice(general_tips))
    
    questions = [
        "What's your current bedtime routine look like? Or do you not really have one?",
        "When you think about your sleep environment, is there anything that might be disrupting your rest?",
        "How long has sleep been an issue? Is it recent or ongoing?",
    ]
    responses.append(random.choice(questions))
    
    return "\n\n".join(responses)


def generate_relationship_response(msg, emotion, intensity):
    """Generate relationship support responses"""
    responses = []
    
    validation = [
        "Relationship struggles are hard because they involve other people who have their own perspectives, needs, and feelings. It's complex.",
        "The fact that you care enough to work on this says a lot about you. Not everyone takes the time to reflect on their relationships.",
        "When something's off in a relationship, it can really weigh on us. These connections matter deeply.",
    ]
    responses.append(random.choice(validation))
    
    if 'partner' in msg or 'boyfriend' in msg or 'girlfriend' in msg or 'spouse' in msg:
        insights = [
            "Romantic relationships have this way of triggering our deepest vulnerabilities. What looks like a surface issue often connects to core needs like feeling valued, understood, or secure.",
            "Communication in relationships isn't just about talking - it's about feeling heard. Are you able to express what you need, and when you do, does it feel like they really get it?",
            "Sometimes relationship issues aren't about right or wrong, but about different needs or communication styles colliding. Understanding that can help.",
        ]
        responses.append(random.choice(insights))
    elif 'friend' in msg or 'friendship' in msg:
        insights = [
            "Friendships can be just as important as romantic relationships, but we don't always give them the same attention when they struggle. I'm glad you're focusing on this.",
            "Friend dynamics can shift as we grow and change. Sometimes what worked before doesn't anymore, and that requires renegotiation.",
            "Healthy friendships need honesty. If you're noticing something's off but not saying anything, that creates distance.",
        ]
        responses.append(random.choice(insights))
    else:
        insights = [
            "Relationships require us to balance our own needs with caring about someone else's. That's not always easy, but it's the work that matters.",
            "How we show up in relationships often mirrors patterns from our past. Sometimes recognizing those patterns is the first step to changing them.",
        ]
        responses.append(random.choice(insights))
    
    communication_tips = [
        "When you need to have a difficult conversation, try using 'I feel... when... because... what I need is...' It's less accusatory and more about your experience.",
        "One barrier in relationships: assuming the other person should 'just know' what we need. But we have to actually communicate it clearly.",
        "Listen to understand, not to respond. When they're sharing, resist the urge to immediately fix or defend - just hear them first.",
    ]
    responses.append(random.choice(communication_tips))
    
    questions = [
        "Have you been able to actually talk to them about any of this, or is it all still just in your head?",
        "What would the ideal version of this relationship look like to you? Can you picture it?",
        "When you think about what you need from this relationship, what comes up for you?",
    ]
    responses.append(random.choice(questions))
    
    return "\n\n".join(responses)


def generate_confidence_response(msg, emotion, intensity):
    """Generate confidence-building responses"""
    responses = []
    
    validation = [
        "Self-doubt is something almost everyone struggles with, even people who seem really confident. You're definitely not alone in this.",
        "Confidence isn't about thinking you're perfect - it's about being okay with yourself even while knowing you're not. That's a really important distinction.",
        "The way we talk to ourselves has such a huge impact on our confidence. And I'm guessing your inner voice might not be very kind right now?",
    ]
    responses.append(random.choice(validation))
    
    reframe = [
        "Here's something to consider: confidence is a skill, not a trait. It's built through small actions, not by waiting until you 'feel ready.'",
        "We often wait to feel confident before doing things. But actually, confidence comes from doing things despite feeling unsure. Action comes first.",
        "Your worth isn't determined by your achievements, appearance, or what others think. But our minds try to convince us otherwise, don't they?",
    ]
    responses.append(random.choice(reframe))
    
    if 'compare' in msg or 'others' in msg:
        responses.append("Comparison is confidence's worst enemy. You're comparing your behind-the-scenes to everyone else's highlight reel - it's not a fair contest.")
    elif 'not good enough' in msg or 'failure' in msg:
        responses.append("That 'not good enough' voice? It's often an echo from the past - old experiences creating rules that aren't true anymore.")
    
    practical = [
        "Try this: What's one thing you've accomplished, no matter how small, in the past week? We often ignore our wins while amplifying our perceived failures.",
        "Quick exercise: Write down 3 things you're actually decent at. They don't have to be big - maybe you make good coffee, you're reliable, you're creative. Start recognizing your strengths.",
        "Self-compassion builds real confidence. Next time you mess up, talk to yourself like you would a good friend. What would you say to them?",
    ]
    responses.append(random.choice(practical))
    
    questions = [
        "If you weren't afraid of failing or being judged, what would you try?",
        "What does confidence look like to you? How would you know if you had it?",
        "Who or what taught you that you're not good enough? Where did that belief come from?",
    ]
    responses.append(random.choice(questions))
    
    return "\n\n".join(responses)


def generate_focus_response(msg, emotion, intensity):
    """Generate focus and clarity responses"""
    responses = []
    
    validation = [
        "Difficulty focusing is incredibly common, especially with how overstimulating our modern world is. Your brain is trying to process a million inputs at once.",
        "When we can't focus, it's frustrating because we feel like we're not in control of our own minds. But there are definitely things that can help.",
        "Mental fog and distraction usually have underlying causes - stress, lack of sleep, too much multitasking, or just information overload.",
    ]
    responses.append(random.choice(validation))
    
    insights = [
        "Our brains aren't designed to focus for long stretches. The Pomodoro Technique works for a reason: 25 minutes of focus, 5 minute break. Work with your brain, not against it.",
        "Every time you switch tasks, your brain takes time to reorient. That's why multitasking kills focus. Single-tasking is actually much more efficient.",
        "Your environment matters more than you think. A cluttered space creates mental clutter. Even small changes - clearing your desk, using headphones - can help.",
    ]
    responses.append(random.choice(insights))
    
    practical = [
        "Try the 'two-minute rule': if you can do something in 2 minutes or less, do it now. Everything else goes on a list. This clears mental clutter.",
        "Use 'implementation intentions': Instead of 'I'll focus today,' try 'When I sit down, I'll put my phone in another room and work for 25 minutes.' Specific plans work better.",
        "Your phone is a focus killer. Try putting it on 'Do Not Disturb' or in another room when you need to concentrate. Out of sight, out of mind.",
    ]
    responses.append(random.choice(practical))
    
    if 'scattered' in msg or 'racing' in msg:
        responses.append("When your mind feels scattered, a few minutes of mindfulness or a short walk can help reset. Movement and mindfulness both clear mental fog.")
    elif 'distracted' in msg:
        responses.append("Identify your specific distractors: Is it your phone? Notifications? People? Thoughts? Once you know what pulls you away, you can address it directly.")
    
    questions = [
        "What time of day is your focus best? Can you protect that time for your most important work?",
        "What's usually distracting you - external things (phone, people) or internal things (thoughts, worry)?",
        "How much sleep are you getting? Because focus and sleep quality are deeply connected.",
    ]
    responses.append(random.choice(questions))
    
    return "\n\n".join(responses)


def get_all_activity_spaces():
    """Return all activity spaces for UI"""
    return ACTIVITY_SPACES
