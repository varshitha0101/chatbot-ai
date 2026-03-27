from flask import Flask, request, jsonify
from flask_cors import CORS

from services.crisis_detection import check_crisis
from services.emotion_detection import detect_emotion as detect_emotion_transformer
from services.distortion_detection import detect_distortion
from services.cbt_engine import generate_cbt_response
from services.session_memory import update_session, detect_repeated_emotion

from services.database import (
    init_db,
    save_conversation,
    get_user_conversations,
    get_user_emotion_stats,
    get_user_daily_trend,
    get_user_distortion_stats,
    get_emotion_distortion_correlation,
    get_dominant_distortion
)

from services.auth import generate_token, token_required
from services.user_store import register_user, verify_user
from services.cbt_engine import is_ai_enabled


app = Flask(__name__)
CORS(app)

init_db()


# ============================
# HOME
# ============================

@app.route("/", methods=["GET"])
def home():
    ai_status = "enabled" if is_ai_enabled() else "disabled (using templates)"
    return jsonify({
        "message": "CBT Chatbot API is running",
        "ai_powered": is_ai_enabled(),
        "ai_status": ai_status
    })


# ============================
# AUTH ROUTES
# ============================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "user_id" not in data or "password" not in data:
        return jsonify({"error": "user_id and password required"}), 400

    register_user(data["user_id"], data["password"])
    return jsonify({"message": "User registered successfully"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "user_id" not in data or "password" not in data:
        return jsonify({"error": "user_id and password required"}), 400

    if not verify_user(data["user_id"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(data["user_id"])
    return jsonify({"token": token})


# ============================
# CHAT ROUTE
# ============================

@app.route("/chat", methods=["POST"])
@token_required
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "message required"}), 400

    user_id = request.user_id
    user_message = data["message"]

    # 1️⃣ Enhanced Crisis Detection with severity levels
    crisis_level = check_crisis(user_message)
    if crisis_level == 'high':
        return jsonify({
            "response": "I'm really concerned about what you just shared. What you're feeling is important, but I want to make sure you're safe. Please reach out to a crisis helpline immediately - they have trained professionals available 24/7. In the US: 988 (Suicide & Crisis Lifeline), or text 'HELLO' to 741741 (Crisis Text Line). You can also go to your nearest emergency room. You don't have to go through this alone.",
            "crisis": "high"
        })
    elif crisis_level == 'moderate':
        # Continue with response but add warning
        crisis_warning = "I'm sensing you're really struggling right now. While I'm here to support you, please consider reaching out to a mental health professional or crisis line if these feelings intensify. "
    else:
        crisis_warning = ""

    # 2️⃣ Emotion Detection
    emotion, intensity, confidence = detect_emotion_transformer(user_message)

    # 3️⃣ Distortion Detection
    distortion = detect_distortion(user_message)

    # 4️⃣ Confidence Gating + Distortion-Based Inference
    if confidence < 0.5:
        if distortion == "overgeneralization":
            emotion = "sadness"
        elif distortion == "catastrophizing":
            emotion = "anxiety"
        elif distortion == "mind_reading":
            emotion = "anxiety"
        elif distortion == "all_or_nothing":
            emotion = "sadness"
        else:
            emotion = "uncertain"

    # 5️⃣ Save Conversation
    save_conversation(user_id, user_message, emotion, intensity, distortion)

    # 6️⃣ Session Memory
    update_session(emotion)
    repeated = detect_repeated_emotion(emotion)

    # 7️⃣ Dominant Distortion
    dominant_distortion = get_dominant_distortion(user_id)

    # 8️⃣ Generate AI-Powered CBT Response
    cbt_response = generate_cbt_response(
        user_message=user_message,
        emotion=emotion,
        intensity=intensity,
        distortion=distortion,
        user_id=user_id
    )
    # Add crisis warning if moderate risk
    if crisis_level == 'moderate':
        cbt_response = crisis_warning + cbt_response
    if repeated:
        cbt_response += " I notice this feeling has appeared multiple times. It may help to explore the core belief behind it."

    if dominant_distortion and dominant_distortion == distortion:
        cbt_response += " I notice this thinking pattern appears frequently. Let’s focus deeply on challenging this pattern."

    return jsonify({
        "user_id": user_id,
        "emotion": emotion,
        "intensity": intensity,
        "confidence": confidence,
        "distortion": distortion,
        "dominant_distortion": dominant_distortion,
        "response": cbt_response
    })


@app.route("/activity-chat", methods=["POST"])
@token_required
def activity_chat():
    """Handle activity-specific chat conversations"""
    from services.activity_spaces import generate_activity_response
    
    data = request.get_json()

    if not data or "message" not in data or "activity_type" not in data:
        return jsonify({"error": "message and activity_type required"}), 400

    user_id = request.user_id
    user_message = data["message"]
    activity_type = data["activity_type"]

    # Quick emotion detection for context
    emotion, intensity, _ = detect_emotion_transformer(user_message)

    # Generate activity-specific response
    response = generate_activity_response(activity_type, user_message, emotion, intensity)

    # Save to conversation history with activity tag
    save_conversation(user_id, f"[{activity_type}] {user_message}", emotion, intensity, "none")

    return jsonify({
        "user_id": user_id,
        "activity_type": activity_type,
        "emotion": emotion,
        "intensity": intensity,
        "response": response
    })


# ============================
# ANALYTICS ROUTES
# ============================

@app.route("/history", methods=["GET"])
@token_required
def history():
    return jsonify(get_user_conversations(request.user_id))


@app.route("/analytics", methods=["GET"])
@token_required
def analytics():
    return jsonify(get_user_emotion_stats(request.user_id))


@app.route("/trend", methods=["GET"])
@token_required
def trend():
    return jsonify(get_user_daily_trend(request.user_id))


@app.route("/distortion_analytics", methods=["GET"])
@token_required
def distortion_analytics():
    return jsonify(get_user_distortion_stats(request.user_id))


@app.route("/emotion_distortion_correlation", methods=["GET"])
@token_required
def emotion_distortion_correlation():
    return jsonify(get_emotion_distortion_correlation(request.user_id))


# ============================
# RUN
# ============================

if __name__ == "__main__":
    app.run(debug=True)