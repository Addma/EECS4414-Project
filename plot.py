import csv
from ctypes.wintypes import INT
from statistics import mode
import string
from numpy import number
import requests
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap as Basemap
import haversine as hs

file = open('./ev_stations.csv', encoding='utf-8')

csvreader = csv.reader(file)
APIkeyGoogle = "AIzaSyD6AHTjGsOAZEiQCGnHY-2xysWFmQjPjtM"
APIkeyBing = "At2ioRmDqk1dOlhUJWyPqLTJbFlT7b58k97kRT6B7_HRNXaMAJStS-IgN167LVjK"
header = []
header = next(csvreader)
rows = []
latLngObjs = []
i = header.index("Latitude")
for row in csvreader:
    rows.append(row)
    
class LatLng:    
    latitude=0
    longitude=0
    def __init__(self, latitude, longitude, state):
        self.latitude = latitude
        self.longitude = longitude        
        self.state = state
    def printLatLng(self):
        print(f'lat:{self.latitude}  long:{self.longitude}')    
    
 
payload = {}
headers = {}
for i in range(len(rows)):
    obj = LatLng(rows[i][header.index("Latitude")], rows[i][header.index("Longitude")], rows[i][header.index("State")])
    latLngObjs.append(obj)
def getDistLatLng(lat1, lat2, long1, long2):
    return hs.haversine((float(lat1),float(long1)), (float(lat2), float(long2)))

USAlatlng = [38.9137131047308, -101.62419014841949]
USAurcrnr = [49.36462470437136, -65.64982795964086]
USAllcrnr = [26.957096614958083, -126.11052388959078]
CAlatLng = ['37.23585350702396', '-119.87477641547004']
m = Basemap(
        projection='lcc',
        resolution='f',
        lat_0=USAlatlng[0],
        lon_0=USAlatlng[1],
        llcrnrlon=USAllcrnr[1],
        llcrnrlat=USAllcrnr[0],
        urcrnrlon=USAurcrnr[1],
        urcrnrlat=USAurcrnr[0],
        suppress_ticks=True)

# position in decimal lat/lon
lats=[]
lons=[]
for i in range(len(latLngObjs)):
    lats.append(float(latLngObjs[i].latitude))
    lons.append(float(latLngObjs[i].longitude))
print(lats, lons)
Gcali=nx.Graph()
pos={}
mx,my=m(lats,lons)
for i in range(len(latLngObjs)):
    Gcali.add_node(latLngObjs[i].state+str(i))
    pos[latLngObjs[i].state+str(i)] = (mx[i], my[i])

print(pos['CA0'])
print(pos['CA1'])
print(pos['CA31555'])
for i in range(100):
    print(i)
    for j in range(len(latLngObjs)):
        if latLngObjs[i].state != latLngObjs[j].state or i == j:
            continue
        dist = getDistLatLng(mx[i], mx[j],my[i],my[j])
        if dist < 200:
            Gcali.add_edge(latLngObjs[i].state+str(i), latLngObjs[j].state+str(j), weight=dist)
labels = nx.get_edge_attributes(Gcali, 'weight')
nodes = nx.get_node_attributes(Gcali, 'name')
nx.draw_networkx(Gcali, pos, node_size=100, node_color='blue', labels=labels)
m.drawcoastlines()
m.drawcounties()
m.drawstates()
m.bluemarble()
plt.show()
plt.savefig('usa.png')





    