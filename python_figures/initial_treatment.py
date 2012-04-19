import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import MySQLdb
from matplotlib.patches import Rectangle

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
fig.subplots_adjust(right=0.85) # Make room for second y-label

#ratio = 0.61803398           # Golden mean
ratio = 0.9
fig_width = 9
fig_width = fig_width /2.54        # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)


gs = gridspec.GridSpec(2, 2)

gs.update(wspace=0.1,hspace=0.4)

axis = plt.subplot(gs[0, :])
#axis = fig.add_subplot(2,2,1)


p = axis.axvspan(460, 490, facecolor='#b6fa77', alpha=0.25)
p = axis.axvspan(710, 740, facecolor='#28cfe9', alpha=0.35)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0,8)
axis.set_yticks((2,4,6))
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(0,300)
axis2.set_yticks((50,150,250))
axis.set_xlim(250,800)
axis.grid(False)    



#arrow = dict(facecolor='black', shrink=0.085,width=1)
arrow = dict(facecolor='black',arrowstyle='->')
axis.annotate('CO', xy=(375, 2.4),  xycoords='data', xytext=(350, 1.1), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=8,)
axis.annotate('CO$_2$', xy=(420, 3.7),  xycoords='data', xytext=(460, 5.4), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=8,)
axis.annotate('Temp.', xy=(440, 6.6),  xycoords='data', xytext=(380, 7.2), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=8,)

axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis2.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)

axis.set_ylabel('SEM Current / nA', fontsize=8)
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=8)
axis.set_xlabel('Time / minutes', fontsize=8)



axis = plt.subplot(gs[1,0])
p = axis.axvspan(460, 490, facecolor='#b6fa77', alpha=0.25)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0,6)
axis.set_yticks((1,3,5))
axis.text(463,1.2,"CO",fontsize=8,)
axis.text(465,2.3,"CO$_2$",fontsize=8,)
axis.text(470,4.9,"T",fontsize=8,)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(0,300)
#axis2.set_yticks((170,180,190,200))
axis.set_xlim(460,490)
axis.set_ylabel('SEM Current / nA', fontsize=8)
axis2.set_ylabel('', fontsize=8)
axis.set_xticks((465,475,485))
axis2.set_yticks(())
axis.set_xlabel('Time / minutes', fontsize=8)
axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis2.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)

axis.grid(False)

axis = plt.subplot(gs[1,1])
#axis = fig.add_subplot(2,2,1)
p = axis.axvspan(710, 740, facecolor='#28cfe9', alpha=0.35)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0,6)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(0,300)
axis2.set_yticks((50,150,250))
axis.set_xticks((715,725,735))
axis.text(715,0.8,"CO",fontsize=8,)
axis.text(722,3.4,"CO$_2$",fontsize=8,)
axis.text(718,4.3,"T",fontsize=8,)
axis.set_xlim(710,740)
axis.set_yticks(())
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=8)
axis.set_xlabel('Time / minutes', fontsize=8)
axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis2.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)



axis.grid(False)

#plt.tight_layout()
plt.show()
plt.savefig('../initial_treatment.png',dpi=300)
