import requests
import json

from dataclasses import dataclass
from decouple import config
from icecream import ic

from models.movie import Movie


class MovieDB():
    def __init__(self):
        self._token = config("MOVIEDB_BEARER")


    def search_for_movie(self, title: str, year: int) -> Movie:
        """
        Searchs for movies based on given title
        """
        print(f"Searching for: {title}")
        if "’" in title:
            title = title.replace("’", "'")

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}"
        }
        url = f"https://api.themoviedb.org/3/search/movie?language=en-US&query={title.replace(' ', '%20') if ' ' in title else title}&page=1&include_adult=false{'' if year == 0 else f'&year={year}'}"
        response = requests.get(url, headers=headers).json()

        movies = [self._get_details(movie) for movie in response["results"] if movie["title"].lower() == title.lower()]

        if len(movies) > 1:
            return self._multiple_choise(movies)

        return movies[0]


    def _get_details(self, response: list[dict]) -> Movie:
        """
        Gets the details and puts them in the Movie model
        """
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
        """
        List the choises if there is more than one option
        """
        while(True):
            print("Possible movies:")
            for i in range(len(movie_list)):
                print(f"[{i}] Name: {movie_list[i].title}\nYear: {movie_list[i].year}\nDescription: {movie_list[i].description}\n")

            selected = input("Which movie are you looking for: ")
            return movie_list[int(selected)]


    def get_movie_details(self, movie_id: int) -> Movie:
        """
        Returns all the wanted details of given movie_id
        """
        url=f"https://api.themoviedb.org/3/movie/{movie_id}?&language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}"
        }
        response = requests.get(url, headers=headers).json()
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
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={self._token}&language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}"
        }
        response = requests.get(url, headers=headers).json()
        genres = dict([(genre["id"], genre["name"]) for genre in response["genres"]])
        return genres


    def movie_to_json(self, movie: Movie):
        return {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "year": movie.year,
            "language": movie.language,
            "vote_average": movie.vote_average,
            "vote_count": movie.vote_count,
            "poster_path": movie.poster_path,
            "genre": movie.genre,
        }

