from tests.waypoints_data import waypoints
from collections import defaultdict

manyparams = []
outputs = []

# closest_waypoints, heading, steering_angle, all_wheels_on_track, speed
list_test = [
    [[22,23], 130, 20, False, 1.0],
    [[22,23], 130, 20, True, 1.0],
    [[22,23], 130, 20, True, 1.51],
    [[22,23], 130, 20, True, 3.01],
    [[22,23], 140, 20, True, 3.01],
    [[52,53], -90, 20, True, 3.01],
    [[52,53], -90, -10, True, 3.01]
]

list_outputs = [
    0.001,
    3,
    5,
    5,
    10,
    10,
    10
]

for ind, (i, j) in enumerate(zip(list_test, list_outputs)):
    params = {}
    params['waypoints'] = waypoints
    params['closest_waypoints'] = i[0] # closest_waypoints
    params['heading'] = i[1] # heading
    params['steering_angle'] = i[2] # steering_angle
    params['all_wheels_on_track'] = i[3] # all_wheels_on_track
    params['speed'] = i[4] # speed
    print("params ", params)
    manyparams.append(params)
    outputs.append(j)
