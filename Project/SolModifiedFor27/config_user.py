# Configuration File

#List of required changes:
#d mapscale - probably needs to be set to 1
#d sizeX, sizeY, sizeZ 
#d start
#d goals
# rXstart, rYstart, rZstart, rXdim, rYdim, rZdim
# obstacles

#Changes for AFTER it is working
# Can't do any plotting now, but if I adapt to py34 and vispy...
# initX, initY, initZ   <-  not using moving goals yet
# T?   <-  appears to be part of moving goals

from __future__ import division
import math
import collections
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sys import exit

testingEnvironment = 4

if testingEnvironment == 1:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_1.npy')
    start = (20, 20, 3)
    goals = np.array([[115., 190., 5.,    0.]]) # goal coordinates
elif testingEnvironment == 3:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_3.npy')
    start = (90,50,5)
    goals = np.array([[450., 200., 35.,    0.]])
elif testingEnvironment == 4:
    vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_4.npy')
    start = (90,50,5)
    goals = np.array([[450., 200., 5.,    0.]])
else:
    exit("testingEnvironment not found...")

sizeX, sizeY, sizeZ = vol1.shape 
#mapscale probably needs to be set to 1 (1)
mapscale = 1

testingMode = False             # suppresses figure generation, outputs from main*.py are not printed
makeFigure = True
makeMovie = False
startWithEmptyMap = True
makeRandObs = False
useMovingGoals = False
restrictVerticalMovement = False
useHierarchicalPlanning = True
numHierLevels = 0

percentFixedRandomObstacles = 0
safetymargin = 1
cX, cY, cZ = 1, 1, 1 #1, 1, 2  # cX and cY currently are unused - modify computeCost if desired
heuristicScale = 1.01

searchRadius = 20
refinementDistance = math.ceil(searchRadius * 1)    # must be an integer
t_max = float('inf')             # Max time to spend on path-finding, in milliseconds. Enter inf to prevent restriction

# Configure Moving Goals
initX = [60, 20]# [12, 6]
initY = [50, 50]#[3, 2]
initZ = [6, 6]#[4, 7]
T = [5, 4]#[5, 2]

# Fixed Individual Obstacles
obstacles = []

# Fixed Rectangular Obstacles
#rXstart = [8,  12, 15,  35, 41, 49]
#rYstart = [2,  15, 35, 10, 20, 47]
#rZstart = [1,  1,  1,  1,  1,  1]
#rXdim   = [4,  20, 30, 5,  8,  6]
#rYdim   = [9,  12, 8,  5,  8,  6]
#rZdim   = [30,  8, 15, 28, 20, 28]

rXstart = []
rYstart = []
rZstart = []
rXdim   = []
rYdim   = []
rZdim   = []

vidname = 'dstarVid'
fps = 10                 # higher = faster playback speed
dpi = 500               # higher = better quality, slower runtime
imgformat = 'png'       # currently only works for png

# Generate Random Dynamic Obstacles
randomint = np.random.random_integers

minObs = 5
maxObs = 50
maxPercent = 5
seedDyn = np.random.randint(0,1000)
#seedDyn = np.random.randint(0,10)
#seedDyn = 432

# Generate Random Fixed Obstacles
num2gen = int(round(percentFixedRandomObstacles/100 * sizeX*sizeY*sizeZ))
seedStatic = np.random.random_integers(0,1000)
#seedStatic = np.random.random_integers(0,10
#seedStatic = 141

"""
====================================================================================
================== Variables below this line are not user inputs ===================
============== They are here for configuration or to create variables ==============
====================================================================================
============== The " # Additional variables " block at the very bottom =============
============== is the exception to this and may be modified if desired =============
====================================================================================
"""

# if testingEnvironment == '3DF_20':
#     sizeX, sizeY, sizeZ = 150, 150, 150
#     start = (75,75,75)
#     goals = np.array([[150, 150, 150, 0]])
#     percentFixedRandomObstacles = 20
#     restrictVerticalMovement = False
#     cX, cY, cZ = 1, 1, 1
#     searchRadius = 7
#     percentFixedRandomObstacles = 20
#
# elif testingEnvironment == '3DF_50':
#     sizeX, sizeY, sizeZ = 150, 150, 150
#     start = (75,75,75)
#     goals = np.array([[150, 150, 150, 0]])
#     percentFixedRandomObstacles = 20
#     restrictVerticalMovement = False
#     cX, cY, cZ = 1, 1, 1
#     searchRadius = 7
#     percentFixedRandomObstacles = 50
#
# elif testingEnvironment == 'city':
#     sizeX = 64
#     sizeY = 64
#     sizeZ = 64
#     start = (3*mapscale , 4*mapscale, 6*mapscale)
#     goals = np.array([[62., 60., 6.,    0.]])  * mapscale
#     percentFixedRandomObstacles = 0
#
#     rXstart = [8,  12, 15,  35, 41, 49]
#     rYstart = [2,  15, 35, 10, 20, 47]
#     rZstart = [1,  1,  1,  1,  1,  1]
#     rXdim =   [4,  20, 30, 5,  8,  6]
#     rYdim =   [9,  12, 8,  5,  8,  6]
#     rZdim =   [30,  8, 15, 28, 20, 28]
#
# elif testingEnvironment == 'random':
#     sizeX = 150
#     sizeY = 150
#     sizeZ = 150
#     start = (5 , 5, sizeZ/2)
#     goals = np.array([[sizeX-5., sizeY-5., sizeZ/2., 0.]])

# Modifying by scale factor
# This can probably all be cut out...
#initX = [mapscale*point for point in initX]
#initZ = [mapscale*point for point in initZ]
#initY = [mapscale*point for point in initY]

#rXstart = [mapscale*(point) for point in rXstart if point >= 1]
#rYstart = [mapscale*(point) for point in rYstart if point >= 1]
#rZstart = [point for point in rZstart if point >= 1]
#rXdim = [mapscale*(point) for point in rXdim if point <= sizeX]
#rYdim = [mapscale*(point) for point in rYdim if point <= sizeY]
#rZdim = [mapscale*(point) for point in rZdim if point <= sizeZ]

#sizeX *= mapscale
#sizeY *= mapscale
#sizeZ *= mapscale

if testingMode:
    makeFigure = False
    makeMovie = False

if makeMovie:
    makeFigure = True

if not useMovingGoals:
    initX = []
    initY = []
    initZ = []
    T = []

goalsVisited, goalhandles, numGoals, goal = [], [], [], []
stepCount = 1              # number of total iterations
number_of_obstacles = 0    # for genRandObs function
numNodes = sizeX*sizeY*sizeZ
goalMoved = False
numlevels = 0

# Set up initial heading angles to factor in direction of travel
oldstart = None

# Set up UAV map and plot
map_ = collections.defaultdict(lambda : 0)
costMatrix = collections.defaultdict(lambda: 1)

if makeFigure:
    fig1 = plt.figure()
    #ax1 = fig1.add_subplot(111, projection='3d')
    ax1 = fig1.gca(projection='3d')

# Used to save some variables
hdl = []
closed_list = 0
output = {}

# Additional variables
zf1, zf2 = 1, 0             # provides more flexibility over coarse z-movement; zf1 = multiplier, zf2 = added constant
                                # use (1,0) for default, or (0,x) to set coarse z-successors at a distance of x
distancerequirement = 7     # used in findPath function. determines cluster size used for coarse paths
                                # shorter = faster, but may have longer paths
                                # too small and it may not find a path, so >=6 recommended
minclustersize = 4          # represents dimension of smallest cluster in terms of L0 nodes
alpha = 0.5             # use 0.5 for centripetal splines
splinePoints = 5        # Enter 2 to not use splines, otherwise 5 is recommended