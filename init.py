# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

import AirsimIO
import Sensor
import UAV
import logFunctions as log
import time
from RepeatedTimer import RepeatedTimer


# Create airsim client
client = AirsimIO.initClient()

n_uavs = 5 # number of uavs
uavs = []

# UAV waypoints and path settings
waypoint_size = 5
path_thickness = 2

# ======== Sensor Enablers ========
# 1: enable; 0: disable
# camera_en = 0    # Camera needs special settings
barometer_en = 0
imu_en = 0
gps_en = 0
magnetometer_en = 0
distance_en = 1
lidar_en = 0

# Sensor dictionary
sensors = {"Barometer":[],
           "Imu":[],
           "Gps":[],
           "Magnetometer":[],
           "Distance":[],
           "Lidar":[]}

# Weather parameters: float 0-1
# Wind: m/s
weather = {"Rain":0,
           "Roadwetness":0,
           "Snow":0,
           "RoadSnow":0,
           "MapleLeaf":0,
           "RoadLeaf":0,
           "Dust":0,
           "Fog":0,
           "WindX":0,
           "WindY":0,
           "WindZ":0,
           "TimeOfDay":"2023-10-27 11:20:00"}


# ======== Repeated Timers ========
rt_draw_paths = RepeatedTimer(1, AirsimIO.plotAllUAVsPaths, client, uavs, duration=1.01)
rt_airsim_updates = RepeatedTimer(0.1, AirsimIO.updateUAVsStatus, client, uavs)


# ======== Functions ========

def setWeather():
    AirsimIO.defineWeather(client,
                           weather["Rain"],
                           weather["Roadwetness"],
                           weather["Snow"],
                           weather["RoadSnow"],
                           weather["MapleLeaf"],
                           weather["RoadLeaf"],
                           weather["Dust"],
                           weather["Fog"],
                           weather["WindX"],
                           weather["WindY"],
                           weather["WindZ"],
                           weather["TimeOfDay"])
    print("Weather is set")
    log.logReport("INFO", "Weather is set")
    
def createSensors(sensor_type):
    # Default sensor name: sensorType_number+1
    # Default sensor pos [0,0,0,0,0,0]
    # Reset sensors list of this type.
    sensors[sensor_type].clear()
    # Create new sensors of this type for each uav
    for s in range(n_uavs):
        sensors[sensor_type].append(Sensor.Sensor(sensor_type, sensor_type+"_"+str(s+1), [0,0,0,0,0,0]))
    print("Sensors of " + sensor_type + " are created")
    log.logReport("INFO", "Sensors of type " + sensor_type + " are created")

def createUAVs():
    # UAVs are homogeneous on creation. They can be changed to heterogeneous afterwards
    uavs.clear() # Reset UAVs list !!!Do NOT use uavs=[]!!!
    for u in range(n_uavs):
        # Set UAV initial location, 2m distance, max 10 UAVs per row.
        X = 5*int(u/5)
        Y = 5*(u%5)
        uavs.append(UAV.UAV(u+1, "UAV_"+str(u+1), [X,Y,0,0,0,0]))

def initUAVs():
    createUAVs()
    # No camera yet. Camera needs special settings
    if barometer_en:
        createSensors("Barometer")
        for u in range(n_uavs):
            uavs[u].addSensor(sensors["Barometer"][u])
    if imu_en:
        createSensors("Imu")
        for u in range(n_uavs):
            uavs[u].addSensor(sensors["Imu"][u])
    if gps_en:
        createSensors("Gps")
        for u in range(n_uavs):
            uavs[u].addSensor(sensors["Gps"][u])
    if magnetometer_en:
        createSensors("Magnetometer")
        for u in range(n_uavs):
            uavs[u].addSensor(sensors["Magnetometer"][u])
    if distance_en:
        createSensors("Distance")
        for u in range(n_uavs):
            uavs[u].addSensor(sensors["Distance"][u])
    if lidar_en:
        createSensors("Lidar")
        for u in range(n_uavs):
            uavs[u].addSensor(sensors["Lidar"][u])
    # arm all UAVs
    # AirsimIO.armEnableAllUAVs(client, uavs)

def cleanUpSimulation():
    log.logReport("INFO", "Cleaning Up Simulation")
    # Cleanup
    AirsimIO.disarmResetDisableAllUAVs(client, uavs)
    print("\n=========================================\nCleanup:\n=========================================")
    time.sleep(5)