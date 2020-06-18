An un-Pythonic Python script that copies ArcMap's Tabulate Area tool which "calculates cross-tabulated areas between two datasets and outputs a table."

In the case of my script, it computes how much Mangrove vegetation, Coconut plantations, Built-up Area, and etc. are there in each municipalities. 

I made this because there is no same tool in QGIS. There are only tools for raster-to-raster but nothing for vector-to-vector.

muni_landCover_area.xlsx is the different results of the same process from ArcMap (Tabulate Area), QGIS (Add Geometry Attributes, for one municipality only), Geopandas, and the script's result

As of 18 June 2020, the next steps are:
- convert as a QGIS processing plug-in
- allow vector-to-raster tabulation
