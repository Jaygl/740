neighbors = []
for x in (-1, 0, 1):
	for y in (-1, 0, 1):
		for z in (-1, 0, 1):
			if not (x == 0 and y == 0 and z == 0):
				neighbors.append((x,y,z))

print neighbors
print len(neighbors)