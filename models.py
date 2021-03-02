from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """ Connect this database to provided Flask app """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ user model """
    __tablename__ = "users"

    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    # if a user is deleted then delete their favorite lists too.
    favorites = db.relationship("Favorite", backref="users", cascade="all, delete")

    @classmethod
    def register(cls, email, password, first_name, last_name):
        """ Register a user, hashing their password """
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(email=email, password=hashed_utf8, first_name=first_name, last_name=last_name)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """ Validate that user exists and password is correct. """
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user 
        else:
            return False 

class Favorite(db.Model):
    """ For favorites lists. """
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey("users.email"))
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))

class Place(db.Model):
    """ For search results of a business """
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    google_id = db.Column(db.String(50))
    address = db.Column(db.String(50))
