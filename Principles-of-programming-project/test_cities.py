import pytest
import math
from cities import compute_total_distance
from cities import read_cities, print_cities, swap_cities, shift_cities, print_map
from unittest.mock import mock_open, patch, call


def test_cycle_path():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755)]
    delta_lat_1 = 39.161921 - 38.197274
    delta_long_1 = -75.526755 - (-84.86311)
    dist_1 = math.sqrt(delta_lat_1**2 + delta_long_1**2)
    delta_lat_2 = 38.197274 - 39.161921
    delta_long_2 = -84.86311 - (-75.526755)
    dist_2 = math.sqrt(delta_lat_2**2 + delta_long_2**2)
    tot_dist = dist_1 + dist_2
    assert compute_total_distance(road_map) == pytest.approx(tot_dist, rel=0.0001)

def test_compute_total_distance_three_cities():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755),
                ("Alabama", "Montgomery", 32.361538, -86.279118)]
    delta_lat_1 = 39.161921 - 38.197274
    delta_long_1 = -75.526755 - (-84.86311)
    dist_1 = math.sqrt(delta_lat_1**2 + delta_long_1**2)
    delta_lat_2 = 32.361538 - 39.161921
    delta_long_2 = -86.279118 -(-75.526755)
    dist_2 = math.sqrt(delta_lat_2**2 + delta_long_2**2)
    delta_lat_3 = 38.197274 - 32.361538
    delta_long_3 = -84.86311 - (-86.279118)
    dist_3 = math.sqrt(delta_lat_3**2 + delta_long_3**2)
    total_dist = dist_1 + dist_2 + dist_3
    assert compute_total_distance(road_map) == pytest.approx(total_dist, rel=0.0001)

def test_can_return_list_of_tuples_floats():
    mock_file_path = 'file/path/mock'
    line_1 = "Alabama	Montgomery	32.361538	-86.279118\n"
    line_2 = "Alaska	Juneau	58.301935	-134.41974\n"
    line_3 = "Arizona	Phoenix	33.448457	-112.073844"
    mock_file_content = line_1 + line_2 + line_3
    m = mock_open(read_data=mock_file_content)

    with patch('cities.open', new=m):
        mock_list = mock_file_content.split("\n")
        mock_tuples_list = []
        for row in mock_list:
            mock_row = row.split("\t")
            mock_row[2] = float(mock_row[2])
            mock_row[3] = float(mock_row[3])
            mock_tuple_row = tuple(mock_row)
            mock_tuples_list.append(mock_tuple_row)
        assert read_cities(mock_file_path) == mock_tuples_list
        for row in read_cities(mock_file_path):
            assert isinstance(row[2], float)
            assert isinstance(row[3], float)

def test_print_cities_prints_right_output():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755)]
    road_map_lists = []
    
    for row in road_map:
        list_row = list(row)
        list_row[2] = str(list_row[2])
        list_row[3] = str(list_row[3])
        road_map_lists.append(list_row)
    
    for i in range(len(road_map_lists)):
        road_map_lists[i] = ", ".join(road_map_lists[i])
    
    with patch('builtins.print') as mock_print:
        for i in range(len(road_map)):
            mock_print.return_value = road_map_lists[i]
            print_cities([road_map[i]])
            assert mock_print.call_args == call(road_map_lists[i])

def test_can_call_swap_cities_with_args():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755)]
    index1 = 0
    index2 = 1
    
    result = swap_cities(road_map, index1, index2)

def test_swap_cities_can_return_list_and_tot_dist():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755)]
    index1 = 0
    index2 = 1
    
    result = swap_cities(road_map, index1, index2)
    
    assert isinstance(result[0], list)
    assert isinstance(result[1], float)

def test_swap_cities_can_return_right_results():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755)]
    index1 = 0
    index2 = 0
    expected_new_road_map = [("Delaware", "Dover", 39.161921, -75.526755),
                             ("Kentucky", "Frankfort", 38.197274, -84.86311)]
    result = swap_cities(road_map, index1, index2)
    
    delta_lat = abs((39.161921 - 38.197274)) + abs((38.197274 - 39.161921))
    delta_long = abs((-75.526755-(-84.86311))) + abs((-84.86311 - (-75.526755)))
    dist = math.sqrt(delta_lat**2 + delta_long**2)
    
    if index1 == index2:
        assert result[0] == road_map
        assert result[1] == compute_total_distance(road_map)
    else:
        assert result[0] == expected_new_road_map
        assert result[1] == pytest.approx(dist, rel=0.0001)
    
    assert isinstance(result, tuple)


def test_can_call_shift_cities():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755)]
    result = shift_cities(road_map)

def test_shift_cities_returns_correct_output():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755),
                ("Alabama", "Montgomery", 32.361538, -86.279118)]
    expected_new_road_map = [("Alabama", "Montgomery", 32.361538, -86.279118),
                             ("Kentucky", "Frankfort", 38.197274, -84.86311),
                             ("Delaware", "Dover", 39.161921, -75.526755)]
    assert shift_cities(road_map) == expected_new_road_map


def test_can_call_print_map():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755),
                ("Alabama", "Montgomery", 32.361538, -86.279118)]
    print_map(road_map)

def test_print_map_prints_right_output():
    road_map = [("Kentucky", "Frankfort", 38.197274, -84.86311),
                ("Delaware", "Dover", 39.161921, -75.526755),
                ("Alabama", "Montgomery", 32.361538, -86.279118)]
    
    with patch('builtins.print') as mock_print:
        string1 = "The 1-st city is Frankfort, Kentucky.\n" +\
                  "The next city is Dover, Delaware.\n" +\
                  "The cost of this connection is 9.3861.\n"
        string2 = "The 2-nd city is Dover, Delaware.\n" +\
                  "The next city is Montgomery, Alabama.\n" +\
                  "The cost of this connection is 12.7224.\n"
        string3 = "The 3-rd city is Montgomery, Alabama.\n" +\
                  "The next (and last) city is Frankfort, Kentucky.\n" +\
                  "The cost of this connection is 6.0051.\n"
        string4 = "The total cost for this cycle is: 28.1135"
        print_map(road_map)
        calls = [call(string1), call(string2), call(string3), call(string4)]
        mock_print.assert_has_calls(calls, any_order=False)



