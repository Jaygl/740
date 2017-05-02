import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2*np.pi*t)
plt.rcParams.update({'font.size': 40})
plt.plot(time_findPath)
plt.xlabel('Step')
plt.ylabel('Time (s)')
plt.title('Path Planning Time')
plt.grid(True)
plt.show()
#plt.savefig("test.png")
