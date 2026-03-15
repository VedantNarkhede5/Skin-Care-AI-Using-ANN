# face_logic.py
# Simple logic: given ANN label + inputs → routine + food + products

# ── Products (image + price, suggestion only) ────────────────
PRODUCTS = {
    "oily": [
        {"name": "CeraVe Foaming Cleanser",       "price": "₹599",  "use": "Cleanser",    "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=200&q=80"},
        {"name": "Neutrogena Oil-Free Moisturizer","price": "₹749",  "use": "Moisturizer", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200&q=80"},
        {"name": "Salicylic Acid Serum 2%",        "price": "₹499",  "use": "Serum",       "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=200&q=80"},
    ],
    "dry": [
        {"name": "Cetaphil Gentle Cleanser",       "price": "₹399",  "use": "Cleanser",    "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=200&q=80"},
        {"name": "Neutrogena Hydro Boost Gel",     "price": "₹899",  "use": "Moisturizer", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200&q=80"},
        {"name": "Hyaluronic Acid Serum",          "price": "₹549",  "use": "Serum",       "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=200&q=80"},
    ],
    "combination": [
        {"name": "La Roche-Posay Cleanser",        "price": "₹799",  "use": "Cleanser",    "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=200&q=80"},
        {"name": "Niacinamide 10% Serum",          "price": "₹449",  "use": "Serum",       "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=200&q=80"},
        {"name": "Gel Moisturizer SPF 30",          "price": "₹649",  "use": "Moisturizer", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200&q=80"},
    ],
    "sensitive": [
        {"name": "Avene Gentle Milk Cleanser",     "price": "₹899",  "use": "Cleanser",    "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=200&q=80"},
        {"name": "Ceramide Repair Moisturizer",    "price": "₹799",  "use": "Moisturizer", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200&q=80"},
        {"name": "Centella Calming Serum",         "price": "₹599",  "use": "Serum",       "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=200&q=80"},
    ],
    "normal": [
        {"name": "Simple Kind to Skin Cleanser",   "price": "₹349",  "use": "Cleanser",    "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=200&q=80"},
        {"name": "Vitamin C Brightening Serum",    "price": "₹649",  "use": "Serum",       "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=200&q=80"},
        {"name": "SPF 50 Daily Sunscreen",          "price": "₹449",  "use": "Sunscreen",   "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200&q=80"},
    ],
    "acne": [
        {"name": "Benzoyl Peroxide Wash 5%",       "price": "₹399",  "use": "Cleanser",    "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=200&q=80"},
        {"name": "Adapalene Gel 0.1%",             "price": "₹549",  "use": "Treatment",   "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=200&q=80"},
        {"name": "Oil-Free SPF Moisturizer",       "price": "₹499",  "use": "Moisturizer", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200&q=80"},
    ],
    "aging": [
        {"name": "Retinol 0.5% Night Serum",       "price": "₹999",  "use": "Serum",       "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=200&q=80"},
        {"name": "Collagen Boost Moisturizer",     "price": "₹1199", "use": "Moisturizer", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200&q=80"},
        {"name": "Vitamin C + E Serum",            "price": "₹749",  "use": "Serum",       "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=200&q=80"},
    ],
    "sun": [
        {"name": "SPF 50+ PA++++ Sunscreen",        "price": "₹549",  "use": "Sunscreen",   "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200&q=80"},
        {"name": "Antioxidant Defense Serum",      "price": "₹699",  "use": "Serum",       "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=200&q=80"},
        {"name": "Aloe Vera Soothing Gel",          "price": "₹299",  "use": "Soothing",    "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=200&q=80"},
    ],
}

# ── Skincare Routines (Morning + Night) ──────────────────────
ROUTINES = {
    0: {"morning": ["Foaming cleanser", "Niacinamide serum", "Oil-free moisturizer", "SPF 30"],
        "night":   ["Foaming cleanser", "Salicylic acid serum", "Light gel moisturizer"]},
    1: {"morning": ["Cream cleanser", "Hyaluronic acid serum", "Rich moisturizer", "SPF 30"],
        "night":   ["Gentle cleanser", "Peptide serum", "Heavy night cream"]},
    2: {"morning": ["Gentle cleanser", "Niacinamide serum", "Lightweight moisturizer", "SPF 30"],
        "night":   ["Gentle cleanser", "BHA serum (T-zone only)", "Gel moisturizer"]},
    3: {"morning": ["Mild cleanser", "Vitamin C serum", "Moisturizer", "SPF 50"],
        "night":   ["Mild cleanser", "Retinol (2x/week)", "Regular moisturizer"]},
    4: {"morning": ["Fragrance-free cleanser", "Calming serum", "Ceramide moisturizer", "Mineral SPF"],
        "night":   ["Micellar water", "Centella serum", "Barrier repair cream"]},
    5: {"morning": ["Benzoyl peroxide wash", "Oil-free moisturizer", "SPF 30"],
        "night":   ["Salicylic cleanser", "Adapalene gel", "Non-comedogenic moisturizer"]},
    6: {"morning": ["Gentle cleanser", "Vitamin C serum", "Collagen moisturizer", "SPF 50"],
        "night":   ["Gentle cleanser", "Retinol serum", "Night repair cream"]},
    7: {"morning": ["Gentle cleanser", "Antioxidant serum", "Moisturizer", "SPF 50+ PA++++"],
        "night":   ["Double cleanse", "Soothing aloe serum", "Repairing night cream"]},
}

# ── Food Recommendations ─────────────────────────────────────
FOODS = {
    0: {"eat":   ["Green veggies", "Cucumber", "Watermelon", "Pumpkin seeds", "Green tea"],
        "avoid": ["Fried food", "Dairy", "Sugary drinks", "White bread"]},
    1: {"eat":   ["Avocado", "Walnuts", "Olive oil", "Salmon", "8+ glasses of water daily"],
        "avoid": ["Alcohol", "Caffeine", "Salty snacks"]},
    2: {"eat":   ["Berries", "Spinach", "Flaxseeds", "Probiotic yogurt", "Whole grains"],
        "avoid": ["Processed food", "Excess sugar", "Spicy food"]},
    3: {"eat":   ["Colourful vegetables", "Fruits", "Lean protein", "Nuts", "Green tea"],
        "avoid": ["Excess junk food", "Sugary beverages"]},
    4: {"eat":   ["Turmeric", "Chamomile tea", "Blueberries", "Oats", "Probiotic yogurt"],
        "avoid": ["Spicy food", "Alcohol", "Artificial additives"]},
    5: {"eat":   ["Chickpeas (zinc)", "Fish (omega-3)", "Green vegetables", "Probiotics"],
        "avoid": ["Dairy", "High-sugar foods", "Whey protein", "Fast food"]},
    6: {"eat":   ["Bone broth (collagen)", "Citrus (Vitamin C)", "Berries", "Dark chocolate"],
        "avoid": ["Excess sugar", "Alcohol", "Processed meat"]},
    7: {"eat":   ["Tomatoes (lycopene)", "Watermelon", "Carrots", "Green tea", "Vitamin E nuts"],
        "avoid": ["Alcohol", "Excess caffeine", "Sugary drinks"]},
}

# ── Main Function ─────────────────────────────────────────────
def get_face_recommendations(label, skin_type, acne_level, age_group, sun_exposure):
    # Choose which product set to show
    if acne_level in ["moderate", "severe"]:
        product_key = "acne"
    elif age_group in ["40s", "50+"]:
        product_key = "aging"
    elif sun_exposure == "high":
        product_key = "sun"
    else:
        product_key = skin_type  # oily / dry / combination / normal / sensitive

    return {
        "routine":  ROUTINES.get(label, ROUTINES[3]),
        "food":     FOODS.get(label, FOODS[3]),
        "products": PRODUCTS.get(product_key, PRODUCTS["normal"]),
    }
