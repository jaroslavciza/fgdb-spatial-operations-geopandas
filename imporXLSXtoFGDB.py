#Skript na vytvoreni feature class ve FGDB z XLSX s GPS souradnicemi (popripade import z DB)

import pandas as pd
import geopandas as gpd
from tkinter import filedialog

#import fiona

# vstupní proměnné
working_dir = "./_data/"
geodatabase_name = 'output.gdb'
feature_class_name = 'zpv'
xlsx_file = ''

xlsx_file = filedialog.askopenfilename(initialdir = working_dir)

if xlsx_file == "":
    xlsx_file = working_dir + 'zpv.xlsx'

# Načtení XLSX souboru pomocí Pandas
df = pd.read_excel(xlsx_file)

# Vytvoření GeoDataFrame
zpv_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['GPS_E'], df['GPS_N']), crs='EPSG:4326')  #WGS84 = 4326
zpv_gdf_buffer = zpv_gdf.to_crs(epsg=5514)  # Projekce geometrií na vhodný CRS
                                            # UTM (EPSG:32633)  
                                            # WGS84 (EPSG:4326)
                                            # S-JTSK Krovak East North (EPSG:5514) 
# Vytvoření bufferu 500 metrů kolem bodů
buffer_radius = 500  # v metrech
zpv_gdf_buffer['geometry'] = zpv_gdf_buffer['geometry'].buffer(buffer_radius)

# Vytvoření souborové geodatabáze a zapsani bodové vrstvy
zpv_gdf.to_file(f'{working_dir}{geodatabase_name}', driver='OpenFileGDB', layer = "zpv")
zpv_gdf_buffer.to_file(f'{working_dir}{geodatabase_name}', driver='OpenFileGDB', layer = "zpv_buffer_500m")

# print (fiona.supported_drivers)