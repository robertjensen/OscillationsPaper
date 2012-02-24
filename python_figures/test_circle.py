import matplotlib
import matplotlib.pyplot as plt
import numpy as np

N = 1000
R = np.random.rand(N)
Theta = np.random.rand(N)*2*np.pi
area = 25

colors = np.zeros(N)

for i in range(0,N):
    if (R[i]>0.7) and (Theta[i] < 1):
        colors[i] = 1
    
ax = plt.subplot(111, polar=True)

c = plt.scatter(Theta, R, c=colors, s=area)

c.set_alpha(0.75)


ax.tick_params(direction='in', length=3, width=1, colors='k',labelsize=6,axis='both',pad=3)
plt.setp(ax, xticks=[], yticks=[])

plt.show()