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
cursor.execute("SELECT x/3600000,y FROM xy_values_microreactor where measurement = 6694")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/3600000,y FROM xy_values_microreactor where measurement = 6696")
data['M44'] =  np.array(cursor.fetchall())

#CO Flow
cursor.execute("SELECT x/3600000,y FROM xy_values_microreactor where measurement = 6702")
data['CO_FLOW'] = np.array(cursor.fetchall())


i = 0
old_flow = 0
flow_sections = [] #Holds the times of the concentrations steps
for row in data['CO_FLOW']:
    i = i+1
    if (row[1] > (old_flow + 0.04)):
        flow_sections.append(row[0])
        old_flow = row[1]
        
    if (i%10==0):
        old_flow = row[1]

steps = len(flow_sections)


fig = plt.figure()
axis_array = []
axis2_array = []

for i in range(0,steps-1):
    axis_array.append(fig.add_subplot((steps-1)/2,2,i+1))
    axis_array[i].plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
    axis_array[i].plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'b-')
    axis_array[i].set_ylim(0,0.1*(i+1)*1.85)
    axis2_array.append(axis_array[i].twinx())
    axis2_array[i].plot(data['CO_FLOW'][:,0], data['CO_FLOW'][:,1]/(4+data['CO_FLOW'][:,1]), 'k-')
    axis2_array[i].set_ylim(0.01,0.25)
    
    axis_array[i].set_xlim(flow_sections[i],flow_sections[i+1])
    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
    axis2_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='y',pad=5)
    
axis_array[4].set_ylabel('SEM Current / nA', fontsize=20)
axis2_array[4].set_ylabel('CO/O2 Ratio', fontsize=20)
axis_array[4].set_xlabel('Time/h', fontsize=20)


#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')