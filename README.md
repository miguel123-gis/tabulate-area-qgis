Un-Pythonic Python and PyQGIS scripts that copy ArcMap's Tabulate Area tool which "calculates cross-tabulated areas between two datasets and outputs a table." The Python (GeoPandas and Pandas) script is 100% working while the PyQGIS script is 85% working.

In the case of my script, it computes how much of each land cover classification (Mangrove vegetation, Coconut plantations, Built-up Area, etc.) are there in each municipality. 

I made this because there is no same tool in QGIS. There are only tools for raster-to-raster but nothing for vector-to-vector.

As of 27 June 2020, the next steps are:
- fix tbt_pyQGIS_groupCSV that it properly groups the values of the output CSV of the PyQGIS script
- combine tbt_pyQGIS and tbt_pyQGIS_groupCSV to make a fully functioning QGIS processing plug-in script
- allow vector-to-raster tabulation

