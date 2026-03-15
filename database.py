# database.py
# MongoDB operations — users + assessments

from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ── Connect ──────────────────────────────────────────────────
# Replace this with your MongoDB Atlas URI if using cloud

#clint you mongodb line
#db  your database name

users       = db["users"]        # stores user accounts
assessments = db["assessments"]  # stores face assessments

# ── User: Signup ─────────────────────────────────────────────
def signup_user(name, email, password):
    """Returns True if signup success, False if email already exists."""
    if users.find_one({"email": email}):
        return False  # email already taken
    users.insert_one({
        "name":     name,
        "email":    email,
        "password": generate_password_hash(password),  # never store plain password
        "joined":   datetime.now().strftime("%Y-%m-%d"),
    })
    return True

# ── User: Login ──────────────────────────────────────────────
def login_user(email, password):
    """Returns user dict if login success, None if failed."""
    user = users.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        return user  # valid login
    return None

# ── User: Get by email ───────────────────────────────────────
def get_user(email):
    return users.find_one({"email": email}, {"_id": 0, "password": 0})

# ── Assessment: Save ─────────────────────────────────────────
def save_assessment(user_email, name, face_info, result):
    """Save assessment linked to logged-in user's email."""
    assessments.insert_one({
        "user_email":     user_email,         # links to logged-in user
        "name":           name,
        "inputs":         face_info,
        "recommendation": result["recommendation"],
        "confidence":     result["confidence"],
        "label":          result["label"],
        "date":           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

# ── Assessment: Get only this user's history ─────────────────
def get_my_assessments(user_email):
    """Only returns assessments belonging to this user — not others."""
    records = list(assessments.find(
        {"user_email": user_email},   # filter by logged-in user
        {"_id": 0}
    ))
    return records
