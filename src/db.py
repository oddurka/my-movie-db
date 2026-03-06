import json
import logging
from pathlib import Path

class Database:
    DB_PATH = Path("movie_db.json")

    def _ensure_db_exists(self) -> None:
        """
        Create the database file if it doesn't exist
        """
        if not self.DB_PATH.exists():
            logging.info("Database file not found, creating new one")
            with open(self.DB_PATH, "w") as db:
                json.dump({}, db)


    def save_to_db(self, movie: dict) -> None:
        """
        Saves dict to a json file
        """
        self._ensure_db_exists()
        logging.info(f"Saving to '{movie['title']}' (id={movie['id']}) to database")
        try:
            with open("movie_db.json", "r+") as db:
                db_movies = json.load(db)
                if str(movie["id"]) in db_movies:
                    logging.debug(f"Movie id={movie['id']} already in database, skipping")
                    return
                db_movies[movie["id"]] = movie
                db.seek(0)
                json.dump(db_movies, db, indent = 4)
                db.truncate()
                logging.info(f"Saved '{movie['title']}' successfully")
        except json.JSONDecodeError as e:
            logging.error(f"Database file is corrupted: {e}")
            raise


    @staticmethod
    def load_db() -> dict:
        """
        Load json file
        """
        logging.info("Loading database")
        path = Path("movie_db.json")
        if not path.exists():
            logging.warning("Database file not found, returning empty dict")
            return {}

        try:
            with open(path) as db:
                return json.load(db)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse database file: {e}")
            raise
