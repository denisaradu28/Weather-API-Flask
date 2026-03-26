from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city_name):
    params = {"name": city_name,
              "count": 1,
              "language": "en",
              "format": "json"
    }

    response = requests.get(GEOCODING_URL, params=params, timeout=10)

    if response.status_code != 200:
        return None, {
            "error":"Faild to fetch location data"
        }

    data = response.json()

    if "results" not in data or not data["results"]:
        return None, {
            "error":"City not found"
        }

    location = data["results"][0]

    return {
        "name":location.get("name"),
        "country":location.get("country"),
        "latitude":location.get("latitude"),
        "longitude":location.get("longitude"),
    }, None

def get_current_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code,wind_speed_10m,wind_direction_10m,is_day",
        "timezone": "auto"
    }

    response = requests.get(FORECAST_URL, params=params, timeout=10)

    if response.status_code != 200:
        return None, {
            "error":"Faild to fetch current weather data"
        }

    data = response.json()

    if "current" not in data:
        return None, {
            "error":"Weather data not found"
        }

    current = data["current"]

    return {
        "temperature_c": current.get("temperature_2m"),
        "weather_code": current.get("weather_code"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_direction": current.get("wind_direction_10m"),
        "is_day": current.get("is_day"),
        "time": current.get("time")
    }, None

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Weather API is running",
        "usage": "/weather?city=Bucharest"
    })

@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({
            "error":"Missing required query parameter: city"
        }), 400

    location, location_error = get_coordinates(city)

    if location_error:
        return jsonify(location_error), 404

    weather_data, weather_error = get_current_weather(
        location["latitude"],
        location["longitude"]
    )

    if weather_error:
        return jsonify(weather_error), 502

    result = {
        "city": location["name"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "temperature_c": weather_data["temperature_c"],
        "weather_code": weather_data["weather_code"],
        "wind_speed": weather_data["wind_speed"],
        "wind_direction": weather_data["wind_direction"],
        "is_day": weather_data["is_day"],
        "time": weather_data["time"]
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)