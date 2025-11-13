from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    genre: str | None = None
    rating: float | None = None
    description: str | None = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int

    class Config:
        orm_mode = True
