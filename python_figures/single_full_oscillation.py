import matplotlib
#matplotlib.use('svg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

data = {}
#Mass28
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 572")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 573")
data['M44'] =  np.array(cursor.fetchall())

#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 578")
data['TEMPERATURE'] = np.array(cursor.fetchall())


fig = plt.figure()
fig.subplots_adjust(bottom=0.2) # Make room for x-label

#ratio = 0.61803398           # Golden mean
ratio = 0.4                  # This figure should be very wide to span two columns
fig_width = 17
fig_width = fig_width /2.54        # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

axis = fig.add_subplot(1,1,1)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0.1,1.2)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(160,205)
axis2.set_yticks((170,180,190,200))
axis.set_xlim(1001,1133)
axis.grid(True)    

arrow = dict(facecolor='black', shrink=0.085,width=1)
axis.annotate('M28', xy=(1040, 0.83),  xycoords='data', xytext=(1058, 0.93), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)
axis.annotate('M44', xy=(1040, 0.41),  xycoords='data', xytext=(1058, 0.27), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)
axis.annotate('Temp.', xy=(1070, 1.08),  xycoords='data', xytext=(1095, 0.93), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)

axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis2.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)

axis.set_ylabel('SEM Current / nA', fontsize=8)
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=8)
axis.set_xlabel('Time/minutes', fontsize=8)

#plt.tight_layout()
plt.show()
plt.savefig('../single_full_oscillation.png',dpi=300)
