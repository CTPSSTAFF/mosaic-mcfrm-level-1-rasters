# mosaic-mcfrm-level-1-rasters
Tool to mosaic the MC-FRM LEVEL_1 TIF rasters

## Background
The raw LEVEL_l MC-FRM data is shipped in a highly 'fragmented' form:
a single TIF file for each municipality for each year (present=2018,
2030, 2050, 2070) and for each 'kind' of data (probability, 
depth at 0.1% probability, depth at 0.5% proabaility, depth at 1% probability).
Futher complicating matters, the TIF files for 'North' municipalities are 
stored a a separate folder for 'South' municipalities.

The following figure summarizes the organization of the data, as shipped:

```
LEVEL_1/
	Year/
		North-or-South/
			Kind-of-data/
				individual TIF files
```

Where __north-or-south__ can be:
* North - towns roughly from the north side of Cape Cod to the New Hampshire border
* South - towns on the south side of Cape Cod, the "south coast" and the Islands

And __year__ can be:
* Present (2018)
* 2030
* 2050
* 2070

And __kind\_of\_data__ can be:
* Probability
* Depth at 1% probability
* Depth at 0.5% probability
* Depth at 0.1% probability

## Purpose
The purpose of this tool is to create a single raster mosaic for 
each {year, kind-of-data) from all the relevant TIFs.

## Pre-requisites
This tool relies upon the __glob__ library from the Python standard library,
and the ESRI __arcpy__ library.

## Execution
This script is inteneded to be run in the interactive Python console
in ArcMap or ArcGIS Pro. 

## Colophon
Author: Ben Krepp  
Date: 18 May 2023, 30 May 2023  
Place: Cyberspace
