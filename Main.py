# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

# ========================================================= #
# Main file to run code in this skeleton template           #
# Replaces function of GUI worker                           #
# ========================================================= #

# ===== Import libraries =====
import logFunctions as log
import AirsimIO
import init

import time
import threading
from RepeatedTimer import RepeatedTimer
from Algorithms.Control.WaypointVisiting.WaypointVisiting import waypointVisiting, waypointVisitingAllUAVs

from Algorithms._wpts import Get_Waypoints
from Algorithms._path_follow import Follow_Path

# ===== Initialisation part =====
print("========================== Start ============================")
log.resetLog()
log.logReport("INFO","Initialisation started")

# ===== Weather Settings =====
# Using the default weather can make the simulation more fluent.
# Number: percent(*100%)
init.weather["Rain"] = 0
init.weather["Roadwetness"] = 0
init.weather["Snow"] = 0
init.weather["RoadSnow"] = 0
init.weather["MapleLeaf"] = 0
init.weather["RoadLeaf"] = 0
init.weather["Dust"] = 0
init.weather["Fog"] = 0
init.weather["WindX"] = 0   # m/s
init.weather["WindY"] = 0
init.weather["WindZ"] = 0
init.weather["TimeOfDay"] = "2023-06-08 11:30:00"
# init.setWeather() # Setting weather can slow down the simulation

# ==== UAV settings ====
init.n_uavs = 5 # number of UAVs

# Sensors on each UAV
# 1: enable; 0: disable
# init.camera_en = 0 # No camera yet. Camera needs special settings
init.barometer_en = 0
init.imu_en = 0
init.gps_en = 0
init.magnetometer_en = 0
init.distance_en = 0
init.lidar_en = 0

# Create UAVs and sensors, arm all UAVs
init.initUAVs()

# Scheduler. Execute every a period of time
# rt = RepeatedTimer(1, AirsimIO.plotAllUAVsPaths, init.client, init.uavs, duration=1.1)
# rt_plot_names = RepeatedTimer(1, AirsimIO.plotAllUAVsNames, init.client, init.uavs, duration=0.9)

# ===== Running simulation =====
if __name__ == "__main__":

    print("Main simulation started")
    log.logReport("INFO","Main simulation started")

    get_waypoints = Get_Waypoints(init.uavs)
    get_waypoints.initWaypoints()
    get_waypoints.initPathForAllUavs()

    # rt.start() # Start repeated timer and plot paths
    # init.rt_draw_paths.start()

    AirsimIO.plotAllUAVsPaths(init.client, init.uavs, duration=-1, is_persistent=True)
    # AirsimIO.plotAllUAVsNames(init.client, init.uavs, duration=-1).join()

    # NOTE: Strings can only be cleaned by setting duration to a positive value
    AirsimIO.plotAllUAVsWaypontsLabels(init.client, init.uavs, duration=30) 

    path_following = Follow_Path(init.client, init.uavs)
    stop_simulation = path_following.runSimulation()
    
    time.sleep(1)
    AirsimIO.goHomeAllUAVs(init.client, init.uavs)
    time.sleep(10)
    AirsimIO.rotateAllUAVsTo(init.client, init.uavs, 0)
    time.sleep(2)
    AirsimIO.landAllUAVs(init.client, init.uavs)
    time.sleep(3)


    # rt.stop()
    # init.rt_draw_paths.stop()
    # init.rt_airsim_updates.stop()
    
    # Clean all plots
    AirsimIO.cleanAllPersistentPlots(init.client)
    
    init.cleanUpSimulation()
    

    print("========================== End ============================")
