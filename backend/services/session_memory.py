# Advanced session tracking with topic monitoring and pattern detection

session_data = {
    "message_count": 0,
    "emotion_history": [],
    "topics_discussed": set(),  # Track recurring themes
    "distortion_patterns": {},  # Count distortion types
    "session_start_time": None,
    "crisis_alerts": 0
}

# Store conversation history per user (in-memory)
# In production, this should be stored in database
conversation_store = {}

# Store session insights per user
session_insights = {}


def update_session(emotion, topics=None, distortion=None):
    """Enhanced session tracking with topics and distortions"""
    session_data["message_count"] += 1
    session_data["emotion_history"].append(emotion)
    
    # Track topics
    if topics:
        if isinstance(topics, list):
            session_data["topics_discussed"].update(topics)
        else:
            session_data["topics_discussed"].add(topics)
    
    # Track distortion patterns
    if distortion:
        if distortion not in session_data["distortion_patterns"]:
            session_data["distortion_patterns"][distortion] = 0
        session_data["distortion_patterns"][distortion] += 1


def get_session_summary():
    return {
        **session_data,
        "topics_discussed": list(session_data["topics_discussed"])
    }


def detect_repeated_emotion(current_emotion):
    history = session_data["emotion_history"]

    if len(history) >= 3:
        last_three = history[-3:]
        if all(e == current_emotion for e in last_three):
            return True

    return False


def reset_session():
    session_data["message_count"] = 0
    session_data["emotion_history"] = []
    session_data["topics_discussed"] = set()
    session_data["distortion_patterns"] = {}
    session_data["crisis_alerts"] = 0


# ── Conversation History Management ──

def add_to_conversation(user_id, user_message, assistant_response, metadata=None):
    """Store a conversation turn with metadata for context"""
    if user_id not in conversation_store:
        conversation_store[user_id] = []
    
    turn = {
        "user": user_message,
        "assistant": assistant_response,
        "timestamp": None  # Could add datetime
    }
    
    if metadata:
        turn["metadata"] = metadata  # Store emotion, topics, distortions
    
    conversation_store[user_id].append(turn)
    
    # Keep only last 30 turns for better context
    if len(conversation_store[user_id]) > 30:
        conversation_store[user_id] = conversation_store[user_id][-30:]


def get_conversation_history(user_id, last_n=10):
    """Get recent conversation history for a user"""
    history = conversation_store.get(user_id, [])
    if last_n:
        return history[-last_n:]
    return history


def get_session_themes(user_id):
    """Analyze conversation to identify recurring themes"""
    history = conversation_store.get(user_id, [])
    if not history:
        return []
    
    themes = {
        'work_stress': 0,
        'relationship_issues': 0,
        'self_worth': 0,
        'anxiety_patterns': 0,
        'depression_symptoms': 0
    }
    
    for turn in history:
        msg = turn["user"].lower()
        if any(w in msg for w in ['work', 'job', 'boss', 'career']):
            themes['work_stress'] += 1
        if any(w in msg for w in ['relationship', 'partner', 'friend', 'family']):
            themes['relationship_issues'] += 1
        if any(w in msg for w in ['worthless', 'failure', 'not good enough', 'hate myself']):
            themes['self_worth'] += 1
        if turn.get("metadata", {}).get("emotion") == "anxiety":
            themes['anxiety_patterns'] += 1
        if turn.get("metadata", {}).get("emotion") == "sadness":
            themes['depression_symptoms'] += 1
    
    # Return themes that appear 2+ times
    return [theme for theme, count in themes.items() if count >= 2]


def get_conversation_insights(user_id):
    """Generate insights about the conversation patterns"""
    history = get_conversation_history(user_id, last_n=None)
    if len(history) < 3:
        return None
    
    insights = {
        'total_turns': len(history),
        'primary_emotions': {},
        'recurring_topics': get_session_themes(user_id),
        'needs_follow_up': False
    }
    
    # Analyze emotions
    for turn in history:
        emotion = turn.get("metadata", {}).get("emotion")
        if emotion:
            insights['primary_emotions'][emotion] = insights['primary_emotions'].get(emotion, 0) + 1
    
    # Check if follow-up needed (repeated negative emotions)
    negative_count = sum(insights['primary_emotions'].get(e, 0) for e in ['sadness', 'anger', 'fear', 'guilt', 'shame', 'anxiety'])
    if negative_count >= len(history) * 0.7:  # 70% negative
        insights['needs_follow_up'] = True
    
    return insights


def should_reflect(user_id):
    """Determine if it's time to offer reflection/summary"""
    history = get_conversation_history(user_id, last_n=None)
    message_count = len(history)
    
    # Offer reflection every 8-10 messages
    if message_count > 0 and message_count % 8 == 0:
        return True
    return False


def clear_conversation_history(user_id):
    """Clear conversation history for a user"""
    if user_id in conversation_store:
        conversation_store[user_id] = []
