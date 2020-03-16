import matplotlib.pyplot as plt
import imageio
from convectionModel.physics import *


# General Information:
""" Author: Benjamin Schuepbach
    schuepbachjamin@gmail.com
    github.com/taetscher

    Date: 15.03.2020"""


# raster size and timesteps
resX = 100
resY = resX
dpi = 300
timesteps = 10

# fill temperature and height of pre-filled liquid
pre_fill = True
fill_temp = 40
filling_height = 0.75

# set up list to convert output to gif
out_rasters = []
gif_duration = 0.5 #second(s)


#set up iteration
iteration = 0

while iteration < timesteps:

    # set up raster of environmental air temperature
    if pre_fill== True and iteration == 0:
        raster = environmental(resX, resY)
        # add container
        container = addContainer(raster)

        # pre-fill container
        if pre_fill == True and iteration == 0:
            temperature_raster = containerPreFill(container, raster, resX, resY, filling_height, fill_temp)
        else:
            pass

    elif pre_fill == True and iteration >0:
        #get materials from initial raster
        materials = materials(temperature_raster, resX, resY, fill_temp)
        print(materials)
        #calculate temperature diffusion and updraft

        # add container
        container = addContainer(raster)





        pass

    else:
        raster = environmental(resX, resY)
        # add container
        container = addContainer(raster)


    # make sure it can be exported
    print("iteration number {}".format(iteration))
    plt.imshow(temperature_raster, cmap='inferno')


    #save image at step n
    filepath = "output/visualizationTest{}.png".format(iteration)
    plt.savefig(filepath, dpi=dpi)

    out_rasters.append(filepath)

    iteration +=1

# create gif from individual timesteps
print("creating .gif...")

images = []

for raster in out_rasters:
    images.append(imageio.imread(raster))
    imageio.mimsave('gifs/convection.gif', images, duration=gif_duration)


print("done")
