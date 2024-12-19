# Mars Photos Flask App
#### Video Demo:  <URL HERE>

## __Welcome to Mars Photos!__

This Flask app takes the latest photos of Mars from [NASA's Open APIs](https://api.nasa.gov/) and displays them using HTML and Jinja templating. I have used the Python requests module to make an API request. I have also used the Bootstrap framework to style my website. The API updates every few days, so check back soon for fresh images! Read below for explanations of each route. 

## /index
This route displays the homepage of my app. Facts about and images of the Mars rovers are displayed using Bootstrap featurettes. The header of this page features a button that prompts the user to visit the photos page.

<img src="https://github.com/user-attachments/assets/82eebe27-b1a1-40b3-a63a-126664824889" alt="homepage" width="50%">

Homepage

## /photos
This page displays the photos taken by NASA's rovers on Mars! Jinja templating is used to loop through the list of photos returned from the API request and display them in Bootstrap carousels. Images from Perseverance and Curiosity are displayed in separate carousels. The date the photos were taken on is also displayed. There is also an explanation of where the images are from. 

<img src="https://github.com/user-attachments/assets/79fe99d2-a9c4-4c28-958b-67e244231cfd" alt="drawing" width="50%"/>

Photos page with explanation and carousel

```
 <div id="perseveranceCarousel" class="carousel slide" data-interval="false">
    <div class="carousel-inner">
      {% for i in perseverance_photos | batch(3) %}
      <div class="carousel-item {% if loop.first %}active{% endif %}">
        <div class="row">
          {% for photo in i %}
          <div class="col-md-4 col-sm-12">
            <img src="{{ photo['image'] }}" class="d-block w-100 resizable-image" alt="Perseverance Photo">
          </div>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
    </div>
```
Jinja syntax used to render carousels

## /about
This route provides the link to the API where the images are sourced from and credits the cover image on the home page. 

<img src="https://github.com/user-attachments/assets/89da87a7-9bc8-4f3c-b8bd-235827a408d0" alt="About page" width = 50%>

About page

## /cats
This route displays a photo of Felicity and Erik, creatures who were instrumental in creating this project. You can only access this route by folllowing the link in the About page. This easter egg is for committed fans of Mars and cats!

<img src="https://github.com/Ava-HW/mars_flask_app/blob/master/static/images/20240731_151317.jpg" width = 40%>

## Credits
The images displayed in this app are from [NASA's Open APIs](https://api.nasa.gov/). <br>
Cover image on home page: [Perseverance’s Selfie With ‘Cheyava Falls’](https://science.nasa.gov/resource/perseverances-selfie-with-cheyava-falls)





