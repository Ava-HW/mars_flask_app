import requests
import json
from datetime import datetime, timedelta

# Set up variables
api_key = 'DEMO_KEY'  # Replace with your own NASA API key for more requests
rover_name = 'perseverance'  # Change to 'opportunity' or 'spirit' if needed

# Get today's date in YYYY-MM-DD format
today_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')

# Define the endpoint and parameters
url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos'
params = {
    'earth_date': today_date,
    'api_key': api_key,
}

# Send the request to the API
response = requests.get(url, params=params)
print("Response received...")
data = response.json()


# Check if photos were found and print their URLs
photos = data.get('photos', [])
if photos:
    print("Photos received...")
    print(f"Photos taken by {rover_name} on {today_date}:")
    for photo in photos:
        print(photo['img_src'], photo['camera']['name'])
else:
    print(f"No photos found for {rover_name} on {today_date}.")
