#!/usr/bin/env python
# coding: utf-8

# #  Method 2: Rendering an interactive map
# 
# In the previous exercise, we were able to render a static image of the Philippines using the MODIS Land Surface Temperature dataset. In this next part, we’ll render the same image but on an interactive map using Google Earth. To create a Google Earth interactive map, we can use a library called folium which provides the abstractions to manipulate a Google Earth satellite image and add the MODIS satellite dataset as another layer on top.
# 
# ##  Complete Code

# In[1]:


import ee
import folium
import geehydro

#ee.Authenticate() # remove comment on initial run
ee.Initialize()

coords = [13.2735, 122.1247]  # [lat, long]
Map = folium.Map(location=coords, zoom_start=6)
Map.setOptions('SATELLITE')

dataset = ee.ImageCollection("MODIS/006/MOD11A1")
dataset = dataset.select('LST_Day_1km')

date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
dataset = dataset.filter(date_filter)

image = dataset.mean()
image = image.multiply(0.02).add(-273.15)

visualisation_params = {
    'min': 8,
    'max': 40,
    'palette': ['blue', 'yellow', 'red']
}

Map.addLayer(image, visualisation_params, 'Land Surface Temperature')
Map.setControlVisibility(layerControl=True, fullscreenControl=True)

Map


# ## Walkthrough
# 
# The code for the interactive map looks very similar to the one in the previous exercise on rendering a static image. Let’s focus on the main differences.

# In[2]:


coords = [13.2735, 122.1247]  # [lat, long]
Map = folium.Map(location=coords, zoom_start=6)
Map.setOptions('SATELLITE')


# First, Folium accepts geographic coordinates as latitude and longitude pairs (note: latitude comes first). To load the Google Earth map, we pass the coordinates and an initial zoom value to the `folium.Map` object. Note that we no longer need to use a buffer to zoom out to the region of interest, since an interactive map does that for us.
# 
# Once we’ve instantiated our folium map, we can set the base map type. Here I’ve chosen to use the SATELLITE map type.
# 
# > More info: Footnote 1.6. Supported map types
# 
# Skipping over to the next difference: the visualisation_params variable.

# In[3]:


visualisation_params = {
    'min': 8,
    'max': 40,
    'palette': ['blue', 'yellow', 'red']
}


# Unlike the previous static map’s visualisation_params, there is no need to specify the dimensions and region properties, since we’re no longer rendering a static image of certain dimensions, and the region of interest would have to be added as a layer on top of the map. We add the layer by using the addLayer() function, which takes as arguments the image data, the visualisation parameters, and the name that we want to give to the layer.

# In[4]:


Map.addLayer(image, visualisation_params, 'Land Surface Temperature')


# Interactive maps on Google Earth typically have control buttons in addition to the zoom buttons (which appear by default). The following code adds a layer control button (to show/hide map layers), and a full screen control button to the map.

# In[5]:


Map.setControlVisibility(layerControl=True, fullscreenControl=True)


# ## Output

# In[6]:


import ee
import folium
import geehydro

#ee.Authenticate() # remove comment on initial run
ee.Initialize()

coords = [13.2735, 122.1247]  # [lat, long]
Map = folium.Map(location=coords, zoom_start=6)
Map.setOptions('SATELLITE')

dataset = ee.ImageCollection("MODIS/006/MOD11A1")
dataset = dataset.select('LST_Day_1km')

date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
dataset = dataset.filter(date_filter)

image = dataset.mean()
image = image.multiply(0.02).add(-273.15)

visualisation_params = {
    'min': 8,
    'max': 40,
    'palette': ['blue', 'yellow', 'red']
}

Map.addLayer(image, visualisation_params, 'Land Surface Temperature')
Map.setControlVisibility(layerControl=True, fullscreenControl=True)

Map


# The Modis Land Surface Temperature image of the Philippines as a layer on top of the Google Earth satellite interactive map. When the code is run on Jupyter notebook, you can drag around the output area to see how the temperature data is visualised in other countries. Notice the button on the top right — this allows you to show or hide layers on the map.
