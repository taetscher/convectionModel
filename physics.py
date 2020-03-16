import numpy as np

# set up environmental raster
def environmental(resX,resY):

    '''creates a raster of size resX * resY, containing random values between 0 and 1'''

    #sets up random raster conaining values between 0 and 1
    env_raster = np.array(np.random.random((resX, resY)))

    return env_raster


# set up container
def addContainer(raster):

    '''Adds a container to the input raster layer where the container is centered, half as wide as the raster itself
    and half as high as the raster itself.'''

    #add container to raster
    color_value=-10

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



def containerPreFill(container):

    '''pre-fills the container with fluid'''

    filling_height = 0.75
    color_value = -10





    pass

def containerFill(container, temperature=20):

    '''fills a container with a liquid at specified temperature (degrees celsius). pours from pixel at (x=xmax*0.5,y=0)'''

    pass





