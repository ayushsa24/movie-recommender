# 🎬 Movie Recommendation Web App

A simple full-stack web application that recommends movies based on user input using the OpenAI API. Users can describe their movie preferences (e.g., "action movies with a strong female lead") and receive 3–5 relevant suggestions. All inputs and recommendations are stored in a local SQLite database.

<img width="1920" height="1080" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/5fa4738e-841d-4867-8de9-95be7d3ebd61" />

---

## 📦 Project Structure

```
movie-recommender/
├── frontend/   # React app for user interface
└── backend/    # FastAPI server with OpenAI integration and SQLite database
```

---

## 🚀 Features

- 🤖 **AI-Powered Recommendations**: Utilizes OpenAI (ChatGPT) to generate personalized movie suggestions.
- 💾 **Persistent Storage**: Stores user queries and results in a SQLite database.
- 💡 **Interactive UI**: Glowing, animated UI with responsive design for an engaging user experience.
- 🔗 **Seamless Integration**: Smooth communication between frontend and backend.

---

## 🧠 Tech Stack

- **Frontend**: React + Vite
- **Backend**: FastAPI + OpenAI API
- **Database**: SQLite (via SQLAlchemy)
- **Styling**: CSS with glowing effects and animations

---

## 🖥️ Frontend Setup

### Prerequisites

- Node.js ≥ 20.19.0
- npm or pnpm

### Installation

```bash
cd frontend
npm install
```

### Run Locally

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🐍 Backend Setup

### Prerequisites

- Python ≥ 3.10
- `pip` and `venv`

### Installation

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in `backend/`:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### Initialize Database

```bash
python init_db.py
```

### Run Server

```bash
uvicorn main:app --reload
```

Backend will be live at [http://localhost:8000](http://localhost:8000)

---

## 🔗 Connecting Frontend to Backend

The frontend sends a POST request to:

```
http://localhost:8000/recommend
```

Payload format:

```json
{
  "user_input": "action movies with a strong female lead"
}
```

Response format:

```json
{
  "recommended_movies": [
    { "title": "Movie Title", "description": "Short summary" },
    ...
  ]
}
```

---

## 📁 Database Schema

SQLite database: `recommendations.db`

Table: `recommendations`

| Column            | Type     | Description                          |
|-------------------|----------|--------------------------------------|
| `id`              | Integer  | Primary key                          |
| `user_input`      | String   | User's movie preference              |
| `recommended_movies` | String | Raw text of recommended movies       |
| `timestamp`       | DateTime | When the recommendation was made     |

---

## ✅ Deliverables

- Source code (GitHub or ZIP)
- Instructions to run frontend and backend locally
- `.env` file with OpenAI API key (not committed)

---
