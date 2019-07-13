def reward_function(params):

    #Implementing Pure Pursuit logic

    import math

    # Read input parameters
    steering = params['steering_angle']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    x = params['x']
    y = params['y']
    
    # Let's start rewarding our solution!
    reward = 1
        
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track


    #Closest points X and Y Coordinates
    next_point = waypoints[closest_waypoints[1]]
    C_X = next_point[0]
    C_Y = next_point[1]

    #Calculate the distance from the car to the next point
    distance = math.hypot(x - C_X, y - C_Y)

    #Calculate the predicted vehicle location considering the current steering angle.
    P_X = x + (distance * math.cos(steering))
    P_Y = y + (distance * math.sin(steering))

    location_difference = math.hypot(C_X - P_X, C_Y - P_Y)

    if location_difference == 0: #vehicle is pointing to the right direction. 
        reward += 2
    else:                        #vehicle is pointing to the wrong direction. 
        reward += (1 - (location_difference / (distance)))

    return float(reward)    



