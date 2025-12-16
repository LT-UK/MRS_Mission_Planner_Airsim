# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

# ========================================================= #
# This file is used to modify settings.json file         
# After running this file, new setting.json file should 
# replace old one in airsim folder manually.
# Then, UE should be reloaded. (Stop -> PLay) 
# ========================================================= #

# Sensor parameter settings are not ready. 
# No camera yet. Cameras need special settings
# Do NOT import init here, otherwise, this file will try to connect with airsim in UE.

import json

# Number of UAVs
n_uavs = 5
# ======== Sensor Enablers ========
# 1: enable; 0: disable
camera_en = 0
barometer_en = 0
imu_en = 0
gps_en = 0
magnetometer_en = 0
distance_en = 0
lidar_en = 0

settings = {
    "SeeDocsAt":"https://github.com/Microsoft/AirSim/blob/main/docs/settings.md",
	"SettingsVersion":1.2,
	"SimMode":"Multirotor",
	"ViewMode":"",
	"Vehicles":{
    }
}

for u in range(n_uavs):
    # Name uav
    uav_name = "UAV_" + str(u+1)
    # init this UAV in settings
    # Set UAV initial location, 2m distance, max 5 UAVs per row.
    settings["Vehicles"][uav_name] = {
        "VehicleType": "SimpleFlight",
        "AutoCreate": True,
        "X": 5*int(u/5),
        "Y": 5*(u%5),
        "Z": 0.0,
        "Yaw": 0.0,
        "Pitch": 0.0,
        "Roll": 0.0,
        "Sensors": {}
    }
    # Add sensors
    # Different types of sensors have different parameter settings.
    if camera_en:
        sensor_name = "Camera_" + str(u+1)
        # Modify sensor parameter here
        settings["Vehicles"][uav_name]["Cameras"] = {
            # Camera settings
        }
    if distance_en:
        sensor_name = "Distance_" + str(u+1)
        # Modify sensor parameter here
        settings["Vehicles"][uav_name]["Sensors"][sensor_name] = {
            "SensorType": 5,
			"Enabled": True,
            "MinDistance": 0.0,
			"MaxDistance": 50.0,
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0,
            "Yaw": 0.0,
            "Pitch": 0.0,
            "Roll": 0.0,
            "DrawDebugPoints": False
        }

# Generate json file
settings_json = json.dumps(settings, indent=4)
# Open file and overwrite if file exists. Create a new file and write if file dest not exist.
with open('settings.json', 'w') as file:
    file.write(settings_json)