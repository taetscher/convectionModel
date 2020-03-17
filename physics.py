import numpy as np

# set up environmental raster
def environmental(resX,resY):

    '''creates a raster of size resX * resY, containing random values between 0 and 1

    resX, resY = pixel resolution of raster
    pre_fill = boolean; if True a container has been filled'''
    #sets up random raster conaining values between 0 and 1


    temperature_raster = np.array(np.random.uniform(low=15,high=25,size=(resX, resY)))

    return temperature_raster

#---------------------------------------------------------
#                       CONTAINER STUFF
# set up container
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

#pre-fill container
def containerPreFill(container, raster, resX, resY, filling_height, fill_temp):

    '''pre-fills the container with fluid.

    container = dictionary of corners of container
    raster = raster to do operation on
    resX, resY = pixel resolution of raster
    fill_temp = temperature of filled in liquid'''



    #set up fill coordinates
    fill_bl = [(container['container_bl'][0])+1,(container['container_bl'][1])+1]
    fill_tl = [(container['container_tl'][0])+1,(container['container_tl'][1])+1]
    fill_br = [(container['container_br'][0])-1,(container['container_br'][1])-1]
    fill_tr = [(container['container_tr'][0])-1,(container['container_tr'][1])-1]

    fill = [fill_bl,fill_tl,fill_br,fill_tr]

    #fill container
    x =0

    #iterate through rows
    while x < resX:
        y = 0
        #iterate through columns
        while y < resY:

            try:
                #only do this if the selected pixel is within the container
                if x >= fill_bl[0] and x <= fill_br[0]:
                    if y >= resY*filling_height and y <= resY-2:
                        raster[y, x] = fill_temp


            except:
                # this is to prevent the program from collapsing in case one of the above conditions tries to
                # access a pixel outside of the range of a numpy array, like a pixel with index particles[-10,
                # -10] in that case the program should just pass the condition and move on
                print("Pixel out of bounds of np array!")
                pass


            y+=1

        x += 1

    #output raster with pre-filled container
    return raster

def containerFill(container, temperature=20):

    '''fills a container with a liquid at specified temperature (degrees celsius). pours from pixel at (x=xmax*0.5,y=0)'''

    pass

#---------------------------------------------------------
#                       PHYSICS STUFF


def diffusion(in_raster, resX, resY, diffusion_index, container_temp):

    """Calculates how much the liquid rises and diffuses energy
    because of its temperature.

    - based on input raster with temperatures """

    temporary_raster = np.zeros(shape=(resX, resY), dtype=int)
    edges = [[0, resY-1],[resX-1, 0],[0, resX-1],[resY-1, 0]]
    for edge in edges:
        np.put(temporary_raster,edge,20)
        print(temporary_raster)

    x = 0

    while x < resX-1:

        y = 0
        while y < resY-1:

            temporary_raster = decider_diffusion(in_raster,temporary_raster,x,y, diffusion_index)
            #print(decided)

            y+=1
        x+=1






    out_raster = np.add(in_raster, temporary_raster)
    return out_raster






def decider_diffusion(in_raster, temporary_raster, x, y, diffusion_index):
    '''decides from where to where diffusion is taking place'''

    pixel = in_raster[x, y]

    neighbouring_cells = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    neighbour_values = []

    for neighbour in neighbouring_cells:
        neighbour_values.append(in_raster[neighbour])

    minimum = min(neighbour_values)
    min_index = neighbour_values.index(minimum)
    maximum = max(neighbour_values)
    max_index = neighbour_values.index(maximum)

    if pixel > maximum:
        #value of pixel is highest in surroundings
        #print("pixel value is {}, max value is {}".format(pixel, maximum))

        #calculation of energy exchange
        diff = pixel*diffusion_index
        tempX = x+neighbouring_cells[min_index][0]
        tempY = y+neighbouring_cells[min_index][1]

        if tempX < 0 or tempY < 0:
            #print("tried to access pixel out of bounds")
            pass

        else:
            count = minCounter(neighbour_values)

            if count > 1:
                print(count)
            else:
                pass
            temporary_raster[x, y] = pixel - diff
            temporary_raster[tempX, tempY] += diff


        #print("pixel at {},{} gave {} to temp_pixel at {},{}".format(x,y,diff,tempX,tempY))
        #print("{},{}---->{},{}\n\n".format(x, y, tempX, tempY))

    elif pixel < minimum:
        #value of pixel is lowest in surroundings
        #print("pixel value is {}, min value is {}".format(pixel, minimum))

        # calculation of energy exchange
        diff = maximum * diffusion_index
        tempX = x + neighbouring_cells[max_index][0]
        tempY = y + neighbouring_cells[max_index][1]

        if tempX < 0 or tempY < 0:
            #print("tried to access pixel out of bounds")
            pass

        else:
            count = maxCounter(neighbour_values)
            if count > 1:
                print(count)
            else:
                pass
            temporary_raster[x, y] += pixel+diff
            temporary_raster[tempX, tempY] -= diff

        #print("pixel at {},{} gave {} to temp_pixel at {},{}".format(x,y,diff,tempX,tempY))
        #print("{},{}---->{},{}\n\n".format(x, y, tempX, tempY))

    elif minimum < pixel < maximum:
        #value of pixel is in range of surrounding values
        #print("pixel value is {}, range is from {} to {}".format(pixel, minimum, maximum))

        diff = maximum * diffusion_index
        tempX = x + (neighbouring_cells[max_index][0])
        tempY = y + (neighbouring_cells[max_index][1])

        if tempX < 0 or tempY < 0:
            #print("tried to access pixel out of bounds")
            pass

        else:
            temporary_raster[x, y] += pixel+diff
            temporary_raster[tempX,tempY] -= diff

        #print("pixel at {},{} gave {} to temp_pixel at {},{}".format(x,y,diff,tempX,tempY))
        #print("{},{}---->{},{}\n\n".format(x,y,tempX,tempY))

    else:
        #print("What the hell happened here at pixel {},{}??".format(x,y))
        pass

    return temporary_raster

def maxCounter(list):

    count = list.count(max(list))
    return count

def minCounter(list):
    count = list.count(min(list))
    return count





def gravity():
    """introduces gravity for liquid in container"""
    pass

def materials(in_raster, resX, resY, fill_temp):
    '''Gets information on materials from initial raster.

    0 == Air

    2 == Container

    3 == Pre-fill Liquid

    '''


    materials_raster = np.zeros((resX,resY))

    #iterate through input raster to get data on materials
    x=0

    while x <= resX-1:

        y=0

        while y <= resY-1:

            pixel = in_raster[x,y]

            if pixel == -10:
                materials_raster[x,y] = 2

            elif pixel == fill_temp:
                materials_raster[x,y] = 3
            else:
                pass



            y += 1

        x += 1

    return materials_raster


#---------------------------------------------------------

#---------------------------------------------------------




#---------------------------------------------------------





