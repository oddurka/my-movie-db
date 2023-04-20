import requests
import json

from dataclasses import dataclass
from decouple import config

from models.movie import Movie


class MovieDB():
    def __init__(self):
        self._token = config("MOVIEDB_TOKEN")

    def search_for_movie(self, title: str, year: int) -> Movie:
        """
        Searchs for movies based on given title
        """
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={self._token}&language=en-US&query={title.replace(' ', '%20') if ' ' in title else title}&page=1&include_adult=false&year={year}"
        ).json()

        movies = [self._get_details(movie) for movie in response["results"] if movie["title"].lower() == title.lower()]

        if len(movies) > 1:
            return self._multiple_choise(movies)

        return movies

    def _get_details(self, response: list[dict]) -> Movie:
        genres = self.get_genres()
        return Movie(
            id = response["id"],
            title = response["title"],
            description = response["overview"],
            year = response["release_date"],
            language = response["original_language"],
            vote_average = response["vote_average"],
            vote_count = response["vote_count"],
            poster_path = response["poster_path"],
            genre = [genres[g] for g in response["genre_ids"]],
        )

    def _multiple_choise(self, movie_list: list) -> Movie:
        """List the choises if there is more than one option"""
        # TODO: make view for this and make user choose the correct movie
        # based on the description and poster
        # TODO: find out if it is possible to show pictue in terminal

        for movie in movie_list:
            print(f"Name: {movie.title}\nYear: {movie.year}")
        pass


    def get_movie_details(self, movie_id: int) -> Movie:
        """
        Returns all the wanted details of given movie_id
        """
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self._token}&language=en-US").json()
        movie = Movie(
            id = response["id"],
            title = response["title"],
            description = response["overview"],
            year = response["release_date"],
            language = response["original_language"],
            vote_average = response["vote_average"],
            vote_count = response["vote_count"],
            poster_path = response["poster_path"],
            genre = [g["name"] for g in response["genres"]]
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

