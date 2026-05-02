<div align="center">

<br/>

```
╔═══════════════════════════════════════════════════════════╗
║   ██████╗██╗     ██╗███╗   ███╗ █████╗                   ║
║  ██╔════╝██║     ██║████╗ ████║██╔══██╗                  ║
║  ██║     ██║     ██║██╔████╔██║███████║                  ║
║  ██║     ██║     ██║██║╚██╔╝██║██╔══██║                  ║
║  ╚██████╗███████╗██║██║ ╚═╝ ██║██║  ██║                  ║
║   ╚═════╝╚══════╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝                  ║
║            P R E D I C T                                 ║
╚═══════════════════════════════════════════════════════════╝
```

### *Don't just monitor your environment — predict it.*

<br/>

![ClimaPredict cover](ClimaPredict.png)

<br/>

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![MQTT](https://img.shields.io/badge/MQTT-3C5280?style=for-the-badge&logo=eclipse-mosquitto&logoColor=white)](https://mqtt.org/)

<br/>

</div>

---

## ⚡ What is ClimaPredict?

> **ClimaPredict** is an explainable, predictive environmental analytics platform that transforms indoor health monitoring from a passive activity into an active, anticipatory science.

Rather than simply logging temperature, humidity, and CO₂ readings after the fact, ClimaPredict ingests live IoT sensor streams, applies machine learning models, and surfaces **what's about to happen** — giving you the window to act before conditions deteriorate.

Built for labs, offices, research facilities, and smart buildings that demand more than a dashboard.

---

## 🗺️ Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                           │
│   ┌──────────────────────────────────────────────────────┐     │
│   │   React.js Frontend  │  Glassmorphism UI  │  AI Chat  │     │
│   └──────────────────────────────────────────────────────┘     │
└──────────────────────────────┬──────────────────────────────────┘
                               │  REST API
┌──────────────────────────────▼──────────────────────────────────┐
│                        BACKEND LAYER                           │
│   ┌──────────────┐   ┌───────────────┐   ┌──────────────────┐  │
│   │  Flask API   │   │  ML Pipeline  │   │  Gemini AI API   │  │
│   │  (REST)      │   │  (Forecast +  │   │  (Chatbot +      │  │
│   │              │   │   Anomaly)    │   │   Insights)      │  │
│   └──────┬───────┘   └───────────────┘   └──────────────────┘  │
└──────────┼──────────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────────┐
│                         DATA LAYER                             │
│   ┌───────────────────────┐     ┌──────────────────────────┐   │
│   │  MongoDB              │     │   MQTT Broker            │   │
│   │  (Raw + Filtered Data)│◄────│   (Live IoT Streams)     │   │
│   └───────────────────────┘     └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔴 Real-Time Monitoring
Live ingestion of IoT sensor data via the **MQTT protocol**. Track critical indoor climate metrics — temperature, humidity, CO₂ — with sub-second refresh rates and zero missed readings.

</td>
<td width="50%">

### 🔮 Predictive Forecasting
Goes beyond dashboards. Historical sensor data feeds ML models that generate **forward-looking predictions**, giving operators a clear view of environmental trajectories before thresholds are breached.

</td>
</tr>
<tr>
<td width="50%">

### 🤖 Context-Aware AI Assistant
An integrated **Google Gemini** chatbot that understands your live data. Ask it why CO₂ spiked at 3pm, request an interpretation of today's humidity trend, or get guided through the UI — all in natural language.

</td>
<td width="50%">

### 🚨 Anomaly Detection
An automated backend pipeline continuously validates incoming sensor readings. Sudden environmental spikes — a CO₂ surge from proximity, a temperature anomaly — are flagged, filtered, and surfaced to users in real time.

</td>
</tr>
<tr>
<td width="50%">

### 📊 Interactive Visualizations
Drill-down and drill-up across hierarchical time-series data. Apply advanced filters by date range, sensor type, or environmental metric. Every chart is designed to answer questions, not just display numbers.

</td>
<td width="50%">

### 🎨 Dual-Theme UI/UX
Two carefully crafted visual experiences:
- **Dark Mode** — Cyberpunk glassmorphism with animated aurora backgrounds
- **Light Mode** — Clean, professional, brand-aligned precision design

</td>
</tr>
</table>

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React.js | Component-driven UI with dynamic micro-animations |
| **Styling** | Modern CSS | Glassmorphism, aurora effects, responsive layouts |
| **Backend** | Python + Flask | REST API, ML pipeline orchestration |
| **Database** | MongoDB | Raw stream storage, anomaly-filtered data |
| **IoT Protocol** | MQTT | Real-time sensor data ingestion |
| **AI / ML** | Google Gemini API | Chatbot intelligence + predictive analytics |

---

## 🚀 Getting Started

### Prerequisites

```bash
node >= 18.x
python >= 3.10
mongodb >= 6.x
mosquitto (MQTT broker)
```

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Hansamalee0630/ClimaPredict.git
cd ClimaPredict
```

**2. Set up the backend**
```bash
cd Backend
python -m venv .venv

# Activate virtual environment:
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

**3. Configure environment variables**
Create a `.env` file in the root backend directory:
```bash
MONGO_URI=mongodb://localhost:27017/
GEMINI_API_KEY=your_gemini_api_key
MQTT_BROKER=localhost
MQTT_PORT=1883
```

**4. Start the Flask backend**
```bash
python api.py
# API running at http://localhost:5000
```

**5. Set up and start the frontend**
Open a new terminal window:
```bash
cd frontend/react-app
npm install
npm start
# App running at http://localhost:3000
```

**6. Start your ingestion pipeline**
Open another terminal window:
```bash
cd Backend
python mqtt_to_mongo.py
```

---

## 📁 Project Structure

```text
ClimaPredict/
├── 📂 frontend/
│   └── 📂 react-app/
│       ├── 📂 src/              # React frontend application
│       ├── 📂 public/           # Static assets
│       └── package.json         # Node dependencies
│
├── 📂 Backend/
│   ├── api.py                   # Flask API endpoints & Routes
│   ├── mqtt_to_mongo.py         # MQTT subscriber & DB ingestion script
│   ├── export_to_csv.py         # Data export utility
│   └── *.pkl                    # Machine learning models (Ignored in Git)
│
├── .gitignore                   # Git ignore file
└── README.md                    # Project documentation
```

---

## 🔌 Core API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/sensor_data` | Fetch historical sensor readings |
| `GET` | `/api/predictive_forecast` | Retrieve ML predictive forecasts |
| `GET` | `/api/anomalies` | Fetch filtered anomaly data |
| `POST` | `/api/chat` | Send queries to the Gemini AI chatbot |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get involved:

```bash
# Fork the repository
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git commit -m "feat: add your feature description"

# Push and open a Pull Request
git push origin feature/your-feature-name
```

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) specification and ensure all tests pass before submitting.

---

## 📜 License

This project is licensed under the **MIT License**.

---

<div align="center">

<br/>

*Built with precision. Designed to predict.*

**ClimaPredict** — shifting environmental monitoring from reactive to proactive.

<br/>

⭐ **If this project helped you, consider giving it a star!** ⭐

</div>
