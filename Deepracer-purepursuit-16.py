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
        reward += 1
    else:
        reward = -1 * (speed / 2)  #penalize speed (divided by two is just to avoid huge penalty) 
        return float(reward)
        
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 10
    else:
        reward = -1 * (speed / 2)  # likely crashed/ close to off track

    #Closest points X and Y Coordinates. We will get an average of the next 5 points in front of us. 
    next_point = closest_waypoints[1]
    len_maxpoints = len(waypoints)
    iteractions = 3 #arbitrary number. 

    sum_X = 0
    sum_Y = 0
    for i in range(next_point, next_point+iteractions,1):
        w = waypoints[i % len_maxpoints] #use mod to avoid errors. Think about completing one full lap. 
        sum_X += w[0] #Getting X coordinate. 
        sum_Y += w[1] #Getting Y coordinate. 

    C_X = sum_X / iteractions 
    C_Y = sum_Y / iteractions


    #Calculate the distance from the car to the next point
    distance = math.hypot(x - C_X, y - C_Y)

    #Calculate the predicted vehicle location considering the current yaw. Yaw and Steering are in angles, convert to radians first.
    P_X = x + (distance * math.cos(math.radians(yaw + steering)))
    P_Y = y + (distance * math.sin(math.radians(yaw + steering)))

    predicted_distance = math.hypot(C_X - P_X, C_Y - P_Y)

    if predicted_distance <= marker_1: #vehicle is pointing to the right direction. 
        reward += 10
    else:         #vehicle is pointing to the wrong direction. 
        reward -= ((predicted_distance / (distance * 2)) * (speed / 2))
    
    #Remember, logs will be written on: /aws/robomaker/SimulationJobs
    #printheader: (Reward,Progress,X,Y,P_X,P_Y,C_X,C_Y,distance,predicted_distance,yaw,steering,speed,all_wheels_on_track,distance_from_center, track_width, closest_waypoints)
    print('REWARD_LOGIC', reward,',', progress,',', x,',', y,',', P_X,',', P_Y,',', C_X,',', C_Y,',', distance,',', predicted_distance,',', yaw,',', steering,',', speed,',', 
        all_wheels_on_track,',', distance_from_center,',', track_width,',', closest_waypoints)

    return float(reward)