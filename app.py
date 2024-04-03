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
        city = request.form['city']

        # city -> coordinate
        api_key = "ac54255fd4537cb0be0554fe603f1412"
        url_geo = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'
        req = get(url_geo)
        geodata = req.json()[0]

        lat = geodata["lat"]
        lon = geodata["lon"]

        # coordinate -> weather
        url_weather = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=la'
        req = get(url_weather)
        weatherdata = req.json()
        temperature = weatherdata['main']['temp']
        apraksts = weatherdata['weather'][0]['description']
        icon = weatherdata['weather'][0]['icon']

        print(temperature, apraksts, icon)

        return redirect("/")
    else:
        ...
    


if __name__ == '__main__':
    app.run(debug=True)