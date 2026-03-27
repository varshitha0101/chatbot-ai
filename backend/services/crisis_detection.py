high_risk_keywords = [
    "suicide", "suicidal", "kill myself", "end my life", "want to die",
    "self harm", "cutting myself", "hurt myself", "can't go on",
    "no reason to live", "better off dead", "end it all",
    "no point living", "give up", "overdose", "jump off",
    "hang myself", "not worth living", "everyone would be better without me",
    "plan to die", "nothing to live for", "living is pointless"
]

# Moderate risk indicators
moderate_risk_keywords = [
    "hopeless", "can't take it anymore", "worthless", "burden",
    "meaningless", "no hope", "giving up", "can't do this",
    "too much pain", "can't cope", "breaking down"
]

def check_crisis(message):
    """
    Enhanced crisis detection with severity levels
    Returns: 'high', 'moderate', or None
    """
    message = message.lower()

    # Check for high-risk keywords first
    for keyword in high_risk_keywords:
        if keyword in message:
            return 'high'
    
    # Check for moderate risk
    moderate_count = 0
    for keyword in moderate_risk_keywords:
        if keyword in message:
            moderate_count += 1
    
    # If multiple moderate indicators, escalate to moderate crisis
    if moderate_count >= 2:
        return 'moderate'
    
    return None