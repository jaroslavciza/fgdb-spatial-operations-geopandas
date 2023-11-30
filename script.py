import random
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Seznam s názvy měst v České republice
cities = ["Praha", "Brno", "Ostrava", "Plzeň", "Liberec", "Olomouc", "České Budějovice", "Hradec Králové", "Ústí nad Labem", "Pardubice",
          "Zlín", "Jihlava", "Tábor", "Karlovy Vary", "Český Krumlov", "Kutná Hora", "Teplice", "Cheb", "Kladno", "Opava"]

# Slovník pro ukládání názvu města a jeho náhodných souřadnic
cities_points = {}

# Generování náhodných souřadnic pro každé město
for city in cities:
    latitude = round(random.uniform(48.5, 51.5), 6)  # Zeměpisná šířka
    longitude = round(random.uniform(12.5, 18.5), 6)  # Zeměpisná délka
    cities_points[city] = (latitude, longitude)

# Výpis vytvořeného slovníku
for city, coords in cities_points.items():
    print(f"{city}: {coords}")

# Vytvoření GeoDataFrame
geometry = [Point(lon, lat) for lat, lon in cities_points.values()]
gdf_cities = gpd.GeoDataFrame(geometry=geometry, index=cities, crs="EPSG:4326")  # WGS84 = 4326

# Stáhnutí mapy světa ze zadaného zdroje
world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Vytvoření mapy
ax = world_map.plot(figsize=(10, 6), color='lightgrey')

# Vykreslení bodů
gdf_cities.plot(ax=ax, marker='o', color='red', markersize=50)

# Přidání popisků
for city, (lon, lat) in cities_points.items():
    plt.text(lon, lat, city, fontsize=8)

# Nastavení titulu a zobrazení mapy
plt.title('Vizualizace pole bodů v České republice')
plt.show()
