from dataclasses import dataclass
from datetime import datetime
from opcua import Client
import pandas as pd

url = "opc.tcp://192.168.11.104:4840"
client = Client(url)

try:
    client.connect()
    print("Client connected")
except:
    print('Connexion failed !')

nb_prod = 0
cycle_time,cycle_time_dur = datetime.now(),0.0

temp_values,cycle_time_values,energy_values = [],[],[]

def update_values() :

    global cycle_time,nb_prod,cycle_time_dur,database

    Temp = client.get_node("ns= 2; i= 3")
    Temperature = Temp.get_value()

    Step_3 = client.get_node("ns= 2; i= 6")
    step_3 = Step_3.get_value()

    Energy = client.get_node("ns= 2; i= 7")
    energy_cons = Energy.get_value()

    if step_3 == True :

        nb_prod += 1
        cycle_time_dur = (datetime.now()-cycle_time).total_seconds()
        cycle_time = datetime.now()

    print(Temperature, cycle_time_dur, energy_cons)

    return Temperature,cycle_time_dur*100,energy_cons/100

def update_plots(): #function to call repeatedly to update the Graph object in the dashboard

    global temp_values,cycle_time_values,energy_value

    temp,cy_time,energy = update_values()

    temp_values.append(temp)
    cycle_time_values.append(cy_time)
    energy_values.append(energy)

    abscisses = list(range(len(temp_values)))

    fig = {
        'data': [
            {'x': abscisses, 'y': temp_values,'name' : 'Temperature'},
            {'x': abscisses, 'y': cycle_time_values,'name' : 'Cycle time'},
            {'x': abscisses, 'y': energy_values,'name' : 'Energy consumed'},
        ],
        'layout': {
            'title': 'Molding machine state variables visualization'
        }
    }

    return fig
    
