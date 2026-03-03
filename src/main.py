import logging
import re
from db import Database as db
from moviedb import MovieDB
from models.movie import Movie
from pathlib import Path
from icecream import ic
from ui.main import App

def read_movie_file(txt_file: str) -> list:
    with open(f"src/{txt_file}") as txt:
        movie_list = txt.readlines()
        movies = []
        for movie in movie_list:
            movie, year = movie.split(", ")
            movies.append((movie, int(year.replace("/n", ""))))

        return movies


def extract_movie_title(filename: str) -> str:
    """
    Extracts the movie title from the file name
    """
    name = filename.replace(".", " ")
    match = re.search(r"\b(19|20)\d{2}\b", name)
    if not match:
        logging.warning(f"No year found in filename: {filename} - returning full name")

    title = name[:match.start()].strip() if match else name.strip()
    if match:
        logging.debug(f"Extracted title: '{title}' from '{filename}'")

    return title


def read_movie_directory(directroy_path: str) -> list:
    """
    Finds movie files in the given directroy path
    """
    logging.info(f"Reading movie files from {directroy_path}")
    path = Path(directroy_path)
    if not path.exists():
        logging.error(f"Directory does not exist: {directroy_path}")
        return []
    if not path.is_dir():
        logging.error(f"Path is not a directroy: {directroy_path}")
        return []

    titles = [
        extract_movie_title(file_path.stem)
        for file_path in path.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in {".mkv", ".mp4"}
    ]
    logging.info(f"Found {len(titles)} movie file(s) in {directroy_path}")

    return titles


def get_existing_title(existing_movies: dict) -> set[str]:
    """
    Gets the titles of movies that is already in the database
    """
    titles = {movie["title"].lower() for movie in existing_movies.values()}
    logging.debug(f"Loaded {len(titles)} existing title(s) from database")
    return titles


def get_new_movies(directroy_path: str) -> list[str]:
    """
    Gets the movie files from the given path.
    Only movies that aren't already in the database
    """
    existing_movies = db.load_db()
    existing_titles = get_existing_title(existing_movies)
    movies = read_movie_directory(directroy_path)
    new_movies = [movie for movie in movies if movie.lower() not in existing_titles]
    logging.info(f"{len(new_movies)} new movie(s) to process (skipping {len(movies) - len(new_movies)} already in DB)")
    logging.debug(f"New movies: {new_movies}")

    return new_movies


def movie_menu():
    mdb = MovieDB()
    database = db()
    local_movies = get_new_movies("/mnt/c/Users/TheIc/Videos")
    for lm in local_movies:
        try:
            movie = mdb.search_for_movie(lm)
            database.save_to_db(mdb.movie_to_json(movie))
        except ValueError as e:
            logging.info(f"Skipping: {e}")
    #ic(db.load_db())


def main():
    movie_menu()


if __name__ == "__main__":
    #main()
    app = App()
    app.mainloop()
