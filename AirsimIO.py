# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

# ========================================================= #
# This file contains a set of custom functions that use the #
# AirSim Python APIs to collect data from AirSim and update #
# the attributes of each Python UAV object accordingly      #
# ========================================================= #

# WARNING: ".join()" command in UAV operations should be avoided, 
# because a thread with this command interferes with other threads.


# ===== Import libraries =====
import airsim
import numpy as np
import cv2
import logFunctions as log
import time
from datetime import datetime


# ========== AirSim Client Handling ==========
# Initialises and returns an AirSim client
def initClient():
    client = airsim.MultirotorClient()
    client.confirmConnection()
    log.logReport("INFO", "AirSim client is created")
    return client


# Arms and enables API control of uav
def armEnableUAV(client, uav):
    client.enableApiControl(True, uav.getName())
    client.armDisarm(True, uav.getName())
    # print(uav.getName() + " is armed")
    # log.logReport("INFO", uav.getName() + " is armed")


# Arms and enables API control of all uavs
def armEnableAllUAVs(client, uavs):
    for uav in uavs:
        armEnableUAV(client, uav)
    print("All UAVs are armed")
    log.logReport("INFO", "All UAVs are armed")


# ===== Clean Exit =====
# Disarms, resets and disables API control of uav
def disarmResetDisableAllUAVs(client, uavs):
    for uav in uavs:
        client.armDisarm(False, uav.getName())
    log.logReport("INFO", "All UAVs are disarmed")
    resetClient(client)


# Reset client
def resetClient(client):
    client.reset()
    log.logReport("INFO", "AirSim client is removed")


# ========== UAV Motions ==========
# ==== Single UAV ====
# Takes off the uav
def takeoffUAV(client, uav):
    command = client.takeoffAsync(vehicle_name=uav.getName())
    uav.setCurrentCommand("takeoff")
    uav.setCurrentCommandStartTime(datetime.now())
    return command


# Hovers the uav
def hoverUAV(client, uav):
    command = client.hoverAsync(vehicle_name=uav.getName())
    uav.setCurrentCommand("hover")
    uav.setCurrentCommandStartTime(datetime.now())
    return command


# Land UAV
def landUAV(client, uav):
    command = client.landAsync(timeout_sec=600, vehicle_name=uav.getName())
    uav.setCurrentCommand("land")
    uav.setCurrentCommandStartTime(datetime.now())
    return command


# Go Home. Hover above home location at a hight of around 0.5m not landing.
def goHomeUAV(client, uav):
    command = client.goHomeAsync(timeout_sec=3e+38, vehicle_name=uav.getName())
    uav.setCurrentCommand("goHome")
    uav.setCurrentCommandStartTime(datetime.now())
    return command


# Rotates the uav to 'yaw' orientation
def rotateUAVto(client,uav,yaw):
    command = client.rotateToYawAsync(yaw, vehicle_name=uav.getName())
    uav.setCurrentCommand("rotateToYaw")
    uav.setCurrentCommandStartTime(datetime.now())
    return command


# Moves the uav to point(x,y,z) at a specified velocity
def moveUAVto(client, uav, point, vel):
    # point: World NED (need to change to Body frame NED)
    point_bodyframe = [point[i]-uav.getInitPose()[i] for i in range(3)]
    command = client.moveToPositionAsync(point_bodyframe[0], point_bodyframe[1], point_bodyframe[2], vel, vehicle_name=uav.getName())
    uav.setCurrentCommand("moveToPosition")
    uav.setCurrentCommandStartTime(datetime.now())
    return command


# Moves the uav to altitude z at a specified velocity
def moveUAVtoZ(client, uav, z, vel):
    # World NED
    command = client.moveToZAsync(z, vel, vehicle_name=uav.getName())
    uav.setCurrentCommand("moveToZ")
    uav.setCurrentCommandStartTime(datetime.now())
    return command


# Moves the uav by 'vx', 'vy' for a specified duration in its body frame, maintaining altitude 'z'
def moveUAVbyVelZ(client, uav, vx, vy, z, duration):
    # Body NED
    command = client.moveByVelocityZBodyFrameAsync(vx, vy, z, duration, vehicle_name=uav.getName())
    uav.setCurrentCommand("moveByVelZ")
    uav.setCurrentCommandStartTime(datetime.now())
    return command



# ==== Commands to All UAVs ====
def takeoffAllUAVs(client, uavs):
    print("All UAVs start to take off")
    log.logReport("INFO", "All UAVs start to take off")
    for uav in uavs:
        command = takeoffUAV(client, uav)
    # command.join()  # Waite untill the last UAV finished this command
    time.sleep(5) # Allow running other threads 
    print("All UAVs have taken off")
    log.logReport("INFO", "All UAVs have taken off")


def landAllUAVs(client, uavs):
    # UAVs should Go Home first before landing
    print("All UAVs start to land")
    log.logReport("INFO", "All UAVs start to land")
    for uav in uavs:
        command = landUAV(client, uav)
    # command.join()  # Waite untill the last UAV has finished this command
    time.sleep(3) # Allow running other threads 
    print("All UAVs have landed")
    log.logReport("INFO", "All UAVs have landed")


def hoverAllUAVs(client, uavs):
    print("All UAVs start to hover")
    log.logReport("INFO", "All UAVs start to hover")
    for uav in uavs:
        command = hoverUAV(client, uav)
    

def rotateAllUAVsTo(client, uavs, yaw):
    print("All UAVs start to rotate to "+str(yaw)+" degree")
    log.logReport("INFO", "All UAVs start to rotate to "+str(yaw)+" degree")
    for uav in uavs:
        command = rotateUAVto(client, uav, yaw)
    # command.join()  # Waite untill the last UAV has finished this command
    time.sleep(2) # Allow running other threads
    print("All UAVs have finished rotating")
    log.logReport("INFO", "All UAVs have finished rotating")


def goHomeAllUAVs(client, uavs):
    # Extra waiting time is needed. The amount of time can be calculated according to distance from home.
    print("All UAVs start to go home")
    log.logReport("INFO", "All UAVs start to go home")
    for uav in uavs:
        command = goHomeUAV(client, uav)
    # command.join()  # Waite untill the last UAV has finished this command
    time.sleep(2) # Allow running other threads
    # print("All UAVs have returned home")
    # log.logReport("INFO", "All UAVs have returned home")


# ========== Get Data from Airsim ==========
# Updates UAV object parameters based on airsim inputs
# Max frequency 10hz, based on 10 UAVs
def updateUAVsStatus(client, uavs):
    for uav in uavs:
        # Updates current pose of the UAV
        # NOTE: CurrPose = current position/orientation relative to the UAV start coordinate frame
        # NOTE: CurrWorldPose = current position/orientation relative to the world frame - calculate using a custom function in this file
        uav.setCurrPose(np.append(getUAVpos(client, uav), getUAVorientation(client, uav)))
        uav.setCurrWorldPose(np.append(getUAVposWorld(client, uav), getUAVorientationWorld(client, uav)))

        # Updates whether or not the UAV is currently colliding with anything, True/False
        uav.setCollision(getUAVcollision(client, uav).has_collided)

        # Update the data collected from each sensor
        # NOTE: sensor data = entire data object obtained from airsim
        # NOTE: sensor value = useful value from the data object, ex. just the distance measurement from a distance sensor
        for s in range(0,len(uav.getSensors())):
            uav.sensors[s].setData(getSensorData(client, uav, uav.getSensors()[s]))
            uav.sensors[s].setValue(getSensorValue(client, uav, uav.getSensors()[s]))

# Get world pose only for speeding up
def updateUAVsWorldPose(client, uavs):
    for uav in uavs:
        updateUAVWorldPose(client, uav)

# Update single UAV
def updateUAVWorldPose(client, uav):
    uav.setCurrWorldPose(np.append(getUAVposWorld(client, uav), getUAVorientationWorld(client, uav)))

# ===== Vehicle Pose =====
# Returns position vector of uav relative to initial starting pose
def getUAVpos(client, uav):
    current_pose = client.simGetVehiclePose(vehicle_name=uav.getName())
    current_pos = [current_pose.position.x_val, current_pose.position.y_val, current_pose.position.z_val]
    return current_pos


# Returns position vector of uav in world frame, by adding the initial UAV position to its current position
def getUAVposWorld(client, uav):
    return (np.add(getUAVpos(client, uav), uav.getInitPose()[0:3]))


# Returns orientation of uav relative to initial starting pose
def getUAVorientation(client, uav):
    current_pose = client.simGetVehiclePose(vehicle_name=uav.getName())
    current_or = np.rad2deg(airsim.to_eularian_angles(current_pose.orientation))
    return current_or


# Returns orientation of uav in world frame, by adding the initial UAV orientation to its current orientation
def getUAVorientationWorld(client, uav):
    return (np.add(getUAVorientation(client,uav), uav.getInitPose()[3:6]))

# Returns collision info
def getUAVcollision(client, uav):
    return (client.simGetCollisionInfo(vehicle_name=uav.getName()))


# ===== Sensor Data =====
# Returns data of uav sensor
def getSensorData(client, uav, sensor):
    if(sensor.getSensorType() == "Distance"):
        data = client.getDistanceSensorData(distance_sensor_name = sensor.getName(), vehicle_name=uav.getName())
    elif(sensor.getSensorType() == "Camera"):
        datas = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)], vehicle_name=uav.getName(), external=False)
        data = datas[0]

    # ... elif for any other type of sensor needed ...

    else:
        data = 0

    return data


# Returns value of uav sensor
def getSensorValue(client, uav, sensor):
    if(sensor.getSensorType() == "Distance"):
        # For a distance sensor, the distance measurement is considered as its 'value'
        data = client.getDistanceSensorData(distance_sensor_name = sensor.getName(), vehicle_name=uav.getName())
        value = data.distance
    elif(sensor.getSensorType() == "Camera"):
        # For a camera, the image is considered as its 'value'
        data = client.simGetImage("front_center", 0, vehicle_name=uav.getName())
        value = np.asarray(bytearray(data), dtype="uint8")
        value = cv2.imdecode(value, cv2.IMREAD_COLOR)

    # ... elif for any other type of sensor needed ...

    else:
        # TODO exception handling if needed
        value = 0

    return value


# ========== Set Simulation Weather ==========
# Weather: float 0-1
# Wind: m/s
def defineWeather(client, rain, road_wetness, snow, road_snow, maple_leaf, road_leaf, dust, fog, wind_x, wind_y, wind_z, tod):
    # Configure Weather
    client.simEnableWeather(True)
    client.simSetWeatherParameter(airsim.WeatherParameter.Rain, rain)
    client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, road_wetness)
    client.simSetWeatherParameter(airsim.WeatherParameter.Snow, snow)
    client.simSetWeatherParameter(airsim.WeatherParameter.RoadSnow, road_snow)
    client.simSetWeatherParameter(airsim.WeatherParameter.MapleLeaf, maple_leaf)
    client.simSetWeatherParameter(airsim.WeatherParameter.RoadLeaf, road_leaf)
    client.simSetWeatherParameter(airsim.WeatherParameter.Dust, dust)
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, fog)
    
    # Set wind to (X,Y,Z) in NED (forward direction)
    wind = airsim.Vector3r(wind_x, wind_y, wind_z)
    client.simSetWind(wind)

    # Configure time of day
    client.simSetTimeOfDay(True, tod)


# ========== AirSim Plots ==========
# Lines from point[0] to point[1], point[2] to point[3]
# Caution: no line between point[1] and point[2]!!! The number of points must be even!
def plotLineList(client, point_list, color_rgba=[1.0, 0.0, 0.0, 1.0], thickness=5.0, duration=-1.0, is_persistent=False):
    points = [] # World NED
    for i in range(len(point_list)):
        point_3r = airsim.Vector3r(point_list[i][0], point_list[i][1], point_list[i][2])
        points.append(point_3r)
    client.simPlotLineList(points, color_rgba, thickness, duration, is_persistent)


# Lines from point[0] to point[1], point[1] to point[2].
# Lines between all points
def plotLineStrip(client, point_list, color_rgba=[1.0, 0.0, 0.0, 1.0], thickness=5.0, duration=-1.0, is_persistent=False):
    # Convert points to Vector3r format, convert height to negative in NED coordinates
    points = [] # World NED
    for i in range(len(point_list)):
        point_3r = airsim.Vector3r(point_list[i][0], point_list[i][1], point_list[i][2])
        points.append(point_3r)

    client.simPlotLineStrip(points, color_rgba, thickness, duration, is_persistent)


# Plot points
def plotPoints(client, point_list, color_rgba=[1.0, 0.0, 0.0, 1.0], size=10.0, duration=-1.0, is_persistent=False):
    # Convert points to Vector3r format, convert height to negative in NED coordinates
    points = [] # World NED
    for i in range(len(point_list)):
        point_3r = airsim.Vector3r(point_list[i][0], point_list[i][1], point_list[i][2])
        points.append(point_3r)

    client.simPlotPoints(points, color_rgba, size, duration, is_persistent)

# Plot UAV waypoints labels
def plotUAVwaypontsLabels(client, uav, label_scale=1, color_rgba=[0.0, 0.0, 1.0, 1.0], duration=10):
    # NOTE: Strings plot by simPlotStrings() cannot be cleaned by cleanAllPersistentPlots()
    # Set duration (unit: sec) to clean the string plots
    uav_no = uav.getNumber()
    waypoints_labels = [] 
    waypoints_pos_3r = []
    for idx, wp in enumerate(uav.getWaypoints()):
        waypoints_labels.append(str(uav_no) + "_" + str(idx))
        wp_3r = airsim.Vector3r(wp[0], wp[1], wp[2])
        waypoints_pos_3r.append(wp_3r)
    client.simPlotStrings(waypoints_labels, waypoints_pos_3r, label_scale, color_rgba, duration)

# Plot all UAVs waypoints labels
def plotAllUAVsWaypontsLabels(client, uavs, label_scale=1, color_rgba=[0.0, 0.0, 1.0, 1.0], duration=-1.0):
    for uav in uavs:
        if uav.getWaypoints():
            plotUAVwaypontsLabels(client, uav, label_scale, color_rgba, duration)

# Plot UAV path
def plotUAVpath(client, uav, waypoint_size=5, path_thickness=2, duration=-1.0, is_persistent=False):
    plotPoints(client, uav.getWaypoints(), uav.getWaypointColor(), waypoint_size, duration, is_persistent)
    plotLineStrip(client, uav.getWaypoints(), uav.getPathColor(), path_thickness, duration, is_persistent)


# Plot All UAVs' paths
def plotAllUAVsPaths(client, uavs, waypoint_size=5, path_thickness=2, duration=-1.0, is_persistent=False):
    for uav in uavs:
        if uav.getWaypoints():
            plotUAVpath(client, uav, waypoint_size, path_thickness, duration, is_persistent)


# Plot All UAVs' names
def plotAllUAVsNames(client, uavs, name_scale=1, color_rgba=[0.0, 0.0, 1.0, 1.0], duration=-1.0):
    uavs_names = []
    uavs_curr_pos = []
    for uav in uavs:
        uavs_names.append(uav.getName())
        uav_curr_world_pose = uav.getCurrWorldPose() 
        uav_curr_pos_3r = airsim.Vector3r(uav_curr_world_pose[0], uav_curr_world_pose[1], uav_curr_world_pose[2])
        uavs_curr_pos.append(uav_curr_pos_3r)
    client.simPlotStrings(uavs_names, uavs_curr_pos, name_scale, color_rgba, duration)


# Clean all persistent plots
def cleanAllPersistentPlots(client):
    client.simFlushPersistentMarkers()
    
