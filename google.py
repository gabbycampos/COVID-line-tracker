from flask import Flask, render_template, request
import requests
# from secrets import key 
from populartimes import get_id
import datetime

#API_BASE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={key}"

# place search
#response = requests.get(f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=dantes&inputtype=textquery&fields=place_id,name,formatted_address&key={key}')

#place details
#response = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?key={key}&place_id=ChIJx3IBfKrSD4gRxX9ucld95J8&fields=name,opening_hours,place_id')

#spinninJ place_id: 'ChIJx3IBfKrSD4gRxX9ucld95J8'

# response = get_id(f'{key}', 'ChIJ4VuSG-Bl24ARSOf2qkoteQ4' )
# print(response)
# today = datetime.datetime.today().weekday()
# day = response['populartimes'][today]['data'][datetime.datetime.now().hour]
# print(day)
# wait_time = round(day / 2)
# print(wait_time)

#print(today)
#print(today.strftime("%A"))

#print(response['populartimes'][0])

# API_BASE_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext'

# response = requests.get(f'{API_BASE_URL}/json?input=dantes&inputtype=textquery&fields=place_id,name,formatted_address&key={key}')
# data = response.json()

# result = {
#     'name': data['candidates'][0]['name'],
#     'address': data['candidates'][0]['formatted_address'],
#     'place_id': data['candidates'][0]['place_id']
# }

# #print(resp['place_id'])
# place = result['place_id']
# print(place)
# # #print(result['place_id'])
# time_res = get_id(f"{key}", place)
# print(time_res['populartimes'][0]['data'])


#place = Place(name=result['name'], address=result['address'], place_id=result['place_id'])

