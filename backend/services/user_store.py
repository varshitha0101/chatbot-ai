import bcrypt

users = {}

def register_user(user_id, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[user_id] = hashed

def verify_user(user_id, password):
    if user_id not in users:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), users[user_id])