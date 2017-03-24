import numpy as np
import sklearn.metrics as metrics
import matplotlib
import matplotlib.pyplot as plt
import csv
import dateutil.parser as dparser

"""
Calclate the time the battery has been charged during a charging phase.
Time in second
"""
def calculate_charge_time(vehicle):
    in_charge = False
    start_time = 0
    charge_time = 0
    for node in vehicle.timestamp_nodes:
        charging_state = node.charging_state
        if charging_state == 'Complete':
            in_charge = False
            charge_time = 0
            continue
        elif charging_state == 'Disconnected':
            if in_charge == True:
                in_charge = False
            else:
                continue
        elif charging_state == 'Charging' or charging_state == 'Starting':
            if in_charge == False:
                in_charge = True
                start_time = node.date_time
                charge_time = 0
            else:
                present_time = node.date_time
                difference_time = present_time - start_time
                difference = divmod(difference_time.days * 86400 + difference_time.seconds, 60)
                charge_time = difference[0] * 60 + difference[1]
        node.update_charge_time(charge_time)

"""
Disgard any node which is not charging
"""
def throw_out_none_charging_nodes_and_outliers(vehicle):
    index_to_delete = []
    for i in range(len(vehicle.timestamp_nodes)):
        node = vehicle.timestamp_nodes[i]
        if node.charging_state == 'Disconnected' or node.charging_state == 'Complete':
            index_to_delete.append(i)
    count = 0
    for index in index_to_delete:
        del vehicle.timestamp_nodes[index - count]
        count += 1

"""
Training function
"""
def train(vehicle):
    X = np.empty((0,8), int)
    y_list = []
    for node in vehicle.timestamp_nodes:
        X = np.append(X, np.array([[float(node.charge_time), float(node.latitude), float(node.longitude), 
            float(node.inside_temp), float(node.outside_temp), float(node.battery_current), float(node.odometer), 
            float(node.usable_battery_level)]]), axis=0)
        y_list.append(node.charge_rate)
    y = np.array(y_list)
    beta = train_sgd(X, y)
    return beta

def logistic(x):
    return 1 / (1 + np.exp(-(x)))

"""
Build a model from X_train -> Y_train using batch gradient descent
"""
def train_gd(X_train, Y_train, num_iter = 10, alpha = 0.2, reg = 0.05):
    ''' Build a model from X_train -> Y_train using batch gradient descent '''
    beta = np.random.random((X_train.shape[1], 1))
    for i in range(num_iter):
        sigmoid = logistic(X_train @ beta)
        beta -= (1/X_train.shape[0])*alpha*(2*reg*beta - (X_train.T @ (Y_train - sigmoid)))  
    return beta

"""
Build a model from X_train -> Y_train using stochastic gradient descent
"""
def train_sgd(X_train, Y_train, num_iter = 1000, alpha = 0.2, reg = 0.05):
    beta = np.random.random((X_train.shape[1], 1))
    for i in range(num_iter):
        random = np.random.randint(X_train.shape[0])
        Xi = np.matrix(X_train[random])
        yi = np.matrix(Y_train[random])
        sigmoid = logistic(Xi @ beta)
        beta -= alpha / (1 + alpha * reg * i) * (2 * reg * beta - np.dot(Xi.T, (yi - sigmoid)))
    return beta

"""
Load the dataset where we will do some basic operation.
"""
def load_dataset():
    with open('battery_data_v3.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        vehicle = Vehicle('1129095010')
        # count = 0
        for row in reader:
            # if count == 1000:
            #     break
            # count += 1
            if row['vehicle'] == '1129095010':
                if row['vehicle'] != 'None' and row['timestamp'] != 'None' and row['latitude'] != 'None' and row['longitude'] != 'None' \
                and row['inside_temp'] != 'None' and row['outside_temp'] != 'None' and row['battery_current'] != 'None' and row['odometer'] != 'None' \
                and row['usable_battery_level'] != 'None' and row['charge_rate'] != 'None' and row['charging_state'] != 'None':
                    date_time = dparser.parse(row['timestamp'],fuzzy=True)
                    next = Timestamp_node(row['vehicle'], row['timestamp'], date_time, row['latitude'], row['longitude'], row['inside_temp'], 
                        row['outside_temp'], row['battery_current'], row['odometer'], row['usable_battery_level'], 
                        row['charge_rate'], row['charging_state'])
                    vehicle.add_timestamp_node(next)
    return vehicle

"""
Vehicle class contains all data for a specfic vehicle.
"""
class Vehicle(object):
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.timestamp_nodes = []

    def add_timestamp_node(self, node):
        self.timestamp_nodes.append(node)

"""
Timestamp_node class represents data for a timestamp in a charging phase.
variables: 
"""
class Timestamp_node(object):
    def __init__(self, vehicle, timestamp, date_time, latitude, longitude, inside_temp, outside_temp, battery_current, 
        odometer, usable_battery_level, charge_rate, charging_state):   
        self.vehicle = vehicle
        self.timestamp = timestamp
        self.date_time = date_time
        self.latitude = latitude
        self.longitude = longitude
        self.inside_temp = inside_temp
        self.outside_temp = outside_temp
        self.battery_current = battery_current
        self.odometer = odometer
        self.usable_battery_level = usable_battery_level
        self.charge_rate = charge_rate
        self.charging_state = charging_state
        self.charge_time = 0
      
    def __str__(self):
        return 'vehicle:' + self.vehicle + '; ' + 'latitude: ' + self.latitude + '; ' \
        + 'inside temperature:' + self.inside_temp + '; ' + 'outside_temp:' + self.outside_temp

    def __eq__(self, other):
        print(self.timestamp)
        print(other.timestamp)
        print(str(self.timestamp) == str(other.timestamp))
        return self.timestamp == other.timestamp

    def update_charge_time(self, charge_time):
        self.charge_time = charge_time

"""
Charging_pahse class represents one complete Charging_phase.
"""
# class Charging_phase(object):
#     def __init__(self):

if __name__ == "__main__":
    vehicle = load_dataset()
    calculate_charge_time(vehicle)
    throw_out_none_charging_nodes_and_outliers(vehicle)
    beta = train(vehicle)
    print(beta)


