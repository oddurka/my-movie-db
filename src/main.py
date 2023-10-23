from db import Database as db
from moviedb import MovieDB
from models.movie import Movie
from icecream import ic


def read_movie_file(txt_file: str) -> list:
    #TODO: make able to read files in given directroy and its subdirectories
    with open(f"src/{txt_file}") as txt:
        movie_list = txt.readlines()
        movies = []
        for movie in movie_list:
            movie, year = movie.split(", ")
            movies.append((movie, int(year.replace("/n", ""))))
        return movies


def movie_menu():
    mdb = MovieDB()
    local_movies = read_movie_file("movies.txt")
    for i in local_movies:
        movie = mdb.search_for_movie(i[0], i[1])
        db.save_to_db(mdb.movie_to_json(movie))
    ic(db.load_db())
    #movie = mdb.search_for_movie("Deliverance", 1972)
    #ic(movie)

def main():
    movie_menu()

if __name__ == "__main__":
    main()
