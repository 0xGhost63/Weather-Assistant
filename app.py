from flask import Flask,render_template,request
from dotenv import load_dotenv
import os
import requests
 
#Loading the API from the env file ---> make sure to add youe API key in the 
#.env file in the variable OPENWEATHER_API_KEY to make the app work !!!
load_dotenv()
WEATHER_API_KEY=os.getenv("OPENWEATHER_API_KEY")
IMAGES_API_KEY=os.getenv("PIXABAY_API_KEY")


app=Flask(__name__)

@app.route("/")
def home():
    
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    city = request.form.get("city")

    #WEATHER !

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(weather_url)
    if response.status_code==200:    
        weather_data = response.json()
    else:
        weather_data="Invalid City"

    #IMAGE Section
    if weather_data=="Invalid City":
        city="sarcastic+funny+fail"
    else:
        city=city
        
    pixabay_url= f"https://pixabay.com/api/?key={IMAGES_API_KEY}&q={city}+landmark&image_type=photo&per_page=5"
    pixabay_data = requests.get(pixabay_url).json()

    city_image = ""
    if pixabay_data["hits"]:
        # pick a random landmark from top 5 results
        import random
        city_image= random.choice(pixabay_data["hits"])["largeImageURL"]
    print(city_image) 

    return render_template("index.html", weather=weather_data,city_image=city_image)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # use Railway's PORT
    app.run(host="0.0.0.0", port=port, debug=False)