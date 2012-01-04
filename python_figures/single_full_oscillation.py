import matplotlib
#matplotlib.use('svg')
#matplotlib.use('Agg')
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

axis = fig.add_subplot(1,1,1)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'b-')
axis.set_ylim(0.1,1.2)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'k-')
axis2.set_ylim(160,205)
axis.set_xlim(1001,1133)
axis.grid(True)    

axis.tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)

axis.set_ylabel('SEM Current / nA', fontsize=20)
axis2.set_ylabel('Temperature', fontsize=20)
axis.set_xlabel('Time/minutes', fontsize=20)

#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')