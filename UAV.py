# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #
import logFunctions as log
from datetime import datetime
import numpy as np
import math


# UAV cmd lib: 
#   takeoff, 
#   hover, 
#   rotateToYaw, rotateByYawRate
#   land, 
#   moveToZ, moveToPosition, moveToGPS
#   goHome

# ===== Class =====
class UAV:
    
    # ===== Class variables =====
    vehicle_type = "UAV"

    # ===== Constructor =====
    def __init__(self, number, name, init_pose):
        self.number = number
        self.name = name
        self.curr_pose = [0,0,0,0,0,0]  # Body frame (NED), relative to the initial pose Format: [0,0,0,0,0,0]
        self.curr_world_pose = init_pose # World frame (NED)
        self.init_pose = init_pose # World frame (NED)
        self.curr_speed = 0
        self.sensors = []
        self.waypoints = [] # World frame (NED)
        self.waypoint_index = 0  # The index of the waypoint that the UAV is heading to 
        self.task_points_indices = []  # The indices of the waypoints where the UAV should hover and execute task
        self.waypoint_color_rgba = [1.0, 0.0, 0.0, 1.0]
        self.path_color_rgba = [0.0, 1.0, 0.0, 1.0]
        self.taken_off = False  # flag of whether the UAV has taken off
        self.landed = False     # flag of whether the UAV has landed
        self.has_collided = False # flag of whethre the UAV has colided with anything
        self.destination = [0, 0, 0]  # World frame landing location
        self.curr_cmd = "" # takeoff, hover, rotateToYaw, land, moveToZ, moveToPosition, goHome ...
        self.curr_cmd_start_time = datetime.now()
        self.target_yaw = init_pose[-1] # World frame, target yaw angle for rotate cmd
        print(name + " is created")
        log.logReport("INFO", name + " is created")

    # ===== Getters and setters for instance variables =====

    # UAV number
    def setNumber(self, number):
        self.number = number

    def getNumber(self):
        return self.number

    # UAV name
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    # UAV initial pose
    def setInitPose(self, init_pose):
        self.init_pose = init_pose

    def getInitPose(self):
        return self.init_pose

    # UAV current pose
    def setCurrPose(self, curr_pose):
        self.curr_pose = curr_pose

    def getCurrPose(self):
        return self.curr_pose

    # UAV current world pose
    def setCurrWorldPose(self, curr_world_pose):
        self.curr_world_pose = curr_world_pose

    def getCurrWorldPose(self):
        return self.curr_world_pose

    # UAV current speed
    def setCurrSpeed(self, curr_speed):
        self.curr_speed = curr_speed

    def getCurrSpeed(self):
        return self.curr_speed

    # UAV sensors
    def setSensors(self, sensors):
        self.sensors = sensors

    def getSensors(self):
        return self.sensors
    
    def addSensor(self, sensor):
        self.sensors.append(sensor)

    # UAV waypoints
    def setWaypoints(self, waypoints):
        self.waypoints = waypoints

    def getWaypoints(self):
        return self.waypoints
    
    def addWaypoint(self, waypoint, pos=-1):
        if pos in range(len(self.waypoints)):
            self.waypoints.insert(pos, waypoint)
        else:
            self.waypoints.append(waypoint)
    # Remove waypoint?
    
    # UAV waypoint index
    def setWaypointIndex(self, waypoint_index):
        self.waypoint_index = waypoint_index

    def getWaypointIndex(self):
        return self.waypoint_index
    
    # UAV task points indices
    def setTaskPointsIndices(self, task_points_indices):
        self.task_points_indices = task_points_indices

    def getTaskPointsIndices(self):
        return self.task_points_indices
    
    # UAV waypoints color
    def setWaypointColor(self, waypoint_color_rgba):
        self.waypoint_color_rgba = waypoint_color_rgba

    def getWaypointColor(self):
        return self.waypoint_color_rgba
    
    # UAV path color
    def setPathColor(self, path_color_rgba):
        self.path_color_rgba = path_color_rgba

    def getPathColor(self):
        return self.path_color_rgba

    # UAV collision
    def setCollision(self, has_collided):
        self.has_collided = has_collided

    def getCollision(self):
        return self.has_collided
    
    # TakenOff?
    def setTakenOff(self, taken_off):
        self.taken_off = taken_off

    def getTakenOff(self):
        return self.taken_off
    
    # Landed?
    def setLanded(self, landed):
        self.landed = landed

    def getLanded(self):
        return self.landed
    
    # Final destination, landing location
    def setFinalDestination(self, destination):
        self.destination = destination

    def getFinalDestination(self):
        return self.destination
    
    # Current Command
    def setCurrentCommand(self, cmd):
        self.curr_cmd = cmd

    def getCurrentCommand(self):
        return self.curr_cmd
    
    # Current Command Start Time
    def setCurrentCommandStartTime(self, datetime):
        self.curr_cmd_start_time = datetime

    def getCurrentCommandStartTime(self):
        return self.curr_cmd_start_time
    
    # Target Yaw Angle
    def setTargetYaw(self, yaw):
        self.target_yaw = yaw

    def getTargetYaw(self):
        return self.target_yaw
    
    def calculateTargetYaw(self):
        target_yaw = np.rad2deg(math.atan2((self.waypoints[self.waypoint_index][1]-self.curr_world_pose[1]),(self.waypoints[self.waypoint_index][0]-self.curr_world_pose[0])))
        return target_yaw
        