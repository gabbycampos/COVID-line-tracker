from flask import Flask, render_template, redirect, session, flash, request, jsonify
from models import db, connect_db, User, Favorite, Place
from sqlalchemy.exc import IntegrityError
from forms import RegisterForm, LoginForm, FavoriteForm, DeleteForm, PlaceForm
from werkzeug.exceptions import Unauthorized
import requests
from secrets import key 

API_BASE_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext'

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///covid_lt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.config["SQLALCHEMY_ECHO"] = True 
app.config["SECRET_KEY"] = "covidsecretapp"

connect_db(app)
db.create_all()

#################### HOME PAGE AND HOMEPAGE-SEARCH FORM ############################
@app.route('/')
def home_page():
    form = PlaceForm()
    return render_template('home.html', form=form, button="Search")

@app.route('/', methods=["GET", "POST"])
def get_place():
    """ Shows search form and process it """
    form = PlaceForm()
     
    if form.validate_on_submit():
        query = form.name.data
        location = form.location.data
        response = requests.get(f'{API_BASE_URL}/json?input={query}&inputtype=textquery&fields=place_id,name,formatted_address&key={key}')
        data = response.json()

        result = {
            'name': data['candidates'][0]['name'],
            'address': data['candidates'][0]['formatted_address'],
            'place_id': data['candidates'][0]['place_id']
        }
        #print(result['name'])

        place = Place(name=result['name'], address=result['address'], google_id=result['place_id'])

        db.session.add(place)
        db.session.commit()

        return render_template('/home.html', form=form, place=place, button="Search")
    else:
        return redirect("/", form=form, button="Search")


##################### REGISTER AND LOGIN routes ####################################
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


##################### User's FAVORITE LISTS PAGE and SEARCH FORM ####################################
@app.route('/users/<email>', methods=["GET", "POST"])
def show_favorites(email):
    """ Shows a users lists of favorites & button to search form"""
    favorites = Favorite.query.all()

    if 'email' not in session or email != session['email']:
        raise Unauthorized()
    
    user = User.query.get(email)
    form = DeleteForm()

    return render_template("/favorites.html", user=user, favorites=favorites, form=form, button='Go To Search Form')

@app.route('/users/<email>/search', methods=["GET", "POST"])
def get_search_form(email):
    """ Shows search form and process it """
    if 'email' not in session or email != session['email']:
        raise Unauthorized()

    user = User.query.get(email)
    form = PlaceForm()
     
    if form.validate_on_submit():
        query = form.name.data
        location = form.location.data
        response = requests.get(f'{API_BASE_URL}/json?input={query}&inputtype=textquery&fields=place_id,name,formatted_address&key={key}')
        data = response.json()

        result = {
            'name': data['candidates'][0]['name'],
            'address': data['candidates'][0]['formatted_address'],
            'place_id': data['candidates'][0]['place_id']
        }
        #print(result['name'])

        place = Place(name=result['name'], address=result['address'], google_id=result['place_id'])

        db.session.add(place)
        db.session.commit()

        return render_template('/results.html', form=form, place=place, user=user, button="Search")
    else:
        return render_template("/search_form.html", user=user, form=form, button="Search")


######################## NEW LIST & LIST DETAILS & ADD TO LIST #####################################################
@app.route('/users/<email>/add_list', methods=['GET', 'POST'])
def add_list(email):
    """ Makes a new list. If valid redirect to a user's list of lists """
    favorites = Favorite.query.all()

    if 'email' not in session or email != session['email']:
        raise Unauthorized()

    user = User.query.get(email)
    form = FavoriteForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data 

        new_list = Favorite(name=name, description=description)

        db.session.add(new_list)
        db.session.commit()
        return redirect(f"/users/{email}", favorite=favorites)
    return render_template('new_list.html', form=form, user=user, button="Add")

@app.route('/users/<int:')
def list_details():
    """ Shows a users list details"""

@app.route('/users/add_to_list', methods=['GET', 'POST'])
def add_place():
    """ Add a place to an existing list """