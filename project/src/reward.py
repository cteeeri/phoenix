from tests.waypoints_data import waypoints

import math
def rwd(params):    # params is a dictionary
    waypoints = params['waypoints'] # [ ...[2.5,3.5], [3.5,4.5], [5.6,6.7]...]
    closest_waypoints = params['closest_waypoints'] # e.g. [16,17]
    next_point = waypoints[closest_waypoints[1]]
    previous_point = waypoints[closest_waypoints[0]]
    heading = params['heading']
    steering_angle = params['steering_angle']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']

    # reward weight, 20 point based
    reward = 0.0
    DIRECTION_WEIGHT = 6
    DIRECTION_MAGNITUDE_WEIGHT = 4

    STEERING_CORRECTION_WEIGHT = 3

    # below exclusive
    SPEED_GREAT_WEIGHT = 4
    SPEED_LESS_IDEAL_WEIGHT = 2

    # threshold
    DIR_DIFF_THRESHOLD = 10
    SPEED_THRESHOLD_LESS_IDEAL = 1.5
    SPEED_THRESHOLD_GREAT = 2.5 
    
    
    def _track_heading_diff(previous_point, next_point, heading):
        next_point = waypoints[closest_waypoints[1]]
        previous_point = waypoints[closest_waypoints[0]]

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        track_direction = math.atan2(next_point[1] - previous_point[1], next_point[0] - previous_point[0]) 
        # Convert to degree
        track_direction = math.degrees(track_direction)

        # Calculate the difference between the track direction and the heading direction of the car
        # track_dir_rel_to_heading = (track_direction - heading)
        track_dir_rel_to_heading = abs(track_direction - heading)
        if track_dir_rel_to_heading > 180:
            track_dir_rel_to_heading = 360 - track_dir_rel_to_heading
        # if direction_diff > 0:
        #     return f'track turning left, now {direction_diff} degree steering_angle definition'
        # else:
        #     return f'track turning right, now {direction_diff} degree steering_angle definition'

        return (track_dir_rel_to_heading, track_direction) # return e.g. 20 (left), -15 (right)

    def steering_towards_track(track_direction, steering_angle):
        res = False
        if track_direction < 0:
            track_direction = abs(track_direction)
            steering_angle = -1 * steering_angle
        
        if track_direction < 90 and steering_angle < 0:
            res = True
        elif track_direction > 90 and steering_angle > 0:
            res = True
        else:
            res = False        
        # print(f'steering_towards_track {res}')
        return res

    track_heading_diff, track_direction = _track_heading_diff(previous_point, next_point, heading)

    if not all_wheels_on_track:
        reward = 0.001
        print(f' off track reward {reward}')
        return reward

    # positive reinforcement
    # reward track and steering 
    if (track_heading_diff <= DIR_DIFF_THRESHOLD):  # in same direction
        # collect reward weight
        reward = reward +  DIRECTION_WEIGHT
        print(f' gain same dir reward {DIRECTION_WEIGHT}')
    else: # tarck and heading has big gap
        if (steering_towards_track(track_direction, steering_angle)): # reward if steering back toward track direction
            print(f' gain steering correction reward {STEERING_CORRECTION_WEIGHT}')
            reward = reward + STEERING_CORRECTION_WEIGHT
    
    # reward speed nonetheless?
    if speed >= SPEED_THRESHOLD_GREAT and 2 * track_heading_diff <= DIR_DIFF_THRESHOLD:
        reward = reward + SPEED_GREAT_WEIGHT
        print(f' gain speed great reward {SPEED_GREAT_WEIGHT}')
    elif speed >= SPEED_THRESHOLD_LESS_IDEAL:
        reward = reward + SPEED_LESS_IDEAL_WEIGHT
        print(f' gain speed less ideal reward {SPEED_LESS_IDEAL_WEIGHT}')
    else:
        pass # no reward

    del params['waypoints']
    # print(f'{params}')
    # print(f'track_heading_diff {track_heading_diff} degree, track_direction {track_direction}')
    # print(f'reward: {reward}')
    return float(reward)

if __name__ == "__main__":

    input = {}
    input['waypoints'] = waypoints
    input['closest_waypoints'] = [22,23] # closest_waypoints
    input['heading'] = 130 # heading
    input['steering_angle'] = 20.0 # steering_angle
    input['all_wheels_on_track'] = True # all_wheels_on_track
    input['speed'] = 1.0 # speed
    print(rwd(input))
