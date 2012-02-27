
#This will be a simple implementation of a program that summaries the oscillation period as a function of oscillation number
#We will also need a simple program that summarises duty cycle as a function of oscillation

import matplotlib
#matplotlib.use('svg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb

def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print average([20, 30, 70])
    40.0
    """
    return sum(values, 0.0) / len(values)


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
mass_indexes = []
oscillations = [] #Holds the switching times
for row in data['M44']:
    i = i+1
    if (row[1] > (4.5)) and (old_m44<4.5):
        oscillations.append(row[0])
        old_m44 = row[1]
        mass_indexes.append(i)
        
    if (i%10==0):
        old_m44 = row[1]
    
    
periods = []
periods.append(0)
m44_average = []
m44_average.append(0)
m28_average = []
m28_average.append(0)
eff = []
eff.append(0)
for i in range(1,len(oscillations)):
    periods.append(oscillations[i]-oscillations[i-1])
    
    m44_av = average(data['M44'][mass_indexes[i-i]:mass_indexes[i],1])
    m44_average.append(m44_av)
    m28_av = average(data['M28'][mass_indexes[i-i]:mass_indexes[i],1])
    m28_average.append(m28_av)
    eff.append(m44_av/m28_av)

#print len(periods)

fig = plt.figure()
fig.subplots_adjust(bottom=0.2) # Make room for x-label
ratio = 0.61803398              # Golden mean
fig_width = 9
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

axis = fig.add_subplot(1,1,1)
axis.plot(oscillations, m28_average, 'r.',markersize=0.5)
axis.plot(oscillations, m44_average, 'b.',markersize=0.5)
axis.plot(oscillations, eff, 'k.',markersize=0.5)
#axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
#axis.plot(data['M44'][:,0], data['M44'][:,1], 'b-')
axis.set_ylim(1,4)
axis.set_xlim(700,6000)

axis.tick_params(direction='in', length=6, width=2, colors='k',labelsize=8,axis='both',pad=5)
axis.grid(False)    

#axis.set_ylabel('SEM Current / nA', fontsize=20)
axis.set_ylabel('Integrated charge (a.u.)', fontsize=8)
axis.set_xlabel('Time/minutes', fontsize=8)



#plt.tight_layout()
#plt.show()
plt.savefig('../duty_cycles_long_measurement_supplemental.png',dpi=300)
