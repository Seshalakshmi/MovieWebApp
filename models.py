from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        print("Successfully created users table")

    def __repr__(self):
        return f"id: {self.id}, Name: {self.name}"
    

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(50))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String)

    def __str__(self):
        print("Successfully created movie table")

    def __repr__(self):
        return f"id: {self.id}, Name: {self.name}, Director: {self.director}, Year: {self.year}, Poster_url: {self.poster_url}"
    

class UserMovies(db.Model):
    __tablename__ = "user_movies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __str__(self):
        print("Successfully created user movies table")    