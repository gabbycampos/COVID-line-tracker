from flask import Flask, render_template, request
import requests
from secrets import key 
from populartimes import get_id

#API_BASE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={key}"

# place search
#response = requests.get(f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=dantes&inputtype=textquery&fields=place_id,name,formatted_address&key={key}')

#place details
#response = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?key={key}&place_id=ChIJx3IBfKrSD4gRxX9ucld95J8&fields=name,opening_hours,place_id')

#spinninJ place_id: 'ChIJx3IBfKrSD4gRxX9ucld95J8'
response = get_id(f'{key}', 'ChIJSYuuSx9awokRyrrOFTGg0GY' )
print(response['populartimes'])
