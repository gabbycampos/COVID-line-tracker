# COVID Line Tracker app
#### API: "https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"

### About The Project
> This project is designed to let users know their estimated wait time to receieve an order from a business while following COVID guidelines. A user can do the following on the website:
- Create an account with an encrypted password.
- Search for a place and receive the name and address via a Google Maps API with an estimated wait time to receive an order based on the current popular times data.
- Make a list to save places.
- Edit or delete a list.
- Delete an account.

### Built With:
- Python
- Flask
- Google Maps API
- Populartimes Library
- Bootstrap
- Jinja
- Postgres
- SQLAlchemy
- Flask-Bcrypt
- WTForms
- Font Awesome

## Live Demo:
> coming soon...

### How to Run the Project:
> To get a local copy to run on your computer follow these steps:

#### Clone Repo
1. Clone the repo by clicking on the "Code" button at the top of the page. Or by typing the following in your terminal:

```bash
git clone https://github.com/gabbycampos/COVID-line-tracker.git
```
2. Create a virtual environment in the same directory of the cloned, unzipped code.

#### Library Installations
3. Activate your virtual environment
4. Use the package manager pip to install the requirements.txt

```bash
pip install -r requirements.txt
```

#### Postgres Installation
5. Install Postgres
6. Create a database named "covid_lt" in your terminal

```bash
createdb covid_lt
```
7. Start a server!