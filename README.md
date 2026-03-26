# Weather-API-Flask

A simple Flask API that fetches real-time weather data for a city using the Open-Meteo API.

## Features

- Search for the weather by city name
- Get current temperature
- Get wind speed and wind direction
- Get weather condition code and description
- Return clean JSON responses

## Technologies Used

- Python
- Flask
- Requests
- Open-Meteo API

## Project Structure

```text
weather-api-flask/
│
├── app.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/denisaradu28/Weather-API-Flask.git
cd Weather-API-Flask
```

2. Install dependecies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```
The API will run locally at:
```bash
http://127.0.0.1:5000
```

## API Endpoints

### GET `/`
Check if the API is running.

**Response:**
```json
{
  "message": "Weather API is running",
  "endpoint": "/weather?city=Bucharest"
}
```

### GET '/weather?city=<city_name>'
Returns current weather data for a given city.

---

### Query Parameters

| Parameter | Type   | Required | Description        |
|----------|--------|----------|--------------------|
| city     | string | yes      | Name of the city   |

---

### Example Request

```text
GET /weather?city=Bucharest
```

### Example Response

```json
{
  "city": "Bucharest",
  "country": "Romania",
  "latitude": 44.4328,
  "longitude": 26.1043,
  "temperature_c": 18.2,
  "weather_code": 3,
  "weather_description": "Overcast",
  "wind_speed": 9.4,
  "wind_direction": 210,
  "is_day": 1,
  "time": "2026-03-27T12:00"
}
```

### Error Response (Missing city)

```json
{
  "error": "Missing required query parameter: city"
}
```

### Error Response (City not found)
```json
{
  "error": "City not found"
}
```
