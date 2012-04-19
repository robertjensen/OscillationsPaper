import matplotlib
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
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6303")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6305")
data['M44'] =  np.array(cursor.fetchall())

#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6309")
data['TEMPERATURE'] = np.array(cursor.fetchall())


fig = plt.figure()
fig.subplots_adjust(bottom=0.2) # Make room for x-label
fig.subplots_adjust(right=0.85) # Make room for second y-label

ratio = 0.61803398           # Golden mean
fig_width = 9
fig_width = fig_width /2.54        # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

axis = fig.add_subplot(1,1,1)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0,8)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(140,225)
axis2.set_yticks((190,200,210,220))
axis.set_xlim(30,250)
axis.grid(False)    

arrow = dict(facecolor='black',arrowstyle='->')
#arrow = dict(facecolor='black', shrink=0.085,width=1)
axis.annotate('CO', xy=(80, 3.5),  xycoords='data', xytext=(120, 4.5), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)
axis.annotate('CO$_2$', xy=(80, 1.2),  xycoords='data', xytext=(120, 2.25), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)
axis.annotate('Temp.', xy=(70, 5.7),  xycoords='data', xytext=(120, 7), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)

axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis2.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)

axis.set_ylabel('SEM Current / nA', fontsize=8)
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=8)
axis.set_xlabel('Time / minutes', fontsize=8)

#plt.tight_layout()
plt.show()
plt.savefig('../temperature_dependence_supplemental.png',dpi=300)
