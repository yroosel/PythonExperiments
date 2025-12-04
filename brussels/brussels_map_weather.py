from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# WeatherAPI key (user's key)
API_KEY = 'YOUR API KEY 7974a3f19d4c41b08155316242609'
CURRENT_WEATHER_URL = 'http://api.weatherapi.com/v1/current.json'
FORECAST_URL = 'http://api.weatherapi.com/v1/forecast.json'

# City for weather data
CITY = 'Brussels'

@app.route('/')
def map_page():
    return render_template('map.html')

@app.route('/weather')
def weather_page():
    try:
        # Fetch current weather
        current_params = {
            'key': API_KEY,
            'q': CITY,
            'aqi': 'no'  # Air Quality Index is optional
        }
        current_response = requests.get(CURRENT_WEATHER_URL, params=current_params)
        current_response.raise_for_status()
        current_weather = current_response.json()

        # Fetch 3-day weather forecast
        forecast_params = {
            'key': API_KEY,
            'q': CITY,
            'days': 3,  # Number of days for forecast
            'aqi': 'no',  # Air Quality Index is optional
            'alerts': 'no'  # Weather alerts optional
        }
        forecast_response = requests.get(FORECAST_URL, params=forecast_params)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Extract 3-day forecast
        daily_forecast = forecast_data['forecast']['forecastday']

        return render_template('weather.html', current=current_weather, daily=daily_forecast)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return f"Error fetching weather data: {e}"

if __name__ == '__main__':
    app.run(debug=True)
