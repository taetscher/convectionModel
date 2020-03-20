import numpy as np
import matplotlib.pyplot as plt
import imageio
import math

#---------------------------------------------------------
#                       SETUP STUFF

def plotter(filepath, raster, upper, lower, t):
    ''' plots input raster'''

    plt.imshow(raster, cmap='inferno')
    plt.title("timestep: {}".format(t))
    plt.colorbar()
    plt.clim(lower, upper)
    plt.savefig(filepath)
    plt.close('all')

def timestepper(t,timesteps, in_raster, container_temp, filling_height, fill_temp, diffusion_index, loss_over_time, diffusion_degree):
    """ allows to set up initial system and also pass on raster to future steps"""

    raster = in_raster

    resX = in_raster.shape[0]
    resY = in_raster.shape[1]
    out_rasters = []
    upper = 40
    lower = -10

    while t < timesteps+1:
        # define where to save to
        filepath = "output/visualizationTest{}.png".format(t)

        if t == 0:

            # set up initial system state
            raster = environmental(resX,resY)

            # add a container
            container = addContainer(raster,container_temp)

            # fill the container with liquid
            raster = containerPreFill(container,raster,resX,resY,filling_height=filling_height,fill_temp=fill_temp)

            # save figure
            plotter(filepath,raster,upper,lower,t)

        else:
            print("Calculating diffusion at step {}...".format(t))

            # calculate temperature diffusion
            raster = diffusion(raster, resX, resY, diffusion_index, container_temp, loss_over_time, t, diffusion_degree)


            # save figure
            plotter(filepath,raster,upper,lower,t)

        out_rasters.append(filepath)
        t += 1

    return out_rasters

def environmental(resX,resY):

    '''creates a raster of size resX * resY, containing random values between 0 and 1

    resX, resY = pixel resolution of raster
    pre_fill = boolean; if True a container has been filled'''
    #sets up random raster conaining values between 0 and 1

    temperature_raster = np.array(np.random.uniform(low=15, high=25, size=(resX, resY)))
    #temperature_raster = np.full(shape=(resX,resY),fill_value=20)

    return temperature_raster

def abs(x):
    if x >= 0:
        return x
    n = math.sqrt(x ** 2)
    return abs(type(x)(n))

#---------------------------------------------------------
#                       CONTAINER STUFF

def addContainer(raster, container_temp):

    '''Adds a container to the input raster layer where the container is centered, half as wide as the raster itself
    and half as high as the raster itself.'''

    #add container to raster
    color_value=container_temp

    #get dimensions from raster
    dimensions = raster.shape

    x_dim = dimensions[0]
    y_dim = dimensions[1]

    #print("dimensions: {},{}".format(x_dim,y_dim))


    # define container width and height
    container_width = x_dim / 2
    container_height = y_dim/2

    # set coordinates of container corners
    container_bl = [int(container_width/2),0]
    container_br = [int(container_bl[0])+int(container_width),0]
    container_tl = [int(container_width/2),(int(container_height))]
    container_tr = [int(container_bl[0])+int(container_width),int(container_height)]

    #print("Corners:\ntl: {}\nbl: {}\ntr: {}\nbr: {}".format(container_tl,container_bl,container_tr,container_br))


    # create bottom of container
    col_cont_bl = container_bl[0]
    col_cont_br = container_br[0]

    # get rows/cols of edges of container
    bottomrow_index = y_dim - 1
    bottomedge_row = raster[-1,:]
    leftedge_col = raster[:,container_tl[0]]
    rightedge_col = raster[:,container_tr[0]]

    #set edges of container to be values to 10
    np.put(bottomedge_row, [range(container_bl[0], container_br[0]+1)],v=color_value)
    np.put(leftedge_col, [range(container_tl[1], bottomrow_index)], v=color_value)
    np.put(rightedge_col, [range(container_tr[1], bottomrow_index)], v=color_value)

    #ooutput container information to pass to other functions
    container = {'container_bl': container_bl,
                 'container_tl':container_tl,
                 'container_br':container_br,
                 'container_tr':container_tr}

    return container

def coolingRaster(resX, resY, container_temp):

    '''Creates a layer with only the cooling container information, can be added to other rasters to simulate cooling the container'''

    #add container to raster
    color_value=container_temp

    #get dimensions from raster
    x_dim = resX
    y_dim = resY

    raster = np.zeros(shape=(resX,resY))

    #print("dimensions: {},{}".format(x_dim,y_dim))


    # define container width and height
    container_width = x_dim / 2
    container_height = y_dim/2

    # set coordinates of container corners
    container_bl = [int(container_width/2),0]
    container_br = [int(container_bl[0])+int(container_width),0]
    container_tl = [int(container_width/2),(int(container_height))]
    container_tr = [int(container_bl[0])+int(container_width),int(container_height)]

    #print("Corners:\ntl: {}\nbl: {}\ntr: {}\nbr: {}".format(container_tl,container_bl,container_tr,container_br))


    # create bottom of container
    col_cont_bl = container_bl[0]
    col_cont_br = container_br[0]

    # get rows/cols of edges of container
    bottomrow_index = y_dim - 1
    bottomedge_row = raster[-1,:]
    leftedge_col = raster[:,container_tl[0]]
    rightedge_col = raster[:,container_tr[0]]

    #set edges of container to be values to 10
    np.put(bottomedge_row, [range(container_bl[0], container_br[0]+1)],v=color_value)
    np.put(leftedge_col, [range(container_tl[1], bottomrow_index)], v=color_value)
    np.put(rightedge_col, [range(container_tr[1], bottomrow_index)], v=color_value)

    #ooutput container information to pass to other functions
    container = {'container_bl': container_bl,
                 'container_tl':container_tl,
                 'container_br':container_br,
                 'container_tr':container_tr}

    return raster

def containerPreFill(container, raster, resX, resY, filling_height, fill_temp):

    '''pre-fills the container with fluid.

    container = dictionary of corners of container
    raster = raster to do operation on
    resX, resY = pixel resolution of raster
    fill_temp = temperature of filled in liquid'''

    # Make sure a container can actually be filled
    if resX < 8:
        print("Could not add pre-fill, raster resolution must be 8x8 or greater")
        raise ValueError('Raster resolution too small. Change resolution to at least 8x8 pixels.')


    else:
        # set up fill coordinates
        fill_bl = [(container['container_bl'][0]) + 1, (container['container_bl'][1]) + 1]
        fill_tl = [(container['container_tl'][0]) + 1, (container['container_tl'][1]) + 1]
        fill_br = [(container['container_br'][0]) - 1, (container['container_br'][1]) - 1]
        fill_tr = [(container['container_tr'][0]) - 1, (container['container_tr'][1]) - 1]

        fill = [fill_bl, fill_tl, fill_br, fill_tr]

        # fill container
        x = 0

        # iterate through rows
        while x < resX:
            y = 0
            # iterate through columns
            while y < resY:

                try:
                    # only do this if the selected pixel is within the container
                    if x >= fill_bl[0] and x <= fill_br[0]:
                        if y >= resY * filling_height and y <= resY - 2:
                            raster[y, x] = fill_temp


                except:
                    # this is to prevent the program from collapsing in case one of the above conditions tries to
                    # access a pixel outside of the range of a numpy array, like a pixel with index particles[-10,
                    # -10] in that case the program should just pass the condition and move on
                    print("Pixel out of bounds of np array!")
                    pass

                y += 1

            x += 1

        # output raster with pre-filled container
        return raster

def containerFill(container, temperature=20):

    '''fills a container with a liquid at specified temperature (degrees celsius). pours from pixel at (x=xmax*0.5,y=0)'''

    pass

#---------------------------------------------------------
#                       PHYSICS STUFF

def diffusion(in_raster, resX, resY, diffusion_index, container_temp, loss_over_time, iteration, diffusion_degree):

    """Calculates how much the liquid rises and diffuses energy
    because of its temperature.

    - based on input raster with temperatures """


    # set up a temporary raster to allow for energy transfer and pad the array to account for external influence
    temporary_raster = np.zeros(shape=(resX,resY))

    # pad the raster to prevent overflow (pad width = diffusion_degree+1)
    padding = diffusion_degree + diffusion_degree
    temporary_raster = np.pad(temporary_raster,((padding,padding),(padding,padding)),mode='maximum')
    in_raster = np.pad(in_raster, ((padding, padding), (padding, padding)), mode='empty')
    resY = np.shape(temporary_raster)[1]
    resX = np.shape(temporary_raster)[0]



    # loop through and calculate energy transfer per cell
    y = padding
    # loop through rows
    while y < resY-padding :

        x = padding
        # loop through columns
        while x < resX-padding :

            decider_diffusion_temp(in_raster,temporary_raster,x,y, diffusion_index, diffusion_degree)

            x+=1


        y+=1

    # unpad the raster to regain its beauty [ymin,ymax][xmin,xmax]
    temporary_raster = temporary_raster[padding:-padding, padding:-padding]
    in_raster = in_raster[padding:-padding, padding:-padding]

    # add in_raster to temporary raster to compute diffusion of energy
    temporary_raster = np.add(in_raster, temporary_raster)

    # simulate cooling of the container at each timestep
    resY = np.shape(temporary_raster)[1]
    resX = np.shape(temporary_raster)[0]
    cooling = coolingRaster(resX, resY, container_temp)
    temporary_raster = np.add(temporary_raster, cooling)


    return temporary_raster

def decider_diffusion_temp(in_raster, temporary_raster, x, y, diffusion_index, diffusion_degree):
    '''decides from where to where diffusion is taking place, is executed on each pixel'''

    # locate the pixel the decider is assessing (x = columns, y=rows)!
    pixel = in_raster[x, y]
    res = np.shape(in_raster)[0]

    # set up to record neighbouring cells
    neighbouring_cells = neighbourhood(x,y,diffusion_degree)
    neighbour_values = []

    # record neighbouring cells' values, as well as maxima/minima
    for neighbour in neighbouring_cells:
        neighbour_values.append(in_raster[neighbour])

    # calculate indices for neighbouring cells
    neighs = []
    for neighbour in neighbouring_cells:

        x_temp = x + neighbour[0]
        y_temp = y + neighbour[1]

        neighs.append((x_temp, y_temp))

    # get how many are legal (within bounds)
    division = len(neighs)
    diff = pixel - (pixel * diffusion_index)

    # check that a double minus is not converted to plus
    if diff < 0 and temporary_raster[x, y] <0:
        temporary_raster[x,y] += diff
    else:
        temporary_raster[x,y] -= diff

    # diffuse
    for neigh in neighs:

        try:
            # if index of target cell is in bounds, add diffusion value
            temporary_raster[neigh[0], neigh[1]] += diff/division

        except:
            # print("pixel outta bounds 3")
            pass

    return temporary_raster

def neighbourhood(x,y,degree):
    """finds surrounding pixel of the input pixel"""

    neighbours = []

    # loop through rows
    a = y - degree + 1
    while a < y + degree :

        # loop through columns
        b = x - degree + 1
        while b < x + degree:


            index_rel_a = y-a
            index_rel_b = x-b

            # establish radial diffusion
            if index_rel_a == index_rel_b and abs(index_rel_a) == degree:
                pass
            else:
                neighbours.append((index_rel_a,index_rel_b))

            b += 1
        a += 1

    return neighbours

#---------------------------------------------------------
#                       GIF CONVERSION

def makeGif(mode,out_rasters,gif_duration):
    # create gif from individual timesteps
    if mode == True:
        print("creating .gif...")
        images = []

        for raster in out_rasters:
            images.append(imageio.imread(raster))
            imageio.mimsave('gifs/convection.gif', images, duration=gif_duration)
        print(out_rasters)
    else:
        pass

#---------------------------------------------------------