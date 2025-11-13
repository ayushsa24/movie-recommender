from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import random

from movie_database import MOVIE_DB  

from database import fetch_movies_by_genre, fetch_random_movies

app = FastAPI(title="Movie Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    user_input: str
    mode: str  

def get_offline_recommendations(user_text: str):
    """Generate movie recommendations from local DB (preferred) or local MOVIE_DB."""
    user_text = user_text.lower()
    
    for genre in ["action", "comedy", "drama", "thriller", "romance", "sci-fi", "horror"]:
        if genre in user_text:
            rows = fetch_movies_by_genre(genre, limit=3)
            if rows:
                return rows

    try:
        rows = fetch_random_movies(limit=3)
        if rows:
            return rows
    except Exception:
        pass

    for genre, movies in MOVIE_DB.items():
        if genre in user_text:
            return random.sample(movies, min(3, len(movies)))
    return random.sample(sum(MOVIE_DB.values(), []), 3)


async def get_online_recommendations(user_text: str):
    """Fetch recommendations using OpenAI API (if key provided)."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API Key Missing ⚠️. Please switch to Offline Mode or set OPENAI_API_KEY in the environment."
        )
    
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a movie recommendation assistant."},
                        {"role": "user", "content": f"Suggest 3 movies based on: {user_text}. Return JSON with title and description."}
                    ]
                },
            )

        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]["content"]
        return [{"title": "Online Mode Active ✅", "description": message}]

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"API request failed: {str(e)}")

@app.post("/recommend")
async def recommend_movies(payload: UserInput):
    """Return movie recommendations (online/offline)."""
    mode = payload.mode.lower()
    if mode == "offline":
        recommendations = get_offline_recommendations(payload.user_input)
    else:
        recommendations = await get_online_recommendations(payload.user_input)

    return {
        "mode": mode,
        "input": payload.user_input,
        "recommended_movies": recommendations,
    }

@app.get("/")
async def root():
    return {
        "message": "🎬 Movie Recommendation API is running!",
        "available_modes": ["online", "offline"],
        "example": {"user_input": "action movies with female lead", "mode": "offline"},
    }
