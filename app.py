from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User, Favorite, Business
from sqlalchemy.exc import IntegrityError
from forms import RegisterForm, LoginForm, FavoriteForm, DeleteForm
from werkzeug.exceptions import Unauthorized
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///covid_lt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.config["SQLALCHEMY_ECHO"] = True 
app.config["SECRET_KEY"] = "covidsecretapp"

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect("/register")

@app.route('/register', methods=["GET", "POST"])
def register():
    """ Register a user. Form and handle register"""

    if "email" in session:
        return redirect(f"/users/{session['email']}")

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data 

        user = User.register(email, password, first_name, last_name)

        db.session.commit()
        session['email'] = user.email 

        return redirect(f"/users/{user.email}")
    else:
        return render_template("/register.html", form=form, button="Register")

@app.route('/login', methods=["GET", "POST"])
def login():
    """ Login form or handle login """

    if "email" in session:
        return redirect(f"/users/{session['email']}")
    
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data 
        password = form.password.data 

        user = User.authenticate(email, password)
        if user:
            session['email'] = user.email 
            return redirect(f"/users/{user.email}")
        else:
            form.email.errors = ["Invalid email/password"]
            return render_template("users/login.html", form=form, button='Login')

    return render_template("/login.html", form=form, button="Login")

@app.route('/logout')
def logout():
    """ Logout route """ 

    session.pop("email")
    return redirect("/")

@app.route('/users/<email>')
def show_favorites(email):
    """ Shows a users lists of favorites """
    if 'email' not in session or email != session['email']:
        raise Unauthorized()
    
    user = User.query.get(email)
    form = DeleteForm()

    return render_template("/favorites.html", user=user, form=form)