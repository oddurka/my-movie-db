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
    name = filename.replace(".", " ")
    match = re.search(r"\b(19|20)\d{2}\b", name)

    return name[:match.start()].strip() if match else name.strip()


def read_movie_directory(directroy_path: str) -> list:
    path = Path(directroy_path)

    return [
        extract_movie_title(file_path.stem)
        for file_path in path.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in {".mkv", ".mp4"}
    ]


def get_existing_title(existing_movies: dict) -> set[str]:
    return {movie["title"].lower() for movie in existing_movies.values()}


def get_new_movies(directroy_path: str) -> list[str]:
    existing_movies = db.load_db()
    existing_titles = get_existing_title(existing_movies)
    movies = read_movie_directory(directroy_path)

    return [movie for movie in movies if movie.lower() not in existing_titles]


def movie_menu():
    mdb = MovieDB()
    database = db()
    local_movies = get_new_movies("/mnt/c/Users/TheIc/Videos")
    for lm in local_movies:
        try:
            movie = mdb.search_for_movie(lm)
            database.save_to_db(mdb.movie_to_json(movie))
        except ValueError as e:
            print(f"Skipping: {e}")
    ic(db.load_db())


def main():
    movie_menu()


if __name__ == "__main__":
    #main()
    app = App()
    app.mainloop()
