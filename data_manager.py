from models import db, User, Movie, UserMovies
import requests
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

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


class DataManager:
  # Define Crud operations as methods
    def create_user(self, name):
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = f"Error creating author: {e}"
            

    def get_users(self):
        data = User.query.all()
        return data
    
    def get_all_movies(self):
        data = Movie.query.all()
        return data
    
    def get_movies(self, user_id):
        data = (Movie.query
        .join(UserMovies, Movie.id == UserMovies.movie_id)
        .filter(UserMovies.user_id == user_id).all())
        return data
    
    def add_movie(self, name, user_id):
        fetch_movie_details = get_movie_details(name)
        if not fetch_movie_details:
            return None
        movie_title = fetch_movie_details.get('Title', '')
        movie_director = fetch_movie_details.get('Director', 'Unknown')
        movie_year = fetch_movie_details.get('Year', 'Unknown')
        movie_poster = fetch_movie_details.get('Poster',
                                    "https://placehold.co/380x562?text=No+Poster")
        try:
            movie = Movie.query.filter_by(name=movie_title).first()

            if not movie:
                new_movie = Movie(
                    name=movie_title, 
                    director=movie_director, 
                    year=movie_year, 
                    poster_url=movie_poster
                    )
                db.session.add(new_movie)
                db.session.flush()

                new_user_movie = UserMovies(
                    user_id=user_id, 
                    movie_id=new_movie.id
                    )

                db.session.add(new_user_movie)
                db.session.commit()
            
            else:
                data = Movie.query.filter_by(name=name).first()
                new_user_movie = UserMovies(
                    user_id=user_id, 
                    movie_id=data.id
                    )

                db.session.add(new_user_movie)
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = f"Error creating author: {e}"


    def update_movie(self, user_id, movie_id, new_title):
        try:
            data = (Movie.query
                    .join(UserMovies, Movie.id == UserMovies.movie_id)
                    .filter(UserMovies.movie_id == movie_id, 
                            UserMovies.user_id == user_id).first())
            data.name = new_title
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating movie: {e}")
        

    def delete_movie(self, user_id, movie_id):
        try:
            data = UserMovies.query.filter(
                UserMovies.user_id == user_id, 
                UserMovies.movie_id == movie_id).first()
            db.session.delete(data)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting movie: {e}")
