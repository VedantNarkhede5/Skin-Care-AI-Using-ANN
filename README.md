# 🌿 Skin Care AI App

An AI-powered skincare web app built with **Python (Flask)**, **MongoDB**, and **ANN (Artificial Neural Network)**.
Users sign up, describe their face, and get a personalised skincare routine, food tips, and product suggestions.

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | HTML, CSS                         |
| Backend    | Python, Flask                     |
| Database   | MongoDB Atlas (cloud) + Compass   |
| AI Model   | ANN — scikit-learn MLPClassifier  |

---

## 📁 Project Structure

```
skincare_ai/
│
├── app.py              ← Flask server — all routes
├── ann_model.py        ← ANN model (train + predict)
├── database.py         ← MongoDB — users + assessments
├── face_logic.py       ← Routine, food, product logic
├── requirements.txt    ← Python packages
│
├── templates/
│   ├── index.html      ← Home page
│   ├── login.html      ← Login page
│   ├── signup.html     ← Sign up page
│   ├── face.html       ← Face assessment form
│   ├── face_result.html← Result — routine + food + products
│   └── history.html    ← User's personal history
│
└── static/
    └── style.css       ← All styling
```

---

## 🚀 How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Set your MongoDB Atlas URI in `database.py`
```python
# Replace this line in database.py:
client = MongoClient("your-mongodb-atlas-uri-here")

# Example:
client = MongoClient("mongodb+srv://admin:password@cluster0.abc123.mongodb.net/")
```

### Step 3 — Run the app
```bash
python app.py
```

### Step 4 — Open in browser
```
http://127.0.0.1:5000
```

---

## 🔁 How the App Works (Flow)

```
User visits app
      ↓
Sign Up → saved to MongoDB (users collection)
      ↓
Login → Flask session stores user_email
      ↓
Fill Face Assessment Form (12 inputs)
      ↓
7 inputs encoded as numbers → fed into ANN
      ↓
ANN predicts skin label (0 to 7)
      ↓
face_logic.py maps label → routine + food + products
      ↓
Result saved to MongoDB (linked to user_email)
      ↓
face_result.html shows full personalised report
      ↓
History page shows only THIS user's past reports
```

---

## 🤖 ANN Model Details

| Property        | Value                              |
|-----------------|------------------------------------|
| Library         | scikit-learn MLPClassifier         |
| Architecture    | Input(7) → Hidden(16) → Hidden(8) → Output(8) |
| Activation      | ReLU                               |
| Training Samples| 72 samples                         |
| Accuracy        | ~80%                               |
| Output Classes  | 8 skin categories                  |

### Input Features (7 total)
| Feature      | Options                                      |
|--------------|----------------------------------------------|
| skin_type    | oily, dry, combination, normal, sensitive    |
| age_group    | teen, 20s, 30s, 40s, 50+                    |
| sensitivity  | low, medium, high                            |
| acne_level   | none, mild, moderate, severe                 |
| dryness      | none, mild, moderate, severe                 |
| oiliness     | none, mild, moderate, severe                 |
| sun_exposure | low, medium, high                            |

### Output Labels (8 categories)
| Label | Category         | Recommendation Focus              |
|-------|------------------|-----------------------------------|
| 0     | Oily             | Foaming cleanser + salicylic acid |
| 1     | Dry              | Hydrating cleanser + hyaluronic   |
| 2     | Combination      | Balanced cleanser + niacinamide   |
| 3     | Normal           | Mild cleanser + vitamin C         |
| 4     | Sensitive        | Fragrance-free + ceramide         |
| 5     | Severe Acne      | Benzoyl peroxide + adapalene      |
| 6     | Aging (40s+)     | Retinol + collagen moisturizer    |
| 7     | High Sun Exposure| SPF 50+ + antioxidant serum       |

---

## 💾 MongoDB Structure

**Database name:** `skincare_ai`

### Collection 1 — `users`
Stores all user accounts.
```json
{
  "name":     "Vedant Narkhede",
  "email":    "vedant@email.com",
  "password": "hashed_password_here",
  "joined":   "2024-01-15"
}
```

### Collection 2 — `assessments`
Stores every skin assessment — linked to the user who did it.
```json
{
  "user_email":     "vedant@email.com",
  "name":           "vedant narkhede",
  "inputs": {
    "Face Shape":   "Oval",
    "Skin Tone":    "Medium",
    "Dark Circles": "Yes",
    "Skin Type":    "Oily",
    "Acne Level":   "Mild"
  },
  "recommendation": "Use a foaming cleanser + oil-free moisturizer",
  "confidence":     91.5,
  "label":          0,
  "date":           "2024-01-15 10:30:00"
}
```

> ✅ History is private — each user only sees their own assessments.
> MongoDB query used: `assessments.find({"user_email": logged_in_user_email})`

---

## 🔐 Login & Signup System

| Feature        | How it works                                              |
|----------------|-----------------------------------------------------------|
| Signup         | Name + email + password saved to MongoDB `users` collection |
| Password       | Hashed using `werkzeug generate_password_hash` — never stored as plain text |
| Login          | `check_password_hash` verifies password                   |
| Session        | Flask `session["user_email"]` keeps user logged in        |
| Logout         | `session.clear()` removes login state                     |
| Route Guard    | `/face`, `/history` redirect to login if not logged in    |
| Private History| MongoDB filters by `user_email` — users cannot see others' data |

---

## 📦 Requirements

```
flask
pymongo
scikit-learn
numpy
werkzeug
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🎯 Interview Q&A

**Q: What is ANN and which one did you use?**
A: ANN stands for Artificial Neural Network. I used MLPClassifier (Multi-Layer Perceptron) from scikit-learn — it has an input layer, 2 hidden layers (16 and 8 neurons), and an output layer with 8 classes.

**Q: How does the model predict?**
A: User inputs are encoded as integers, scaled using StandardScaler, then passed to the trained MLP. It outputs a class label (0–7) and confidence score using `predict_proba`.

**Q: Why MongoDB and not SQL?**
A: MongoDB stores flexible JSON-like documents — no fixed schema needed. Each user's skin profile can have different fields and it's easy to link assessments to users using `user_email`.

**Q: How is user history kept private?**
A: Every assessment is saved with the logged-in user's email. The history query always filters by `{"user_email": session["user_email"]}` so users only ever see their own data.

**Q: How are passwords stored?**
A: Passwords are never stored as plain text. We use `werkzeug.security.generate_password_hash` to hash them before saving, and `check_password_hash` to verify at login.

**Q: What happens if someone visits /history without logging in?**
A: The `is_logged_in()` function checks if `user_email` exists in Flask session. If not, the user is redirected to the login page with a flash message.

**Q: What is face_logic.py?**
A: It's a simple Python file with dictionaries that map the ANN output label to three things — a morning/night skincare routine, food to eat/avoid, and 3 product suggestions with image and price. No complex ML — just clean, readable Python logic.

---

## 📌 Notes

- No buy button on products — suggestions only
- No image upload — user describes face via form
- Passwords are always hashed — never plain text
- App tested with ANN accuracy of **80%**
