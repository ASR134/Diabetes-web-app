# 🩺 GlucoSense — Diabetes Risk Analyzer

A modern, AI-powered web application that predicts diabetes risk from clinical parameters. Built with **Streamlit** and powered by a **FastAPI** machine learning backend.

---

## ✨ Features

- **Instant Predictions** — Submit 8 biomarkers and get a result in ~1 second
- **Dark Clinical UI** — Custom CSS dark theme with teal accents and animated result cards
- **Risk Visualization** — Animated risk meter bar clearly communicates low vs high risk
- **Input Summary** — Expandable panel showing all submitted parameters after prediction
- **Responsive Layout** — Two-column card layout that works on desktop and mobile

---

## 🖥️ Demo

| Non-Diabetic Result | Diabetic Risk Detected |
|---|---|
| ✅ Green result card + balloon animation | ⚠️ Red/amber result card with high-risk meter |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/glucosense.git
cd glucosense

# 2. Install dependencies
pip install streamlit requests

# 3. Run the app
streamlit run diabetes_app.py
```

The app will open automatically at **http://localhost:8501**

---

## 🔌 API

The app connects to a hosted FastAPI prediction endpoint:

```
POST https://diabetes-prediction-api-ekdt.onrender.com/predict
```

### Request Body

```json
{
  "Pregnancies": 2,
  "Glucose": 120,
  "BloodPressure": 70,
  "SkinThickness": 20,
  "Insulin": 80,
  "BMI": 28.5,
  "DiabetesPedigreeFunction": 0.5,
  "Age": 33
}
```

### Response

```json
{
  "predicted category ": "Non Diabetic"
}
```

Possible values: `"Non Diabetic"` or `"Diabetic"`

> **Note:** The API is hosted on Render's free tier and may take 30–60 seconds to wake up on the first request after a period of inactivity.

---

## 📊 Input Parameters

| Parameter | Unit | Range | Description |
|---|---|---|---|
| Pregnancies | count | 0 – 20 | Number of times pregnant |
| Glucose | mg/dL | 1 – 300 | Plasma glucose (2-hr OGTT) |
| Blood Pressure | mm Hg | 1 – 200 | Diastolic blood pressure |
| Skin Thickness | mm | 0 – 100 | Triceps skin fold thickness |
| Insulin | mu U/ml | 0 – 900 | 2-hour serum insulin |
| BMI | kg/m² | 0.1 – 49.9 | Body mass index |
| Pedigree Function | score | 0.0 – 2.5 | Diabetes family history score |
| Age | years | 1 – 119 | Age of patient |

---

## 🗂️ Project Structure

```
glucosense/
│
├── diabetes_app.py     # Main Streamlit application
└── README.md           # Project documentation
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + custom CSS |
| Fonts | DM Serif Display, DM Sans (Google Fonts) |
| HTTP Client | Python `requests` |
| ML Backend | FastAPI (hosted on Render) |

---

## ⚠️ Disclaimer

This application is intended for **educational and informational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional regarding any medical concerns.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
