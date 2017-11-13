from enum import Enum

class Node(object):

    def __init__(self, id_, type_, position, demand, \
          ready_time, due_date, service_time):
        self._id = id_
        self._type = type_
        self._position = position
        self._demand = demand
        self._ready_time = ready_time
        self._due_date = due_date
        self._service_time = service_time

    # Getter
    def get_id(self):
        return self._id

    def get_type(self):
        return self._type

    def get_pos(self):
        return self._position

    def get_dem(self):
        return self._demand

    def get_readytime(self):
        return self._ready_time

    def get_duedate(self):
        return self._due_date

    def get_servicetime(self):
        return self._service_time

    def print_info(self):
        print("id ",self._id,"type ",self._type, "pos ",self._position, \
                "dem ",self._demand,"ready ",self._ready_time, \
                "due ",self._due_date,"service ",self._service_time)

    def is_available(self, t):
        if t < self._ready_time:
            return TimeWindow.early
        if t > self._due_date:
            return TimeWindow.late
        return TimeWindow.within


class TimeWindow(Enum):
    within = 0
    early = 1
    late = 2


class NodeList(list):
  
    def __init__(self, capacity):
        list.__init__(self)
        self._capacity = capacity
        self._depot = None
        self._is_first_get_depot = True

    def get_depot(self):
        if self._is_first_get_depot:
            for node in self:
                if node.get_type() == 0:
                    self._depot = node
                    self._is_first_get_depot = False
                    return self._depot
        return self._depot

    def get_node_from_id(self, id_):
        for node in self:
            if node.get_id() == id_:
                return node

    def get_customers(self):
        return [costomer for costomer in self if costomer.get_type()==1]

    def get_customers_id_list(self):
        return [costomer.get_id() for costomer in self if costomer.get_type()==1]

    def get_node_pos_from_id(self, id_):
        for node in self:
            if node.get_id() == id_:
                return node.get_pos()

    def is_feasible(self, route):
        # Capacity check
        amount = 0.0
        for node in self:
            if node.get_id() in route:
                amount += node.get_dem()
        if amount > self._capacity:
            print("capacity over")
            return False

        # Time Window check
        t = 0.0
        for id_ in route:
            node = self.get_node_from_id(id_)
            ready_time = node.get_readytime()
            due_date = node.get_duedate()
            service_time = node.get_servicetime()
            t = max(t, ready_time) + service_time
            if t > due_date:
                return False
        depot = self.get_depot()
        if t > depot.get_duedate():
            return False

        return True
