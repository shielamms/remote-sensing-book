#!/usr/bin/env python
# coding: utf-8

# #  Method 1: Rendering a static map
# 
# In this exercise, we’ll render a static map of the land surface temperature of the Philippines in 2021 using the MODIS Terra Land Surface Temperature dataset in Google Earth Engine.
# 
# ## Complete Code

# In[1]:


import ee
import geehydro
from IPython.display import Image

# ee.Authenticate() # remove comment on initial run
ee.Initialize()

poi = ee.Geometry.Point([122.1247, 13.2735]) # [long, lat]
roi = poi.buffer(distance=9.2e5)

dataset = ee.ImageCollection("MODIS/006/MOD11A1")
dataset = dataset.select('LST_Day_1km')
date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
dataset = dataset.filter(date_filter)

image = dataset.mean()
image = image.multiply(0.02).add(-273.15)
visualisation_params = {
    'min': 8,
    'max': 40,
    'dimensions': 620,
    'region': roi,
    'palette': ['blue', 'yellow', 'red']
}
url = image.getThumbUrl(visualisation_params)
Image(url=url)


# ## Walkthrough
# 
# First, let’s identify the point on earth that we want to visualise. I’ve chosen coordinates that center to the Philippines. We use `ee.Geometry.Point` to specify a point in the earth using a [longitude, latitude] pair.

# In[2]:


poi = ee.Geometry.Point([122.1247, 13.2735]) 


# > **More info: Footnote 1.1.** Where to get location coordinates
# 
# A point alone would not be able to show us an entire country. So, we’ll need to “zoom out” of that point using a buffer, which expands the geometry by the given distance in meters (by default). In our example, let’s zoom out to a radius of 9.2 x 10^5 meters (or 920 km) from the point of interest. You can adjust this buffer by as much as you like.
# 

# In[3]:


roi = poi.buffer(distance=9.2e5)


# > **More info: Footnote 1.2.** Geometry.Point buffer
# 
# Now that we’ve established the region that we want to see, let’s grab some satellite data from the Google Earth Engine datasets. In this example, I’ll use a dataset from a satellite called MODIS, which provides an Image Collection of Global Land Surface Temperature.
# 

# In[4]:


dataset = ee.ImageCollection("MODIS/006/MOD11A1")
dataset = dataset.select('LST_Day_1km')


# > **More info: Footnote 1.3.** Information about the MODIS dataset
# 
# > **More info: Footnote 1.4.** Google Earth Engine Images, Features, ImageCollections, and FeatureCollections

# We can filter the ImageCollection by a range of dates. Let’s say we want to get the land surface temperature of the Philippines in the year 2021. We use the `ee.Filter` object to define a date filter, and then pass this to the `filter()` function of `dataset`.
# 

# In[5]:


date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
dataset = dataset.filter(date_filter)


# The first date parameter is the initial date of observation (inclusive), while the second date parameter is the day after the last day of observation. This filter gives us the whole range of dates in the year 2021.
# 
# We’re still left with a bunch of images from the dataset. By default, these images are sorted by date, and they are stacked on top of each other, the latest image being at the top of the stack. This is called a mosaic. We want an image that could show us the average (or sometimes, the median) of all these images. This combination of images is called a composite, and this is one of the most useful ways we can visualise a collection of raster data over date ranges.
# 
# In this example, we’ll create the composite image of the Philippines’ 2021 Land Surface Temperature by calculating the mean of the overlapping pixels of its images.

# In[6]:


image = dataset.mean()
image = image.multiply(0.02).add(-273.15)


# The second line in the above code snippet looks like an arbitrary transformation, but fear not. There is an explanation to it by looking back at the [dataset description](https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD11A1#bands), a portion of which is below. Under the Scale column, you’ll find the value 0.02. This means that in order to render the `LST_Day_1km` band in a 256x256 pixel image, we need to scale it by 0.02 (thus, image.multiply(0.02)). Next, under the Units column, notice that the temperature data is provided in Kelvin, which is not normally used in everyday conversation. We can convert this to a more familiar measurement unit like Celsius or Fahrenheit. I’ve chosen to convert it to Celsius through add(-273.15).

# ```{figure} images/lstday1-screenshot.png
# ---
# name: lstday1-screenshot
# ---
# ```

# > More info: Footnote 1.5. How images are scaled in Google Earth Engine
# 
# The last part of the code is setting up the visualisation parameters. These specify what ranges of the temperature data we want to visualise, what colours to use, and what the size of the final image will be.

# In[7]:


visualisation_params = {
    'min': 8,
    'max': 40,
    'dimensions': 620,
    'region': roi,
    'palette': ['blue', 'yellow', 'red']
}

url = image.getThumbUrl(visualisation_params)
Image(url=url)


# Let’s put a bit more detail into the `visualisation_params` variable:
# 
# - min: the minimum temperature value that we want to visualise in the region
# - max: the maximum temperature value that we want to visualise in the region
# - dimensions: the size (in pixels) of the output image
# - region: the region that we want to apply the visualisation to
# - palette: the colours that we want to use to indicate the different temperature levels
# 
# So, given these definitions, setting `min: 8`, `max: 40` and `palette: [‘blue’, ‘yellow’, ‘red’]` roughly means that areas with temperatures from 8 to around 18 degrees on average will appear bluish, then as temperatures increase, they appear more yellow. When the temperatures are up to around 28 degrees, they start to appear orange (because of the mix of yellow and red), and then as temperatures increase even more until the max temperature of 40 degrees, the areas appear red. See the example of the northern part of the Philippines, wherein the mountainous areas have blue streaks as the mean temperatures there are cooler. The area encompassing Metropolitan Manila is completely red, indicating the hottest temperatures on average.

# ## Output

# In[8]:


import ee
import geehydro
from IPython.display import Image

# ee.Authenticate() # remove comment on initial run
ee.Initialize()

poi = ee.Geometry.Point([122.1247, 13.2735]) # [long, lat]
roi = poi.buffer(distance=9.2e5)

dataset = ee.ImageCollection("MODIS/006/MOD11A1")
dataset = dataset.select('LST_Day_1km')
date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
dataset = dataset.filter(date_filter)

image = dataset.mean()
image = image.multiply(0.02).add(-273.15)
visualisation_params = {
    'min': 8,
    'max': 40,
    'dimensions': 620,
    'region': roi,
    'palette': ['blue', 'yellow', 'red']
}
url = image.getThumbUrl(visualisation_params)
Image(url=url)


# Mean land surface temperature of the Philippines in 2021 showing temperature ranges from 8 degrees to 40 degrees Celsius. The bluish spots indicate the cooler temperatures in the mountainous regions; Yellow areas correspond to relatively mild temperate regions; Meanwhile, orange to red areas indicate the hottest regions throughout the year. The reddest area is, as expected, the densest city in the country — Metro Manila.
# 
# 

# In[ ]:




