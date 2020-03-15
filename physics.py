import numpy as np



# set up environmental raster
def environmental(resX,resY):

    #sets up random raster conaining values between 0 and 1
    env_raster = np.array(np.random.random((resX, resY)))

    return env_raster




# set up container
def addContainer(raster):

    #add container to raster

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

    print("Corners:\ntl: {}\nbl: {}\ntr: {}\nbr: {}".format(container_tl,container_bl,container_tr,container_br))


    # create bottom of container
    col_cont_bl = container_bl[0]
    col_cont_br = container_br[0]

    # get rows/cols of edges of container
    bottomrow_index = y_dim - 1
    bottomedge_row = raster[-1,:]
    leftedge_col = raster[:,container_tl[0]]
    rightedge_col = raster[:,container_tr[0]]

    print("leftedge col: {}".format(leftedge_col))



    #set edges of container to be values to 10
    np.put(bottomedge_row, [range(container_bl[0], container_br[0]+1)],v=10)
    np.put(leftedge_col, [range(container_tl[1], bottomrow_index)], v=10)
    np.put(rightedge_col, [range(container_tr[1], bottomrow_index)], v=10)

    print(bottomedge_row)
    print("leftedge col: {}".format(leftedge_col))
    print("rightedge col: {}".format(rightedge_col))








