from convectionModel.physics import *

# General Information:
""" Author: Benjamin Schuepbach
    schuepbachjamin@gmail.com
    github.com/taetscher

    Date: 15.03.2020"""

# raster size and timesteps
resX = 200
resY = resX
timesteps = 400
container_temp = -1

# fill temperature and height of pre-filled liquid as well as energy lost to the exterior of the system
pre_fill = True
fill_temp = 40
filling_height = 0.6
diffusion_index = 0.01 #how much of the total energy of a pixel is deffused at each time step (range between 0-1)
diffusion_degree = 5 #int(resX/10)
loss_over_time = 0

# set up list to convert output to gif r
gif_output = True
gif_duration = 0.1 #second(s)

# set up iteration
iteration = 0

# initialize the system
print("Initializing the system...\n")
plt.ioff()
t = 0
in_raster = np.random.random(size=(resX,resY))

# do the simulation
out_rasters = timestepper(t,timesteps, in_raster, container_temp, filling_height, fill_temp, diffusion_index, loss_over_time, diffusion_degree)

# make the gif from the outputs
makeGif(mode=gif_output, out_rasters=out_rasters, gif_duration=gif_duration)

print("Done!")