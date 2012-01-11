
#This will be a simple implementation of a program that summaries the oscillation period as a function of oscillation number
#We will also need a simple program that summarises duty cycle as a function of oscillation

import matplotlib
#matplotlib.use('svg')
#matplotlib.use('Agg')
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
for i in range(1,len(oscillations)):
    periods.append(oscillations[i]-oscillations[i-1])
    
    m44_average.append(average(data['M44'][mass_indexes[i-i]:mass_indexes[i],1]))
    m28_average.append(average(data['M28'][mass_indexes[i-i]:mass_indexes[i],1]))

#print len(periods)

fig = plt.figure()

axis = fig.add_subplot(1,1,1)
axis.plot(oscillations, m28_average, 'ro')
axis.plot(oscillations, m44_average, 'bo')
#axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
#axis.plot(data['M44'][:,0], data['M44'][:,1], 'b-')
#axis.set_ylim(0,7)
#axis.set_xlim(0,500)

axis.tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
axis.grid(True)    

#axis.set_ylabel('SEM Current / nA', fontsize=20)
axis.set_ylabel('Integrated charge (a.u.) / oscillation', fontsize=20)
axis.set_xlabel('Time/minutes', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../summary_of_long_measurement.png')
