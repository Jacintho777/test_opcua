from datetime import datetime
from opcua import Client, ClientDiscovery
import database
# import pandas as pd

# url = "opc.tcp://192.168.1.78:4848"
# client = Client(url)

#################### Discovery Client test ##########################

"""
Here the idea is to automatically find the OPCUA server
endpoint with no need to hard-code it !

"""

# Create a Discovery Client
discovery_client = ClientDiscovery()

# Discover available servers on the network
available_servers = discovery_client.find_servers()

# Choose a server from the list (you may implement a selection mechanism)
selected_server = available_servers[0]

print(selected_server.endpoint)

# Connect to the selected server
client = Client(selected_server.endpoint)

###################################################################

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
    
