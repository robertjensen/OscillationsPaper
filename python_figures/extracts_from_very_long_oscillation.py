import matplotlib
#matplotlib.use('svg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb

matplotlib.rc('text',usetex=True) # Magic fix for the font warnings

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

data = {}
#Mass28
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6133")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6135")
data['M44'] =  np.array(cursor.fetchall())

#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6139")
data['TEMPERATURE'] = np.array(cursor.fetchall())

fig = plt.figure()
fig.subplots_adjust(bottom=0.1) # Make room for x-label
fig.subplots_adjust(right=0.85) # Make room for right y-label
#ratio = 0.61803398              # Golden mean
ratio = 1
fig_width = 12
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

axis_array = []
axis2_array = []

limit = []
#limit.append((700,900))
limit.append((700,800))
#limit.append((2800,3000))
limit.append((2800,2900))
#limit.append((5800,6000))
limit.append((5900,6000))

for i in range(0,3):
    axis_array.append(fig.add_subplot(3,1,i+1))
    axis_array[i].plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
    axis_array[i].plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
    axis_array[i].set_ylim(0,7)
    axis2_array.append(axis_array[i].twinx())
    axis2_array[i].plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
    axis2_array[i].set_ylim(181,229)
    axis_array[i].set_xlim(limit[i])
    axis_array[i].set_yticks((1,3,5))
    
    axis_array[i].tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=2)
    axis2_array[i].tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='y',pad=2)
    axis_array[i].grid(False)    

arrow = dict(facecolor='black',arrowstyle='->')
axis_array[0].annotate('CO', xy=(710, 3.9),  xycoords='data', xytext=(710, 5.7), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=8,)
axis_array[0].annotate('CO$_2$', xy=(725, 1.7),  xycoords='data', xytext=(715, 0.5), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=8,)
axis_array[0].annotate('T', xy=(728, 4.9),  xycoords='data', xytext=(720, 5.3), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=8,)

axis_array[1].set_ylabel('SEM Current / nA', fontsize=8)
axis2_array[1].set_ylabel('Temperature / $^\circ$C', fontsize=8)
axis_array[2].set_xlabel('Time / min', fontsize=8)


#plt.tight_layout()
#plt.show()
plt.savefig('../extracts_from_very_long_oscillation.eps')
