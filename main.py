import csv
import networkx as nx
import matplotlib.pyplot as plt
# import cartopy as ccrs
from mpl_toolkits.basemap import Basemap
from vincenty import vincenty
import numpy as np
import networkx as nx

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

# GSF = 122500 #100km squares
GSF = 60000 #50km squares
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
print(f'each square is {GSF/xyPerKm} side length')

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

# Make the graph of adjacent nodes
g = nx.Graph()
print(f'average for color determination is: {sum(cellcount)/len(cellcount)}')

for i in range(h):
    for j in range(w):
        if(matrix[i][j] > 0):
            c = (0, min(1, matrix[i][j]/(sum(cellcount)/len(cellcount))), 0.5)
            g.add_node((i,j), pos=(j,i), color=c)
            if(i+1 < h and matrix[i+1][j] > 0):
                g.add_node((i+1,j), pos=(i+1,j), color=c)
                g.add_edge((i,j), (i+1, j))
            if(j+1 < w and matrix[i][j+1] > 0):
                g.add_node((i,j+1), pos=(i,j+1), color=c)
                g.add_edge((i,j), (i, j+1))
        # print(f'{matrix[i][j]} ', end='')
    # print('')

print(g)
pos = nx.get_node_attributes(g, 'pos')
colors = list(nx.get_node_attributes(g, 'color').values())
nx.draw(g, node_size=50, pos=pos, node_color='lightgreen')
CC = sorted(nx.connected_components(g), key=len, reverse=True)

GCC = g.subgraph(CC[0])
nx.draw(GCC, node_size=50, pos=pos)
GCC2 = g.subgraph(CC[1])
nx.draw(GCC2, node_size=50, node_color='red', pos=pos)

# Returns a copy of graph with new node at x y 
def addNode(graph, x, y):
    gcopy = nx.Graph(graph)
    gcopy.add_node((x, y), pos=(y, x), color=(1, 0, 0))
    if(x-1 >= 0 and matrix[x-1][y] > 0):
        gcopy.add_edge((x,y), (x-1, y))
    if(x+1 < h and matrix[x+1][y] > 0):
        gcopy.add_edge((x,y), (x+1, y))
    if(y-1 >= 0 and matrix[x][y-1] > 0):
        gcopy.add_edge((x,y), (x, y-1))
    if(y+1 < w and matrix[x][y+1] > 0):
        gcopy.add_edge((x,y), (x, y+1))
    return gcopy

# Returns the biggest 
def getBiggerGCC(g, h):
    cc = sorted(nx.connected_components(g), key=len, reverse=True)
    gcc = g.subgraph(cc[0])
    cc = sorted(nx.connected_components(h), key=len, reverse=True)
    hcc = h.subgraph(cc[0])
    ret = max(gcc, hcc, key=len)
    return ret

biggestGCC = nx.complete_graph(1)
for x in range(h):
    for y in range(w):
        if(matrix[x][y] == 0): #if this spot is empty...
            if((x+1 < h and matrix[x+1][y] > 0) or
                (x-1 >= 0 and matrix[x-1][y] > 0) or
                (y+1 < w and matrix[x][y+1] > 0) or 
                (y-1 >= 0 and matrix[x][y-1] > 0)): #if empty spot has at least 1 live neighbour...
                    test = addNode(g, x, y)
                    biggestGCC = getBiggerGCC(biggestGCC, test)

plt.figure()
nx.draw(g, node_size=50, pos=pos, node_color='lightgreen')
biggestGCCpos = nx.get_node_attributes(biggestGCC, 'pos')
nx.draw(biggestGCC, node_size=50, pos=biggestGCCpos, node_color='red')
nx.draw(GCC, node_size=50, node_color='blue', pos=pos)

plt.figure()
nx.draw(g, node_size=50, pos=pos, node_color=colors)


plt.figure()
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)

map.scatter(cellys, cellxs)

# parallels = np.linspace(min(lats), max(lats), num=h)
# map.drawparallels(parallels)

plt.show()