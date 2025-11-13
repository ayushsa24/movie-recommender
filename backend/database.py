from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import random
import logging


import movie_database

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

OFFLINE_MODE = False

try:
    
    if not (DB_HOST and DB_USER and DB_PASS and DB_NAME):
        raise EnvironmentError("Database credentials missing; switching to offline mode.")

    
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)

    def fetch_movies_by_genre(genre: str, limit: int = 10):
        with SessionLocal() as session:
            q = text("SELECT * FROM movies WHERE :genre = ANY(genres) LIMIT :limit")
            result = session.execute(q, {"genre": genre, "limit": limit})
            return [dict(row) for row in result]

    def fetch_random_movies(limit: int = 10):
        with SessionLocal() as session:
            q = text("SELECT * FROM movies ORDER BY RANDOM() LIMIT :limit")
            result = session.execute(q, {"limit": limit})
            return [dict(row) for row in result]

except Exception as e:
    
    logging.warning("Running in OFFLINE_MODE: %s", e)
    OFFLINE_MODE = True


    def fetch_movies_by_genre(genre: str, limit: int = 10):
        if hasattr(movie_database, "fetch_movies_by_genre"):
            return movie_database.fetch_movies_by_genre(genre, limit)
        movies = getattr(movie_database, "MOVIES", [])
        filtered = [m for m in movies if genre.lower() in (g.lower() for g in m.get("genres", []))]
        return filtered[:limit]

    def fetch_random_movies(limit: int = 10):
        if hasattr(movie_database, "fetch_random_movies"):
            return movie_database.fetch_random_movies(limit)
        movies = getattr(movie_database, "MOVIES", [])
        return random.sample(movies, min(limit, len(movies)))
