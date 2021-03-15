from flask import Flask, render_template, redirect, session, flash, request, jsonify
from models import db, connect_db, User, Favorite, Place, FavoritePlace
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

        place = Place(name=result['name'], address=result['address'], place_id=result['place_id'])

        db.session.add(place)
        #db.session.commit()
        
        if not result['place_id']:
            db.session.commit()

        return render_template('/home.html', form=form, place=place, button="Search")
    else:
        return redirect("/", form=form, button="Search")


##################### REGISTER AND LOGIN routes ####################################
@app.route('/register', methods=["GET", "POST"])
def register():
    """ Register a user. Form and handle register"""

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data 

        user = User.register(email, password, first_name, last_name)

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            form.email.errors.append('Email taken. Please try again.')
            return render_template('register.html', form=form, button='Register')
        session['user_id'] = user.id
        flash('Welcome! Successfully Created Your Account!')
        return redirect(f'/users/{user.id}')
    return render_template('register.html', form=form, button='Register')

@app.route('/login', methods=["GET", "POST"])
def login():
    """ Login form or handle login """
    
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data 
        password = form.password.data 

        user = User.authenticate(email, password)

        if user:
            flash(f"Welcome Back, {user.email}!", "info")
            session['user_id'] = user.id
            return redirect(f"/users/{user.id}")
        else:
            form.email.errors = ["Invalid email/password"]

    return render_template("login.html", form=form, button='Login')
    
@app.route('/logout')
def logout():
    """ Logout route """

    session.pop('user_id')
    flash('Goodbye!')
    return redirect("/")


##################### User's FAVORITE LISTS PAGE and SEARCH FORM ####################################
@app.route('/users/<int:user_id>', methods=["GET", "POST"])
def show_favorites(user_id):
    """ Shows a users lists of favorites & button to search form"""

    if 'user_id' not in session:
        flash('Please login first')
        return redirect('/login')

    user = User.query.get_or_404(user_id)
    favorites = db.session.query(Favorite).filter_by(user_id=user_id).all()
    form = DeleteForm()
    return render_template('favorites.html', user=user, favorites=favorites, form=form, button='Go To Search Form')

@app.route('/users/<int:user_id>/search', methods=["GET", "POST"])
def get_search_form(user_id):
    """ Shows search form and process it """

    user = User.query.get(user_id)
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

        place = Place(name=result['name'], address=result['address'], place_id=result['place_id'])

        db.session.add(place)
        #db.session.commit()
        if not result['place_id']:
            db.session.commit()

        return render_template('/home.html', form=form, place=place, user=user, button="Search")
    else:
        return render_template("/search_form.html", user=user, form=form, button="Search")


# ######################## NEW LIST & LIST DETAILS & ADD TO LIST ###############################################
@app.route('/users/<int:user_id>/add_list', methods=['GET', 'POST'])
def add_list(user_id):
    """ Makes a new list. Add current place to list. If valid redirect to a user's list of lists """
    if 'user_id' not in session:
        flash('Please login first')
        return redirect('/login')

    user = User.query.get_or_404(user_id)
    favorites = db.session.query(Favorite).filter_by(user_id=user_id).all()

    form = FavoriteForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data 

        new_list = Favorite(name=name, description=description, user_id=user_id)

        db.session.add(new_list)
        db.session.commit()
        return redirect(f"/users/{user_id}")
    return render_template('new_list.html', form=form, user=user, button="Add")

@app.route('/users/<int:user_id>/lists/<int:favorite_id>', methods=['GET', 'POST'])
def list_details(favorite_id, user_id):
    """ Shows a users list details"""
    form = FavoriteForm()
    user = User.query.get_or_404(user_id)
    favorite = Favorite.query.get_or_404(favorite_id)
    return render_template('list_details.html', favorite=favorite, form=form, user=user)

# @app.route('/users/<int:user_id>/add_to_list', methods=['GET', 'POST'])
# def add_place():
#     """ Add a place to an existing list """




########################### DELETE & EDIT ROUTES #################################################
@app.route('/users/<int:user_id>/delete/<int:favorite_id>', methods=["GET", "POST"])
def delete_favorites(user_id, favorite_id):
    """ Deletes a favorite list"""
    if session.get('user_id'):
        favorite = Favorite.query.get_or_404(favorite_id)
        db.session.delete(favorite)
        db.session.commit()
        flash("List deleted", "info")
        return redirect(f"/users/{user_id}")
    else:
        flash("Please login first", "danger")
        return redirect('/login')

@app.route('/users/<int:user_id>/edit/<int:favorite_id>', methods=["GET", "POST"])
def edit_favorite(user_id, favorite_id):
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect('/login')
    favorite = Favorite.query.get_or_404(favorite_id)
    form = FavoriteForm(obj=favorite)
    if form.validate_on_submit():
        favorite.name = form.name.data 
        favorite.content = form.description.data
        db.session.commit()
        flash("List updated successfully", "info")
        return redirect(f'/users/{user_id}')
    return render_template('edit_list.html', button='Edit', form=form, favorite=favorite)