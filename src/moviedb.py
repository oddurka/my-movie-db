import requests
import json

from dataclasses import dataclass
from decouple import config
from icecream import ic

from models.movie import Movie
import logging


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

        movies = [m for m in results if m["title"].lower() == title.lower()]

        # Checks if movie was found in the first page
        if not movies and total_pages > 1:
            # Look for movie in all the pages
            logging.debug(f"No exact match on page 1, searching remaining {total_pages - 1} page(s)")
            for page in range(2, total_pages + 1):
                params["page"] = page
                try:
                    response = requests.get(
                        "https://api.themoviedb.org/3/search/movie",
                        headers=headers,
                        params=params
                    ).json()
                except Exception as e:
                    logging.error(f"API request failed on page {page} for '{title}': {e}", exc_info=True)
                results.extend(response["results"])
                movies = [m for m in results if m["title"].lower() == title.lower()]
                # When movie is found break the loop
                if movies:
                    logging.debug(f"Exact match found on page {page}")
                    break

        movies = [self._get_details(movie) for movie in results if movie["title"].lower() == title.lower()]

        if not movies:
            logging.warning(f"No exact title match found for: '{title}'")
            raise ValueError(f"No movie found for title: '{title}'")
        if len(movies) > 1:
            logging.info(f"{len(movies)} matches found for {title}, prompting user to choose")
            return self._multiple_choise(movies)

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


    def _multiple_choise(self, movie_list: list) -> Movie:
        """
        List the choises if there is more than one option
        """
        logging.info(f"Prompting user to choose between {len(movie_list)} movies")
        while(True):
            print("Possible movies:")
            for i in range(len(movie_list)):
                print(f"[{i}] Name: {movie_list[i].title}\nYear: {movie_list[i].year}\nDescription: {movie_list[i].description}\n")
            selected = input("Which movie are you looking for: ")
            try:
                choice = int(selected)
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

