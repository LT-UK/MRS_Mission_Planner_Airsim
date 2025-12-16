import os, sys
import time
import math
import numpy as np
from datetime import datetime
import AirsimIO
import logFunctions as log

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)


# === Basic class for hard-coded waypoint following ====
class Follow_Path:

    def __init__(self, client = None, uavs = None):

        self.client = client
        self.uavs = uavs
        self.is_complete = np.zeros(len(uavs))
        # self.waypoints = waypoints

    def waypointFollow(self, uav, taskpoint_hover_time=0, dist_err_tol=1.0, angle_err_tol=10, max_vel=5):

        """ 
        Inputs:
        #   client: UE client for connection
        #   uav: UAV obj
        #   xxx_hover_time: unit (s)
        #   dist_err_tol: distance error tolerance - unit (m) 
        #   angle_err_tol: yaw angel error tolerance - unit (deg) 
        #   max_vel: maximum velocity, unit (m/s)

        Outputs:
        #   is_completed: whether all the waypoints have been visited

        Mission Process: 
        ---> Start with hover
        |    | - Check if waypoints are set - No -> Continue
        |    | - Check if finish taskpoint hover time - No -> Continue
        |    | - Check if all waypoints done - Yes - > Land
        |    Set next waypoint & Rotate (Calculate and update target_yaw)
        |    |
        |    moveToPosition (PID update UAV speed according to real-time distance)
        |    | - Check if arrive waypoint (Update waypoint_index) - No -> Continue
        <--- Hover
        """

        # PID parameters (PID not working well!)
        Kp_vel = 0.5
        # Limit the min velocity for moveXX cmd. Don't be too slow.
        min_vel = 0.1 # m/s 
        # Rotate time unit:s (let UAV yaw converge to target_yaw)
        rotate_time = 1.5
        
        # Limit the min error tolerance here if needed. 
        # Otherwise, if the input xx_err_tol is too small, the process will get halted since the Airsim has its inherent errors!!!
        dist_err_tol= max(2.0, dist_err_tol)
        
        # Update UAV status (single UAV)
        AirsimIO.updateUAVWorldPose(self.client, uav)
        # Calculate the command time difference
        curr_time = datetime.now()
        time_diff = (curr_time-uav.getCurrentCommandStartTime()).total_seconds()


        if uav.getCurrentCommand() == 'hover':

            if taskpoint_hover_time > 0 and uav.getWaypointIndex() in uav.getTaskPointsIndices() and time_diff < taskpoint_hover_time:
                # Hover not completed
                return False
            else:
                if uav.getWaypointIndex() >= len(uav.getWaypoints()):
                    is_completed = True
                    return is_completed
                else:
                    # Calculate target yaw
                    target_yaw = round(uav.calculateTargetYaw(),0)
                    uav.setTargetYaw(target_yaw)
                    # Rotate to target yaw
                    AirsimIO.rotateUAVto(self.client, uav, target_yaw)
                    print('{} starts to rotate to yaw angle {} deg'.format(uav.getName(), round(uav.getTargetYaw(),1)))
                    return False

        # cmd: rotate
        elif uav.getCurrentCommand() == "rotateToYaw":
            # Check current cmd completed or not 
            # Check rotating by angle error. Change to check both angle and angular rate if needed.
            if abs(uav.getTargetYaw()-uav.getCurrWorldPose()[5]) < angle_err_tol:
                print('{} reached yaw angle {} deg'.format(uav.getName(), uav.getTargetYaw()))
                # Move to the next waypoint with speed control (PID).
                next_waypoint = uav.getWaypoints()[uav.getWaypointIndex()]
                uav_curr_world_pos = uav.getCurrWorldPose()[:3]
                dist = math.dist(next_waypoint, uav_curr_world_pos)
                # PID control (P only)
                vel = min(Kp_vel*dist, max_vel) # limit max speed
                vel = max(vel, min_vel) # limit min
                AirsimIO.moveUAVto(self.client, uav, next_waypoint, vel)
                print('{} starts to move to waypoint {}'.format(uav.getName(), uav.getWaypointIndex()))
            # No completion under this cmd
            return False

        elif uav.getCurrentCommand() == 'moveToPosition':
            # pull out states to confirm where the drone is at
            uav_curr_world_pos = uav.getCurrWorldPose()[0:3]
            uav_waypoint = uav.getWaypoints()[uav.getWaypointIndex()][0:3]
            proximity_to_waypoint = math.dist(uav_curr_world_pos, uav_waypoint)
            
            # switch the waypoint if arrives at the last one
            if proximity_to_waypoint < dist_err_tol:
                # update the waypoint index
                uav.setWaypointIndex(uav.getWaypointIndex() + 1)
                AirsimIO.hoverUAV(self.client, uav)
            return False


    def takeoffAllUAVs(self):
        # Take off UAVs for those haven't
        fs = []
        for uav in self.uavs:
            if not uav.getTakenOff():
                fs.append(AirsimIO.takeoffUAV(self.client, uav))
                uav.setTakenOff(True) 
        for f in fs:
            f.join() # wait util all drones take off
        print('all uavs have taken off.')


    def hoverAllUAVs(self):
        AirsimIO.hoverAllUAVs(self.client, self.uavs)

    def getSimCompleted(self):
        return all(self.is_complete)

    def runSimulation(self):
        
        ###### DEBUG - display the inital locations before simulation ######
        log.logReport("INFO","Simulation Running")
        AirsimIO.armEnableAllUAVs(self.client, self.uavs)
        AirsimIO.updateUAVsStatus(self.client, self.uavs)
        for idx, uav in enumerate(self.uavs):
            print('uav {} current location {} next waypoint {}'.format(
                idx, [round(xyz, 1) for xyz in uav.getCurrWorldPose()[0:3]], uav.getWaypoints()[0:3]))
        #######
            
        self.takeoffAllUAVs()
        self.hoverAllUAVs()

        # Waypoint Following
        while self.getSimCompleted() == False:

            for idx, uav in enumerate(self.uavs):
                is_complete = self.waypointFollow(uav)
                self.is_complete[idx] = is_complete

            # Delay
            time.sleep(0.1)

        return self.getSimCompleted()