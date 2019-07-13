def reward_function(params):

    #Implementing Pure Pursuit logic

    import math

    # Read input parameters
    steering = params['steering_angle']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    x = params['x']
    y = params['y']
    
    # Let's start rewarding our solution!
    reward = 1
    
    # Give a high reward if no wheels go off the track. IF it's not on track, dont even continue.
    if all_wheels_on_track:
        reward += 1
    else:
        reward = 1e-3
        return float(reward)

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
        reward += 1
    else:                        #vehicle is pointing to the wrong direction. 
        reward += (1 - (location_difference / (distance * 2)))

    return float(reward)    



