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
timesteps = 50
container_temp = -10

# fill temperature and height of pre-filled liquid as well as energy lost to the exterior of the system
pre_fill = True
fill_temp = 40
filling_height = 0.75
diffusion_index = 0.3
diffusion_degree = 5
loss_over_time = 0

# set up list to convert output to gif r
gif_output = True
gif_duration = 0.5 #second(s)


#set up iteration
iteration = 0



# initialize the system
print("Initializing the system...\n")
plt.ioff()

t = 0

in_raster = np.random.random(size=(resX,resY))

out_rasters = timestepper(t,timesteps, in_raster, container_temp, filling_height, fill_temp, diffusion_index, loss_over_time, diffusion_degree)


# create gif from individual timesteps
print("creating .gif...")
images = []

#for raster in out_rasters:
    #images.append(imageio.imread(raster))
    #imageio.mimsave('gifs/convection.gif', images, duration=gif_duration)
print(out_rasters)
print("done")
