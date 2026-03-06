import re
import requests
import json

from dataclasses import dataclass
from decouple import config
from icecream import ic

from models.movie import Movie
import logging

from exceptions import MovieNotFoundError


class MovieDB():
    def __init__(self):
        self._token = config("MOVIEDB_BEARER")


    def search_for_movie(self, title: str, year: int = 0) -> Movie:
        """
        Searchs for movies based on given title
        """
        logging.info(f"Searching for: '{title}'" + (f" {year}" if year else ""))
        if "’" in title:
            title = title.replace("’", "'")

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}"
        }
        params = {
            "language": "en-US",
            "query": title,
            "include_adult": False,
            "page": 1
        }
        if year:
            params["year"] = year

        url = "https://api.themoviedb.org/3/search/movie"

        try:
            first_response = requests.get(url, headers=headers, params=params).json()
        except Exception as e:
            logging.error(f"API request failed for '{title}': {e}", exc_info=True)
            raise

        total_pages = first_response["total_pages"]
        results = first_response["results"]
        logging.debug(f"Page 1 returned {len(results)} result(s), {total_pages} total page(s)")

        movies = [self._get_details(movie) for movie in results if movie["title"].lower() == title.lower()]

        try:
            if not movies:
                logging.warning(f"No exact title match found for: '{title}'")
                movies = [self._get_details(movie) for movie in results]
                return self._multiple_choice(movies)
            if len(movies) > 1:
                logging.info(f"{len(movies)} matches found for {title}, prompting user to choose")
                return self._multiple_choice(movies)
        except MovieNotFoundError as e:
            logging.error(f"Movie not found for: '{title}': {e}")
        except Exception as e:
            logging.error(f"No movie found for: '{title}': {e}", exc_info=True)
            raise

        logging.info(f"Single match found: '{movies[0].title}' ({movies[0].year})")
        return movies[0]


    def _get_details(self, response: list[dict]) -> Movie:
        """
        Gets the details and puts them in the Movie model
        """
        logging.debug(f"Fetching details for movie id={response['id']} title='{response['title']}'")
        try:
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
        except KeyError as e:
            logging.error(f"Missing expected field in API response for '{response.get('title', '?')}': {e}")


    def _multiple_choice(self, movie_list: list) -> Movie:
        """
        List the choises if there is more than one option
        """
        logging.info(f"Prompting user to choose between {len(movie_list)} movies")
        while(True):
            print("\nPossible movies:")
            for i in range(len(movie_list)):
                print(f"[{i}] Name: {movie_list[i].title}\nYear: {movie_list[i].year}\nDescription: {movie_list[i].description}\n")
            selected = input("Which movie are you looking for: ")
            try:
                choice = int(selected)
                if choice == len(movie_list):
                    logging.info(f"User skipped '{movie_list[0].title}'")
                    raise MovieNotFoundError(f"User skipped: '{movie_list[0]}'")
                if 0 <= choice < len(movie_list):
                    logging.info(f"User selected: '{movie_list[choice].title}' ({movie_list[choice].year})")
                    return movie_list[choice]
                logging.warning(f"Selection {choice} out of range (0-{len(movie_list) - 1}), retrying")
            except ValueError:
                logging.warning(f"Invalid input '{selected}' - expected a number, retrying")


    def get_movie_details(self, movie_id: int) -> Movie:
        """
        Returns all the wanted details of given movie_id
        """
        logging.info(f"Fetching details for movie id={movie_id}")
        url=f"https://api.themoviedb.org/3/movie/{movie_id}?&language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}"
        }
        try:
            response = requests.get(url, headers=headers).json()
        except Exception as e:
            logging.error(f"Failed to fetch details for movie id={movie_id}: {e}", exc_info=True)
            raise

        try:
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
        except KeyError as e:
            logging.error(f"Missing expected field in details response for id={movie_id}: {e}")
            raise

        logging.info(f"Successfully fetched: '{movie.title}' ({movie.year})")
        return movie


    def get_genres(self) -> dict:
        """
        Return a dict with all available genres
        Key is the id number of the genre, and the value is the name of the genre
        """
        logging.debug("Fetching genre list from API")
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={self._token}&language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}"
        }
        try:
            response = requests.get(url, headers=headers).json()
        except Exception as e:
            logging.error(f"Failed to fetch genres: {e}", exc_info=True)

        genres = dict([(genre["id"], genre["name"]) for genre in response["genres"]])
        logging.debug(f"Loaded {len(genres)} genre(s)")
        return genres


    def movie_to_json(self, movie: Movie):
        logging.debug(f"Serializing movie to JSON: '{movie.title}'")
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
