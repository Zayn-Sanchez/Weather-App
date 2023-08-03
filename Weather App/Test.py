import requests

response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=London&appid=4b04fd4ec399f4cbbe1fe0a2fea7a27b')
data = response.json()

print(data)
