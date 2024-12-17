# Mars Photos Flask App
#### Video Demo:  <URL HERE>

## __Welcome to Mars Photos!__

This Flask app takes the latest photos of Mars from [NASA's Open APIs](https://api.nasa.gov/) and displays them. I have used the Python requests module to make an API request. I have also used the Bootstrap framework to style my website. The API updates every few days, so check back soon for fresh images! Read below for explanations of each route. 

# /index
This route displays the homepage of my app. Facts and images of the Mars rovers are displayed using Bootstrap featurettes. 

# /photos
This page displays the photos taken by NASA's rovers on Mars! Jinja templating is used to loop through the list of photos returned from the API request and display them in Bootstrap carousels. Images from Perseverance and Curiosity are displayed in separate carousels. The date the photos were taken on is also displayed. 

# /about
This route provides the link to the API where the images are sourced from. 

# /cats
This route displays a photo of Felicity and Erik, two people who were instrumental in creating this project. 

# Credits
The images displayed in this app are from [NASA's Open APIs](https://api.nasa.gov/). 
Cover image on home page: [Perseverance’s Selfie With ‘Cheyava Falls’](https://science.nasa.gov/resource/perseverances-selfie-with-cheyava-falls)





