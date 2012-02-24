#import matplotlib
#import matplotlib.pyplot as plt
#import numpy as np


from pylab import *

N = 1000

R = rand(N)
Theta = rand(N)*2*pi
area = 25

colors = zeros(N)


for i in range(0,N):
    if (R[i]>0.7) and (Theta[i] < 1):
        colors[i] = 1
    
ax = subplot(111, polar=True)

c = scatter(Theta, R, c=colors, s=area)

c.set_alpha(0.75)


ax.tick_params(direction='in', length=3, width=1, colors='k',labelsize=6,axis='both',pad=3)
setp(ax, xticks=[], yticks=[])

show()