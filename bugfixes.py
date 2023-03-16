import numpy as np
from Class import Slicer
import matplotlib.pyplot as plt


# create square inside a square
poly = np.array([[0,0],[0,10],[10,10],[10,8],[1.25,8],[1.25,6],[10,6],[10,4],[3,4],[3,2],[10,2],[10,0]])


sliced = Slicer(0.4,1)

path,segments = sliced.zig_zag(poly)

plt.figure()
#plot poly and points
plt.plot(poly[:,0],poly[:,1])
# plt.plot([p[0] for p in points],[p[1] for p in points],'o')
#plot path
for segment in segments:
    plt.plot([segment[0][0],segment[1][0]],[segment[0][1],segment[1][1]])

plt.show()

