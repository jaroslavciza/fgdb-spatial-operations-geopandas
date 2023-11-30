import pandas as pd
import geopandas as gpd
#import tkinter as tk
from tkinter import filedialog

#import fiona

# vstupní proměnné
working_dir = "./_data/"
geodatabase_name = 'output.gdb'
feature_class_name = 'zpv'
xlsx_file = ''

#xlsx_file = filedialog.askopenfilename(initialdir = working_dir)

if xlsx_file == "":
    xlsx_file = working_dir + 'zpv.xlsx'

#print (xlsx_file)
# Načtení XLSX souboru pomocí Pandas
df = pd.read_excel(xlsx_file)

# Vytvoření GeoDataFrame
zpv_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['GPS_E'], df['GPS_N']), crs='EPSG:4326')  #WGS84 = 4326

# Vytvoření bufferu 500 metrů kolem bodů
buffer_radius = 500  # v metrech
zpv_gdf_buffer = zpv_gdf.to_crs(epsg=32633)  # Projekce geometrií na vhodný CRS (např. UTM)
zpv_gdf_buffer['geometry'] = zpv_gdf_buffer['geometry'].buffer(buffer_radius)

# print (fiona.supported_drivers)

# Vytvoření souborové geodatabáze a zapsani bodové vrstvy
zpv_gdf.to_file(f'{working_dir}{geodatabase_name}', driver='OpenFileGDB', layer = "zpv")
zpv_gdf_buffer.to_file(f'{working_dir}{geodatabase_name}', driver='OpenFileGDB', layer = "zpv_buffer_500m")