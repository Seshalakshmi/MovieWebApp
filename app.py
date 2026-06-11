from flask import Flask, request, render_template, redirect
from data_manager import DataManager
from models import db
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('home.html', users=users) 

@app.route('/users', methods=["GET", "POST"])
def list_users():
    users = data_manager.get_users()
    if request.method == "POST":
        name = request.form.get('name')
        data_manager.create_user(name)
        return redirect('home.html', users=users)
    elif request.method == "GET":
        return render_template('home.html', users=users)
    
@app.route('/users/<int:user_id>/movies', methods=["GET", "POST"])
def get_and_add_movie_by_user_id(user_id):
    movies = data_manager.get_movies(user_id)
    if request.method == "post":
        movie_name = request.form.get('movie_name')
        data_manager.add_movie(movie_name, user_id)
        return redirect('movies.html', movies=movies)
    elif request.method == "GET":
        return render_template('movies.html', movies=movies)
    
    
@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=["POST"])
def update_movie_name(user_id, movie_id):
    movies = data_manager.get_movies(user_id)
    movie_name = request.form.get('update_name')
    data_manager.update_movie(user_id, movie_id, movie_name)
    return render_template('movies.html', movies=movies)

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=["POST"])
def delete_movie_by_user_id(user_id, movie_id):
    movies = data_manager.get_movies(user_id)
    data_manager.delete_movie(user_id, movie_id)
    return render_template('movie.html', movies=movies)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)