from models import db, User, Movie
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
FILE_PATH = f"http://www.omdbapi.com/?apikey={API_KEY}"

def get_movie_details(movie_name):
    try:
        res = requests.get(FILE_PATH, params={'t': movie_name}, timeout=20)
        data = res.json()

        if data.get("Response") == "False":
            print(f"Movie not found: {movie_name}")
            return None

        return data

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the movie API.")

    except requests.exceptions.Timeout:
        print("Error: The request timed out.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Unexpected request error: {e}")

    return None


class DataManager():
  # Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        data = User.query.get()
        return data
    
    def get_movies(self, user_id):
        data = Movie.query.get(user_id)
        return data
    
    def add_movie(self, name, director, year, poster_url, user_id):
        new_movie = Movie(name=name, director=director, year=year, poster_url=poster_url, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()

    