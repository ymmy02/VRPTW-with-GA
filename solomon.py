import sys,os
import numpy as np

from node import Node, NodeList

def _trim(list_):
    return [elem.strip() for elem in list_ if len(elem) != 0]

def _create_node(elements, type_):
    id_ = int(elements[0])
    x = float(elements[1])
    y = float(elements[2])
    demand = float(elements[3])
    ready_time = float(elements[4])
    due_date = float(elements[5])
    service_time = float(elements[6])
    position = np.array([x, y])

    node = Node(id_, type_, position, demand, ready_time, due_date, service_time)
    return node

def loaddata(vehicle_capacity_filename, node_filename):

    # Error Check
    if not os.path.exists(vehicle_capacity_filename):
        print("!!!!! " + vehicle_capacity_filename + " Does NOT Exist !!!!!")
        sys.exit()
    if not os.path.exists(node_filename):
        print("!!!!! " + node_filename + " Does NOT Exist !!!!!")
        sys.exit()

    vcap_file = open(vehicle_capacity_filename, 'r')
    node_file = open(node_filename, 'r')

    # Read Vehicle Capacity
    vehicle_capacity = int(vcap_file.read())
    # Read Header
    header = node_file.readline()
    # Read Node Info
    nodes = NodeList(vehicle_capacity)
    line = node_file.readline()
    elements = _trim(line.split(" "))
    node = _create_node(elements, 0)        # Depot
    nodes.append(node)
    line = node_file.readline()
    while line:
        elements = _trim(line.split(" "))
        node = _create_node(elements, 1)        # Customer
        nodes.append(node)
        line = node_file.readline()

    return nodes
