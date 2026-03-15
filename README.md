# 🌿 Skin Care AI App

An AI-powered skincare recommendation web app built with:
- **Python + Flask** — backend server
- **MongoDB** — stores all user assessments
- **ANN (MLPClassifier)** — predicts personalized skincare routine
- **HTML + CSS** — clean, simple frontend

---

## 📁 Project Structure

```
skincare_ai/
├── app.py            ← Flask routes (main server)
├── ann_model.py      ← ANN model (train + predict)
├── database.py       ← MongoDB connection & queries
├── requirements.txt  ← Python dependencies
├── templates/
│   ├── index.html    ← Home page
│   ├── assess.html   ← Skin assessment form
│   ├── result.html   ← Recommendation result
│   └── history.html  ← Past assessments
└── static/
    └── style.css     ← All styling
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Make sure MongoDB is running
```bash
# On Windows
net start MongoDB

# On Mac/Linux
sudo systemctl start mongod
```

### 3. Start the app
```bash
python app.py
```

### 4. Open in browser
```
http://127.0.0.1:5000
```

---

## 🤖 How the ANN Works

- **Model**: `MLPClassifier` from scikit-learn (Multi-Layer Perceptron = ANN)
- **Architecture**: Input(7) → Hidden(16) → Hidden(8) → Output(8)
- **Inputs**: skin_type, age_group, sensitivity, acne_level, dryness, oiliness, sun_exposure
- **Output**: One of 8 skincare recommendation categories
- **Accuracy**: 75%+ on test data

---

## 💾 MongoDB Structure

**Database**: `skincare_ai`  
**Collection**: `assessments`

Each document stores:
```json
{
  "name": "Priya",
  "email": "priya@email.com",
  "inputs": { "Skin Type": "Oily", ... },
  "recommendation": "Use a foaming cleanser + ...",
  "confidence": 91.5,
  "label": 0,
  "date": "2024-01-15 10:30:00"
}
```

---

## 🎯 Interview Q&A

**Q: What is ANN?**  
A: Artificial Neural Network — layers of nodes that learn patterns from data. Here we use MLP (Multi-Layer Perceptron) with 2 hidden layers.

**Q: Why MLPClassifier?**  
A: It's simple, effective, and part of scikit-learn — easy to understand and explain. Perfect for classification tasks like this.

**Q: Why MongoDB?**  
A: MongoDB stores flexible JSON-like documents — great for storing varied user profiles without a fixed schema.

**Q: What are the input features?**  
A: 7 features — skin type, age group, sensitivity, acne level, dryness, oiliness, sun exposure — all encoded as integers.
