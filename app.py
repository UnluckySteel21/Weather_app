from flask import (
    Flask,
    render_template,
    request,
    redirect
)
from requests import get
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/get_weather', methods=['GET', 'POST'])
def get_weather():
    if request.method == 'POST':
        try:
            city = request.form['city']
            days = request.form['days']

            # city -> coordinate
            #api_key = "ac54255fd4537cb0be0554fe603f1412"
            api_key = "ac54255fd4537cb0be0554fe603f1412"
            url_geo = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'
            req = get(url_geo)

            if req.status_code != 200:
                return render_template("layout.html",text="Neizdevās ielādēt datus")
            
            geodata = req.json()[0]
            lat = geodata["lat"]
            lon = geodata["lon"]
            place = geodata["name"]
            country = geodata["country"]

            # coordinate -> weather
            if days == "1":
                url_weather = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=la'

                req = get(url_weather)

                if req.status_code != 200:
                    return render_template("layout.html",text="Neizdevās ielādēt datus")
                
                weatherdata = req.json()
                temperature = weatherdata['main']['temp']
                apraksts = weatherdata['weather'][0]['description']
                icon = weatherdata['weather'][0]['icon']
                icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

                search_rez = {
                    "temperature": temperature,
                    "apraksts": apraksts,
                    "icon": icon_url,
                    "place" : place,
                    "country" : country
                }

                return render_template("layout.html",search_rez=search_rez)
            elif days == "5":
                url_weather = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=la'
                req = get(url_weather)

                if req.status_code != 200:
                    return render_template("layout.html",text="Neizdevās ielādēt datus")
                
                weatherdata = req.json()
                forecast = []

                for item in weatherdata['list']:
                    if item['dt_txt'].split()[1] == '12:00:00':  # Check if the time matches
                        icon = item['weather'][0]['icon']
                        icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
                        forecast.append({
                            'date': item['dt_txt'].split()[0],
                            'temp': item['main']['temp'],
                            'description': item['weather'][0]['description'],
                            'icon': icon_url,
                            'place' : place,
                            'country' : country
                        })

                return render_template("layout.html", forecast=forecast)
        except:
            return render_template("layout.html",text="Neizdevās ielādēt datus")
    else:
        ...
    


if __name__ == '__main__':
    app.run(debug=True)