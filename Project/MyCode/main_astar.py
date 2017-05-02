import astarFunctions as fcn
import numpy as np
import time
import fileIO as fl

sensor_range = 20
MAP = 4
TARGET = 3

if MAP == 1:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_1.npy')
elif MAP == 3:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_3.npy')
elif MAP == 4:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_4.npy')
elif MAP == 5: #Maze 1
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_5.npy')
elif MAP == 6: #Maze 2
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_6.npy')
elif MAP == 7:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_7.npy')
elif MAP == 8:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_8.npy')
else:
    exit("MAP not found...")

if TARGET == 1:
    start = (20, 20, 3)
    goal = (115, 190, 5)
    goals = np.array([[115., 190., 5.,    0.]]) # goal coordinates
elif TARGET == 2:
    start = (90, 50, 5)
    goal = (450, 200, 35)
    goals = np.array([[450., 200., 35.,    0.]])
elif TARGET == 3:
    start = (90, 50, 5)
    goal = (450, 200, 5)
    goals = np.array([[450., 200., 5.,    0.]])
elif TARGET == 4:
    start = (9,78,1)
    goal = (81,45,1)
    goals = np.array([[81., 45., 1.,    0.]])
elif TARGET == 5:
    start = (12,105,2)
    goal = (108,60,2)
    goals = np.array([[108., 60., 2.,    0.]])
elif TARGET == 6:
    start = (25,218,5)
    goal = (200,50,5)
    goals = np.array([[200., 50., 5.,    0.]])
elif TARGET == 7:
    start = (12,105,25)
    goal = (108,60,25)
    goals = np.array([[108., 60., 25.,    0.]])
else:
    exit('That target location is undefined!')
#This can be useful to test expanded nodes for an empty expanse.
#This will test tie-breaking ability...
#vol1 = np.zeros_like(vol1)

final_pathX, final_pathY, final_pathZ = [start[0]], [start[1]], [start[2]]
current = start
tic1 = time.time()
path_planning_time = []
expanded_nodes = 0
path_final = [start]
vol2 = np.zeros_like(vol1)
lifetime_path = []
lifetime_pos = []

xSize, ySize, zSize = vol1.shape 

while current != goal:
    #UPDATE VISIBLE VOLUME
    vol2[max(current[0]-sensor_range,0):min(current[0]+sensor_range, xSize), 
        max(current[1]-sensor_range,0):min(current[1]+sensor_range, ySize),
        max(current[2]-sensor_range,0):min(current[2]+sensor_range, zSize)] = vol1[max(current[0]-sensor_range,0):min(current[0]+sensor_range, xSize), 
        max(current[1]-sensor_range,0):min(current[1]+sensor_range, ySize),
        max(current[2]-sensor_range,0):min(current[2]+sensor_range, zSize)]
    print(current)
    #PLAN PATH TO GOAL 
    tic2 = time.time()
    path, num_expanded = fcn.astar(vol2, current, goal)
    path_planning_time.append(time.time() - tic2)
    
    current = path[0]
    #print current
    expanded_nodes += num_expanded
    lifetime_path.append(path)
    lifetime_pos.append(len(path_final))
    path_final.append(current)
    #print path_planning_time[-1]
    #time.sleep(.1)
path_final.append(goal)

mean_time_findPath = 1000*sum(path_planning_time) / len(path_planning_time)
#print path_final
print 'Number of expanded nodes: ' + str(expanded_nodes)
print 'Pathplanning time: ' + str(time.time() - tic1)
print 'Mean Path-finding Time: ' + str(mean_time_findPath) + ' ms'
print 'Min Path-finding Time: ' + str(1000* min(path_planning_time)) + ' ms'
print 'Max Path-finding Time: ' + str(1000* max(path_planning_time)) + ' ms'
for x,y,z in path_final:
    final_pathX.append(x)
    final_pathY.append(y)
    final_pathZ.append(z)
diffs = []
for k in xrange(1,len(final_pathX)):
    dx = final_pathX[k] - final_pathX[k-1]
    dy = final_pathY[k] - final_pathY[k-1]
    dz = final_pathZ[k] - final_pathZ[k-1]
    diffs.append(sqrt(dx*dx + dy*dy + dz*dz))

import pdb; pdb.set_trace()  # breakpoint f6a3a7db //

fl.save_all('A', MAP, TARGET, final_pathX, final_pathY, final_pathZ, path_planning_time, lifetime_path, lifetime_pos)

#np.savez('AstarOutput', final_pathX, final_pathY, final_pathZ)

