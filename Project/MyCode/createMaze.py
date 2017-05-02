import numpy as np
from math import ceil
import matplotlib.pyplot as pyplot

xspan, yspan, zspan = 120, 120, 50
myEnvironment = np.zeros((xspan, yspan,zspan),int)	
#myEnvironment[:,:,zspan-1] = 1
#myEnvironment[:,:,0] = 1
myEnvironment[round(xspan/5), round(yspan/4):yspan,:zspan] = 5
myEnvironment[round(xspan/5):round(xspan/3), round(yspan/4),:zspan] = 5
myEnvironment[round(xspan/2), :round(7*yspan/8),:zspan] = 5
myEnvironment[round(xspan/2):round(7*xspan/8),round(7*yspan/8),:zspan] = 5
myEnvironment[round(2*xspan/3):xspan, round(2*yspan/3),:zspan] = 5

start = (round(xspan/10), round(7*yspan/8), 0)
goal = (round(9*xspan/10), round(yspan/2), 0)
toShow = myEnvironment[:,:,:]
#toShow[start[0],start[1],start[2]] = 2
#toShow[goal[0],goal[1],goal[2]] = 2
pyplot.imshow(toShow[:,:,3],origin='lower')
print start
print goal
pyplot.show()

np.save('C:/Root/740/Project/Data/generatedEnvironment_8.npy', myEnvironment, 1, 1)
