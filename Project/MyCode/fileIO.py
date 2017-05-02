import numpy as np

def load_all(filename):

	_, ALGORITHM, MAP, TARGET, LONGPATH = filename.split('_')
	TARGET, LONGPATH = int(TARGET), int(LONGPATH)

	vol1 = np.load('C:/Root/740/Project/Data/generatedEnvironment_' + MAP + '.npy')

	if TARGET == 1:
		start = (20, 20, 3)
		goal = (115, 190, 5)
	elif TARGET == 2:
		start = (90, 50, 5)
		goal = (450, 200, 35)
	elif TARGET == 3:
		start = (90, 50, 5)
		goal = (450, 200, 5)
	elif TARGET == 4:
		start = (9,78,0)
		goal = (81,45,0)
	elif TARGET == 5:
   		start = (12,105,2)
   		goal = (108,60,2)
	elif TARGET == 6:
   		start = (25,218,5)
   		goal = (200,50,5)
	elif TARGET == 7:
   		start = (25,218,25)
   		goal = (200,50,25)	
	else:
		print(TARGET)
		exit('That target location is undefined!')
	temp = np.load('C:/Root/740/Project/Data/' + filename + '.npz')
	xpath, ypath, zpath, time_findPath = temp['arr_0'], temp['arr_1'], temp['arr_2'], temp['arr_3']
	xpath, ypath, zpath = temp['arr_0'], temp['arr_1'], temp['arr_2']

	if LONGPATH:
		cpath = np.load('C:/Root/740/Project/Data/Long_path_' + ALGORITHM + '_' + MAP + '_' + str(TARGET) + '.npy', encoding='bytes')
		cpos = np.load('C:/Root/740/Project/Data/Long_pos_' + ALGORITHM + '_' + MAP + '_' + str(TARGET) + '.npy', encoding='bytes')
	else:
		cpath = []
		cpos = []
	return vol1, xpath, ypath, zpath, time_findPath, start, goal, cpath, cpos

def save_all(ALGORITHM, MAP, TARGET, xpath, ypath, zpath, time_findPath, lifetime_path, lifetime_pos):
	filepath = 'C:/Root/740/Project/Data/'
	LONGPATH = 1
	if len(lifetime_path) == 0:
		LONGPATH = 0
	filemod = ALGORITHM + '_' + str(MAP) + '_' + str(TARGET) + '_' + str(LONGPATH)
	filemod2 = ALGORITHM + '_' + str(MAP) + '_' + str(TARGET)
	np.savez(filepath + 'Finaloutput_' + filemod, xpath, ypath, zpath, time_findPath)
	np.save(filepath + 'Long_path_' + filemod2, lifetime_path, True, True)
	np.save(filepath + 'Long_pos_' + filemod2, lifetime_pos, True, True)

	
