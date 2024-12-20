import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

class Application:
    def __init__(self):
        self.graph = {}
        self.coords = {}

    def add_city(self, city, lat, lon):
        if city not in self.graph:
            self.graph[city] = []
            self.coords[city] = (lat, lon)

    def add_path(self, city1, city2, length):
        if city1 in self.graph and city2 in self.graph:
            self.graph[city1].append((city2, length))
            self.graph[city2].append((city1, length))

    def dijkstra(self, start):
        dist = {city: float('inf') for city in self.graph}
        dist[start] = 0
        queue = [(start, 0)]
        prev = {city: None for city in self.graph}

        while queue:
            curr_city, curr_dist = min(queue, key=lambda x: x[1])
            queue.remove((curr_city, curr_dist))

            if curr_dist > dist[curr_city]:
                continue

            for neighbor, length in self.graph[curr_city]:
                new_dist = curr_dist + length
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = curr_city
                    queue.append((neighbor, new_dist))

        return dist, prev

    def shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            print("City should exist. You can add the city.")
            return

        dist, prev = self.dijkstra(start)
        if dist[end] == float('inf'):
            print(f"No path from {start} to {end}.")
            return

        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = prev[curr]
        path.reverse()

        print(f"Shortest path: {start} -> {end} (length {dist[end]})")
        return path, dist[end]

    def draw_map(self, highlight_path=None):
        m = Basemap(projection='merc', llcrnrlat=39, urcrnrlat=43, llcrnrlon=69, urcrnrlon=81, resolution='i')
        m.drawcountries()
        m.drawcoastlines()
        m.fillcontinents(color='lightgreen', lake_color='aqua')
        m.drawmapboundary(fill_color='aqua')

        for city, (lat, lon) in self.coords.items():
            x, y = m(lon, lat)
            plt.plot(x, y, 'bo', markersize=5)
            plt.text(x, y, city, fontsize=9, ha='center')

        if highlight_path:
            path_coords = [self.coords[city] for city in highlight_path]
            path_x, path_y = zip(*[m(lon, lat) for lat, lon in path_coords])
            plt.plot(path_x, path_y, 'r-', linewidth=2)

        plt.title("PUTI Logistics Map")
        plt.show()

app = Application()

cities = {
    "Bishkek": (42.87, 74.59),
    "Osh": (40.53, 72.79),
    "Karakol": (42.48, 78.39),
    "Naryn": (41.43, 76.00),
    "Talas": (42.52, 72.23),
    "Batken": (40.06, 70.81),
    "Jalal-Abad": (40.93, 73.00),
    "Cholpon-Ata": (42.65, 77.08),
    "Tokmok": (42.84, 75.29),
    "Kant": (42.89, 74.85)
}

for city, (lat, lon) in cities.items():
    app.add_city(city, lat, lon)

paths = [
    ("Bishkek", "Osh", 600), ("Bishkek", "Tokmok", 70),
    ("Tokmok", "Kant", 20), ("Tokmok", "Cholpon-Ata", 200),
    ("Cholpon-Ata", "Karakol", 150), ("Osh", "Batken", 250),
    ("Osh", "Jalal-Abad", 100), ("Jalal-Abad", "Naryn", 300),
    ("Naryn", "Talas", 400), ("Talas", "Bishkek", 310),
    ("Bishkek", "Jalal-Abad", 400), ("Jalal-Abad", "Cholpon-Ata", 350),
    ("Karakol", "Naryn", 200), ("Batken", "Talas", 350),
    ("Osh", "Kant", 300), ("Cholpon-Ata", "Talas", 250),
    ("Naryn", "Batken", 450), ("Talas", "Kant", 200)
]

for city1, city2, length in paths:
    app.add_path(city1, city2, length)

print("PUTI Logistic Application!")
print("Cities we operate in:")

for city in cities.keys():
    print(city)

print("Our Routes:")

for city1, city2, distance in paths:
    print(f'{city1} --> {city2} {distance}km')

start_city = input("\nEnter the start city: ")
end_city = input("Enter the destination city: ")

short_path, path_length = app.shortest_path(start_city, end_city)
if short_path:
    app.draw_map(highlight_path=short_path)