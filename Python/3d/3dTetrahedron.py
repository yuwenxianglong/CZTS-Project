from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig=plt.figure()
ax = Axes3D(fig)

# Face 1
x1 = np.array([[0, 0.5, 0.5, 1],
               [0, 0, 0, 0]])
y1 = np.array([[0, 0.866, 0.866, 0],
               [0, 0, 0, 0]])
z1 = np.array([[0, 0, 0, 0],
               [0, 0, 0, 0]])

# Face 2
x2 = np.array([[0, 0.5, 0.5, 0],
               [0, 0, 0, 0]])
y2 = np.array([[0, 0.866, 0.433013, 0],
               [0, 0, 0, 0]])
z2 = np.array([[0, 0, 0.866, 0],
               [0, 0, 0, 0]])
# Face 3
x3 = np.array([[1, 0.5, 0.5, 1],
               [1, 1, 1, 1]])
y3 = np.array([[0, 0.866, 0.433013, 0],
               [0, 0, 0, 0]])
z3 = np.array([[0, 0, 0.866, 0],
               [0, 0, 0, 0]])

# Face 5
x4 = np.array([[1, 0, 0.5, 1],
               [1, 1, 1, 1]])
y4 = np.array([[0, 0, 0.433013, 0],
               [0, 0, 0, 0]])
z4 = np.array([[0, 0, 0.866, 0],
               [0, 0, 0, 0]])

#ax.plot_surface(x1,y1,z1)
ax.plot_surface(x2,y2,z2)
ax.plot_surface(x3,y3,z3)
ax.plot_surface(x4,y4,z4)
print x1

#0.433
plt.show()