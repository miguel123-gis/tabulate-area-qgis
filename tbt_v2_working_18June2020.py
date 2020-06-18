import os
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame
os.chdir(r'C:\Users\imper\Documents\new_GISfiles\tabulateArea_forQGIS\\')

gdf1 = gpd.read_file('camSur_municities.shp') 
gdf2 = gpd.read_file('camSur_landCover_2003.shp')

data = [] # list of lists of sqm values per muni
for a in range(gdf1.shape[0]):
    muni = gdf1.loc[gdf1['NAME_2'] == gdf1['NAME_2'][a]] # muni index
    intersection = gpd.overlay(muni, gdf2, how='intersection') # intersection operation
    area = intersection['geometry'].map(lambda p: p.area) # calculates area of intersection
    type_in = intersection['DESCRIPT'].values.tolist() # types in muni
    type_all = gdf2['DESCRIPT'].values.tolist() # all types (with duplicates)
    type_all_uniq = [] # all unique types
    
    for i in type_all: # loops through type_all
        if i not in type_all_uniq: # checks if type is in type_all
            type_all_uniq.append(i) # appends type_all_uniq with each types (no duplicates now)
            
    type_out = set(type_all_uniq) - set(type_in) # gets the types not in a muni
    type_out = list(type_out) # converts to list
    
    df1 = area.to_frame() # converts area to dataframe
    df1.insert(0, 'type', type_in) # insert types
    df1.rename(columns={'geometry':'sqm'}, inplace=True) # renames geom col
    df2 = df1.groupby(['type']).sum() # groups same types
    df2 = df2.reset_index(drop=False) # adds index
    
    for i in type_out: # lopps through type_out
        df2.loc[len(df2), 'type'] = i # adds the types outside a muni in df2 
        
    df2.sort_values(by=['type'], inplace=True) # sorts the types columns
    df2_tpd = df2.T # transposes df2
    
    values = list(df2_tpd.loc['sqm'].values) # converts to list the sqm values
    data.append(values) # appends values to data which creates a list of lists
    
cols = gdf2.DESCRIPT.unique() # gets land use types
cols.sort() # sorts cols alphaetically
rows = gdf1['NAME_2'].values # gets munis

df3 = pd.DataFrame(data, columns = cols) # creates df
df3.insert(0, 'zones', rows) # creates df's rows
df3.to_csv('CamarinesSur_munis_landCover_tabulated.csv')
