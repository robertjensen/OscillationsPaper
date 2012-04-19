#This will be a simple implementation of a program that summaries the oscillation period as a function of oscillation number
#We will also need a simple program that summarises duty cycle as a function of oscillation

import matplotlib
#matplotlib.use('svg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb
from scipy import optimize

matplotlib.rc('text',usetex=True) # Magic fix for the font warnings

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

data = {}
#Mass28
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 6133")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 6135")
data['M44'] =  np.array(cursor.fetchall())

#Limit: everytime M44 goes above 4.5nA we start a new oscillation
i = 0
old_m44 = 0
oscillations = [] #Holds the switching times
for row in data['M44']:
    i = i+1
    if (row[1] > (4.5)) and (old_m44<4.5):
        oscillations.append(row[0])
        old_m44 = row[1]
        
    if (i%10==0):
        old_m44 = row[1]
    

    
periods = []
periods.append(0)
for i in range(1,len(oscillations)):
    periods.append(oscillations[i]-oscillations[i-1])

#print len(periods)

fig = plt.figure()
fig.subplots_adjust(bottom=0.2) # Make room for x-label
ratio = 0.61803398              # Golden mean
fig_width = 9
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)


axis = fig.add_subplot(1,1,1)
axis.plot(oscillations, periods, 'b.')
#axis.plot([750,6000],[1.8,17],'r-')
#axis.plot([750,5000],[5,43],'r-')
range = np.arange(700,6500)

fitfunc = lambda p, x: p[0]*(x**p[1])+p[2]       # Target function
errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
p0 = [0.2,0.6,2] # Initial guess for the parameters
p1, success = optimize.leastsq(errfunc, p0[:], args=([700,1000,2000,4000,6000],[4,6,20,37,45]),maxfev=1000)
print p1, success
axis.plot(range,p1[0]*(range**(p1[1]))+p1[2],'r-')

p1, success = optimize.leastsq(errfunc, p0[:], args=([500,1000,2000,4000,6000],[0,2,9,11,16]),maxfev=1000)
print p1, success
axis.plot(range,p1[0]*(range**(p1[1]))+p1[2],'r-')
#axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
#axis.plot(data['M44'][:,0], data['M44'][:,1], 'b-')
#axis.set_ylim(0,7)
#axis.set_xlim(0,500)

axis.tick_params(direction='in', length=6, width=2, colors='k',labelsize=8,axis='both',pad=3)
axis.grid(False)    

axis.set_ylabel('Oscil. period / minutes', fontsize=8)
axis.set_xlabel('Time / minutes', fontsize=8)

a = plt.axes([.18, .65, .3, .15], axisbg='w')
a.plot(oscillations, periods, 'b,')
a.tick_params(direction='in', length=3, width=1, colors='k',labelsize=6,axis='both',pad=3)
plt.setp(a, xlim=(700,1500), ylim=(2,8),xticks=[900,1100,1300], yticks=[3,5,7])

#plt.tight_layout()
#plt.show()
plt.savefig('../summary_of_long_measurement.png',dpi=300)
