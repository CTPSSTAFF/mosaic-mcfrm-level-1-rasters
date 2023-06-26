# MC-FRM LEVEL_1 data raster mosaic-ing tool.
#
# Background
# ===========
#
# The raw LEVEL_l MC-FRM data is shipped in a highly 'fragmented' form:
# a single TIF file for each municipality for each year (present=2018,
# 2030, 2050, 2070) and for each 'kind' of data (probability, 
# depth at 0.1% probability, depth at 0.5% proabaility, depth at 1% probability).
# Futher complicating matters, the TIF files for 'North' municipalities are 
# stored a a separate folder for 'South' municipalities.
#
# The following figure summarizes the organization of the data, as shipped:
#
# LEVEL_1/
#     Year/
#       North-or-South/
#           Kind-of-data/
#               individual TIF files
#
# Purpose
# =======
# The purpose of this tool is to create a single raster mosaic for 
# each {year, kind-of-data) from all the relevant TIFs.
#
# Pre-requisites
# ==============
# This tool relies upon the "glob" library from the Python standard library,
# and the ESRI "arcpy" library.
#
# Execution
# ==========
# This script is inteneded to be run in the interactive Python console
# in ArcMap or ArcGIS Pro. Converting it into an ESRI "toolbox" tool 
# is left as an exercise for the reader.
#
# Author: Ben Krepp
# Date: 18 May 2023, 30 May 2023

import arcpy
import glob

coordinate_system="PROJCS['NAD_1983_StatePlane_Massachusetts_Mainland_FIPS_2001',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',200000.0],PARAMETER['False_Northing',750000.0],PARAMETER['Central_Meridian',-71.5],PARAMETER['Standard_Parallel_1',41.71666666666667],PARAMETER['Standard_Parallel_2',42.68333333333333],PARAMETER['Latitude_Of_Origin',41.0],UNIT['Meter',1.0]];-36530900 -28803200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"

years = ["Present", "2030", "2050", "2070"]
areas = ["North", "South"]

data_kinds =  ["Probability", "Depth_0.1_Percent", "Depth_0.5_Percent", "Depth_1_Percent"]
data_kinds_abbrevs = ["Probability", "Depth_pt1_pct", "Depth_pt5_pct", "Depth_1_pct"]

root = r'//lilliput/groups/Certification_Activities/Resiliency/data/mcfrm/LEVEL_1/'

def mylog(s):
    # print(s)
    arcpy.AddMessage(s)
#


# Add all the individual TIF rastesrs of the kind 'data_kind' for the year indicated by 'year_folder'
# to the mosaic data set indicated by 'mosaic_full_path'.
def add_rasters_to_mosaic(year_folder, data_kind, mosaic_full_path):
    # Create semicolon-delimited list of TIFs to add to the mosaic
    north_folder = year_folder + 'North/' + data_kind + '/'
    south_folder = year_folder + 'South/' + data_kind + '/'
    north_tif_list = glob.glob(north_folder + '*.tif')
    south_tif_list = glob.glob(south_folder + '*.tif')
    full_tif_list = north_tif_list + south_tif_list
    #
    # Delimit with semicolons - don't append semicolon to last items
    final_tif_list = []
    for x in full_tif_list[:-1]:
        final_tif_list.append(x + ';')
    #
    final_tif_list.append(full_tif_list[len(full_tif_list)-1])
    # Convert to string for use in ESRI API call
    final_tif_list_as_str = ''
    for i in final_tif_list:
        final_tif_list_as_str += i
    #
    # Here: actually add the rasters to the mosaic
    arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset=mosaic_full_path,
                                               raster_type="Raster Dataset", 
                                               input_path=final_tif_list_as_str,
                                               update_cellsize_ranges="UPDATE_CELL_SIZES", 
                                               update_boundary="UPDATE_BOUNDARY", 
                                               update_overviews="NO_OVERVIEWS", 
                                               maximum_pyramid_levels="", 
                                               maximum_cell_size="0", 
                                               minimum_dimension="1500", 
                                               spatial_reference="", 
                                               filter="#", 
                                               sub_folder="NO_SUBFOLDERS", 
                                               duplicate_items_action="ALLOW_DUPLICATES",
                                               build_pyramids="BUILD_PYRAMIDS", 
                                               calculate_statistics="CALCULATE_STATISTICS",
                                               build_thumbnails="NO_THUMBNAILS", 
                                               operation_description="#", 
                                               force_spatial_reference="NO_FORCE_SPATIAL_REFERENCE", 
                                               estimate_statistics="NO_STATISTICS", 
                                               aux_inputs="")
#

# Main driver logic
# parameter 'all_subfolder_name' is the name of the subfolder to create
#           immediately 'below' the root/<year> folder, at the same 
#           levels as the 'North' and 'South' folders in the delivered data.
def main_routine(all_subfolder_name='All'):
    for year in years:
        # Create 'All' subfolder
        year_folder = root + year + '/'
        # all_subfolder_name = "All"
        all_subfolder_path = year_folder + all_subfolder_name
        mylog('Creating folder: ' + all_subfolder_path)
        arcpy.CreateFolder_management(year_folder, all_subfolder_name)
        #
        # Create File GDBs and create a mosaic dataset in each one; add all raster TIFs in 'North' and 'South' subdirectories to the mosaic
        for (dk, dk_abbrev) in zip(data_kinds, data_kinds_abbrevs):
            fgdb_name = year + '_' + dk + '.gdb'
            fgdb_path = all_subfolder_path + '/' + fgdb_name
            mylog('Creating FGDB: ' + fgdb_path)
            arcpy.CreateFileGDB_management(all_subfolder_path, fgdb_name)
            #
            mosaic_ds_name = 'mosaic_' + year + '_' + dk_abbrev
            mylog('Creating mosaic: ' + mosaic_ds_name)
            arcpy.CreateMosaicDataset_management(in_workspace=fgdb_path, 
                                                 in_mosaicdataset_name=mosaic_ds_name,
                                                 coordinate_system=coordinate_system,
                                                 num_bands="1", 
									             pixel_type="32_BIT_FLOAT", 
									             product_definition="NONE", 
									             product_band_definitions="")
            #
            # Add rasters to mosaic
            mosaic_full_path = fgdb_path + '/' + mosaic_ds_name
            add_rasters_to_mosaic(year_folder, dk, mosaic_full_path)
        #
    #
#
