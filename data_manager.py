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
    
    def add_movie(self, name, user_id):
        
        fetch_movie_details = get_movie_details(name)
        movie_title = fetch_movie_details.get('Title', 0)
        movie_director = fetch_movie_details.get('Director', 0)
        movie_year = fetch_movie_details.get('Year', 0)
        movie_poster = fetch_movie_details.get('Poster',
                                    "https://placehold.co/380x562?text=No+Poster")
        
        new_movie = Movie(name=movie_title, director=movie_director, year=movie_year, poster_url=movie_poster, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()


    