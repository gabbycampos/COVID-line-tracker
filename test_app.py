from unittest import TestCase

from app import app
from models import db, User, Favorite, Place, FavoritePlace

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///covid_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

class UserViewsTestCase(TestCase):
    """ Tests for views for Users """

    def setUp(self):
        """ Add Sample user """
        db.drop_all()
        db.create_all()
        
        user = User.register("test1@test.com", "password", "John", "Smith")
        userid = 1122
        user.id = userid

        db.session.commit()

        user = User.query.get(userid)

        self.user = user
        self.userid = userid

        self.client = app.test_client()
    
    def tearDown(self):
        """ Clean up any fouled transaction """
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_register(self):
        """ Test registration """
        user = User.register('test@test.com','password','John', 'Smith')
        user.id = 9999
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.first_name,'John')

    def test_valid_authentication(self):
        """Test user is logged in """
        user = User.authenticate('John', 'password')

    #  place = Place(name="Spinning J Bakery and Soda Fountain", google_id="ChIJx3IBfKrSD4gRxX9ucld95J8", address="1000 N California Ave, Chicago, IL 60622, United States")
    #     db.session.add(place)
    #     db.session.commit()
