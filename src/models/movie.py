from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    title: str
    description: str
    year: str
    language: str
    vote_average: float
    vote_count: int
    poster_path: str
    genre: list[str]
