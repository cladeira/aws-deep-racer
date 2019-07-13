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
    x = params['x']
    y = params['y']
    progress = params['progress']
    
    # Let's start rewarding our solution!
    reward = 0

    # Give a high reward if no wheels go off the track. IF it's not on track, don't even continue.
    if all_wheels_on_track:
        reward += 5
    else:
        reward = -1   
        return float(reward)
        
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.50 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 10
    elif distance_from_center <= marker_2:
        reward += 5
    elif distance_from_center <= marker_3:
        reward += 1
    else:
        reward = -1   # likely crashed/ close to off track

    #Closest points X and Y Coordinates
    i = closest_waypoints[1]
    n = waypoints[i]
    C1_X = n[0]
    C1_Y = n[1]

    i = (i+1)%169
    n = waypoints[i]
    C2_X = n[0]
    C2_Y = n[1]

    i = (i+1)%169
    n = waypoints[i]
    C3_X = n[0]
    C3_Y = n[1]

    i = (i+1)%169
    n = waypoints[i]
    C4_X = n[0]
    C4_Y = n[1]

    i = (i+1)%169
    n = waypoints[i]
    C5_X = n[0]
    C5_Y = n[1]

    C_X = (C1_X + C2_X + C3_X + C4_X + C5_X) / 5
    C_Y = (C1_Y + C2_Y + C3_Y + C4_Y + C5_Y) / 5

    #Calculate the distance from the car to the next point
    distance = math.hypot(x - C_X, y - C_Y)

    #Calculate the predicted vehicle location considering the current yaw. Yaw is in angles, convert to radians first.
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

    reward = reward * (1 + (progress/100))
    return float(reward)
