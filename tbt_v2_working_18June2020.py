import os
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame

os.chdir(r'C:\Users\imper\Documents\new_GISfiles\tabulateArea_forQGIS\\')
gdf1 = gpd.read_file('camSur_municities.shp') 
gdf2 = gpd.read_file('camSur_landCover_2003.shp')
data = []
for a in range(gdf1.shape[0]):
    muni = gdf1.loc[gdf1['NAME_2'] == gdf1['NAME_2'][a]] # muni index
    intersection = gpd.overlay(muni, gdf2, how='intersection') # intersection operation
    area = intersection['geometry'].map(lambda p: p.area) # calculates area of intersection
    type_in = intersection['DESCRIPT'].values.tolist() # types in muni
    type_all = gdf2['DESCRIPT'].values.tolist()
    type_all_uniq = []
    for i in type_all:
        if i not in type_all_uniq: # checks if type is in type_all
            type_all_uniq.append(i)
    type_out = set(type_all_uniq) - set(type_in)
    type_out = list(type_out)
    df1 = area.to_frame() # converts area to dataframe
    df1.insert(0, 'type', type_in) # insert types
    df1.rename(columns={'geometry':'sqm'}, inplace=True) # renames geom col
    df2 = df1.groupby(['type']).sum() # groups same types
    df2 = df2.reset_index(drop=False) # adds index
    index = df2.index # sets index title
    index.name = gdf1['NAME_2'].values[a]
    for i in type_out:
        df2.loc[len(df2), 'type'] = i
    df2.sort_values(by=['type'], inplace=True)
     # muni is index title
    df2_tpd = df2.T
    values = list(df2_tpd.loc['sqm'].values)
    data.append(values)
cols = gdf2.DESCRIPT.unique() # gets land use types
cols.sort() # sorts cols alphaetically
rows = gdf1['NAME_2'].values # gets munis
df3 = pd.DataFrame(data, columns = cols) # creates df
df3.insert(0, 'zones', rows) # creates df's rows
df3.to_csv('CamarinesSur_munis_landCover_tabulated.csv')