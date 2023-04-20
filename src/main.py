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


def movie_menu():
    mdb = MovieDB()
    local_movies = read_movie_file("movies.txt")

    movies = mdb.search_for_movie(local_movies[0][0], local_movies[0][1])
    ic(movies)


def main():
    movie_menu()

if __name__ == "__main__":
    main()
