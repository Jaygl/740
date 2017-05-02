# Based on an A* implementation (2D) by Christian Careaga (christian.careaga7@gmail.com)

import numpy as np
from heapq import *
from math import sqrt, ceil
from time import sleep

alpha = .01
beta = .05
#FOR TESTING NODE EXPANSIONS
#alpha = 0
#beta = 0
def heuristic(a, b):
    #Distance squared <- Not good, but it came this way
    #return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) **2
    
    #Distance <- This takes forever
    #return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) **2)

    # Diagonal Distance
    dv = (abs(b[0] - a[0]), abs(b[1] - a[1]), abs(b[2] - a[2]))
    triples = min(dv);
    doubles = min([dv[x] for x in [0,1,2] if x != dv.index(triples)]) - triples
    return sum(dv) - (3 - sqrt(3))*triples - (2 - sqrt(2))*doubles

def distance(a, b):
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) **2)

def astar(array, start, goal):
    shortest_dist = distance(start, goal)
    neighbors = []
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            for z in (-1, 0, 1):
                if not (x == 0 and y == 0 and z == 0):
                    neighbors.append((x,y,z))
    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}

    oheap = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:
        #Current node is the "best" node in the heap
        current = heappop(oheap)[1]
        #print 'Start: ' + str(start) + '   Goal: ' + str(goal)
        #print 'Best node:' + str(current)
        #sleep(.1)
        #print current
        #sleep(.01)
        #Found the goal location, save path and return
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data = data[::-1]
            num_expanded = len(close_set)
            
            return data, num_expanded

        #Add current to the closed list
        close_set.add(current)

        #Expand each neighbor if it is inside the boundary
        for i, j, k in neighbors:
            neighbor = current[0] + i, current[1] + j, current[2] + k           
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if 0 <= neighbor[2] < array.shape[2]:
                        if array[neighbor[0]][neighbor[1]][neighbor[2]] >= 1:
                            continue
                    else:
                        # array bound z walls
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
            
            #g_score is the distance from start node to current position
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            #print 'Neighbor: ' + str(neighbor)
            #print 'tentative_g_score: ' + str(tentative_g_score)
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                #print 'No update required'
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                #print 'Adding neighbor values'
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                #beta = 0 and alpha = 0.01 worked pretty well
                fscore[neighbor] = tentative_g_score + (1+alpha)*heuristic(neighbor, goal) + beta * distance(neighbor, goal)/shortest_dist
                #beta = .01 and alpha = 0 worked pretty well...
                #fscore[neighbor] = tentative_g_score + (1+alpha)*heuristic(neighbor, goal) + beta * distance(neighbor, goal)/shortest_dist
                heappush(oheap, (fscore[neighbor], neighbor))
                #print 'Fscore: ' + str(fscore[neighbor])

    return False

'''Here is an example of using my algo with a numpy array,
   astar(array, start, destination)
   astar function returns a list of points (shortest path)'''

#nmap = np.array([
#    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#    [1,1,1,1,1,1,1,1,1,1,1,1,0,1],
#    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#    [1,0,1,1,1,1,1,1,1,1,1,1,1,1],
#    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#    [1,1,1,1,1,1,1,1,1,1,1,1,0,1],
#    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#    [1,0,1,1,1,1,1,1,1,1,1,1,1,1],
#    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#    [1,1,1,1,1,1,1,1,1,1,1,1,0,1],
#    [0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
#nmap = np.repeat(nmap[:, :, np.newaxis], 2, axis=2)
    
#print astar(nmap, (0,0,0), (10,13,0))