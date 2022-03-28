#!/usr/bin/env python
# coding: utf-8

# # Chapter 2: Understanding True Colour and False Colour Composites

# Our eyes can only see a very small portion of the spectrum of light that surrounds us. This portion is called the “visible spectrum”, for which we have assigned names to the various shades of colour that we can see. Scientific instruments onboard satellites have sensors of light outside of our visible range in the electromagnetic spectrum, like infrared and ultraviolet light. But of course, even if we can produce an image from an infrared sensor, our eyes can’t see infrared. To visualise what objects look like with infrared eyes, we have to use colours from our visible spectrum and map them to what the infrared sensors detect.
# 
# An image is a **“True Colour”** composite if the colours in the image are the same colours that we see with our eyes — that is, a combination of red, green, and blue (RGB) light intensities. Our computer screens can represent one pixel as a set of RGB values, where each band is an integer from 0 to 255. For example, {ref}`the following shade of green <rgb-pallete>` is represented as Red=229, Green=255, and Blue=204.
# 
# 
# ```{figure} images/rgb-palette.png
# ---
# height: 200px
# name: rgb-pallete
# ---
# Check out the complete colour chart in [RapidTables](https://www.rapidtables.com/web/color/RGB_Color.html).
# ```
# 
# <!-- <figure>
#     <img src="rgb-palette.png" width=300 />
#     <figcaption>Check out the complete colour chart in [RapidTables](https://www.rapidtables.com/web/color/RGB_Color.html).</figcaption>
# </figure> -->
# 
# Meanwhile, an image is a **“False Colour”** composite if the colours in the image are a representation of the invisible band of light that was captured.
# 
# Remote sensors in satellites can “see” the invisible light from the sun’s radiation to the earth by measuring how much of that light is reflected from the earth’s surface. As a classic example, infrared light bounces off surfaces with higher levels of vegetation, but is absorbed by water. That means that a remote infrared sensor will see brighter light in a forested area, but oceans and other bodies of water on earth will appear dark.
# 
# Now, if we were to display that image in the infrared band, we can only do so with the colours in our visible bands. There are two ways to do this:
# 
# 1. Display infrared in one visible band, like greyscale, such that higher infrared reflectance would show as lighter grey, while lower infrared reflectance would appear darker grey to black; or
# 
# 2. Display infrared as a combination of three visible bands: Red, Green, and Blue.
# 
# {ref}`The image on the left below <laguna>` is a true colour composite of an area on earth. The image on the right is a greyscale composite image of that same area captured in infrared. Most of the time, it is difficult for the naked eye to clearly identify the boundary between bodies of water and land from a true colour composite because of the mixing of colours. With false colour composites, these boundaries are much sharper because different types of surfaces reflect invisible light at much varied levels.
# 
# ```{figure} images/laguna.png
# ---
# name: laguna
# ---
# Composite images of Metro Manila and its neighbouring Laguna Lake. *On the left:* a true colour composite shows the water as green as its surrounding land areas, which could make the lake difficult to spot when we zoom out the map. *On the right:* The same image in the infrared band, represented by greyscale, which shows the higher contrast of the lake with its surrounding land area because of the difference in reflectiveness of infrared light on water and on land.
# ```
# 
# Let’s explore this a bit deeper using the Google Earth Engine API and the Surface Reflectance data from the Landsat 8 satellite.
# 
# ---
# 
# 
# ## Let’s build a map from Google Earth!
# 
# For this example, I’m going to get image data from the [Landsat 8 Satellite](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_TOA#bands), and get the median composites in true colour, false colour, and greyscale infrared in the year 2021. The subject of my image is the Taal Lake and Taal Volcano, situated some kilometres south of Manila, Philippines. The lake and its surrounding areas are a popular tourist destination close to the capital. The lake surrounds the the volcano, which is the 2nd most active volcano in the country.
# 
# Here’s the complete code if you want to go straight at it. Otherwise, feel free to skip past this next code block and into the walkthrough.
# 

# ### Complete Code

# In[1]:


import ee
import folium
import geehydro

ee.Initialize()

image = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')
date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
image = (image
         .filter(date_filter)
         .filter(ee.Filter.lt("CLOUD_COVER", 30))
        .median())

l8_map = folium.Map(location=[13.9999502, 121.011384], zoom_start=11.5)
l8_map.setOptions('SATELLITE')

near_infrared_params = {
    'bands': 'B5',
    'min': 0,
    'max': 0.4,
}
false_color_params = {
    'bands': ['B5', 'B4', 'B3'],
    'min': 0,
    'max': 0.5
}
true_color_params = {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 0.4,
}

l8_map.addLayer(image, near_infrared_params, 'greyscale infrared')
l8_map.addLayer(image, false_color_params, 'false color infrared')
l8_map.addLayer(image, true_color_params, 'true color')

l8_map.setControlVisibility(layerControl=True)
display(l8_map)


# **Walkthrough**
# 
# First, we import the needed Google Earth Engine libraries and the Folium library to create an interactive map.

# In[2]:


import ee
import folium
import geehydro
ee.Initialize()


# Now let’s import the Landsat Image Collection. You can find more info about this dataset from the [Google Earth Engine catalog page for Landsat 8](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_TOA#description). We then filter only the images in the year 2021.

# In[3]:


images = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')
date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
image = (images
         .filter(date_filter)
         .filter(ee.Filter.lt("CLOUD_COVER", 30))
        .median())


# The second filter is needed because we need to discard images where the clouds are covering the area we want to analyse. This filter (and by the way, there are “cloud masking” techniques in image composition which can be a subject for another article) is especially important when processing images from sensors that detect visible light. In other words, a satellite hovering on top of a cloudy area will see only clouds in visible light, which makes land and water surface analyses nearly impossible.

# In[4]:


ee.Filter.lt("CLOUD_COVER", 30)


# The above filter means that we’re getting images in the collection where the cloud cover is less than 30% of an image. Without it, the median composite would look like this:

# In[5]:


images = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')
date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
image = images.filter(date_filter).median()

l8_map = folium.Map(location=[13.9999502, 121.011384], zoom_start=11.5)
l8_map.setOptions('SATELLITE')
l8_map.addLayer(image, true_color_params, 'true color')
display(l8_map)


# The next step is initialising the folium map. We tell folium to centre the map to the given [ latitude, longitude ] coordinates, and then zoom in to 11.5 levels. This area will be our region of interest.

# In[6]:


l8_map = folium.Map(location=[13.9999502, 121.011384], zoom_start=11.5)
l8_map.setOptions('SATELLITE')   #optional


# Calling setOptions is optional - it's just mainly to tell folium to load a Google Maps Satellite layer. Without this, the map would just use the default OpenStreetMap base layer, which doesn't matter in our current example.
# 
# We now have the base layer and filtered the dataset. The median() function gives us the composite, but we still need to separate the bands of light for our visualisation. Let's start by visualising the image in true colour.
# 
# ### Adding the True Colour Layer

# In[7]:


true_color_params = {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 0.4,
}
l8_map.addLayer(image, true_color_params, 'true color')


# The `bands` parameter in the above code snippet means the band or bands that we want to visualise. We can assign it a single band or a list of bands. If we provide only one band, the image will be represented in greyscale showing the relative intensities of the given band on our region of interest. If we provide a list of bands, each band will be mapped to a palette in Red, Green, and Blue, in that order. (If that sounds confusing, please read along. These thing can get counterintuitive).
# 
# According to the [Landsat 8 TOA Reflectance Data Documentation](https://medium.com/r/?url=https%3A%2F%2Fdevelopers.google.com%2Fearth-engine%2Fdatasets%2Fcatalog%2FLANDSAT_LC08_C02_T1_TOA%23bands), the Red, Green, and Blue optical bands can be referenced by the names B4, B3, and B2, respectively. So providing it as a list in the bands parameter, the B4 band will be represented by the Red colour palette, B3 will be represented by the Green palette, and B2 will be represented by the Blue palette. Take good care of the ordering of these bands on the list, as switching B4 and B3 positions would mean that the B4 (red light) will be represented by green colours, while B3 (green light) will be represented by red colours - which is confusing.
# 
# You may be asking - why do we need to do this mapping if red would just be represented by the red colour, green by the green colour, and blue by the blue colour? While it does sound like an overkill to do this for the visible spectrum, it would make a lot more sense for the invisible spectrum, which we can't see and therefore need to represent with colours that we can see. We'll get to that more in a little while.
# 
# Our next concerns are the min and max parameters. What are they? I was puzzled about them myself when I was starting out with the Google Earth Engine API, as there doesn't seem to be any good documentation about them. The best resource I found about it was an [obscure article from Google Earth Outreach](https://medium.com/r/?url=https%3A%2F%2Fwww.google.com%2Fearth%2Foutreach%2Flearn%2Fintroduction-to-google-earth-engine%2F%23earth-engine-explorer-0%23data-range-4-12). Here's a quote from the page:
# 
# > Visualisation of data requires that a given value range be scaled between 0 and 255 for each band being displayed. The range parameter (min and max) allows you to adjust the range of values to display. The defined min value will be drawn to 0 and the max to 255, all data values in between the defined min and max range are scaled linearly. Data outside the min and max range are set to either 0 or 255, depending on whether they are less than or greater than the provided range.
# 
# So there are two things I can infer from this paragraph:
# 
# - Optical band data from a satellite sensor can take on a range of values, which are presumably the intensity of the reflected light from that band. Whatever those ranges are depend on the type of instrument that measures it, and sadly there's not an easily accessible online resource to tell us the min and max values of each band from each remote sensing instrument out there. Mostly we're going to have to do some guess work and playing around with the min and max values. Fortunately for Landsat 8 images, a lot of online examples show values between 0 and 1, so I concluded that bands B4, B3, and B2 from Landsat 8 are values between 0 and 1.
# 
# - If we set min=0 and max=1 for a particular band (say, B4 which is mapped to the Red palette), then all the B4 values between 0 and 1 will be interpolated to values between 0 and 255 of the red colour palette.
# 
# To understand this in a simplified world, let's say we have a hypothetical colour palette with only 5 colours (0 to 4). And then we have a hypothetical band whose values can range from 0 to 9. If we want to visualise all 0 to 9 values, only the first 5 values can be uniquely represented by the hypothetical colour palette. All other band values from 5 to 9 will be pulled down to the maximum value of the palette that represents it, which is 4. This would cause our image to be skewed towards the darker colours. For example, if more values of a band are mapped to the max Red palette colour, the image would be darker.
# 
# | Hypothetical band value | Hypothetical palette colour to represent the hypothetical band value |
# | ----------------------- | -------------------------------------------------------------------- |
# | 0 (min limit)           | 0 (min limit)                                                        |
# | 1                       | 1                                                                    |
# | 2                       | 2                                                                    |
# | 3                       | 3                                                                    |
# | 4                       | 4 (max limit)                                                        |
# | 5                       | 4                                                                    |
# | 6                       | 4                                                                    |
# | 7                       | 4                                                                    |
# | 8                       | 4                                                                    |
# | 9 (max limit)           | 4                                                                    |
# 
# 
# However, if we reduce the range of band values that we want to visualise, then these range of values would fit the palette colour range. Back to our hypothetical 5-colour palette example, if we set the desired band values to just be min=0 and max=3, then this will only utilise the same relative range from the colour palette.
# 
# | Hypothetical band value | Hypothetical palette colour to represent the hypothetical band value |
# | ----------------------- | -------------------------------------------------------------------- |
# | 0 (min limit)           | 0 (min limit)                                                        |
# | 1                       | 1                                                                    |
# | 2                       | 2                                                                    |
# | 3                       | 3                                                                    |
# | -                       | -                                                                    |
# | -                       | -                                                                    |
# | -                       | -                                                                    |
# | -                       | -                                                                    |
# | -                       | -                                                                    |
# | (max limit)             | (max limit)                                                          |
# 
# 
# Phew! That was a long explanation about min and max band parameters! Let's go back to the code for true colour parameters:

# In[8]:


true_color_params = {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 0.4,
}
l8_map.addLayer(image, true_color_params, 'true color')


# Okay, so we want to represent three bands B4, B3, and B2 with values scaled within the RGB values of 0 to 255. But we provided only one value for each of min and max while we provided a list of bands. Technically, we could have written it this way for clarity and it would mean the same thing:

# In[9]:


true_color_params = {
    'bands': ['B4', 'B3', 'B2'],
    'min': [0, 0, 0],
    'max': [0.4, 0.4, 0.4],
}


# Technically each band can have different min and max values, but we don't want to complicate our visualisation too early, so we can just leave them as they are.
# 
# The output of this is a map with the true colour layer. Note that there's still some wisps of cloud there, since we only did a simple cloud filter on the image collection. There are other ways to effectively remove clouds from the composite computation, which we won't cover in this article.
# 
# ```{figure} images/taal-true-color.png
# ---
# height: 400px
# name: taal-true-color
# ---
# Taal Volcano surrounded by Taal Lake in true colour. The colours are what we would see ourselves if we were on the satellite looking at this region on earth.
# ```

# ### Adding the Infrared Layer

# Now let's add in a layer showing the median composite in the infrared band. The [Landsat 8 TOA Reflectance Data Documentation](https://medium.com/r/?url=https%3A%2F%2Fdevelopers.google.com%2Fearth-engine%2Fdatasets%2Fcatalog%2FLANDSAT_LC08_C02_T1_TOA%23bands) tells us that Infrared Bands are B7, B6, and B5. For now, we can just use B5, which is the Near-Infrared band or NIR. In the bands parameter, we set only one value B5, and then set the range of NIR values from 0 to 0.4 to be represented in the image. This would mean that surfaces with lower near-infrared reflectance would appear brighter than they would if we represented all values from 0 to 1.

# In[10]:


near_infrared_params = {
    'bands': 'B5',
    'min': 0,
    'max': 0.4,
}
l8_map.addLayer(image, near_infrared_params, 'greyscale infrared')


# The output is a new layer on our map showing near-infrared represented in greyscale:
# 
# ```{figure} images/taal-infrared-grey.png
# ---
# height: 400px
# name: taal-infrared-grey
# ---
# Taal Volcano surrounded by Taal Lake viewed in near infrared represented by greyscale. Vegetation reflects infrared light while water absorbs it, which is the reason why the surrounding forested land area appears bright grey, while the lake appears very dark. The volcano in the middle of the lake doesn’t have much vegetative cover, but it does reflect some amount of infrared, which gives it a dark grey colour in this image.
# ```
# 

# ### Adding the False Colour Layer

# The False Colour composite is where you can unleash your artistic side. Since we're representing invisible light (or a combination of invisible and visible) using a 'visible colour', we can pretty much use any colour we want to represent certain reflective surfaces on the map. However, the industry has its standards when we're presenting these maps for official use, as explained by [this article](https://medium.com/r/?url=http%3A%2F%2Fgsp.humboldt.edu%2Folm%2FCourses%2FGSP_216%2Flessons%2Fcomposites.html), so do be conscious of the colours and bands that you use for non-experimental use cases. In our example of false colour composite, we'll represent the B5 band (NIR) with the red palette, B4 with the green palette, and B3 with the blue palette. At this point, it gets counterintuitive since we're representing B4 (red) with green colours and B3 (green) with blue colours.
# 
# I've set the max value to 0.5, but as I've mentioned, it takes a bit of playing around with the min and max to get the right brightness and contrast that's pleasing to the eyes.

# In[11]:


false_color_params = {
    'bands': ['B5', 'B4', 'B3'],
    'min': 0,
    'max': 0.5
}
l8_map.addLayer(image, false_color_params, 'false color infrared')


# The result of the code above is a layer showing the lake's surrounding forested areas in shades of bright red, since these areas are reflecting infrared much more than the lake and the volcano. The volcano itself reflects a tiny amount of infrared at its edges, but its colour is mostly a combination blue and green colours representing reflected visible red and green lights, respectively.
# 
# ```{figure} images/taal-infrared-false-color.png
# ---
# height: 400px
# name: taal-infrared-false-color
# ---
# Taal Volcano surrounded by Taal Lake viewed in near infrared represented by RGB colours. The reflected infrared light from the forested areas are shown in red.
# ```
# 

# ### Output
# 
# The final output of all the code above is a Folium interactive map using Google Earth satellite as the base layer. Play around with the layer control button on the upper right to toggle between the map layers.

# In[12]:


import ee
import folium
import geehydro

ee.Initialize()

image = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')
date_filter = ee.Filter.date('2021-01-01', '2022-01-01')
image = (image
         .filter(date_filter)
         .filter(ee.Filter.lt("CLOUD_COVER", 30))
        .median())

l8_map = folium.Map(location=[13.9999502, 121.011384], zoom_start=11.5)
l8_map.setOptions('SATELLITE')

near_infrared_params = {
    'bands': 'B5',
    'min': 0,
    'max': 0.4,
}
false_color_params = {
    'bands': ['B5', 'B4', 'B3'],
    'min': 0,
    'max': 0.5
}
true_color_params = {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 0.4,
}

l8_map.addLayer(image, near_infrared_params, 'greyscale infrared')
l8_map.addLayer(image, false_color_params, 'false color infrared')
l8_map.addLayer(image, true_color_params, 'true color')

l8_map.setControlVisibility(layerControl=True)
display(l8_map)


# ---
# 
# ## Conclusion
# 
# In this article, we've differentiated true colour composites and false colour composites by understanding the reflectance of certain bands of light on various surfaces on earth. We can produce composites of the same region of interest using different bands of light to study the surface features on that region. This is especially important when we want to detect geophysical anomalies or huge changes to the region, like loss of forested areas over time, and we want to see them beyond the limitations of our human eyes.
# 
# ---
# 
# ## References and Further Reading
# - [Natural and False Color Composites](https://medium.com/r/?url=http%3A%2F%2Fgsp.humboldt.edu%2Folm%2FCourses%2FGSP_216%2Flessons%2Fcomposites.html) by http://gsp.humboldt.edu.
# - [Introduction to Google Earth Engine](https://medium.com/r/?url=https%3A%2F%2Fwww.google.com%2Fearth%2Foutreach%2Flearn%2Fintroduction-to-google-earth-engine%2F%23earth-engine-explorer-0%23data-range-4-12) by Google Earth Outreach:
# - The [Landsat data catalog](https://medium.com/r/?url=https%3A%2F%2Fdevelopers.google.com%2Fearth-engine%2Fdatasets%2Fcatalog%2Flandsat) on Google Earth Engine
