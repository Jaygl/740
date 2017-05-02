import astarFunctions as fcn
import numpy as np
import time
#testingEnvironment = 4, alpha = .1, beta = .05 (77.744s) (4918 nodes)
emptyTest = 1
MAP = 4 
TARGET = 4

if MAP == 1:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_1.npy')
elif MAP == 3:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_3.npy')
elif MAP == 4:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_4.npy')
elif MAP == 5: #Maze 1
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_5.npy')
else:
    exit("MAP not found...")

if TARGET == 1:
    start = (20, 20, 3)
    goal = (115, 190, 5)
    #goals = np.array([[115., 190., 5.,    0.]]) # goal coordinates
elif TARGET == 2:
    start = (90, 50, 5)
    goal = (450, 200, 35)
    #goals = np.array([[450., 200., 35.,    0.]])
elif TARGET == 3:
    start = (90, 50, 5)
    goal = (450, 200, 5)
    #goals = np.array([[450., 200., 5.,    0.]])
elif TARGET == 4:
    start = (9,78,1)
    goal = (81,45,1)
    #goals = np.array([[81., 45., 0.,    0.]])
else:
    exit('That target location is undefined!')

#vol1 = vol1[:,:,0]

#This can be useful to test expanded nodes for an empty expanse.
#This will test tie-breaking ability...
if emptyTest:
    vol1 = np.zeros_like(vol1)
    start = (5,5,5)
    goal = (75,50,25)
final_pathX, final_pathY, final_pathZ = [start[0]], [start[1]], [start[2]]

tic1 = time.time()

path, num_expanded = fcn.astar(vol1, start, goal)

print path
print 'Number of expanded nodes' + str(num_expanded)
print 'Pathplanning time: ' + str(time.time() - tic1)

for x,y,z in path:
    final_pathX.append(x)
    final_pathY.append(y)
    final_pathZ.append(z)

import pdb; pdb.set_trace()  # breakpoint 97db5c81 //

#np.savez('AstarOutput', final_pathX, final_pathY, final_pathZ)

