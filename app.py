# app.py
# Flask backend with login, signup, session, and protected routes

from flask import Flask, render_template, request, redirect, url_for, session, flash
from ann_model import predict, accuracy
from database import signup_user, login_user, get_user, save_assessment, get_my_assessments
from face_logic import get_face_recommendations

app = Flask(__name__)
app.secret_key = "skincare_secret_key_2024"   # needed for session (login state)

# ── Encode map for ANN ───────────────────────────────────────
ENCODE = {
    "skin_type":    {"oily": 0, "dry": 1, "combination": 2, "normal": 3, "sensitive": 4},
    "age_group":    {"teen": 0, "20s": 1, "30s": 2, "40s": 3, "50+": 4},
    "sensitivity":  {"low": 0, "medium": 1, "high": 2},
    "acne_level":   {"none": 0, "mild": 1, "moderate": 2, "severe": 3},
    "dryness":      {"none": 0, "mild": 1, "moderate": 2, "severe": 3},
    "oiliness":     {"none": 0, "mild": 1, "moderate": 2, "severe": 3},
    "sun_exposure": {"low": 0, "medium": 1, "high": 2},
}

# ── Helper: check if logged in ───────────────────────────────
def is_logged_in():
    return "user_email" in session

# ── Home ─────────────────────────────────────────────────────
@app.route("/")
def index():
    user = get_user(session["user_email"]) if is_logged_in() else None
    return render_template("index.html", accuracy=accuracy, user=user)

# ── Signup ───────────────────────────────────────────────────
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if is_logged_in():
        return redirect(url_for("index"))

    if request.method == "POST":
        name     = request.form.get("name").strip()
        email    = request.form.get("email").strip()
        password = request.form.get("password").strip()

        success = signup_user(name, email, password)
        if success:
            session["user_email"] = email   # auto login after signup
            session["user_name"]  = name
            flash("Account created! Welcome 🎉", "success")
            return redirect(url_for("index"))
        else:
            flash("Email already registered. Please login.", "error")

    return render_template("signup.html")

# ── Login ────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for("index"))

    if request.method == "POST":
        email    = request.form.get("email").strip()
        password = request.form.get("password").strip()

        user = login_user(email, password)
        if user:
            session["user_email"] = email
            session["user_name"]  = user["name"]
            flash(f"Welcome back, {user['name']}! 👋", "success")
            return redirect(url_for("index"))
        else:
            flash("Wrong email or password.", "error")

    return render_template("login.html")

# ── Logout ───────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))

# ── Face Assessment Form (login required) ────────────────────
@app.route("/face")
def face():
    if not is_logged_in():
        flash("Please login first.", "error")
        return redirect(url_for("login"))
    return render_template("face.html", user_name=session.get("user_name"))

# ── Face Result (login required) ─────────────────────────────
@app.route("/face-result", methods=["POST"])
def face_result():
    if not is_logged_in():
        return redirect(url_for("login"))

    data = request.form

    skin_type    = data.get("skin_type")
    age_group    = data.get("age_group")
    sensitivity  = data.get("sensitivity")
    acne_level   = data.get("acne_level")
    dryness      = data.get("dryness")
    oiliness     = data.get("oiliness")
    sun_exposure = data.get("sun_exposure")
    face_shape   = data.get("face_shape")
    skin_tone    = data.get("skin_tone")
    dark_circles = data.get("dark_circles")
    pigmentation = data.get("pigmentation")
    wrinkles     = data.get("wrinkles")

    # ANN input encoding
    features = [
        ENCODE["skin_type"][skin_type],
        ENCODE["age_group"][age_group],
        ENCODE["sensitivity"][sensitivity],
        ENCODE["acne_level"][acne_level],
        ENCODE["dryness"][dryness],
        ENCODE["oiliness"][oiliness],
        ENCODE["sun_exposure"][sun_exposure],
    ]

    result = predict(features)
    label  = result["label"]
    recs   = get_face_recommendations(label, skin_type, acne_level, age_group, sun_exposure)

    face_info = {
        "Face Shape":   face_shape.capitalize(),
        "Skin Tone":    skin_tone.capitalize(),
        "Dark Circles": dark_circles.capitalize(),
        "Pigmentation": pigmentation.capitalize(),
        "Wrinkles":     wrinkles.capitalize(),
        "Skin Type":    skin_type.capitalize(),
        "Age Group":    age_group,
        "Acne Level":   acne_level.capitalize(),
        "Sun Exposure": sun_exposure.capitalize(),
    }

    # Save linked to logged-in user's email
    save_assessment(session["user_email"], session["user_name"], face_info, result)

    return render_template("face_result.html",
        name       = session["user_name"],
        face_info  = face_info,
        ann_result = result["recommendation"],
        confidence = result["confidence"],
        routine    = recs["routine"],
        food       = recs["food"],
        products   = recs["products"],
    )

# ── History (only this user's records) ───────────────────────
@app.route("/history")
def history():
    if not is_logged_in():
        flash("Please login to view your history.", "error")
        return redirect(url_for("login"))

    # Only fetch records for the logged-in user
    records = get_my_assessments(session["user_email"])
    return render_template("history.html",
        records    = records,
        user_name  = session["user_name"],
    )

if __name__ == "__main__":
    print("=" * 40)
    print("  Skin Care AI — Running!")
    print(f"  ANN Accuracy: {accuracy}%")
    print("  http://127.0.0.1:5000")
    print("=" * 40)
    app.run(debug=True)