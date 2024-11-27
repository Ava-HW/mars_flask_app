from __future__ import print_function
from flask import Flask, render_template, session
from flask_session import Session
from datetime import datetime, timedelta
import requests
import sys
import os

api_key = "RjE7wCLmJXnlXVS8z6tyyJpe8G8dmXHgXIqafvAc"

curiosity_max_date = 0
perseverance_max_date = 0

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key'

Session(app)

# clears session files every time the app starts

def clear_session_files():
    session_dir = os.path.join(app.root_path, 'flask_session')
    if os.path.exists(session_dir):
        for file in os.listdir(session_dir):
            file_path = os.path.join(session_dir, file)
            try:
                os.remove(file_path)
                app.logger.info(f"Deleted session file: {file_path}")
            except Exception as e:
                app.logger.error(f"Failed to delete {file_path}: {e}")

clear_session_files()

# formats dates
def format_date(max_date):
    date_obj = datetime.strptime(max_date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%#d %B %Y")  # %#d removes leading zero
    print(formatted_date)
    return formatted_date

# renders index.html
@app.route("/")
def index():
    return render_template("index.html")

# renders about.html
@app.route("/about")
def about():
    return render_template('about.html')

# renders cats.html
@app.route("/cats")
def cats():
    return render_template('cats.html')

# renders photos.html and calls function to get photos from api
@app.route("/photos")
def photos():
    perseverance_photos = get_photos('perseverance')
    curiosity_photos = get_photos('curiosity')
    return render_template("photos.html", perseverance_photos=perseverance_photos, curiosity_photos=curiosity_photos, perseverance_max=perseverance_max_date, curiosity_max=curiosity_max_date)


# gets the most recent sol that each rover has photos for
def get_max_sol(rover_name):
    global curiosity_max_date, perseverance_max_date
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
    # sets Curiosity's max_date
    if rover_name == "curiosity":
        curiosity_max = [max_sol, max_date]
        curiosity_max_date = format_date(max_date)
        app.logger.debug(f"curiosity_max: {curiosity_max}")
    # sets Perseverance's max_date
    if rover_name == "perseverance":
        perseverance_max = [max_sol, max_date]
        perseverance_max_date = format_date(max_date)
        app.logger.debug(f"perseverance_max: {perseverance_max}")

    return [max_sol, max_date]


def get_photos(rover_name):
    cache_key = f"{rover_name}_photos"
    # checks if rover's photos are already in the cache
    if cache_key in session:
        return session[cache_key]
    # get max_sol for the rover
    maxes = get_max_sol(rover_name)
    max_sol = maxes[0]
    max_date = maxes[1]
    # Define the API url and parameters
    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?&api_key=RjE7wCLmJXnlXVS8z6tyyJpe8G8dmXHgXIqafvAc'
    params = {
        'sol': max_sol,
        'api_key': api_key,
    }

    # Send the request to the API
    response = requests.get(url, params=params)
    print("Response received...")
    data = response.json()
    # Check if photos were found and add to list of photos
    response = []
    photos = data.get('photos', [])
    if photos:
        for photo in photos:
            response.append({'image': photo['img_src'], 'camera_name': photo['camera']['name']})
    else:
        print(f"No photos found for {rover_name} on {max_date}.")
    # returns list of dicts with image srcs, camera name,
    session[cache_key] = response
    return response

# run command: python -m flask --app app --debug run