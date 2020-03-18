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
container_temp = -10

# fill temperature and height of pre-filled liquid as well as energy lost to the exterior of the system
pre_fill = True
fill_temp = 40
filling_height = 0.75
diffusion_index = 0.75
diffusion_degree = 12
loss_over_time = 0

# set up list to convert output to gif
out_rasters = []
gif_duration = 0.5 #second(s)


#set up iteration
iteration = 0
temperature_raster = np.zeros((resX,resY))


while iteration < timesteps:

    # set up raster of environmental air temperature
    if iteration == 0:
        raster = environmental(resX, resY)
        # add container
        container = addContainer(raster, container_temp)

        # pre-fill container
        temperature_raster = containerPreFill(container, raster, resX, resY, filling_height, fill_temp)


    else:
        #get materials from initial raster
        mats = materials(temperature_raster, resX, resY, fill_temp)

        # calculate temperature diffusion and updraft
        temperature_raster = diffusion(temperature_raster, resX, resY, diffusion_index, container_temp, loss_over_time, iteration, diffusion_degree)

        # add container (for visuals)
        container = addContainer(temperature_raster, container_temp)






    # make sure it can be exported
    print("iteration number {}".format(iteration))
    plt.imshow(temperature_raster, cmap='inferno')
    if iteration <=0:
        plt.colorbar()
    else:
        pass



    #save image at step n
    filepath = "output/visualizationTest{}.png".format(iteration)
    plt.title("Timestep {}".format(iteration+1))
    plt.savefig(filepath, dpi=dpi)

    out_rasters.append(filepath)

    iteration +=1

# create gif from individual timesteps
print("creating .gif...")


images = []

#for raster in out_rasters:
    #images.append(imageio.imread(raster))
    #imageio.mimsave('gifs/convection.gif', images, duration=gif_duration)


print("done")
