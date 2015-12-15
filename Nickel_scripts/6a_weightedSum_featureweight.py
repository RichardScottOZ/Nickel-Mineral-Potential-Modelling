# ============================================================================
# Name: 6a_weightedSum_featureweight.py
# Author:  R. Coghlan, Geoscience Australia
# Date: 2015-10-27
# Desc: Executes a weighted sum calculation using the weight values stored in 
# the attribute table of each input raster.
#
# Requirements: Tool requires ArcView license & Spatial Analyst extension
# ============================================================================


# Import modules
import arcpy
from arcpy.sa import *
from arcpy import env

# Overwrite existing outputs
env.overwriteOutput = True

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Script parameters from ArcToolbox GUI
inputRasters = arcpy.GetParameterAsText(0)
outputRaster = arcpy.GetParameterAsText(1)

# split the list of input rasters into a python list
inputRastersList = inputRasters.split(";")

# Cycles through each raster and populates dict with raster name,
# value and weight for use in Weightsum process later
arcpy.AddMessage("\tBuilding Weighted Sum Table")
counter = 0
rasterDict = {}
for raster in inputRastersList:
    arcpy.AddMessage('\tProcessing ' + raster)
    counter += 1
    weight = 0
    rows = arcpy.SearchCursor(raster, "", "", "Weight")
    for row in rows:
        if row.Weight > weight:
            weight = row.Weight
    output = raster + " Value " + str(weight)
    key = 'raster' + str(counter)
    rasterDict[key] = output
WSTable = ";".join(rasterDict.values())
arcpy.AddMessage("\tWeighted Sum input: {0}".format(WSTable))

# Execute WeightedSum using the table from the previous step
arcpy.env.cellSize = "MINOF"
arcpy.AddMessage("Calculating Weighted Sum")
outWeightedSum = WeightedSum(WSTable)

# Save the output
outWeightedSum.save(outputRaster)

# Check in any necessary licenses
arcpy.CheckInExtension("spatial")

arcpy.AddMessage('Processing complete')
