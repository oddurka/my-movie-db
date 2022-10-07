import requests
import json

from dataclasses import dataclass
from decouple import config


@dataclass
class MyMovie:
    id: int
    title: str
    description: str
    year: int
    language: str
    vote_average: float
    vote_count: int
    poster_path: str
    genre: list[str]

    


class MovieDB():
    def __init__(self):
        self._token = config("MOVIEDB_TOKEN")

    def search_for_movie(self, title: str, year: int) -> dict:
        """
        Searchs for movies based on given title
        """
        # TODO: make it return a single movie
        if " " in title:
            titile = title.replace(" ", "%20")

        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={self._token}&language=en-US&query={title}&page=1&include_adult=false&year={year}"
        ).json()
        return response


    def get_movie_details(self, movie_id: int) -> MyMovie:
        """
        Returns all the wanted details of given movie_id
        """
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self._token}&language=en-US").json()
        movie = MyMovie(
            id = response["id"],
            title = response["title"],
            description = response["overview"],
            year = response["release_date"],
            language = response["original_language"],
            vote_average = response["vote_average"],
            vote_count = response["vote_count"],
            poster_path = response["poster_path"],
            genre = response["genres"],
        )

        return movie

      
    def get_genres(self) -> dict:
        """
        Return a dict with all available genres
        Key is the id number of the genre, and the value is the name of the genre
        """
        response = requests.get(f"https://api.themoviedb.org/3/genre/movie/list?api_key={self._token}&language=en-US").json()
        genres = dict([(genre["id"], genre["name"]) for genre in response["genres"]])
        return genres

