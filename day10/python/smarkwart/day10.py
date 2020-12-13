from itertools import combinations
import sys
import collections

class Adapter:

    def __init__(self):
        self.children = []
        self.number_of_children = 0
        self.number_of_leaves = 0

    def add_child(self, child):
        self.children.append(child)
        self.number_of_children = len(self.children)

    def get_number_of_children(self):
        return self.number_of_children

    def get_number_of_leaves(self):
        if self.number_of_leaves > 0:
            return self.number_of_leaves
        if self.number_of_children == 0:
            return 1
        number_of_leaves = 0
        for child in self.children:
            number_of_leaves += child.get_number_of_leaves()
        return number_of_leaves

    def freeze_node(self):
        self.number_of_leaves = self.get_number_of_leaves()

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        data_list = list(map(int, input_file.readlines()))
    return data_list

def plug_in_outlet(bunch_of_adapters):
    """
    adds joltage of outlet to list
    """
    bunch_of_adapters.append(0)

def plug_in_device(gains):
    """
    adds joltage of device to list
    """
    gains.append(3)

def plug_adapters_together(bunch_of_adapters):
    """
    Plugs adapters ordert together
    """
    bunch_of_adapters.sort()

def measure_individual_gains(bunch_of_adapters):
    """
    Calculates the gain (= difference between two adapters) between each adapter
    """
    gains = [(item - bunch_of_adapters[idx-1]) for idx, item in enumerate(bunch_of_adapters[1:], 1)]
    return gains

def calc_combinations(adapters):
    """
    Calculate number of possible combinations by:
    1) Walk through the reverse sorted (largest to smallest) list of adapters
    2) For each adapter identify the children (according to rule) and take them from the list of already evaluated adapter objects
    3) When all children for an adapter are identified calculate the number of leaves of the current sub-tree (freeze node)
    4) Add adapter to the list of evaluated adapter objects
    5) Repeat steps 2) to 4) for all adapters
    6) Get number of leaves for root node. 
    Since number of leaves of all children is permanently calculated and only once per adapter this has linear complexity
    """
    adapters.reverse()
    adapter_objects = []
    for idx, adapter in enumerate(adapters):
        adapter_object = Adapter()
        for pre_idx, previous in enumerate(adapters[max(0,idx-3):idx],max(0,idx-3)):
            if(previous - adapter) <= 3:
                adapter_object.add_child(adapter_objects[pre_idx])
        adapter_object.freeze_node()
        adapter_objects.append(adapter_object)

    total_number_of_leaves = adapter_objects[-1].get_number_of_leaves()
    return total_number_of_leaves

def measure_total_gain(bunch_of_adapters):
    plug_in_outlet(bunch_of_adapters)
    plug_adapters_together(bunch_of_adapters)
    gains = measure_individual_gains(bunch_of_adapters)
    plug_in_device(gains)
    count_gains = collections.Counter(gains)
    total_gain = count_gains.get(1) * count_gains.get(3)
    return total_gain

bunch_of_adapters = get_input_data_as_list(sys.argv[1])

print(f"The result for 1st star puzzle is: {measure_total_gain(bunch_of_adapters)}")
print(f"The result for 2nd star puzzle is: {calc_combinations(bunch_of_adapters)}")
