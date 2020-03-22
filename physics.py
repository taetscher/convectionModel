import numpy as np
import matplotlib.pyplot as plt
import imageio
import math

#---------------------------------------------------------
#                       SETUP STUFF

def plotter(filepath, raster, upper, lower, t,container_temp,fill_temp,diffusion_index,diffusion_degree,timesteps):
    ''' plots input raster'''

    ext_x = np.shape(raster)[0]
    ext_y = np.shape(raster)[1]

    params = "Parameters used:\n " \
             "Container Temperature: {}°C\n" \
             "Fill Temperature: {}°C\n" \
             "Diffusion per Timestep: {}%\n" \
             "Diffusion Degree: {} pixels\n" \
             "Timesteps: {}\n\n" \
             "Author: Benjamin Schuepbach\n" \
             "github.com/taetscher".format(container_temp,fill_temp,diffusion_index*100,diffusion_degree,timesteps)

    plt.imshow(raster, cmap='inferno')
    plt.title("timestep: {}".format(t))
    plt.axis('off')
    plt.text(ext_x/2, ext_y/5, params,color='black',horizontalalignment='center', verticalalignment='center',bbox=dict(facecolor='white', alpha=0.5))
    plt.colorbar(label='Temperature (°C)', drawedges=False)
    plt.clim(lower, upper)
    plt.savefig(filepath)
    plt.close('all')

def timestepper(t,timesteps, in_raster, container_temp, filling_height, fill_temp, diffusion_index, loss_over_time, diffusion_degree):
    """ allows to set up initial system and also pass on raster to future steps"""

    raster = in_raster

    resX = in_raster.shape[0]
    resY = in_raster.shape[1]
    out_rasters = []
    upper = max(container_temp,fill_temp)-30
    lower = min(container_temp,fill_temp)

    while t < timesteps+1:
        # define where to save to
        filepath = "output/visualizationTest{}.png".format(t)

        if t == 0:

            # set up initial system state
            raster = environmental(resX,resY)
            container = addContainer(raster, container_temp)
            containerPreFill(container, raster, resX, resY, filling_height, fill_temp)

            # cool the container this is not actually redundant, more like a hotfix
            raster = coolingContainer(raster,container_temp)

            # save figure
            plotter(filepath,raster,upper,lower,t,container_temp,fill_temp,diffusion_index,diffusion_degree,timesteps)

        else:
            print("Calculating diffusion at step {}...".format(t))

            # calculate temperature diffusion
            raster = diffusion(raster, resX, resY, diffusion_index, container_temp, loss_over_time, t, diffusion_degree,fill_temp)


            # save figure
            plotter(filepath,raster,upper,lower,t,container_temp,fill_temp,diffusion_index,diffusion_degree,timesteps)

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
    """returns the absolute value of x"""
    if x >= 0:
        return x
    n = math.sqrt(x ** 2)
    return abs(type(x)(n))

def radial_remove(neighbouring_cells, degree):
    '''checks if a pixel belongs to a group of pixel which need to be removed in order to make radial diffusion happen'''


    for neighbour in neighbouring_cells:

        if abs(neighbour[0]) == degree and abs(neighbour[1]) == degree:
            neighbouring_cells.remove(neighbour)
        else:
            pass
        #print(neighbour)

    return neighbouring_cells

def even(x):
    '''checks if a number is even, returns True for even numbers and False for odd numbers'''
    if (x % 2) == 0:
        return True
    else:
        return False
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

def coolingContainer(temp_ras,container_temp):

    '''Simulates cooling of container by over-writing temperature values of container'''

    #get dimensions from raster
    x_dim = np.shape(temp_ras)[0]
    y_dim = np.shape(temp_ras)[1]

    # define container width and height
    container_width = x_dim / 2
    container_height = y_dim/2

    # get coordinates of container corners
    container_bl = [int(container_width/2),0]
    container_br = [int(container_bl[0])+int(container_width),0]
    container_tl = [int(container_width/2),(int(container_height))]
    container_tr = [int(container_bl[0])+int(container_width),int(container_height)]

    # set container temperature
    temp_ras[container_tl[1]:,container_tl[0]]=container_temp
    temp_ras[container_tr[1]:, container_tr[0]] = container_temp
    temp_ras[y_dim-1:, container_bl[0]:container_br[0]] = container_temp


    return temp_ras

def containerPreFill(container, raster, resX, resY, filling_height, fill_temp):

    '''pre-fills the container with fluid.

    container = dictionary of corners of container
    raster = raster to do operation on
    resX, resY = pixel resolution of raster
    fill_temp = temperature of filled in liquid'''

    # Make sure a container can actually be filled
    if resX < 8:
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

#---------------------------------------------------------
#                       PHYSICS STUFF

def diffusion(in_raster, resX, resY, diffusion_index, container_temp, loss_over_time, iteration, diffusion_degree, fill_temp):

    """Calculates how much the liquid rises and diffuses energy
    because of its temperature.

    - based on input raster with temperatures """

    # set up a temporary raster to allow for energy transfer and pad the array to account for external influence
    temporary_raster = np.zeros(shape=(resX,resY))

    # simulate cooling of the container at each timestep
    temporary_raster = coolingContainer(temporary_raster,container_temp)

    # pad the raster to prevent overflow (pad width = diffusion_degree+1)
    padding = diffusion_degree + diffusion_degree
    temporary_raster = np.pad(temporary_raster,((padding,padding), (padding,padding)), constant_values=200)
    in_raster = np.pad(in_raster, ((padding,padding), (padding,padding)), constant_values=200)

    # set new dimensions after pad
    resY = np.shape(temporary_raster)[1]
    resX = np.shape(temporary_raster)[0]

    # loop through and calculate energy transfer per cell
    y = padding
    # loop through rows
    while y < resY-padding :

        # loop either from left to right or right to left in order to avoid drift effects
        if even(y):
            x = padding
            # loop from left to right
            while x < resX - padding:
                decider_diffusion_temp(in_raster, temporary_raster, x, y, diffusion_index, diffusion_degree)

                x += 1

        else:
            x = resX - padding
            # loop from right to left
            while x > 0 + padding:
                decider_diffusion_temp(in_raster, temporary_raster, x, y, diffusion_index, diffusion_degree)

                x -= 1



        y+=1

    # unpad the raster to regain its beauty [ymin,ymax][xmin,xmax]
    temporary_raster = temporary_raster[padding:-padding, padding:-padding]
    in_raster = in_raster[padding:-padding, padding:-padding]

    # clip the max/min values in order to avoid creating energy out of nothing
    temporary_raster = np.clip(temporary_raster,container_temp,fill_temp)

    # add in_raster to temporary raster to compute diffusion of energy
    temporary_raster = np.add(in_raster, temporary_raster)

    return temporary_raster

def decider_diffusion_temp(in_raster, temporary_raster, x, y, diffusion_index, diffusion_degree):
    '''decides from where to where diffusion is taking place, is executed on each pixel'''

    # locate the pixel the decider is assessing (x = columns, y=rows)!
    pixel = in_raster[x, y]

    # calculate and store relative indices of neighbouring cells, remove duplicates
    neighbouring_cells = neighbourhood(x,y,diffusion_degree)
    neighbour_values = []

    # remove indices according to radial settings to achieve pseudo-radial diffusion
    radial_remove(neighbouring_cells,diffusion_degree)

    # record neighbouring cells' values
    for neighbour in neighbouring_cells:
        neighbour_values.append(in_raster[neighbour])

    # define how much to diffuse in total
    #division = len(neighs)
    diff = pixel * diffusion_index

    # calculate absolute indices for neighbouring cells
    neighs = []
    for neighbour in neighbouring_cells:

        x_temp = x + neighbour[0]
        y_temp = y + neighbour[1]

        deg = diff_amount(neighbour[0],neighbour[1],diff,diffusion_degree)

        neighs.append((x_temp, y_temp, deg))



    # diffuse
    for neigh in neighs:

        try:
            # check that a double minus is not converted to plus
            if diff < 0 and temporary_raster[x, y] < 0:
                temporary_raster[neigh[0], neigh[1]] += neigh[2]


            else:
                temporary_raster[neigh[0], neigh[1]] -= neigh[2]


        except:
            #print("whoops")
            pass

    # account for energy leaving the origin cell
    # avoid double minus meaning plus
    if diff < 0 and in_raster[x,y] < 0:
        in_raster[x,y] += diff
    else:
        in_raster[x,y] -= diff



    return temporary_raster

def neighbourhood(x,y,degree):
    """finds surrounding pixel of the input pixel

    alternates between looping from minimum->maximum and maximum->minimum in order to eliminate sideways drift over time
    """

    neighbours = []

    # loop through rows
    a = y - degree

    while a < y + degree:

        # loop through columns
        if even(a):

            # if on an even column, loop row from left to right
            b = x - degree
            while b < x + degree:

                index_rel_a = y - a
                index_rel_b = x - b

                neighbours.append((index_rel_a, index_rel_b))

                b += 1
        else:
            # if on an even column, loop row from left to right
            b = x + degree
            while b > x - degree:

                index_rel_a = y - a
                index_rel_b = x - b

                neighbours.append((index_rel_a, index_rel_b))

                b -= 1

        a += 1

    return neighbours

def diff_amount(x,y,diff,diffusion_degree):
    '''returns the specific amount to be diffused to pixels of different distances'''

    # convert both indices to positive numbers for easy calculation
    xx = abs(x)
    yy = abs(y)


    # check in which degree of neighbourhood input pixel is located
    for deg in range(1,diffusion_degree+1):

        # if pixel is in current degree of neighbourhood
        if xx == deg or yy == deg:

            # calculate the amount of pixels in this neighbourhood degree
            neigh_deg = 8 * (2 ** deg - 1)

            # calculate the amount of energy to be diffused
            diff_amount = (diff * (0.5 / deg)) / neigh_deg
            return diff_amount

        else:
            pass


#---------------------------------------------------------
#                       GIF CONVERSION

def makeGif(mode, out_rasters, gif_duration, save_to_path='gifs/convection.gif'):
    '''create gif from individual timesteps

    mode == Do you want to export a gif or no (True/False)
    out_rasters == list of images to combine in gif
    duration == duration of each tick while playing the gif (seconds)'''

    if mode == True:
        print("creating .gif...")
        images = []

        for raster in out_rasters:
            images.append(imageio.imread(raster))
            imageio.mimsave(save_to_path, images, duration=gif_duration)

    else:
        pass

#---------------------------------------------------------