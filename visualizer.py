import matplotlib.pyplot as plt
import imageio
from convectionModel.physics import *


# General Information:
""" Author: Benjamin Schuepbach
    schuepbachjamin@gmail.com
    github.com/taetscher

    Date: 15.03.2020"""


# raster size and timesteps
resX = 200
resY = resX
dpi = 300
timesteps = 5
container_temp = 'nan'

# fill temperature and height of pre-filled liquid
pre_fill = True
fill_temp = 30
filling_height = 0.75
diffusion_index = 0.5

# set up list to convert output to gif
out_rasters = []
gif_duration = 0.5 #second(s)


#set up iteration
iteration = 0
temperature_raster = np.zeros((resX,resY))


while iteration < timesteps:

    # set up raster of environmental air temperature
    if pre_fill== True and iteration == 0:
        raster = environmental(resX, resY)
        # add container
        container = addContainer(raster, container_temp)

        # pre-fill container
        temperature_raster = containerPreFill(container, raster, resX, resY, filling_height, fill_temp)


    elif pre_fill == True and iteration >=1:
        #get materials from initial raster
        mats = materials(temperature_raster, resX, resY, fill_temp)
        # calculate temperature diffusion and updraft
        temperature_raster = diffusion(temperature_raster, resX, resY, diffusion_index, container_temp)


        # add container
        container = addContainer(temperature_raster, container_temp)





        pass

    else:
        raster = environmental(resX, resY)
        # add container
        container = addContainer(raster, container_temp)


    # make sure it can be exported
    print("iteration number {}".format(iteration))
    plt.imshow(temperature_raster, cmap='inferno')
    if iteration <=0:
        plt.colorbar()
    else:
        pass



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
