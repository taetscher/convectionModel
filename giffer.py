import os
import imageio


files = os.listdir("output")
unsorted = []
sorted = []


for file in files:
    number = file[17:-4]
    unsorted.append(int(number))

unsorted.sort()


for number in unsorted:
    sorted.append("output/visualizationTest{}.png".format(number))


images = []
print("saving...")
for raster in sorted:
    images.append(imageio.imread(raster))
    imageio.mimsave("gifs/convection.gif", images, duration=0.2)
    print("...")


print("done, gif saved")
