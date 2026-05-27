# SpamShield AI — Production-Ready AI-Powered Cybersecurity Platform

SpamShield AI is an internship-grade, portfolio-ready cybersecurity web application designed to scan, analyze, and detect SMS spam and phishing vectors in real-time. Combining robust Natural Language Processing (NLP) with Machine Learning classification pipelines, SpamShield AI provides users with instant, actionable threat intelligence.

---

## 🛡️ Project Overview

SpamShield AI delivers high-fidelity detection results through a futuristic glassmorphic cyberpunk interface. Users can input suspicious text messages, witness the real-time scanning process, and retrieve deep metrics: including classification verdicts, risk-level assessments, prediction confidence, and suspicious keyword detection.

The application utilizes a **Multinomial Naive Bayes** classifier trained on historical SMS datasets, processed alongside a **TF-IDF Vectorizer** to represent natural language mathematically based on term distinctiveness.

---

## ⚡ Key Features

1. **Sub-Millisecond Classification**: Rapid inference powered by Scikit-Learn Multinomial NB.
2. **Advanced NLP Pipeline**: Replicates the exact training preprocessing with NLTK Porter Stemming, tokenization, stopword exclusions, and punctuation filters.
3. **Double-Redundant Analytics**: Records statistics and scan details in both client-side browser `localStorage` and a server-side SQLite database.
4. **Threat Intelligence Console**: High-end dashboard tracking threat ratios, displaying dynamic Chart.js doughnut visualizations, and logging scan histories in an interactive table.
5. **Futuristic Visual Design**: Stunning cyberpunk glassmorphism UI styled with Tailwind CSS, custom grid backdrops, GSAP typewriters, AOS scroll reveals, and responsive mobile-first layouts.
6. **Robust Input Validation**: Strict checks to reject empty strings, invalid payload structures, and oversized messages (capped at 1000 characters).

---

## 🛠️ Technology Stack

| Layer | Technology | Description |
|---|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JS, Tailwind CSS | Layout structures, custom cyberpunk grid animations, and DOM rendering. |
| **Animations** | GSAP, AOS, Particles.js | Neon typing effects, smooth entry fades, and responsive particle backdrops. |
| **Charts** | Chart.js | Dynamic doughnut graphs summarizing spam vs safe statistics. |
| **Icons** | Lucide Icons, Font Awesome | Modern icons for visual threat alerts. |
| **Backend** | Flask, Flask-CORS | WSGI API routing, custom template loading, and server-side logic. |
| **Database** | SQLite3 | Local persistent logging of server inference logs. |
| **ML Engine** | Scikit-Learn, NLTK, joblib | TF-IDF token vectorizer and Multinomial Naive Bayes model. |
| **Deployment** | Docker, Render | Declarative blueprints for single-command hosting. |

---

## 📂 Project Structure

```text
SpamShield-AI/
├── backend/
│   ├── app.py                # Flask app factory, choice loaders, and views
│   ├── routes.py             # Route definitions (/health, /predict, /api/history)
│   ├── config.py             # Environment configurations (dev, testing, production)
│   ├── requirements.txt      # Python dependencies
│   ├── model/
│   │   ├── model.pkl         # Serialized Multinomial Naive Bayes classifier
│   │   └── vectorizer.pkl    # Serialized TF-IDF text vectorizer
│   ├── utils/
│   │   ├── preprocess.py     # NLP pipeline (Porter stemming, tokenise, stopwords)
│   │   ├── predictor.py      # Laser predict inference orchestrator
│   │   ├── keyword_detector.py # Rule-based spam word scan
│   │   └── confidence_score.py # Confidence conversions and risk level weights
│   └── database/
│       └── db.py             # SQLite helper (schema setups, history logs)
├── frontend/
│   ├── templates/
│   │   ├── layout.html       # Outer shell container with CDN loads
│   │   ├── index.html        # Landing page, hero, interactive scanner
│   │   ├── about.html        # Pipeline architecture and ML theory panel
│   │   └── dashboard.html    # Statistics, Chart.js, and logs table
│   ├── static/
│   │   ├── css/style.css     # Cyber grids, neon glows, and animations
│   │   └── js/script.js      # JS orchestrator, forms, async submits, Chart.js
│   └── components/
│       ├── navbar.html       # Sticky glassmorphic neon header
│       └── footer.html       # Modular cyberpunk technology footer
├── dataset/
│   └── spam.csv              # Raw CSV training SMS database
├── notebooks/
│   └── sms_spam_detection.ipynb # Original Google Colab training notebook
├── deployment/
│   ├── Dockerfile            # Container definition
│   ├── Procfile              # Process runner
│   ├── runtime.txt           # Declared target python engine
│   └── render.yaml           # One-click Render infrastructure setup
├── tests/
│   ├── test_api.py           # Integration endpoints validation tests
│   ├── test_model.py         # Binary checks and shape weights tests
│   └── test_ui.py            # Page template rendering checks
├── .gitignore                # Git exclusions
├── LICENSE                   # Open-source MIT terms
├── README.md                 # Detailed project guidebook
└── main.py                   # Local development execution boots script
```

---

## 🚀 Local Installation

Get the project running on your local machine in three steps:

### 1. Clone & Setup Workspace
Ensure Python 3 (Python 3.10+ recommended) is installed.
```bash
git clone https://github.com/yourusername/SpamShield-AI.git
cd SpamShield-AI
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Run the Server
```bash
python main.py
```
The server will boot in development mode and listen at **`http://127.0.0.1:5000`**. Open this URL in your web browser!

---

## 🔌 API Reference

### 1. System Health Status
* **Endpoint**: `/health`
* **Method**: `GET`
* **Response**:
```json
{
  "status": "ok"
}
```

### 2. Analyze Message Vector
* **Endpoint**: `/predict`
* **Method**: `POST`
* **Payload**:
```json
{
  "message": "Congratulations! You won 50,000 cash prize. Click now to claim your award."
}
```
* **Success Response (200 OK)**:
```json
{
  "prediction": "Spam",
  "confidence": 99.4,
  "risk_level": "High",
  "probability": 0.994,
  "keywords": ["congratulations", "win money", "cash prize", "claim reward", "click now"]
}
```

### 3. Retrieve Inference History Logs
* **Endpoint**: `/api/history`
* **Method**: `GET`
* **Response (200 OK)**:
```json
[
  {
    "message": "Congratulations! You won 50,000 cash prize. Click now to claim your award.",
    "prediction": "Spam",
    "confidence": 99.4,
    "risk_level": "High",
    "probability": 0.994,
    "keywords": ["congratulations", "win money", "cash prize", "claim reward", "click now"],
    "created_at": "2026-05-27 12:05:32"
  }
]
```

---

## 📊 Dashboard Guide

* **Stats Grid**: The top stats grid displays counts of total scans, spam instances flagged, and safe messages passed.
* **Accuracy Panel**: Shows model testing metrics (97.8% Accuracy and 100% Precision).
* **Ratio Graph**: Renders a dynamic doughnut chart showing the distribution of safe vs. spam items.
* **Scan logs table**: The interactive logs display recent messages, threat classification outcomes, prediction confidence, threat level weights, and time stamps. Click **Clear Logs** to wipe histories.

---

## ☁️ Deployment

### Render Blueprint
This project is configured with `deployment/render.yaml` for Render. Import your repository, and Render will automatically detect the blueprint and provision a web service executing the `deployment/Dockerfile`.

### Docker Container Setup
To build and run the platform in a container:
```bash
docker build -f deployment/Dockerfile -t spamshield-ai .
docker run -p 5000:5000 spamshield-ai
```

---

## 🔮 Future Roadmap

* **SMS API Gateway Integration**: Connect Twilio or Vonage webhooks to scan incoming SMS messages in real-time.
* **User Authentication**: Secure individual analytics dashboards for enterprise admins.
* **Fine-Tuning Transformer models**: Experiment with DistilBERT or RoBERTa for complex contextual classification.

---

## 📄 License
This codebase is distributed under the [MIT License](LICENSE).
