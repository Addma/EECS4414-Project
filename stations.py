
import requests

APIkey = ''
f = open('ev_stations.csv', 'w', encoding='utf-8')
url = f'https://developer.nrel.gov/api/alt-fuel-stations/v1.csv?api_key={APIkey}&fuel_type=ELEC&limit=all'
request = requests.request("GET", url)
f.write(request.text)
