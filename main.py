import csv
import networkx as nx
import matplotlib.pyplot as plt
# import cartopy as ccrs
from mpl_toolkits.basemap import Basemap
from vincenty import vincenty
import numpy as np

latitude_index = None
longitude_index = None
lats, lons = [],[]

# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.coastlines()
# USAlatlng = [38.9137131047308, -101.62419014841949]
# USAurcrnr = [49.36462470437136, -65.64982795964086]
# USAllcrnr = [26.957096614958083, -126.11052388959078]

# m = Basemap(
#         projection='merc',
#         resolution='l',
#         lat_0=USAlatlng[0],
#         lon_0=USAlatlng[1],
#         llcrnrlon=USAllcrnr[1],
#         llcrnrlat=USAllcrnr[0],
#         urcrnrlon=USAurcrnr[1],
#         urcrnrlat=USAurcrnr[0],
#         suppress_ticks=True)

# Save the plot by calling plt.savefig() BEFORE plt.show()
# plt.savefig('coastlines.pdf')
# plt.savefig('coastlines.png')

# plt.show()

with open('alt_fuel_stations (Feb 10 2022).csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # print(f'Column names are {", ".join(row)}')
        if line_count == 0:
            latitude_index = row.index('Latitude')  
            longitude_index = row.index('Longitude')
        else:
            lats.append(float(row[latitude_index]))
            lons.append(float(row[longitude_index]))
        line_count += 1
        # if line_count > 200: break
    

    
print(f'Processed {line_count} lines.')

map = Basemap(projection='merc', 
			llcrnrlat=min(lats), 
			urcrnrlat=max(lats), 
			llcrnrlon=min(lons), 
			urcrnrlon=max(lons),
			resolution='l')

mx,my = map(lons,lats)
maxx = max(mx)
maxy = max(my)
minx = min(mx)
miny = min(my)
# for i in range(len(mx)):
#     if maxx > mx[i]: maxx = mx[i]
#     if maxy > my[i]: maxy = my[i]
#     if minx < mx[i]: minx = mx[i]
#     if miny < my[i]: miny = my[i]

GSF = 100000
w, h = int((maxx - minx)/GSF)+1, int((maxy - miny)/GSF)+1
print(f'width is {w} and height is {h}')
matrix = [[0 for x in range(w)] for y in range(h)] 
print(f'matrix is {len(matrix)} by {len(matrix[0])}')

for i in range(len(mx)):
	# print(f'touching index {int((mx[i] - minx)/GSF)} and {int((my[i] - miny)/GSF)}')
	matrix[int((my[i] - miny)/GSF)][int((mx[i] - minx)/GSF)] += 1


print(f'MAXES ARE X:{maxx} Y:{maxy}')
print(f'MINES ARE X:{minx} Y:{miny}')
print(f'sum of matrix is {sum(sum(matrix,[]))}')
# print(matrix)
# print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))

fig, ax = plt.subplots()

# ax.scatter(mx, my)

lldistance = vincenty((lats[0], lons[0]), (lats[1], lons[1]))
print(f'lldistance is {lldistance}')
xydistance = ((mx[1] - mx[0])**2 + (my[1] - my[0])**2)**0.5
print(f'xydistance is {xydistance}')
xyPerKm = xydistance/lldistance
print(f'xy distance per km is {xyPerKm}')
print(f'each square is {GSF/xyPerKm}km^2')

cellxs = []
cellys = []
cellcount = []

for i in range(h):
	for j in range(w):
		if matrix[i][j] > 0:
			cellxs.append(i * GSF + GSF/2)
			cellys.append(j * GSF + GSF/2)
			cellcount.append(matrix[i][j])

print('completed cell matrix')

map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)

map.scatter(cellys, cellxs)

# parallels = np.linspace(min(lats), max(lats), num=h)
# map.drawparallels(parallels)

plt.show()