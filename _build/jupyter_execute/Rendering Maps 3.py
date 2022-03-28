#!/usr/bin/env python
# coding: utf-8

# # Summary and Footnotes
# 
# In this chapter, we created the same map using two ways: by rendering a static image, and then by creating an interactive map. We used the Google Earth Engine API to get remotely sensed image data (particularly from the MODIS Terra satellite) on our region of interest so that we can analyse a feature of that region aggregated over a period of time (particularly average land surface temperature in 2021).
# 
# 
# ## Footnotes
# 
# ### 1.1. Where to get location coordinates
# 
# - You can use Google Maps to quickly obtain the coordinates of a certain location (at least that’s what I usually do). Wherever you are on Google Maps, the geographic coordinates of the place at the centre of the screen appears on the address bar. You can copy these coordinates, but remember which one is latitude and which one is longitude. In Google Maps, the latitude value comes first.
#     
#     
# ### 1.2. Geometry.Point buffer
# 
# - The Earth Engine API docs provides more details about buffer.
#   - https://developers.google.com/earth-engine/apidocs/ee-geometry-point-buffer
# 
# 
# ### 1.3. Information about the MODIS dataset
# 
# - MODIS (Moderate Resolution Imaging Spectroradiometer) is an instrument aboard NASA’s Terra and Aqua Satellites, which are low-earth orbiting satellites that measure properties of land and oceans. MODIS can measure atmospheric conditions as well as photosynthetic activity, making it useful for measurements of the impact of environmental changes to the earth’s climate.
#   - Further reading about MODIS:
#       - https://www.spiedigitallibrary.org/journals/journal-of-applied-remote-sensing/volume-12/issue-04/041501/Application-of-MODIS-land-surface-temperature-data--a-systematic/10.1117/1.JRS.12.041501.full?SSO=1
#       - https://terra.nasa.gov/about/terra-instruments/modis
#             
#             
# - One of the datasets collected from MODIS is the Daily Global Land Surface Temperature and Emissivity dataset. It has a 1200km spatial resolution, meaning that each grid in an image covers 1200km of the earth’s surface.
#   - Further reading about the dataset:
#       - https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD11A1#description
# 
# 
# ### 1.4. Data from Google Earth Engine can be images, collections, or features.
# 
# - An image is any raster data (gridded/pixelated data where each pixel refers to a: geographic location)
# - A feature is data about the attributes of a certain area (e.g. vegetation)
# - A collection is set of images or features
# 
# 
# ### 1.5. How images are scaled in Google Earth Engine
# 
# - Further reading: https://developers.google.com/earth-engine/guides/scale
# 
# 
# ### 1.6. Supported map types
# 
# - Further reading: https://developers.google.com/maps/documentation/javascript/maptypes

# In[ ]:




