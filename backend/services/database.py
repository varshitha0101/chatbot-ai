import sqlite3

DB_NAME = "chatbot.db"


# --------------------------
# Initialize Database
# --------------------------

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        message TEXT NOT NULL,
        emotion TEXT,
        intensity TEXT,
        distortion TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# --------------------------
# Save Conversation
# --------------------------

def save_conversation(user_id, message, emotion, intensity, distortion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO conversations (user_id, message, emotion, intensity, distortion)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, message, emotion, intensity, distortion))

    conn.commit()
    conn.close()


# --------------------------
# Conversation History
# --------------------------

def get_user_conversations(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT message, emotion, intensity, distortion, timestamp
    FROM conversations
    WHERE user_id = ?
    ORDER BY timestamp DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "message": row[0],
            "emotion": row[1],
            "intensity": row[2],
            "distortion": row[3],
            "timestamp": row[4]
        }
        for row in rows
    ]


# --------------------------
# Emotion Analytics
# --------------------------

def get_user_emotion_stats(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT emotion, COUNT(*)
    FROM conversations
    WHERE user_id = ?
    GROUP BY emotion
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    distribution = {row[0]: row[1] for row in rows}

    return {
        "total_messages": sum(distribution.values()),
        "emotion_distribution": distribution
    }


# --------------------------
# Daily Trend
# --------------------------

def get_user_daily_trend(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DATE(timestamp), emotion, COUNT(*)
    FROM conversations
    WHERE user_id = ?
    GROUP BY DATE(timestamp), emotion
    ORDER BY DATE(timestamp) DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    trend = {}

    for date, emotion, count in rows:
        if date not in trend:
            trend[date] = {}
        trend[date][emotion] = count

    return trend


# --------------------------
# Distortion Analytics
# --------------------------

def get_user_distortion_stats(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT distortion, COUNT(*)
    FROM conversations
    WHERE user_id = ?
      AND distortion IS NOT NULL
    GROUP BY distortion
    ORDER BY COUNT(*) DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return {row[0]: row[1] for row in rows}


# --------------------------
# Emotion–Distortion Correlation
# --------------------------

def get_emotion_distortion_correlation(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT emotion, distortion, COUNT(*)
    FROM conversations
    WHERE user_id = ?
      AND distortion IS NOT NULL
    GROUP BY emotion, distortion
    ORDER BY emotion
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    correlation = {}

    for emotion, distortion, count in rows:
        if emotion not in correlation:
            correlation[emotion] = {}
        correlation[emotion][distortion] = count

    return correlation


# --------------------------
# Dominant Distortion
# --------------------------

def get_dominant_distortion(user_id):
    stats = get_user_distortion_stats(user_id)
    if not stats:
        return None
    return max(stats, key=stats.get)