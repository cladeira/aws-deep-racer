def reward_function(params):

    #Implementing Pure Pursuit logic
    import math

    # Read input parameters
    steering = params['steering_angle']
    yaw = params['heading']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    progress = params['progress']
    x = params['x']
    y = params['y']
    
    # Let's start rewarding our solution!
    reward = 0

    # Give a high reward if no wheels go off the track. IF it's not on track, dont even continue.
    if all_wheels_on_track:
        reward += 5
    else:
        reward = -1   
        return float(reward)
        
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 10
    elif distance_from_center <= marker_2:
        reward += 5
    elif distance_from_center <= marker_3:
        reward += 1
    else:
        reward = -1  # likely crashed/ close to off track

    #Closest points X and Y Coordinates
    next_point = waypoints[closest_waypoints[1]]
    C_X = next_point[0]
    C_Y = next_point[1]

    #Calculate the distance from the car to the next point
    distance = math.hypot(x - C_X, y - C_Y)

    #Calculate the predicted vehicle location considering the current yaw. Yaw and Steering are in angles, convert to radians first.
    P_X = x + (distance * math.cos(math.radians(yaw)))
    P_Y = y + (distance * math.sin(math.radians(yaw)))

    predicted_distance = math.hypot(C_X - P_X, C_Y - P_Y)

    if predicted_distance <= marker_1: #vehicle is pointing to the right direction. 
        reward += 10
    elif predicted_distance <= marker_2:
    	reward += 5
    elif predicted_distance <= marker_3:
    	reward += 1
    else:                      #vehicle is pointing to the wrong direction. 
        reward = -1 * (predicted_distance / (distance * 2))
    
    #Remember, logs will be written on: /aws/robomaker/SimulationJobs
    print('Reward:', reward, ',Progress:', progress, ',X:', x, ',Y:', y,',P_X:', P_X, ',P_Y:', P_Y, ',C_X:', C_X, ',C_Y:', C_Y, ',Distance:', distance,',LocationDiff:', predicted_distance, ',Yaw:', yaw,',Steering:', steering, ',Speed:', speed, ',On Track:', all_wheels_on_track,',Center:', distance_from_center,',waypoints:', waypoints,',closest_waypoints:', closest_waypoints)

    #Bump the reward based on the progress. 
    reward = reward * (1 + (progress/100))

    return float(reward)

