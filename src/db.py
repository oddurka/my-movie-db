import json
from pathlib import Path

class Database:
    def save_to_db(self, movie: dict) -> None:
        """
        Saves dict to a json file
        """

        with open("movie_db.json", "r+") as db:
            db_movies = json.load(db)
            if str(movie["id"]) not in db_movies.keys():
                db_movies[movie["id"]] = movie
                db.seek(0)
                json.dump(db_movies, db, indent = 4)
                db.truncate()


    def load_db() -> dict:
        """
        Load json file
        """
        path = Path("movie_db.json")
        if not path.exists():
            return {}

        with open(path) as db:
            return json.load(db)
