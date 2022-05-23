import csv
from statistics import mode
import string
import requests

file = open('./ev_stations_v1.csv', encoding='utf-8')

csvreader = csv.reader(file)
APIkey = ""
header = []
header = next(csvreader)
print(header)
print("\n")
rows = []
latLngObjs = []
i = header.index("Latitude")
for row in csvreader:
    rows.append(row)
    
class LatLng:    
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude        
    def printLatLng():
        print(f'lat:  long:')    
    
for i in range(len(rows)):
    obj = LatLng(rows[i][header.index("Latitude")], rows[i][header.index("Longitude")])
    obj.printLatLng
    latLngObjs.append(obj)
    
payload = {}
headers = {}
print(latLngObjs[0].latitude + latLngObjs[0].longitude)
print(latLngObjs[1].latitude + latLngObjs[1].longitude)

url = f"https://maps.googleapis.com/maps/api/directions/json?origin={latLngObjs[0].latitude},{latLngObjs[0].longitude}&destination={latLngObjs[1].latitude},{latLngObjs[1].longitude}&mode=driving&key={APIkey}"
response = requests.request("GET", url, headers=headers, data=payload)
print(url)
print(response.text)



    
