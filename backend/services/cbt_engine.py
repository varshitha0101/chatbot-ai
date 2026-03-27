"""
CBT Response Engine - Now AI-Powered!
Uses AI therapist for natural, empathetic responses
"""
from services.ai_therapist import generate_ai_response, check_ai_available


def generate_cbt_response(user_message, emotion, intensity, distortion=None, user_id=None):
    """
    Generate therapeutic response using AI
    Falls back to templates if AI unavailable
    """
    return generate_ai_response(
        user_message=user_message,
        emotion=emotion,
        intensity=intensity,
        distortion=distortion,
        user_id=user_id
    )


def is_ai_enabled():
    """Check if AI responses are available"""
    return check_ai_available()


# Legacy template-based function (kept for reference)
def generate_template_response(emotion, intensity, distortion=None):
    """
    Original template-based responses
    Now only used as fallback
    """
    base_responses = {
        "anxiety": "It sounds like you're feeling anxious. Let's slow down and examine the thought carefully.",
        "sadness": "It seems you're feeling sad. Let's gently explore what might be contributing to this.",
        "positive": "I'm glad you're feeling positive. What do you think helped create this feeling?",
        "anger": "It sounds like you're feeling angry. Let's pause and examine what triggered this reaction.",
        "uncertain": "Thank you for sharing. Can you describe what happened and how it made you feel?"
    }

    distortion_strategies = {
        "catastrophizing": "Ask yourself: What is the most realistic outcome, not the worst-case scenario?",
        "overgeneralization": "Is this truly 'always' happening, or are there exceptions?",
        "mind_reading": "What actual evidence do you have about what others are thinking?",
        "all_or_nothing": "Is there a middle ground between complete success and total failure?"
    }

    response = base_responses.get(emotion, base_responses["uncertain"])

    if intensity == "high":
        response += " Take a slow breath first — inhale for 4 seconds, hold for 4, exhale for 6."

    if distortion and distortion in distortion_strategies:
        response += " " + distortion_strategies[distortion]

    return response
