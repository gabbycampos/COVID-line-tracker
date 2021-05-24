from models import db, User, Favorite, Place, FavoritePlace
from app import app

# create all tables
db.drop_all()
db.create_all()

# Make users
u1 = User(email="user1@user.com", password="password", first_name="Mario", last_name="Bros")
u2 = User(email="user2@user.com", password="password", first_name="Luigi", last_name="Bros")

db.session.add_all([u1, u2])
db.session.commit()

# Make favorite lists
fav_list1 = Favorite(name="Pizza Spots", description="Chicago pizza spots.", user_id=1)
fav_list2 = Favorite(name="Burger Spots", description="LA burgers", user_id=2)

db.session.add_all([fav_list1, fav_list2])
db.session.commit()