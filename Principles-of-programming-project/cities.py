import math
import random
import os
import matplotlib.pyplot as plt


def read_cities(file_name):
    """
    Read in the cities from the given `file_name`, and return 
    them as a list of four-tuples: 
    [(state, city, latitude, longitude), ...]"""
    
    with open(file_name, 'r') as in_file:
        file_lines = in_file.read().split("\n")
        tuples_list = []
        for file_line in file_lines:
            line = file_line.split("\t")
            line[2] = float(line[2])
            line[3] = float(line[3])
            tuple_line = tuple(line)
            tuples_list.append(tuple_line)
    return tuples_list


def print_cities(road_map):
    """
    Prints a list of cities, along with their locations. 
    Print only one or two digits after the decimal point.
    """
    
    road_map_lists = []
    
    for row in road_map:
        list_row = list(row)
        list_row[2] = str(list_row[2])
        list_row[3] = str(list_row[3])
        road_map_lists.append(list_row)
    
    for i in range(len(road_map_lists)):
        road_map_lists[i] = ", ".join(road_map_lists[i])
    
    for row in road_map_lists:
        print(row)


def compute_total_distance(road_map):
    """
    Returns, as a floating point number, the sum of the distances of all 
    the connections in the `road_map`. Remember that it's a cycle, so that 
    (for example) in the initial `road_map`, Wyoming connects to Alabama...
    """
    total_distance = 0
    
    for i in range(len(road_map)-1):
        delta_lat = road_map[i+1][2] - road_map[i][2]
        delta_long = road_map[i+1][3] - road_map[i][3]
        distance = math.sqrt(delta_lat**2 + delta_long**2)
        total_distance += distance
    
    delta_lat = road_map[0][2] - road_map[-1][2]
    delta_long = road_map[0][3] - road_map[-1][3]
    distance = math.sqrt(delta_lat**2 + delta_long**2)
    total_distance += distance
    
    return round(total_distance, 4)


def swap_cities(road_map, index1, index2):
    """
    Take the city at location `index1` in the `road_map`, and the 
    city at location `index2`, swap their positions in the `road_map`, 
    compute the new total distance, and return the tuple 

        (new_road_map, new_total_distance)

    Allow for the possibility that `index1=index2`,
    and handle this case correctly.
    """
    if index1 == index2:
        return(road_map[:], compute_total_distance(road_map))
    else:
        new_road_map = road_map[:]
        new_road_map[index1] = road_map[index2]
        new_road_map[index2] = road_map[index1]
        new_total_distance = compute_total_distance(new_road_map)
        return(new_road_map, new_total_distance)


def shift_cities(road_map):
    """
    For every index i in the `road_map`, the city at the position i moves
    to the position i+1. The city at the last position moves to the position
    0. Return the new road map. 
    """
    new_road_map = [0 for i in range(len(road_map))]
    new_road_map[0] = road_map[-1]
    for i in range(len(road_map)-1):
        new_road_map[i+1] = road_map[i]
    
    return new_road_map


def find_best_cycle(road_map_0):
    """
    Using a combination of `swap_cities` and `shift_cities`, 
    try `10000` swaps/shifts, and each time keep the best cycle found so far. 
    After `10000` swaps/shifts, return the best cycle found so far.
    Use randomly generated indices for swapping.
    """
    attempts = 10000
    random.seed(1)
    upper_limit = len(road_map_0) - 1
    tracking_list = []
    tracking_list.append(road_map_0)
    index1_0 = random.randint(0, upper_limit)
    index2_0 = random.randint(0, upper_limit)
    tracking_list.append(shift_cities(swap_cities(road_map_0, index1_0, index2_0)[0]))
    current_road_map = tracking_list[-1]
    previous_cost = compute_total_distance(road_map_0)
    current_cost = compute_total_distance(current_road_map)
    
    for i in range(attempts):
        previous_cost = compute_total_distance(tracking_list[-2])
        current_cost = compute_total_distance(tracking_list[-1])
        index1 = random.randint(0, upper_limit)
        index2 = random.randint(0, upper_limit)
        
        if current_cost >= previous_cost:
            current_road_map = shift_cities(swap_cities(tracking_list[-2], index1, index2)[0])
            tracking_list[-1] = current_road_map
        else:
            current_road_map = shift_cities(swap_cities(tracking_list[-1], index1, index2)[0])
            tracking_list.append(current_road_map)
    
    if compute_total_distance(tracking_list[-1]) >= compute_total_distance(tracking_list[-2]):
        tracking_list.pop()
    
    best_cycle = tracking_list[-1]
    
    return best_cycle


def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and 
    their connections, along with the cost for each connection 
    and the total cost.
    """
    
    for i in range(len(road_map)):
        if i == 0:
            adjective = str(i+1) + "-st"
        elif i == 1:
            adjective = str(i+1) + "-nd"
        elif i == 2:
            adjective = str(i+1) + "-rd"
        else:
            adjective = str(i+1) + "-th"
        if i < (len(road_map)-1):
            delta_lat = abs(road_map[i+1][2]-road_map[i][2])
            delta_long = abs(road_map[i+1][3]-road_map[i][3])
            line_1 = "The " + adjective + " city is " + road_map[i][1] + ", " + road_map[i][0] + ".\n"
            line_2 = "The next city is " + road_map[i+1][1] + ", " + road_map[i+1][0] + ".\n"
        else:
            delta_lat = abs(road_map[0][2]-road_map[i][2])
            delta_long = abs(road_map[0][3]-road_map[i][3])
            line_1 = "The " + adjective + " city is " + road_map[i][1] + ", " + road_map[i][0] + ".\n"
            line_2 = "The next (and last) city is " + road_map[0][1] + ", " + road_map[0][0] + ".\n"
        connection_cost = round(math.sqrt(delta_lat**2 + delta_long**2), 4)
        line_3 = "The cost of this connection is " + str(connection_cost) + ".\n"
        string = line_1 + line_2 + line_3
        print(string)
    total_cost = compute_total_distance(road_map)
    print('The total cost for this cycle is: ' + str(total_cost))


def visualise(road_map):
    x = [city[3] for city in road_map]
    y = [city[2] for city in road_map]
    
    plt.scatter(x, y, s=4)
    plt.grid(True)
    plt.title('Road Map visualisation')
    plt.xlabel('Longitude')
    plt.ylabel("Latitude")
    
    for city in road_map:
        name = '(' + str(road_map.index(city)+1) + ')'
        plt.annotate(name, [city[3], city[2]], fontsize=7)
    
    plt.show()


def main():
    """
    Reads in, and prints out, the city data, then creates the "best"
    cycle and prints it out.
    """
    
    initial_road_map_path = input('Please paste here the path to the initial road map: ')

    while os.path.isfile(initial_road_map_path)==False:
        initial_road_map_path = input('File or directory not found. Please try again: ')
        if os.path.isfile(initial_road_map_path)==True:
            break
    
    print('')
    initial_road_map = read_cities(initial_road_map_path)
    print('The initial road map is the following: \n')
    print_map(initial_road_map)
    print("****************************************\n")
    print('Calculating best cycle, please wait....\n')
    best_cycle = find_best_cycle(initial_road_map)
    print('The best cycle found after 10,000 iterations is the following: \n')
    print_map(best_cycle)
    print("****************************************\n")
    
    visualise(best_cycle)


if __name__ == "__main__": #keep this in
    main()
