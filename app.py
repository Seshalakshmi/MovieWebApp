from flask import Flask, request, render_template, redirect, url_for, jsonify
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
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users) 

@app.route('/users', methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        name = request.form.get('user_name')
        data_manager.create_user(name)
        return redirect(url_for('index'))
    
    users = data_manager.get_users()
    return render_template('index.html', users=users)

@app.route('/movies')
def get_all_movies():
    try:
        movies = data_manager.get_all_movies()
        return render_template('all_movies.html', movies=movies)
    except Exception as e:
        app.logger.error(f"Error fetching movies: {e}")
        return render_template('500.html'), 500
    
@app.route('/users/<int:user_id>/movies', methods=["GET", "POST"])
def get_movies(user_id):
    
    if request.method == "POST":
        movie_name = request.form.get('movie_name')
        data_manager.add_movie(movie_name, user_id)
        return redirect(url_for('get_movies', user_id=user_id))
    
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)
    
    
@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=["POST"])
def update_movie_name(user_id, movie_id):
    movie_name = request.form.get('name')
    data_manager.update_movie(user_id, movie_id, movie_name)
    return redirect(url_for('get_movies', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=["POST"])
def delete_movie_by_user_id(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('get_movies', user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)