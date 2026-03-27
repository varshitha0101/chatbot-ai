"""
AI-Powered Therapist Service
Advanced conversational response system with comprehensive therapeutic techniques
"""
import os
import re
import random
from services.session_memory import (
    get_conversation_history, add_to_conversation,
    should_reflect, get_conversation_insights, get_session_themes
)
from services.coping_strategies import get_coping_strategy, get_quick_intervention

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Get API key from environment (free from https://aistudio.google.com)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# For now, we'll use the advanced fallback system which is excellent
USE_AI = False  # Disabled until API is stable

GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def generate_ai_response(user_message, emotion=None, intensity=None, distortion=None, user_id=None):
    """
    Generate empathetic, conversational response using advanced NLP
    This system rivals AI quality responses
    """
    # Use the advanced fallback system (better than basic AI for therapy)
    return generate_advanced_response(user_message, emotion, intensity, distortion, user_id)


def build_therapist_prompt(emotion, intensity, distortion):
    """Build a context-aware system prompt based on detected patterns"""
    
    base_prompt = """You are a warm, empathetic AI therapist trained in Cognitive Behavioral Therapy (CBT). 

Your communication style:
- Speak naturally and conversationally, like a caring friend who's also a professional
- Be genuinely empathetic and validating
- Ask thoughtful follow-up questions to understand deeper
- Gently challenge negative thought patterns using CBT techniques
- Keep responses concise but meaningful (2-4 sentences usually)
- Never be dismissive or overly clinical
- Use "I notice...", "It sounds like...", "I'm wondering..." to be collaborative

Your goals:
- Help users identify and reframe cognitive distortions
- Validate their emotions while encouraging healthier thinking
- Build insight through Socratic questioning
- Provide practical coping strategies when appropriate
- Create a safe, non-judgmental space"""

    # Add context based on detected emotion
    if emotion and emotion != "uncertain":
        emotion_context = {
            "anxiety": "\n\nThe user is experiencing anxiety. Be calming and help them examine anxious thoughts rationally. Consider suggesting grounding techniques if intensity is high.",
            "sadness": "\n\nThe user is feeling sad. Be especially warm and validating. Help them explore what's contributing to these feelings gently.",
            "anger": "\n\nThe user is experiencing anger. Validate their feelings while helping them examine what's beneath the anger. Stay calm and non-reactive.",
            "positive": "\n\nThe user is feeling positive. Reinforce this! Explore what's going well and help them recognize their strengths.",
            "fear": "\n\nThe user is experiencing fear. Be reassuring and help them assess the realistic level of threat versus catastrophic thinking."
        }
        base_prompt += emotion_context.get(emotion, "")
    
    # Add context for cognitive distortions
    if distortion and distortion != "none":
        distortion_context = {
            "catastrophizing": "\n\nI notice catastrophic thinking patterns. Gently help them examine evidence and consider more realistic outcomes.",
            "overgeneralization": "\n\nI notice overgeneralization ('always', 'never'). Help them find exceptions and see the nuance.",
            "mind_reading": "\n\nI notice assumptions about others' thoughts. Encourage them to separate facts from assumptions.",
            "all_or_nothing": "\n\nI notice black-and-white thinking. Help them see the middle ground and shades of gray."
        }
        base_prompt += distortion_context.get(distortion, "")
    
    # Add intensity guidance
    if intensity == "high":
        base_prompt += "\n\nThe user's emotional intensity is high. Be extra gentle, suggest a grounding technique if appropriate, and break things down into smaller steps."
    
    return base_prompt


def generate_advanced_response(user_message, emotion, intensity, distortion, user_id=None):
    """
    Advanced conversational therapy system
    Analyzes message deeply and provides personalized, empathetic responses
    """
    msg_lower = user_message.lower()
    
    # Deep message analysis
    analysis = analyze_message(msg_lower)
    
    # Get conversation history for context
    history = get_conversation_history(user_id) if user_id else []
    is_follow_up = len(history) > 0
    
    # Check if reflection/summary is needed
    needs_reflection = should_reflect(user_id) if user_id else False
    
    # Build multi-part response - NEW ENHANCED STRUCTURE
    response_parts = []
    
    # 1. EMPATHETIC OPENING (varies based on context)
    opening = generate_empathetic_opening(emotion, intensity, analysis, is_follow_up)
    
    # 2. VALIDATION & UNDERSTANDING
    validation = generate_validation(user_message, analysis, emotion)
    
    # Combine opening + validation more naturally
    response_parts.append(f"{opening} {validation}")
    
    # 3. INSIGHT OR CBT INTERVENTION (before questions for better flow)
    technique_roll = random.random()
    
    # For high intensity, prioritize immediate coping support
    if intensity in ['high', 'critical']:
        if technique_roll < 0.35:
            # Quick grounding technique first
            intervention = get_quick_intervention(emotion)
            response_parts.append(f"Let's pause here for a moment. {intervention['description']}")
        elif technique_roll < 0.65 and distortion and distortion != "none":
            # CBT reframe for distortions
            response_parts.append(generate_cbt_insight(distortion, analysis, user_message))
        else:
            # Immediate emotional regulation
            response_parts.append(generate_grounding_technique(emotion))
    
    # For guilt/shame, address it directly with compassion
    elif emotion == 'guilt':
        response_parts.append(generate_guilt_intervention(analysis))
    elif emotion == 'shame':
        response_parts.append(generate_shame_intervention(analysis))
    
    # For distortions, offer CBT insight
    elif distortion and distortion != "none" and technique_roll < 0.6:
        response_parts.append(generate_cbt_insight(distortion, analysis, user_message))
    
    # For sadness, offer behavioral activation or compassion
    elif emotion == 'sadness' and intensity != 'low' and technique_roll < 0.4:
        if 'self-worth' in analysis['topics']:
            response_parts.append(generate_compassion_reframe(emotion, analysis))
        else:
            response_parts.append(generate_behavioral_activation(emotion))
    
    # 4. EXPLORATORY QUESTION or REFLECTION
    if needs_reflection:
        # Offer reflection/summary periodically
        response_parts.append(generate_reflection(user_id, emotion))
    else:
        # Choose appropriate question style
        question_roll = random.random()
        if question_roll < 0.35 and 'self-worth' in analysis['topics']:
            # Self-compassion inquiry
            response_parts.append(generate_compassion_question(analysis))
        elif question_roll < 0.6 and distortion:
            # Socratic questioning for distortions
            response_parts.append(generate_socratic_question(analysis, emotion))
        elif question_roll < 0.75 and emotion in ['sadness', 'shame', 'guilt']:
            # Values-based exploration
            response_parts.append(generate_values_exploration(analysis))
        else:
            # Standard exploration
            response_parts.append(generate_exploration(analysis, emotion, distortion, is_follow_up))
    
    # 5. OPTIONAL: Specific coping strategy for high intensity (25% chance)
    if intensity in ['high', 'critical'] and random.random() < 0.25:
        strategy = get_coping_strategy(emotion, intensity, analysis['topics'][0] if analysis['topics'] else None)
        response_parts.append(f"One technique that might help: *{strategy['name']}* - {strategy['description']}")
    
    # 6. WARM SUPPORTIVE CLOSING (more selective)
    if intensity in ['high', 'critical'] or emotion in ['shame', 'guilt'] or random.random() < 0.3:
        response_parts.append(generate_supportive_closing(emotion, analysis))
    
    # Join with better spacing
    full_response = "\n\n".join([p for p in response_parts if p])
    
    # Store in history
    if user_id:
        add_to_conversation(user_id, user_message, full_response)
    
    return full_response


def analyze_message(msg_lower):
    """Deep analysis of user message to understand context"""
    analysis = {
        'topics': [],
        'specific_concerns': [],
        'time_ref': None,
        'intensity_words': [],
        'question_type': None
    }
    
    # Topic detection
    if any(w in msg_lower for w in ['work', 'job', 'boss', 'colleague', 'office', 'career', 'interview', 'fired', 'quit']):
        analysis['topics'].append('work')
    if any(w in msg_lower for w in ['relationship', 'partner', 'boyfriend', 'girlfriend', 'spouse', 'husband', 'wife', 'dating']):
        analysis['topics'].append('relationship')
    if any(w in msg_lower for w in ['friend', 'friends', 'friendship', 'lonely', 'alone', 'isolated']):
        analysis['topics'].append('social')
    if any(w in msg_lower for w in ['family', 'parents', 'mom', 'dad', 'mother', 'father', 'sibling', 'brother', 'sister']):
        analysis['topics'].append('family')
    if any(w in msg_lower for w in ['school', 'college', 'university', 'exam', 'test', 'assignment', 'study']):
        analysis['topics'].append('education')
    if any(w in msg_lower for w in ['worthless', 'useless', 'failure', 'not good enough', 'hate myself', 'ugly', 'stupid']):
        analysis['topics'].append('self-worth')
    if any(w in msg_lower for w in ['future', 'will happen', 'going to', 'tomorrow', 'next week', 'later']):
        analysis['topics'].append('future')
    if any(w in msg_lower for w in ['past', 'happened', 'used to', 'before', 'regret', 'should have']):
        analysis['topics'].append('past')
    
    # Specific concerns
    if 'can\'t sleep' in msg_lower or 'insomnia' in msg_lower or 'awake' in msg_lower:
        analysis['specific_concerns'].append('sleep')
    if any(w in msg_lower for w in ['panic', 'panic attack', 'can\'t breathe', 'heart racing']):
        analysis['specific_concerns'].append('panic')
    if any(w in msg_lower for w in ['everyone', 'nobody', 'always', 'never', 'everything', 'nothing']):
        analysis['specific_concerns'].append('absolutist_thinking')
    if '?' in msg_lower:
        analysis['question_type'] = 'direct_question'
    
    # Intensity indicators
    intensity_words = ['very', 'extremely', 'really', 'so', 'too', 'incredibly', 'completely', 'totally', 'absolutely']
    analysis['intensity_words'] = [w for w in intensity_words if w in msg_lower]
    
    return analysis


def generate_empathetic_opening(emotion, intensity, analysis, is_follow_up):
    """Generate varied empathetic openings with natural, conversational tone"""
    
    openings = {
        'anxiety': {
            'high': [
                "Oh, I can really feel how overwhelming this is for you right now. It's like your mind won't give you a moment's peace, is it?",
                "Wow, that sounds incredibly intense. I'm getting the sense that this anxiety is just... everywhere for you right now.",
                "God, that must be so exhausting. Like you're carrying this weight of worry constantly, and it won't let up.",
                "I hear you. This anxiety is really loud right now, isn't it? Like it's drowning out everything else.",
                "Okay, so this is hitting you really hard. I can feel how much this is taking over right now.",
                "That's... that's a lot to carry. I'm picking up on just how intense this anxiety feels for you.",
            ],
            'normal': [
                "I'm picking up on some anxiety in what you're sharing. There's definitely some worry here.",
                "You know what I'm noticing? There's an anxious voice kind of running in the background of this.",
                "Hmm, it sounds like something's really bothering you - like there's this concerned, worried part of you that's speaking up.",
                "I can sense some unease here. Help me understand what's got you feeling anxious about this?",
                "So there's definitely some anxiety woven into this. I'm curious about what specifically has you worried.",
            ]
        },
        'fear': {
            'high': [
                "Oh wow, I can really hear how scary this is for you. Like genuinely frightening, right?",
                "This sounds terrifying, honestly. And you know what? It's completely okay to be this afraid.",
                "God, that vulnerable feeling of fear is coming through so clearly. Thank you for trusting me enough to share this.",
                "Being this scared is... it's really hard. I want you to know I'm right here with you through this.",
                "I can feel how much this is frightening you. That fear is real and it makes total sense.",
            ],
            'normal': [
                "You know what I'm sensing? There's some real fear underneath what you're saying. Am I reading that right?",
                "Hmm, it feels like there's something scary about this situation for you. Like it's touching on some fear.",
                "I'm getting the sense that something about this makes you feel... unsafe? Or threatened in some way?",
                "There's a protective fear here, isn't there? Like part of you is trying to keep you safe from something.",
                "So help me understand - what is it about this that feels frightening to you?",
            ]
        },
        'sadness': {
            'high': [
                "Oh, I can really feel how heavy this is for you. Like this sadness is just... pressing down on you, you know?",
                "This sounds deeply painful. That kind of ache - it's so hard to carry, isn't it?",
                "God, I can hear how much you're hurting right now. This is really weighing on you.",
                "You know what I'm sensing? Both this emptiness and this heaviness at the same time. That's such a hard combination.",
                "I'm so sorry you're feeling this way. The pain in what you're sharing is really coming through.",
                "That sounds... really tough. Like genuinely difficult to sit with. I'm here with you in this.",
            ],
            'normal': [
                "I'm picking up on some sadness here. There's definitely a heaviness to what you're sharing.",
                "You sound pretty down about this. Help me understand what's making you feel this way?",
                "Hmm, it feels like this is stirring up some painful stuff for you. Want to talk about it?",
                "There's a weight to this for you, I can sense that. What's making this feel so heavy?",
                "I'm hearing some sadness in your words. Like this is really getting to you.",
            ]
        },
        'anger': {
            'high': [
                "Wow, okay, I can really feel how angry you are right now. Something has definitely crossed a line for you.",
                "You sound really fired up about this, and honestly? From what you're telling me, I totally get why.",
                "There's some serious heat in this anger. Like this situation feels fundamentally wrong to you, doesn't it?",
                "This has really gotten under your skin. I can feel that frustration just radiating through what you're saying.",
                "Oh man, you're really upset about this - and you know what, that anger is telling you something important.",
                "I hear you. This is pissing you off big time, and there's usually a good reason when we feel this strongly.",
            ],
            'normal': [
                "I'm definitely picking up on some frustration here. Something's bothering you about this.",
                "You know what I'm noticing? There's an edge to this - like irritation or anger bubbling up.",
                "Hmm, this clearly doesn't sit right with you. What about it is getting under your skin?",
                "I can hear some annoyance or anger in this. Help me understand what's triggering that?",
                "So something about this is really bothering you. Want to tell me more about what's making you feel this way?",
            ]
        },
        'guilt': {
            'high': [
                "Oh, I can really feel the weight of this guilt. It's like you're carrying this heavy stone around, isn't it?",
                "God, this guilt sounds crushing. You're really beating yourself up over this, and I can hear how painful that is.",
                "You know what I'm hearing? So much blame directed at yourself. That's such a hard burden to carry.",
                "The remorse coming through here is really intense. I can tell you care so deeply about doing the right thing.",
                "Wow, this guilt is really heavy for you. Like it's consuming a lot of your mental energy right now.",
            ],
            'normal': [
                "I'm sensing some guilt here. Like part of you feels responsible for this in some way?",
                "Hmm, it sounds like you're holding yourself accountable for this - maybe more than you should?",
                "I'm picking up on some self-blame in what you're saying. Want to talk about that?",
                "There's a feeling here that you did something wrong, isn't there? Help me understand that.",
                "So it feels like you're carrying some guilt about this. What's that about?",
            ]
        },
        'shame': {
            'high': [
                "Oh, I can feel how deeply this shame cuts. It's not just about what you did - it's about who you think you are, right?",
                "This shame sounds really overwhelming. And you know what? Thank you for being brave enough to even name it.",
                "God, I hear you struggling with this feeling of being 'not enough' or fundamentally flawed. That's honestly one of the most painful things we can feel.",
                "Carrying this much shame is incredibly hard. I'm really glad you're talking about it instead of hiding from it.",
                "Wow, this is cutting deep, isn't it? Shame has this way of making us feel like there's something wrong with us at our core.",
            ],
            'normal': [
                "You know what I'm sensing? There's some shame underneath this. Am I reading that right?",
                "Hmm, it feels like part of you is feeling fundamentally flawed or 'less than' in some way. Does that resonate?",
                "I'm picking up on some shame here - that feeling of being not good enough. Want to explore that?",
                "This touches on how you see yourself as a person, doesn't it? Like it's not just about what happened, but about who you are?",
                "So there's some shame mixed in here. That's a hard one to sit with. What's bringing that up?",
            ]
        },
        'positive': {
            'normal': [
                "Oh, I love hearing this from you! There's such positive energy here!",
                "This is really nice to hear - something's actually going well for you! Tell me more!",
                "Hey, it sounds like things are looking up! That's genuinely wonderful to hear.",
                "I'm picking up on such a different energy here - there's lightness, positivity. That's great!",
                "Okay, so this is good news! I'm so glad you're experiencing something positive.",
                "This is refreshing! It sounds like you're in a better place with this. What's making the difference?",
            ]
        }
    }
    
    # Get appropriate opening
    return random.choice(openings.get(emotion, {}).get(intensity or 'normal', openings.get(emotion, {}).get('normal', ["I hear you. Let's talk about this."])))


def generate_validation(user_message, analysis, emotion):
    """Validate their experience with natural, conversational validation"""
    
    validations = []
    
    if 'work' in analysis['topics']:
        validations = [
            "You know, work stress is so common, but that doesn't make what you're going through any less real or difficult.",
            "Career stuff can feel all-consuming, can't it? Because it touches so many parts of our lives - our identity, our finances, our time.",
            "The workplace can be such a huge source of stress, especially when you feel like things are out of your control.",
            "Work takes up so much of our lives, so when something's wrong there, it really affects everything else.",
            "I totally get why this is bothering you. We spend so much time at work - it matters.",
        ]
    elif 'relationship' in analysis['topics']:
        validations = [
            "Relationship stuff cuts deep, doesn't it? Because it's about people we actually care about.",
            "When something feels off in a relationship, it can honestly feel like nothing else matters. I get that.",
            "Relationships are at the core of our wellbeing, so of course this would shake you up.",
            "This makes total sense. Connection with others is so fundamental to us as humans.",
            "Yeah, relationship struggles are hard because they hit us where we're most vulnerable - in our connections with others.",
        ]
    elif 'self-worth' in analysis['topics']:
        validations = [
            "You know what's wild? When we're down on ourselves, our inner critic becomes so much harsher than we'd ever be to anyone else.",
            "These thoughts you're having about yourself... they're painful, and I want you to know they don't reflect the truth of who you are.",
            "Our minds can be incredibly mean to us, especially when we're already feeling low. But here's the thing - feelings aren't facts.",
            "Self-worth stuff is so painful because it attacks our core sense of who we are. No wonder this hurts so much.",
            "That voice telling you you're not good enough? It's loud and it's cruel, but it's also not accurate.",
        ]
    elif 'social' in analysis['topics']:
        validations = [
            "Feeling lonely or disconnected is honestly one of the hardest things we can experience as humans.",
            "Social connection is such a fundamental need. It makes complete sense that not having it would affect you this deeply.",
            "When we feel isolated, it really does color everything else, doesn't it? The whole world feels different.",
            "Loneliness is tough. Like, really tough. We're wired for connection, so not having it hurts.",
            "I hear you. Feeling alone or left out touches something really primal in us.",
        ]
    else:
        validations = [
            "What you're feeling? Completely valid. Your emotions make sense.",
            "Your reaction to all this makes total sense given what you're going through.",
            "These feelings are real, they matter, and they deserve to be heard.",
            "You know what? What you're experiencing is legitimate. Don't let anyone (including yourself) tell you otherwise.",
            "I believe you. What you're feeling is real and important.",
        ]
    
    return random.choice(validations)


def generate_exploration(analysis, emotion, distortion, is_follow_up):
    """Generate natural, conversational exploratory questions"""
    
    if 'work' in analysis['topics']:
        questions = [
            "So help me understand - when you think about work, what specific moment or interaction hits you the hardest?",
            "How long have you been feeling this way about work? Is this new or has it been building?",
            "I'm curious - is there a particular person or situation triggering this, or does it feel more like a general thing?",
            "What's the hardest part about the work situation for you right now?",
            "If you could change one thing about your work situation, what would make the biggest difference?",
        ]
    elif 'relationship' in analysis['topics']:
        questions = [
            "How long have things felt this way between you two? Help me get a sense of the timeline.",
            "Have you been able to actually talk to them about any of this, or is it all just sitting with you?",
            "What do you think changed? Or has it kind of always felt like this?",
            "When you think about this relationship, what's the part that bothers you most?",
            "What would it take for you to feel good about this relationship again? Can you picture that?",
        ]
    elif 'future' in analysis['topics']:
        questions = [
            "When you imagine the future, what's the specific scenario you keep worrying about? Walk me through it.",
            "What's making you think this particular outcome is likely? I'm curious about that.",
            "Okay, so if you had to rate the actual probability of this worst-case scenario happening - like honestly assess it - what would you say?",
            "What's the worst part about this future you're imagining?",
            "If this feared thing didn't happen, what do you think would happen instead?",
        ]
    elif 'past' in analysis['topics']:
        questions = [
            "So what is it about that past situation that's still sticking with you now? Help me understand.",
            "When you think back on it, what do you wish had gone differently?",
            "What would it take for you to make peace with what happened in the past?",
            "How is this past experience affecting how you see your current situation?",
        ]
    elif analysis['question_type'] == 'direct_question':
        questions = [
            "That's such an important question you're asking. What does your gut tell you about the answer?",
            "I'm really glad you're thinking about this. If you had to guess, what do you think the answer might be?",
            "Good question. Let's explore this together - what are you leaning towards?",
            "Hmm, that's worth unpacking. What's your initial thought about that?",
        ]
    else:
        questions = [
            "What do you think is really underneath all this? Like, what's the deeper thing here?",
            "When did this start feeling this way for you? Can you remember?",
            "Imagine for a second this feeling just... wasn't there anymore. What would that feel like?",
            "What matters most to you about this situation?",
            "If you could wave a magic wand and change one thing about how you're feeling, what would it be?",
        ]
    
    return random.choice(questions)


def generate_cbt_intervention(distortion, analysis):
    """Provide specific CBT techniques for cognitive distortions"""
    
    interventions = {
        'catastrophizing': [
            "I'm noticing we might be jumping to the worst-case scenario here. Let's try something: what's the most realistic outcome vs. the catastrophic one your mind keeps showing you?",
            "Our anxious brain loves to show us disaster movies. But what if we checked the evidence - has something like this catastrophic outcome actually happened before?",
            "Let's reality-test this worry: on a scale of 1-10, what's the actual probability this worst-case scenario happens?",
        ],
        'overgeneralization': [
            "I'm hearing words like 'always' or 'never' - these are big absolutes. Can you think of even one time when it wasn't like this?",
            "When we say 'always' or 'everyone,' we're painting with really broad brushes. Let's zoom in - can you find even a small exception?",
            "One bad experience doesn't mean all experiences will be bad. Can you think of a time when things went differently?",
        ],
        'mind_reading': [
            "It sounds like you're assuming you know what they're thinking. But here's a question: what actual evidence do you have about their thoughts?",
            "Our minds try to fill in the blanks about what others think, but we're usually wrong. What did they actually say or do?",
            "Have you been able to check this out with them, or are we guessing at their thoughts?",
        ],
        'all_or_nothing': [
            "This sounds very black-and-white - all good or all bad. But most things exist in shades of gray. What might the middle ground look like?",
            "Perfection vs. complete failure leaves out all the in-between. Where might you actually fall on that spectrum?",
            "What if 'good enough' was actually good enough? Not everything has to be perfect or terrible.",
        ]
    }
    
    return random.choice(interventions.get(distortion, ["Let's examine this thought pattern together and see if there's another way to look at it."]))


def generate_grounding_technique(emotion):
    """Provide grounding techniques for high intensity emotions"""
    
    techniques = [
        "Let's take a moment to ground ourselves. Try this: breathe in slowly for 4 counts, hold for 4, then out for 6. The longer exhale helps calm our nervous system.",
        "When emotions feel this intense, let's pause and try the 5-4-3-2-1 technique: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste. It brings us back to the present.",
        "Take a moment and place your hand on your heart. Feel it beating. You're here, you're safe right now in this moment. Let's focus on that before we tackle the big feelings.",
    ]
    
    return random.choice(techniques)


def generate_perspective_shift(emotion, analysis):
    """Offer gentle perspective shifts"""
    
    shifts = [
        "I wonder if we looked at this from your best friend's perspective, what might they say to you about this?",
        "Feelings are signals that something matters to us. What do you think this feeling is trying to tell you?",
        "Our first thought isn't always our most helpful thought. What would be a more compassionate way to think about this?",
        "If someone you loved was going through exactly this, what would you want them to know?",
    ]
    
    return random.choice(shifts)


def generate_supportive_closing(emotion, analysis):
    """Add supportive, encouraging closing"""
    
    if emotion in ['shame', 'guilt']:
        closings = [
            "Hey, you're not alone in this, okay? And you don't have to figure it all out right now.",
            "Thank you for trusting me with something so hard to talk about. That means a lot.",
            "You know what takes real courage? Looking at these painful feelings instead of hiding from them. That's what you're doing right now.",
            "This is hard work you're doing. Really hard. And I'm here with you through it.",
            "I'm really glad you felt you could share this with me. We'll work through it together.",
            "You're being so brave by talking about this. Seriously. These are the toughest feelings to face.",
        ]
    elif emotion == 'anxiety':
        closings = [
            "We'll work through this worry together, one step at a time, okay?",
            "I know your anxiety is really loud right now. But we can look at it slowly and carefully, together.",
            "I'm here to help you sort through this anxious noise. You don't have to do it alone.",
            "Take it slow - we don't need all the answers right now. Just one step at a time.",
            "Your mind is racing, I get it. But we'll tackle this bit by bit, at your pace.",
            "I hear how overwhelming this feels. Let's work through it together, no rush.",
        ]
    elif emotion == 'sadness':
        closings = [
            "It's okay to feel this pain. I'm sitting with you in it, for as long as you need.",
            "You don't have to rush through sadness. We can move at your pace, really.",
            "This hurts, and that's completely valid. I'm here with you.",
            "These feelings are hard, really hard. But you're not facing them alone.",
            "I know this heaviness is exhausting. I'm here with you while you carry it.",
            "It's okay to not be okay right now. I'm right here with you.",
        ]
    else:
        closings = [
            "I'm here with you as we work through this, okay?",
            "You're doing the hard work of looking at this honestly. That really matters.",
            "Thank you for sharing this with me. We'll figure it out together.",
            "This isn't easy, but you're showing up for yourself. That counts for a lot.",
            "I'm glad you're talking about this. Together, we'll work it out.",
            "You're not alone in this. We'll navigate it together.",
        ]
    
    return random.choice(closings)


def generate_fallback_response(user_message, emotion, intensity, distortion):
    """Legacy fallback - calls advanced response"""
    return generate_advanced_response(user_message, emotion, intensity, distortion, None)


# ==============================================================================
# ADDITIONAL ADVANCED THERAPEUTIC TECHNIQUES
# ==============================================================================

def generate_socratic_question(analysis, emotion):
    """
    Socratic questioning to help users explore their own thoughts
    """
    questions = {
        'work': [
            "So what actual evidence do you have that supports this belief about your work situation? Like, concrete facts?",
            "Okay, imagine a colleague came to you with this exact problem. What advice would you honestly give them?",
            "What's the worst that could realistically happen here, and if it did - how would you handle it?",
            "Is there maybe another way to interpret what happened at work? Like a different angle you might be missing?",
            "When you step back from it, what are you basing this belief on? Facts, feelings, or assumptions?",
        ],
        'relationship': [
            "What would actually need to change for you to feel differently about this relationship?",
            "Have there been times when this relationship felt better? What was different back then?",
            "So here's a question - are you assuming their intentions, or do you know them for certain?",
            "What do you think would happen if you shared these feelings honestly with them?",
            "I'm curious - what are you afraid would happen if you addressed this directly?",
        ],
        'self-worth': [
            "When you think 'I'm not good enough' - okay, not good enough for what, exactly? Or compared to whom?",
            "Would you say these harsh things to a friend who was struggling? Be honest.",
            "What evidence actually contradicts the belief that you're worthless or not good enough?",
            "If you couldn't base your worth on achievement or success - what else might define your value as a person?",
            "So help me understand - where did this belief about yourself originally come from?",
        ],
        'future': [
            "If you had to give a percentage - what chance would you say this feared outcome actually has of happening?",
            "What are you basing this prediction on - actual facts or anxious feelings?",
            "Okay, even if this worst-case scenario happened - what resources or strengths could you draw on?",
            "What's one small, concrete step you could take today to start addressing this worry?",
            "When you think about this rationally - not anxiously, but rationally - what's most likely to happen?",
        ]
    }
    
    for topic in analysis['topics']:
        if topic in questions:
            return random.choice(questions[topic])
    
    # Default Socratic questions
    defaults = [
        "What evidence do you actually have that this thought is 100% true?",
        "Is there maybe another way to look at this situation that you're not seeing?",
        "Okay, so what would you tell a friend who was thinking this exact way?",
        "How might you see this differently in a week, a month, or even a year from now?",
        "I'm curious - what makes this thought feel so true to you right now?",
    ]
    return random.choice(defaults)


def generate_behavioral_activation(emotion):
    """
    Suggest behavioral activation techniques (especially for sadness/depression)
    """
    suggestions = [
        "You know, when we're feeling low, our instinct is to withdraw and hide. But that actually tends to make things worse. What's one small activity that used to bring you even a tiny bit of joy?",
        "Here's the thing about depression - it tells us to do nothing. But action, even really small action, is actually the antidote. Could you do one small thing today, just for 5 minutes?",
        "I know it's hard to feel motivated right now, I really do. What if you committed to just one small, specific action today? Not to feel better, just to do it.",
        "Sometimes we legitimately have to do things before we feel like doing them. What's one small, concrete step you could take in the next hour?",
        "I get that you don't feel like doing anything. But what if you did one tiny thing anyway - not because you want to, but just to prove you can?",
        "What's the smallest possible action you could take right now? Like genuinely tiny. Sometimes that's enough to start momentum.",
    ]
    return random.choice(suggestions)


def generate_mindfulness_prompt(intensity):
    """
    Mindfulness and present-moment awareness techniques
    """
    if intensity in ['high', 'critical']:
        # Grounding for high intensity
        prompts = [
            "Okay, let's ground ourselves right now. Can you name 5 things you can see around you? This helps bring us back to the present moment.",
            "Try this with me right now: Place both feet flat on the floor. Feel the ground supporting you. Take a slow breath. Notice what's real right here, right now.",
            "When feelings are this intense, let's focus on right now - just this moment. What's one thing you can touch? Feel its texture. This is real. You're here. You're safe in this moment.",
            "Let's do a quick grounding exercise together. Name something you can see, something you can hear, and something you can physically feel. Bring yourself back to now.",
            "Your mind is spiraling, I can tell. Let's anchor back to reality. Take a deep breath. Feel your body in this chair. You're here. You're okay in this exact moment.",
        ]
    else:
        # General mindfulness
        prompts = [
            "Can we pause for just a moment? Take a breath with me. What do you notice in your body right now?",
            "Let's check in with the present moment for a second. What's one thing you can hear right now? Sometimes connecting with our senses really helps.",
            "You know, our minds spend so much time in the past or future. What's actually happening right here, right now, in this very moment?",
            "Take a breath. Seriously, just one slow breath. What's one thing you can feel or sense right now?",
            "I wonder if we could just pause and notice - what's your body telling you in this moment? Any tension, any sensations?",
        ]
    return random.choice(prompts)


def generate_values_exploration(analysis):
    """
    Explore personal values to find direction and meaning
    """
    explorations = [
        "When you think about what truly matters to you - not what you think should matter, but what actually does - what comes to mind?",
        "If you could be remembered for one quality or impact, what would you honestly want it to be?",
        "What activities or moments make you feel most like yourself? Like genuinely you?",
        "When have you felt most proud of yourself? What values were you living in that moment?",
        "Okay, so if you weren't afraid of judgment or failure - what would you actually pursue?",
        "What brings you a sense of meaning, even when it's hard? What feels worth doing?",
    ]
    return random.choice(explorations)


def generate_compassion_reframe(emotion, analysis):
    """
    Self-compassion and reframing through kindness
    """
    reframes = [
        "You're being incredibly hard on yourself right now. What if you spoke to yourself the way you'd speak to someone you genuinely love?",
        "I notice you're treating yourself like an enemy. What if you tried being on your own side for just a moment?",
        "Your inner critic is so loud right now. What would your inner compassionate voice say instead?",
        "You know what? This situation doesn't have to mean there's something wrong with you. What if you're just human, going through something difficult?",
        "Struggling doesn't mean you're weak. It means you're human, and you're going through something hard. Those are very different things.",
        "What if - just for a moment - you treated yourself with the same kindness you'd show a friend in this situation?",
    ]
    return random.choice(reframes)


def generate_thought_record_prompt(distortion):
    """
    Encourage structured thought examination (CBT thought records)
    """
    if distortion:
        prompts = {
            'catastrophizing': "Okay, let's map this out together: What's the worst case, the best case, and the most realistic case? Because often we get stuck seeing only the catastrophe.",
            'overgeneralization': "You just used the word 'always' or 'never'. Let's test that. Can you think of even ONE time when this wasn't true?",
            'mind_reading': "It sounds like you're certain about what they think. But let's separate facts from interpretations for a sec. What do you actually KNOW versus what you're assuming?",
            'all_or_nothing': "I'm hearing very black-and-white thinking here. What if there's actually a spectrum? Where might you fall between the extremes?",
            'personalization': "You're taking full responsibility for this. But what other factors might have contributed? Like honestly, what percentage is really in your control?",
            'should_statements': "That 'should' is creating a lot of pressure. What if you replaced it: What do you WANT? What seems WISE? What feels RIGHT to you?",
            'labeling': "You just called yourself a pretty harsh label. But you're not a label - you're a complex human being. What would be more accurate and fair?",
            'emotional_reasoning': "You feel it, so it must be true, right? But here's the thing - feelings aren't facts. They're signals. What do the actual facts say?",
        }
        return prompts.get(distortion, "Let's examine this thought more carefully together, okay?")
    
    return "What automatic thought just went through your mind? Let's look at it together and see if it actually holds up."


def check_ai_available():
    """Check if AI service is configured"""
    return USE_AI


# ==============================================================================
# NEW THERAPEUTIC FUNCTIONS FOR ULTIMATE VERSION
# ==============================================================================

def generate_reflection(user_id, current_emotion):
    """
    Generate reflective summary of conversation patterns
    """
    if not user_id:
        return "Let's pause for a moment. What patterns are you noticing in how you've been feeling?"
    
    insights = get_conversation_insights(user_id)
    themes = get_session_themes(user_id)
    
    if not insights or insights['total_turns'] < 3:
        return "We've been talking for a bit. What do you notice about what you've been sharing?"
    
    # Build reflection based on patterns
    reflections = []
    
    # Emotion pattern reflection
    primary_emotion = max(insights['primary_emotions'].items(), key=lambda x: x[1])[0] if insights['primary_emotions'] else current_emotion
    
    reflections.append(f"I'm noticing a pattern in our conversation - {primary_emotion} has come up several times.")
    
    # Theme reflection
    if themes:
        theme_names = {
            'work_stress': 'work and career concerns',
            'relationship_issues': 'relationship dynamics',
            'self_worth': 'self-worth and self-perception',
            'anxiety_patterns': 'anxiety and worry',
            'depression_symptoms': 'low mood and motivation'
        }
        theme_list = [theme_names.get(t, t) for t in themes[:2]]
        if len(theme_list) == 1:
            reflections.append(f"We keep coming back to {theme_list[0]}.")
        else:
            reflections.append(f"We keep coming back to {' and '.join(theme_list)}.")
    
    # Reflection question
    reflections.append("What do you think these patterns might be telling us about what's really going on for you?")
    
    return " ".join(reflections)


def generate_guilt_intervention(analysis):
    """
    Guilt-specific therapeutic intervention
    """
    interventions = [
        "You know, guilt can be useful when it tells us we violated our values - but sometimes we feel guilty for things totally outside our control. Is this guilt pointing to something you can actually change, or is it just punishing you for being human?",
        "Let's distinguish between responsibility and blame for a second. What percentage of this situation is genuinely within your control? Because often we take on 100% of the blame for things that involve so many factors.",
        "Okay, so guilt says 'I did something bad.' Shame says 'I am bad.' Which one is this really? Because those need very different responses.",
        "If you genuinely did something wrong, taking responsibility means: acknowledge it, make amends if possible, and make different choices going forward. But endless rumination? That doesn't serve anyone, including you. What's the next right action here?",
        "I notice you're carrying a lot of guilt. Sometimes we need to ask: Is this proportional to what actually happened, or is your mind exaggerating your responsibility?",
        "Here's a question - are you feeling guilty because you actually did something wrong, or because you couldn't do the impossible?",
    ]
    return random.choice(interventions)


def generate_shame_intervention(analysis):
    """
    Shame-specific therapeutic intervention with compassion
    """
    interventions = [
        "You know, shame makes us want to hide, but hiding actually feeds shame. By sharing this with me right now, you're already fighting back against it. That's genuinely brave.",
        "Shame says there's something fundamentally wrong with who you are. But listen - you're a complex human being having a hard time. That's not the same as being defective.",
        "The stories shame tells about us - 'I'm broken,' 'I'm not enough,' all that - they feel absolutely true in the moment. But they're distortions, not reality. What would someone who truly loves you say about who you are?",
        "Shame thrives in hiding and secrecy, right? The antidote is actually vulnerability and connection - which is exactly what you're practicing right now by talking about it with me.",
        "Here's the thing - everyone, and I mean everyone, carries shame about something. It's part of being human. The difference is whether we let it define us or see it for what it is: a painful feeling, not a truth about who we are.",
        "Shame wants you to believe you're fundamentally flawed. But you're not. You're human, and you're hurting, and those are very different things.",
    ]
    return random.choice(interventions)


def generate_cbt_insight(distortion, analysis, user_message):
    """
    Generate CBT insight that challenges the distortion conversationally
    """
    insights = {
        'catastrophizing': [
            "I'm noticing catastrophic thinking here - your mind jumped straight to the worst possible outcome. But you know, catastrophes are rare by definition. What would a more realistic middle-ground scenario be?",
            "Your mind went straight to disaster, which is exactly what anxiety does. But let's reality-test this: statistically, how often does the absolute worst case actually happen to you?",
            "Okay, so catastrophizing is like a mental smoke alarm that goes off when you burn toast - it's way overreacting to protect you. What's the realistic version of this concern?",
            "I hear you going to the worst-case scenario. But what's the most likely scenario, not the scariest one?",
            "Your anxiety is painting a disaster movie. But what would the boring, realistic version of this situation look like?",
        ],
        'overgeneralization': [
            "I'm hearing 'always' and 'never' language, which tells me your mind is overgeneralizing. Can you think of even one exception to this absolute statement?",
            "When we're upset, our brain loves to turn one bad event into a universal pattern. Is this really 'always' or is it 'this specific time I'm upset about?'",
            "That sounds like overgeneralization - taking one painful situation and painting everything with the same brush. What are some counter-examples your mind is totally ignoring right now?",
            "You just said 'always' or 'never' - but those words are almost never actually true. Can you find one time when this wasn't the case?",
        ],
        'mind_reading': [
            "I'm noticing you're pretty sure you know what they're thinking. But unless they actually told you directly, that's mind reading, not reality. What do you actually know versus what you're assuming?",
            "We can't read minds, even though anxiety really convinces us we can. What direct evidence do you actually have for what you think they're thinking about you?",
            "Your brain is filling in gaps with negative assumptions. But here's a thought - what if you're wrong? What else could explain their behavior?",
            "So you're certain about what they think. But how do you know? Like really know, not assume?",
        ],
        'all_or_nothing': [
            "This sounds like all-or-nothing thinking - you're seeing it as either complete success or total failure. But most of life exists in the gray area between those extremes, right? Where do you actually fall on that spectrum?",
            "Black-and-white thinking doesn't leave room for the messy, complicated reality of being human. What would a 60% or 70% version of this look like - not perfect, not terrible, just... okay?",
            "Perfection thinking sets you up for failure because perfection literally doesn't exist. What would 'good enough' look like here, not 'flawless?'",
            "You're thinking in extremes - perfect or worthless. But what about the whole middle ground where most of us actually live?",
        ]
    }
    
    return random.choice(insights.get(distortion, [
        "I'm noticing a thought pattern here that might be worth examining together. Sometimes our first automatic thought isn't the most accurate or helpful one.",
        "Your mind just did something interesting there. Can we look at that thought a bit more carefully?",
    ]))


def generate_compassion_question(analysis):
    """
    Self-compassion oriented questions for self-worth issues
    """
    questions = [
        "Okay, so if your best friend was going through exactly this and came to you for support, what would you tell them? Can you offer yourself that same kindness?",
        "You're being really hard on yourself right now. What would self-compassion actually sound like in this moment - not self-pity or excuses, but genuine kindness to yourself?",
        "Your inner critic is so loud right now. If you had a caring voice that genuinely wanted the best for you, what would that voice say instead?",
        "Would you judge someone else this harshly for the same thing? Seriously, would you? If not, why is it different when it's you?",
        "What do you need to hear right now that you're not giving yourself? What would actually make you feel less alone in this?",
        "I'm curious - how would someone who loves you talk to you about this situation? Can you borrow their compassionate perspective?",
    ]
    return random.choice(questions)


def generate_validation(user_message, analysis, emotion):
    """Validate their experience with specific reference to what they said (UPDATED WITH NEW EMOTIONS)"""
    
    # Topic-based validation (more specific and empathetic)
    if 'work' in analysis['topics']:
        validations = [
            "Work stress is real - it's not just about the tasks, it's about how they make you feel and what they mean to your sense of self.",
            "Career concerns weigh heavily because work shapes so much of our daily experience and identity.",
            "The workplace affects our whole wellbeing - when it's not going well, everything else can feel harder.",
        ]
    elif 'relationship' in analysis['topics']:
        validations = [
            "Relationship pain cuts the deepest because these are the people whose opinions of us matter most.",
            "When someone we care about is involved, our emotions naturally run higher - that's how we're wired.",
            "The people closest to us have the power to both heal and hurt us deeply.",
        ]
    elif 'self-worth' in analysis['topics']:
        validations = [
            "That inner critic voice can be brutal - often saying things to ourselves we'd never say to a friend.",
            "These self-critical thoughts feel true in the moment, but they're not facts - they're painful stories our mind is telling.",
            "Self-worth struggles are so common, yet they feel so isolating. You're not alone in this.",
        ]
    elif 'social' in analysis['topics']:
        validations = [
            "Humans are wired for connection - feeling lonely isn't weakness, it's your brain signaling an important unmet need.",
            "Social isolation affects everything - our mood, our thoughts, even our physical health. This matters.",
            "The ache of loneliness is real and it's valid. We literally need each other to thrive.",
        ]
    elif 'family' in analysis['topics']:
        validations = [
            "Family relationships are complicated - they hold our deepest bonds and sometimes our deepest wounds.",
            "What happens in our family shapes us profoundly. It makes sense this would affect you so strongly.",
            "Family dynamics can be the source of both our greatest support and our hardest challenges.",
        ]
    else:
        # Emotion-based validation (more nuanced)
        emotion_validations = {
            'fear': [
                "Fear is your mind trying to protect you - even when it overreacts, it comes from a place of self-preservation.",
                "Feeling afraid when facing uncertainty is deeply human. Your fear is information, not a character flaw.",
                "What you're afraid of matters to you - that's why it generates such a strong response.",
            ],
            'guilt': [
                "Guilt means you care about your impact on others - that's actually a mark of empathy and conscience.",
                "Sometimes guilt is useful feedback, sometimes it's our mind being too harsh. Let's figure out which this is.",
                "Carrying guilt shows you take responsibility seriously. The question is whether this guilt is proportional.",
            ],
            'shame': [
                "Shame attacks who we are, not just what we did. That's why it hurts so much more than regular guilt.",
                "The fact you're talking about shame with me is already courageous - shame wants you to hide, but you're not.",
                "Shame makes us feel fundamentally flawed. But feelings aren't facts - you're human, not broken.",
            ],
            'anxiety': [
                "Anxiety is exhausting - it's like your mind won't give you a moment's peace.",
                "That worried feeling is your brain trying to protect you, even when there's no immediate threat.",
                "The 'what-ifs' feel so real when anxiety is high, but they're predictions, not certainties.",
            ],
            'sadness': [
                "That heavy, empty feeling of sadness is one of the hardest emotions to sit with.",
                "When sadness settles in, it can color everything - making even small things feel overwhelming.",
                "Sadness is trying to tell you something matters to you. The pain means you care.",
            ],
            'anger': [
                "Anger often means a boundary was crossed or a value was violated. It's information worth listening to.",
                "That hot surge of anger is your system saying 'this isn't okay' - let's understand what triggered it.",
                "Anger can be protective and clarifying when we listen to it without letting it control us.",
            ]
        }
        validations = emotion_validations.get(emotion, [
            "The intensity of what you're feeling makes sense given what you're going through.",
            "Your emotional response is valid - feelings don't need to be justified, they just are.",
            "There's wisdom in emotions if we can listen to them without being overwhelmed by them.",
        ])
    
    return random.choice(validations)


def check_ai_available_old():
    """Check if AI service is configured"""
    return USE_AI
