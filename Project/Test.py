import numpy as np
from math import ceil
#from mpl_toolkits.mplot3d import Axes3D

#Need a "no trees intersecting things" correction
#Change coloration of the objects
#Transparency of Objects
#Show edges perhaps?

#Initialize the Environment
xspan, yspan, zspan = 500, 250, 50
myEnvironment = np.zeros((xspan, yspan,zspan),int)	

#Create Buildings
numBuildings = 3
buildingl = np.random.randint(round(xspan/10), round(xspan/5), numBuildings)
buildingw = np.random.randint(round(yspan/10), round(yspan/5), numBuildings)
buildingh = np.random.randint(round(zspan/3), round(zspan*1.25), numBuildings)
p_x = np.random.permutation(xspan)
p_y = np.random.permutation(yspan)
for k in range(0, len(buildingw)):
	myEnvironment[max(p_x[k]-buildingl[k], 0):min(p_x[k]+buildingl[k],xspan), 
		max(p_y[k]-buildingw[k],0):min(p_y[k]+buildingw[k],yspan), :min(zspan,buildingh[k])] = 2


#Create Trees
numtrees = min(ceil(xspan*yspan/100), yspan)
p_x = np.random.permutation(xspan)
p_y = np.random.permutation(yspan)
p_x = p_x[:numtrees-1]
p_y = p_y[:numtrees-1]
#Create Tree Trunk
treeheights = np.random.randint(round(zspan/3), zspan, numtrees)
for k in range(0, len(p_x)):
	if treeheights[k] < 20:
		tw = 0
	elif treeheights[k] < 35:
		tw = 1
	else:
		tw = 2
	#Check area for intersections. This needs to be upgraded
	if myEnvironment[p_x[k], p_y[k],1] < 1:
		myEnvironment[max(p_x[k]-tw,0):min(p_x[k]+tw,xspan), max(p_y[k]-tw, 0):
			min(p_y[k]+tw,yspan), :min(zspan,treeheights[k])] = 4#1
		for z in range(1, int(min(treeheights[k],zspan)/2)):
			z1 = round(z/2)
			myEnvironment[max(p_x[k]-z1,0):min(p_x[k]+z1,xspan),
				max(p_y[k]-z1,0):min(p_y[k]+z1,yspan), treeheights[k]-z] = 3
#Add Tree Tops



#Make a floor
myEnvironment[:,:,0] = 1

np.save('C:/Root/740/Project/Data/generatedEnvironment1.npy', myEnvironment, 1, 1)