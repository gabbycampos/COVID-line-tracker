from flask import Flask, render_template, redirect, session, flash, request, jsonify
from models import db, connect_db, User, Favorite, Place, FavoritePlace
from sqlalchemy.exc import IntegrityError
from forms import RegisterForm, LoginForm, FavoriteForm, DeleteForm, PlaceForm, AddToList
from werkzeug.exceptions import Unauthorized
import requests
from keys import key 
from populartimes import get_id
import datetime

API_BASE_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext'

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///covid_lt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.config["SQLALCHEMY_ECHO"] = True 
app.config["SECRET_KEY"] = "covidsecretapp"

connect_db(app)
db.create_all()

#################### HOME PAGE  ############################
@app.route('/')
def home_page():
    return redirect("/register")



##################### REGISTER AND LOGIN routes ####################################
@app.route('/register', methods=["GET", "POST"])
def register():
    """ Register a user. Form and handle register"""
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data 

        new_user = User.register(email, password, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.email.errors.append('Email taken. Please try again.')
            return render_template('register.html', form=form, button='Register')
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!')
        return redirect(f'/users/{new_user.id}')
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
        try:
            db.session.commit()
            google = result['place_id']
            time_resp = get_id(f"{key}", google)
            today = datetime.datetime.today().weekday()
            day = time_resp['populartimes'][today]['data'][datetime.datetime.now().hour]
            wait_time = round(day / 2)
            print('hello**********************************************')
            print('wait time', wait_time)
            return render_template('/results.html', form=form, place=place, user=user, wait_time=wait_time, button="Search")

        except IntegrityError:
            db.session.rollback()


        return render_template('/results.html', form=form, place=place, user=user, button="Search")
    else:
        return render_template("/search_form.html", user=user, form=form, button="Search")


# ######################## NEW LIST & LIST DETAILS & ADD TO LIST ###############################################
@app.route('/users/<int:user_id>/add_list', methods=['GET', 'POST'])
def add_list(user_id):
    """ Makes a new list. If valid redirect to a user's list of lists """
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
    favList = Favorite.query.get_or_404(favorite_id)
    # place = Place.query.get_or_404(place_id)
    return render_template('list_details.html', favorite=favorite, form=form, favList=favList, user=user)

@app.route('/users/<int:user_id>/add_to_list', methods=['GET', 'POST'])
def list_choices(user_id):
    """ Shows list choices and add to list. """
    form = AddToList()

    user = User.query.get_or_404(user_id)
    #favorites = db.session.query(Favorite).filter_by(user_id=user_id).all()
    form.fav.choices = [(fav.id, fav.name) for fav in Favorite.query.filter_by(user_id=user_id).all()]

    if form.validate_on_submit():
        #place = request.args['place_id']
        place = Place.query.get(request.args['place_id'])
        #favList = Favorite.query.filter_by(id=form.fav.data).first()
        favList = Favorite.query.get(form.fav.data)
        favList.places.append(place)
        db.session.commit()
        return redirect(f"/users/{user_id}")

    return render_template('list_choices.html', user=user, form=form, button="Add")

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
    """ Edits a list """
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

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Deletes a user """
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect('/login')
    form = LoginForm()
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id')
    flash('Account was deleted', 'warning')
    return redirect('/login')

# @app.route('/users/<int:place_id>/delete', methods=['POST'])
# def delete_place(place_id):
#     """ Deletes a place from a list """
#     place = Place.query.get(place_id)
#     db.session.delete(place)
#     db.session.commit()
#     return redirect('/login')
    
# <div class="col text-right">
#     <form action="/users/{{ place.id }}/delete" method="POST">
#         <button type="submit" class="btn btn-transparent border">Delete Place</button>
#         </form>
# </div>
      

    
   

   