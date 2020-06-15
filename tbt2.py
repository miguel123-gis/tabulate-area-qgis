import os
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame

os.chdir(r'C:\Users\imper\Documents\new_GISfiles\tabulateArea_forQGIS\\')
gdf1 = gpd.read_file('camSur_municities.shp')
gdf2 = gpd.read_file('camSur_landCover_2003.shp')

for i in range(gdf1.shape[0]):
    muni = gdf1.loc[gdf1['NAME_2'] == gdf1['NAME_2'][i]]
    intersection = gpd.overlay(muni, gdf2, how='intersection')
    area = intersection['geometry'].map(lambda p: p.area)
    type_in = intersection['DESCRIPT'].values
    df1 = area.to_frame()
    df1.insert(0, 'type', type_in)
    df1.rename(columns={'geometry':'sqm'}, inplace=True)
    df2 = df1.groupby(['type']).sum()
    print(df2)

# Still working on the final CSV with the results from all 39 municipalities
cols = gdf2.DESCRIPT.unique()
rows = gdf1['NAME_2'].values
df3 = pd.DataFrame([range(len(cols))], range(len(rows)))
df3.columns = cols
cols.sort()
df3.insert(0, 'zones', rows)
df3 = pd.concat([df2, df3])
df3 = df3.reset_index(drop=True)
print(df3)

