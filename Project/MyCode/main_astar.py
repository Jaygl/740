import astarFunctions as fcn
import numpy as np
import time

testingEnvironment = 4
tic1 = time.time()

if testingEnvironment == 1:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_1.npy')
    start = (20, 20, 3)
    goal = (115,190,5)
elif testingEnvironment == 3:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_3.npy')
    start = (90,50,5)
    goal = (450,200,35)
elif testingEnvironment == 4:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_4.npy')
    start = (90,50,5)
    goal = (150, 60, 20) #Set here for testing purposes
    goal = (450,200,5)
else:
    exit("testingEnvironment not found...")

final_pathX, final_pathY, final_pathZ = [start[0]], [start[1]], [start[2]]

path, num_expanded = fcn.astar(vol1, start, goal)

print path
print 'Number of expanded nodes' + str(num_expanded)
print 'Pathplanning time: ' + str(time.time() - tic1)

for x,y,z in path:
    final_pathX.append(x)
    final_pathY.append(y)
    final_pathZ.append(z)

np.savez('AstarOutput', final_pathX, final_pathY, final_pathZ)

