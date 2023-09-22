import json
from moviedb import MovieDB
from models.movie import Movie
from icecream import ic


def read_movie_file(txt_file: str) -> list:
    with open(f"src/{txt_file}") as txt:
        movie_list = txt.readlines()
        movies = []
        for movie in movie_list:
            movie, year = movie.split(", ")
            movies.append((movie, int(year.replace("/n", ""))))
        return movies


def save_to_db(movie: dict):
    with open("movie_db.json", "r+") as db:
        db_movies = json.load(db)
        if str(movie["id"]) not in db_movies.keys():
            db_movies[movie["id"]] = movie
            db.seek(0)
            json.dump(db_movies, db, indent = 4)
            db.truncate()


def load_db():
    with open("movie_db.json") as db:
        return json.load(db)

def movie_menu():
    mdb = MovieDB()
    local_movies = read_movie_file("movies.txt")

    movie = mdb.search_for_movie(local_movies[1][0], local_movies[1][1])
    save_to_db(mdb.movie_to_json(movie))
    ic(load_db())

def main():
    movie_menu()

if __name__ == "__main__":
    main()
