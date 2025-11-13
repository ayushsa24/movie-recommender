import asyncio
from database import Base, engine
from models import Movie

async def init():
    print("📀 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init())
