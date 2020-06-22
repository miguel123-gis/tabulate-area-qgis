import os
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame

os.chdir(r'C:\Users\imper\Documents\new_GISfiles\tabulateArea_forQGIS\\')
gdf1 = gpd.read_file('camSur_municities.shp')
gdf2 = gpd.read_file('camSur_landCover_2003.shp')

for a in range(gdf1.shape[0]):
    muni = gdf1.loc[gdf1['NAME_2'] == gdf1['NAME_2'][a]] # muni index
    intersection = gpd.overlay(muni, gdf2, how='intersection') # intersection operation
    area = intersection['geometry'].map(lambda p: p.area) # calculates area of intersection
    type_in = intersection['DESCRIPT'].values.tolist() # types in muni
    type_all = gdf2['DESCRIPT'].values.tolist() # gets all types as list
    type_all_uniq = [] # all types but grouped
    for i in type_all: # check type_all
        if i not in type_all_uniq: # checks if type is in type_all
            type_all_uniq.append(i) # adds if type isn't in type_all already
    type_out = set(type_all_uniq) - set(type_in) # gets types not in muni
    type_out = list(type_out) # converts to list
    df1 = area.to_frame() # converts area to dataframe
    df1.insert(0, 'type', type_in) # insert types
    df1.rename(columns={'geometry':'sqm'}, inplace=True) # renames geom col
    df2 = df1.groupby(['type']).sum() # groups same types
    df2 = df2.reset_index(drop=False) # adds index
    index = df2.index # index of df2
    index.name = gdf1['NAME_2'].values[a] # index title is the muni
    for i in type_out: # iterate through types not in muni
        df2.loc[len(df2), 'type'] = i # adds types not in muni to df2
    df2.sort_values(by=['type'], inplace=True) # sorts 'type' ascending order
    print(df2)

"""
Working on this part -should add each df2 to a new dataframe with the values transposed
cols = gdf2.DESCRIPT.unique() # gets land use types
rows = gdf1['NAME_2'].values # gets munis
df3 = pd.DataFrame([range(len(cols))], range(len(rows))) # creates df
df3.columns = cols # creates df's cols
cols.sort() # sorts cols alphaetically
df3.insert(0, 'zones', rows) # creates df's rows
df2_values = df2['sqm'].tolist()
df3 = pd.concat([df2_values, df3]) # merges df2 to df3
df3 = df3.reset_index(drop=True) # reset index
print(df3)
"""
