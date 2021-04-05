from wtforms import TextAreaField, StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    """ Login form. """
    email = StringField("Email", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])

class RegisterForm(FlaskForm):
    """ User registration form. """
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class FavoriteForm(FlaskForm):
    """ Form for adding a Favorites list. """
    name = StringField("Name", validators=[InputRequired("Name of List")])
    description = TextAreaField("Description", validators=[InputRequired("List Description")])

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""

class PlaceForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired("Enter Place Name")])
    location = StringField("City (optional)", validators=[Optional("Enter City")])

class AddToList(FlaskForm):
    submit = SubmitField(label="add")