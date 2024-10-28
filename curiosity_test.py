from datetime import datetime, timedelta
import requests

api_key = "RjE7wCLmJXnlXVS8z6tyyJpe8G8dmXHgXIqafvAc"

curiosity_max = 0
perseverance_max = 0

def get_max_sol(rover_name):
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
    if rover_name == "perseverance":
        perseverance_max = [max_sol, max_date]
    return [max_sol, max_date]



def get_photos(days_ago, rover_name):
    # # get max_sol for the rover
    maxes = get_max_sol(rover_name)
    max_sol = maxes[0]
    max_date = maxes[1]
    print(f"Max sol for {rover_name}: {max_sol}")
    print(f"Max date for {rover_name}: {max_date}")

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



    
def main():
    get_photos(1, 'perseverance')
    get_photos(1, 'curiosity')


if __name__ == "__main__":
    main()