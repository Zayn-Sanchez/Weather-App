from flask import Flask, request
import requests
import json
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

def get_weather(city):
    api_key = "4b04fd4ec399f4cbbe1fe0a2fea7a27b"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = json.loads(response.text)
    return data

def get_forecast(city):
    api_key = "4b04fd4ec399f4cbbe1fe0a2fea7a27b"
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = json.loads(response.text)
    return data

@app.route('/', methods=['GET', 'POST'])
def weather():
    city = 'London'
    message = ''
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        if weather_data.get('cod') == '404':
            message = 'City not found. Please try again.'
            city = 'London'
            weather_data = get_weather(city)
    weather_data = get_weather(city)
    forecast_data = get_forecast(city)
    if forecast_data.get('cod') != '200':
        forecast_dict = {}
        message = 'Error fetching forecast.'
    else:
        forecast_list = forecast_data['list']
        forecast_dict = defaultdict(list)
        for forecast in forecast_list:
            date = forecast['dt_txt'].split(' ')[0]  
            forecast_dict[date].append(forecast)

    forecast_str = '<h2>Forecast:</h2>'
    temp_c = 'N/A'
    description = 'N/A'
    for date, forecasts in forecast_dict.items():
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A %d ").lstrip("0") + datetime.strptime(date, "%Y-%m-%d").strftime("%B")
        forecast_str += f'<div class="day"><h3>{formatted_date}</h3><div class="forecasts">'
        for forecast in forecasts:
            time = datetime.strptime(forecast['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            short_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
            temp_k = forecast['main']['temp']
            temp_c = round(temp_k - 273.15)
            description = forecast['weather'][0]['description']
            icon = forecast['weather'][0]['icon']
            forecast_str += f'<div class="forecast"><img src="http://openweathermap.org/img/w/{icon}.png" alt="{description}"><p>{short_date}<br>{time}<br>{temp_c}°C<br>{description}</p></div>'
        forecast_str += '</div></div>'

    return f"""
    <html>
        <head>
            <title>Weather App</title>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    max-width: 800px;
                    margin: auto;
                    padding: 20px;
                    background-color: #FFFFFF;
                }}
                .day {{
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                    margin-bottom: 20px;
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    padding: 15px;
                    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                }}
                .forecasts {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: nowrap;
                    overflow-x: auto;
                }}
                .forecast {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    margin: 10px;
                    text-align: center;
                    border-radius: 10px;
                    background: #f9f9f9;
                    min-width: 120px;
                }}
                .forecast img {{
                    width: 50px;
                    height: 50px;
                }}
                form {{
                    margin-bottom: 20px;
                }}
                input[type="text"] {{
                    padding: 10px;
                    border: 1px solid #ddd;
                    width: 70%;
                    border-radius: 10px;
                }}
                input[type="submit"] {{
                    padding: 10px 20px;
                    border: none;
                    color: white;
                    background: #007BFF;
                    border-radius: 10px;
                }}
                h1, h2, h3 {{
                    color: #007BFF;
                }}
                p {{
                    color: #666666;
                }}
            </style>
        </head>
        <body>
            <h1>Welcome to the Weather App</h1>
            <form method="POST">
                <input type="text" name="city" placeholder="Enter city">
                <input type="submit" value="Get Weather">
            </form>
            <p>{message}</p>
            <p>Weather for {city}: </p>
            <p>Temperature: {temp_c if temp_c != 'N/A' else temp_c}°C</p>
            <p>Description: {description}</p>
            {forecast_str}
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
