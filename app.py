from __future__ import print_function
from flask import Flask, render_template, session
from flask_session import Session
from datetime import datetime, timedelta
import requests
import sys

api_key = "RjE7wCLmJXnlXVS8z6tyyJpe8G8dmXHgXIqafvAc"
curiosity_max = 0
perseverance_max = 0

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key'

Session(app)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/photos")
def photos():
    perseverance_photos = get_photos('perseverance')
    curiosity_photos = get_photos('curiosity')
    return render_template("photos.html", perseverance_photos=perseverance_photos, curiosity_photos=curiosity_photos, perseverance_max=perseverance_max, curiosity_max=curiosity_max)


def get_max_sol(rover_name):
    global curiosity_max
    global perseverance_max
    # make request to api for rover's first sol
    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol=1&api_key={api_key}'
    params ={
        'sol' : 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # convert json to dict
        data = response.json()
        # extract max_sol value
        max_sol = data['photos'][0]['rover']['max_sol']
        max_date = data['photos'][0]['rover']['max_date']
    else:
        print(f"ERROR: {response.status_code} - {response.reason}")
    if rover_name == "curiosity":
        curiosity_max = [max_sol, max_date]
        app.logger.debug(f"curiosity_max: {curiosity_max}")
    if rover_name == "perseverance":
        perseverance_max = [max_sol, max_date]
        app.logger.debug(f"perseverance_max: {perseverance_max}")

    return [max_sol, max_date]

def get_photos(rover_name):
    cache_key = f"{rover_name}_photos"
    if cache_key in session:
        return session[cache_key]
    # # get max_sol for the rover
    maxes = get_max_sol(rover_name)
    max_sol = maxes[0]
    max_date = maxes[1]
    app.logger.debug("This is a debug message")
    # print(f"Max sol for {rover_name}: {max_sol}")
    # print(f"Max date for {rover_name}: {max_date}")
    # Define the endpoint and parameters
    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol=4000&api_key=RjE7wCLmJXnlXVS8z6tyyJpe8G8dmXHgXIqafvAc'
    params = {
        'sol': max_sol,
        'api_key': api_key,
    }

    # Send the request to the API
    response = requests.get(url, params=params)
    print("Response received...")
    data = response.json()
    # Check if photos were found and print their URLs
    response = []
    photos = data.get('photos', [])
    if photos:
        print("Photos received...")
        print(f"Photos taken by {rover_name} on {max_sol}:")
        amount = 0
        for photo in photos:
            if amount <= 5:
                response.append({'image': photo['img_src'], 'camera_name': photo['camera']['name']})
                amount += 1
            else:
                break
    else:
        print(f"No photos found for {rover_name} on {max_date}.")
    print(curiosity_max, perseverance_max)

    # make re
    # if no photos for today, try the day before (get_photos(days_ago + 1)
    # returns list of dicts with image srcs, camera name, 
    session[cache_key] = response
    return response

# run command: flask --app app --debug run