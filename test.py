import numpy as np
import random
from convectionModel.physics import neighbourhood

array = np.zeros(shape=(5,5))

x = 0

while x < 5:

    y=0
    while y < 5:

        array[x,y] = random.randint(0,15)
        neighbours = neighbourhood(x, y, 1)

        print("pixel at {},{} has value {}".format(x,y,array[x,y]))
        print("it has neighcbours {}\n".format(neighbours))
        print(array)
        y += 1
    x+=1

print(array)




