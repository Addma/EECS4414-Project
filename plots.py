from asyncio.windows_events import NULL
import csv
from ctypes.wintypes import INT
from email.mime import base
from statistics import mode
import string
from tkinter.font import names
from numpy import number
import requests
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap as Basemap
import haversine as hs
import numpy as np
import time

names = ('Latitude,Longitude,''State').split(',')
df = pd.read_csv('./ev_stations.csv', dtype='unicode')
APIkeyBing = "At2ioRmDqk1dOlhUJWyPqLTJbFlT7b58k97kRT6B7_HRNXaMAJStS-IgN167LVjK"
CAlatLng = [37.23585350702396, -119.87477641547004]
AKlatlng = [65.91557839885878, -150.94801773210332]
USAlatlng = [38.9137131047308, -101.62419014841949]
USAurcrnr = [49.36462470437136, -65.64982795964086]
USAllcrnr = [26.957096614958083, -126.11052388959078]

def getDistLatLng(lat1, lat2, long1, long2):
    return hs.haversine((float(lat1),float(long1)), (float(lat2), float(long2)))

def makeBasemap(center, urcrnr, llcrnr):
    m = Basemap(
        projection='lcc',
        resolution='f',
        # Center coordinates
        lat_0=center[0],
        lon_0=center[1],
        llcrnrlon=llcrnr[1], 
        llcrnrlat=llcrnr[0],
        urcrnrlon=urcrnr[1],
        urcrnrlat=urcrnr[0],
        suppress_ticks=True)
    return m
G=nx.Graph()
allLat = df['Latitude'].tolist()
allLong = df['Latitude'].tolist()
base = makeBasemap(USAlatlng, USAurcrnr, USAllcrnr)
print(type(allLat))
lats = []
lons = []
for i in range(len(allLat)):
    lats.append(float(allLat[i]))
    lons.append(float(allLong[i]))
states = df['State'].tolist()
print(type(allLat[0]))
mx,my=base(lats, lons)
plt.show()
for i in range(100):
    G.add_node(states[i] + str(i), pos=(mx[i], my[i]))
nx.draw_networkx(G, nx.get_node_attributes(G,'pos'), node_size=100, node_color='blue', with_labels=True)
base.drawcounties()
base.drawstates()
base.bluemarble()
plt.show()
plt.savefig('usa.png')
if False==True:
    for i in range(len(states)):
        print(i)
        for j in range(len(states)):
            url = f"""http://dev.virtualearth.net/REST/v1/Routes?wp.1={lats[i]},{lons[i]}&wp.2={lats[j]},{lons[j]}
                &optimize=distance&avoid=tolls,&routeAttributes=routeSummariesOnly&distanceUnit=km&key={APIkeyBing}"""
            if j == i or states[i] != states[j]:
                continue
            dist = getDistLatLng(lats[i], lats[j], lons[i], lons[j])
            if  dist < 200:
                G.add_edge(states[i] + str(i), states[j] + str(j), weight=dist)

def plotState(state):
    G=nx.Graph()
    stations = df[df['State'] == state]
    Lat = stations['Latitude'].array
    Long = stations['Longitude'].array
    lats=Lat.tolist()
    lons=Long.tolist()
    m = makeBasemap(USAlatlng, USAurcrnr, USAllcrnr)
    for i in range(len(stations)):
        lats.append(float(Lat[i]))
        lons.append(float(Long[i]))
    
    mx,my=m(lats,lons)
# Iterate through all stations
    j = 1        
    for i in range(10):
        for j in range(10):
            if j == i:
                continue
            header={}
            payload={}
            url = f"""http://dev.virtualearth.net/REST/v1/Routes?wp.1={mx[i]},{my[i]}&wp.2={mx[j]},{my[j]}
            &optimize=distance&avoid=tolls,&routeAttributes=routeSummariesOnly&distanceUnit=km&key={APIkeyBing}"""
            G.add_node(state+str(i), pos=(mx[i], my[i]))
            G.add_node(state+str(j), pos=(mx[j], my[j]))
            # If the distance between coordinates are in range of an EV charge, then 
            if getDistLatLng(mx[i], mx[j], my[i], my[j]) < 200:
                resp = requests.request("GET", url, headers=header, data=payload).json()
                try:
                    dist = float(resp["resourceSets"][0]["resources"][0]["travelDistance"])
                    if dist < 200:
                        G.add_edge(state + str(i),state + str(i+1), weight=dist)
                except:
                    print(url)
    nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'),node_size=100, font_size=10, with_labels=True)
    m.drawcoastlines()
    m.drawcounties()
    m.drawstates()
    m.bluemarble()
    plt.show()
    

    