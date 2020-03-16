import matplotlib.pyplot as plt
import imageio
from convectionModel.physics import environmental, addContainer


# General Information:
""" Author: Benjamin Schuepbach
    schuepbachjamin@gmail.com
    github.com/taetscher

    Date: 15.03.2020"""


# raster size and timesteps
resX = 100
resY = resX
dpi = 300
timesteps = range(10)



# set up list to convert output to gif
out_rasters = []
gif_duration = None


for step in timesteps:

    # set up raster of environmental noise
    raster = environmental(resX,resY)

    # add container
    container = addContainer(raster)
    print(container)

    # make sure it can be exported
    print("iteration number {}".format(step))
    plt.imshow(raster, cmap='inferno')


    #save image at step n
    filepath = "output/visualizationTest{}.png".format(step)
    plt.savefig(filepath, dpi=dpi)

    out_rasters.append(filepath)

# create gif from individual timesteps
print(out_rasters)
print("creating .gif...")

images = []

for raster in out_rasters:
    images.append(imageio.imread(raster))
    imageio.mimsave('gifs/convection.gif', images, duration=gif_duration)


print("done")
