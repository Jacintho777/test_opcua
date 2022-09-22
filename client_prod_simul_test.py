from datetime import datetime
from opcua import Client
import database
# import pandas as pd

url = "opc.tcp://192.168.11.110:4840"
client = Client(url)

try:
    client.connect()
    print("Client connected")
except:
    print('Connexion failed !')

cycle_time,cycle_time_dur = datetime.now(),0.0

temp_values,cycle_time_values,energy_values = [],[],[]

def update_values() :

    global cycle_time,nb_prod,cycle_time_dur,database

    """Rather than getting the input values from the OPC-UA server,
    let's get them from the database"""

    Temp = client.get_node("ns= 2; i= 3")
    Temperature = Temp.get_value()

    Cycle_time = client.get_node("ns= 2; i= 8")
    cycle_time_dur = Cycle_time.get_value()

    Energy = client.get_node("ns= 2; i= 7")
    energy_cons = Energy.get_value()

    print(Temperature, cycle_time_dur, energy_cons)

    # Temperature,cycle_time_dur,energy_cons = database.load_data()

    return Temperature,cycle_time_dur,energy_cons

def update_plots(): #function to call repeatedly to update the Graph object in the dashboard

    global temp_values,cycle_time_values,energy_values

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
    
