from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def weather_code_to_description(code):
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        95: "Thunderstorm"
    }
    return weather_descriptions.get(code, "Unknown")


def get_coordinates(city_name):
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    if response.status_code != 200:
        return None, {"error": "Failed to fetch location data"}

    data = response.json()
    if "results" not in data or not data["results"]:
        return None, {"error": "City not found"}

    location = data["results"][0]
    return {
        "name": location.get("name"),
        "country": location.get("country"),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude")
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
        return None, {"error": "Failed to fetch weather data"}

    data = response.json()
    if "current" not in data:
        return None, {"error": "Weather data not available"}

    current = data["current"]
    return {
        "temperature_c": current.get("temperature_2m"),
        "weather_code": current.get("weather_code"),
        "weather_description": weather_code_to_description(current.get("weather_code")),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_direction": current.get("wind_direction_10m"),
        "is_day": current.get("is_day"),
        "time": current.get("time")
    }, None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Missing required query parameter: city"}), 400

    location, location_error = get_coordinates(city)
    if location_error:
        return jsonify(location_error), 404

    weather_data, weather_error = get_current_weather(
        location["latitude"],
        location["longitude"]
    )
    if weather_error:
        return jsonify(weather_error), 502

    return jsonify({
        "city": location["name"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "temperature_c": weather_data["temperature_c"],
        "weather_code": weather_data["weather_code"],
        "weather_description": weather_data["weather_description"],
        "wind_speed": weather_data["wind_speed"],
        "wind_direction": weather_data["wind_direction"],
        "is_day": weather_data["is_day"],
        "time": weather_data["time"]
    })


if __name__ == "__main__":
    app.run(debug=True)