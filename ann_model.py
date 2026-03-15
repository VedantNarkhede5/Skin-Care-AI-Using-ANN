# ann_model.py
# Simple ANN using scikit-learn MLPClassifier
# Predicts skin care recommendation based on user inputs

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ── Recommendation Labels ────────────────────────────────────
RECOMMENDATIONS = [
    "Use a foaming cleanser + oil-free moisturizer + salicylic acid serum",        # 0 - Oily
    "Use a hydrating cream cleanser + rich moisturizer + hyaluronic acid serum",   # 1 - Dry
    "Use a balanced cleanser + lightweight moisturizer + niacinamide serum",       # 2 - Combination
    "Use a mild cleanser + SPF moisturizer + vitamin C serum",                     # 3 - Normal
    "Use a fragrance-free cleanser + ceramide moisturizer + calming serum",        # 4 - Sensitive
    "Use a deep cleansing wash + clay mask weekly + benzoyl peroxide treatment",   # 5 - Severe Acne
    "Use a gentle exfoliating cleanser + retinol serum + night cream",             # 6 - Aging (40s+)
    "Use micellar water + SPF50 sunscreen + antioxidant serum",                    # 7 - High Sun Exposure
]

# ── Feature Encoding Guide ───────────────────────────────────
# [skin_type, age_group, sensitivity, acne_level, dryness, oiliness, sun_exposure]
# skin_type:    oily=0, dry=1, combination=2, normal=3, sensitive=4
# age_group:    teen=0, 20s=1, 30s=2, 40s=3, 50+=4
# sensitivity:  low=0, medium=1, high=2
# acne_level:   none=0, mild=1, moderate=2, severe=3
# dryness:      none=0, mild=1, moderate=2, severe=3
# oiliness:     none=0, mild=1, moderate=2, severe=3
# sun_exposure: low=0, medium=1, high=2

# ── Training Data ────────────────────────────────────────────
X = np.array([
    # Oily skin → label 0
    [0, 0, 0, 1, 0, 2, 1],  [0, 1, 0, 1, 0, 2, 1],  [0, 2, 0, 2, 0, 3, 2],
    [0, 2, 0, 1, 0, 2, 0],  [0, 1, 1, 1, 0, 2, 1],  [0, 0, 0, 2, 0, 2, 1],
    [0, 3, 0, 1, 0, 2, 1],  [0, 1, 0, 0, 0, 3, 0],  [0, 2, 1, 0, 0, 3, 1],
    # Severe acne → label 5
    [0, 1, 1, 3, 0, 3, 1],  [0, 0, 0, 3, 0, 3, 0],  [0, 2, 1, 3, 0, 3, 1],
    [2, 1, 0, 3, 1, 2, 1],  [0, 3, 0, 3, 0, 3, 1],  [0, 1, 0, 3, 0, 3, 0],
    [2, 2, 1, 3, 0, 2, 1],  [0, 0, 1, 3, 0, 2, 0],  [3, 1, 0, 3, 0, 1, 1],
    # Dry skin → label 1
    [1, 1, 1, 0, 2, 0, 0],  [1, 2, 1, 0, 3, 0, 1],  [1, 3, 2, 0, 3, 0, 1],
    [1, 0, 1, 0, 2, 0, 0],  [1, 1, 0, 0, 3, 0, 1],  [1, 2, 0, 0, 2, 0, 0],
    [1, 0, 0, 0, 3, 0, 0],  [1, 3, 1, 0, 2, 0, 1],  [1, 1, 2, 0, 3, 0, 0],
    # Combination skin → label 2
    [2, 1, 1, 1, 1, 1, 1],  [2, 2, 1, 1, 1, 2, 1],  [2, 0, 0, 1, 1, 1, 0],
    [2, 3, 1, 0, 1, 1, 2],  [2, 1, 0, 0, 1, 2, 1],  [2, 2, 0, 1, 2, 1, 1],
    [2, 0, 1, 0, 1, 1, 0],  [2, 3, 1, 1, 1, 1, 1],  [2, 1, 0, 0, 2, 1, 0],
    # Normal skin → label 3
    [3, 1, 0, 0, 0, 0, 1],  [3, 2, 0, 0, 0, 0, 1],  [3, 0, 0, 0, 0, 0, 0],
    [3, 1, 0, 1, 0, 1, 1],  [3, 2, 0, 0, 0, 1, 1],  [3, 0, 0, 1, 0, 0, 0],
    [3, 2, 1, 0, 0, 0, 0],  [3, 1, 0, 0, 1, 0, 1],  [3, 0, 0, 0, 0, 1, 1],
    # Sensitive skin → label 4
    [4, 1, 2, 0, 1, 0, 0],  [4, 2, 2, 0, 2, 0, 0],  [4, 0, 2, 1, 1, 0, 0],
    [4, 3, 2, 0, 2, 0, 1],  [1, 3, 2, 0, 3, 0, 0],  [4, 1, 2, 1, 2, 0, 0],
    [4, 2, 2, 1, 1, 0, 0],  [4, 0, 2, 0, 2, 0, 0],  [1, 2, 2, 0, 3, 0, 0],
    # Aging / 40s+ → label 6
    [1, 4, 1, 0, 3, 0, 1],  [3, 4, 0, 0, 1, 0, 1],  [2, 4, 1, 0, 1, 1, 1],
    [0, 4, 0, 1, 0, 2, 1],  [1, 3, 1, 0, 3, 0, 0],  [3, 3, 0, 0, 1, 0, 1],
    [2, 3, 0, 0, 2, 1, 0],  [4, 4, 1, 0, 2, 0, 0],  [1, 4, 2, 0, 3, 0, 0],
    # High sun exposure → label 7
    [3, 3, 0, 0, 0, 0, 2],  [3, 3, 1, 0, 1, 1, 2],  [0, 3, 0, 0, 0, 2, 2],
    [1, 3, 1, 0, 2, 0, 2],  [3, 4, 1, 0, 1, 0, 2],  [0, 2, 1, 2, 0, 3, 2],
    [2, 2, 0, 0, 1, 1, 2],  [3, 2, 0, 0, 0, 0, 2],  [1, 2, 1, 0, 1, 0, 2],
])

y = np.array([
    0,0,0, 0,0,0, 0,0,0,   # oily (9)
    5,5,5, 5,5,5, 5,5,5,   # severe acne (9)
    1,1,1, 1,1,1, 1,1,1,   # dry (9)
    2,2,2, 2,2,2, 2,2,2,   # combination (9)
    3,3,3, 3,3,3, 3,3,3,   # normal (9)
    4,4,4, 4,4,4, 4,4,4,   # sensitive (9)
    6,6,6, 6,6,6, 6,6,6,   # aging (9)
    7,7,7, 7,7,7, 7,7,7,   # high sun (9)
])

# ── ANN Model Setup ──────────────────────────────────────────
scaler = StandardScaler()

model = MLPClassifier(
    hidden_layer_sizes=(16, 8),  # 2 hidden layers - simple ANN
    activation='relu',
    max_iter=2000,
    random_state=42,
    learning_rate_init=0.01,
)

def train_model():
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"[ANN] Trained successfully. Accuracy: {acc * 100:.1f}%")
    return round(acc * 100, 1)

def predict(features: list) -> dict:
    arr = np.array(features).reshape(1, -1)
    arr_scaled = scaler.transform(arr)
    label = int(model.predict(arr_scaled)[0])
    confidence = round(float(max(model.predict_proba(arr_scaled)[0])) * 100, 1)
    return {
        "label": label,
        "recommendation": RECOMMENDATIONS[label],
        "confidence": confidence,
    }

# Train when module is loaded
accuracy = train_model()
