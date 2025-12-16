# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

from datetime import datetime
import AirsimIO
import math

# All UAVs
def waypointVisitingAllUAVs(client, uavs, taskpoint_hover_time=0, dist_err_tol=0.5, angle_err_tol=5, max_vel=5):
    """ 
    Inputs:
    #   client: UE client for connection
    #   uav: UAV obj
    #   xxx_hover_time: unit (s)
    #   dist_err_tol: distance error tolerance - unit (m) 
    #   angle_err_tol: yaw angel error tolerance - unit (deg) 
    #   max_vel: maximum velocity, unit (m/s)

    Outputs:
    #   all_completed: whether all UAVs have completed tasks
    """
    all_completed = False # flag of whether all UAVs have completed their tasks
    is_completed_list = [] # flag of each UAV's mission status. 0: not completed, 1: completed 
    for uav in uavs:
        is_completed = waypointVisiting(client, uav, taskpoint_hover_time, dist_err_tol, angle_err_tol, max_vel)
        is_completed_list.append(is_completed)
    if 0 in is_completed_list:
        all_completed = False
    else:
        all_completed = True
    return all_completed
    

# Single UAV
def waypointVisiting(client, uav, taskpoint_hover_time=0, dist_err_tol=0.5, angle_err_tol=10, max_vel=5):
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
        Takeoff 
        |
        Arrive waypoint (Update waypoint_index)
        |
        Check taskpoint hover 
        |
        Rotate (Calculate and update target_yaw)
        |
        moveToPosition (PID update UAV speed according to real-time distance)
    """

    is_completed = False # flag of completing the final waypoint
    
    # PID parameters (PID not working well!)
    Kp_vel = 0.5
    # Limit the min velocity for moveXX cmd. Don't be too slow.
    min_vel = 0.1 # m/s 
    # Rotate time unit:s (let UAV yaw converge to target_yaw)
    rotate_time = 1.5
    
    # Limit the min error tolerance here if needed. 
    # Otherwise, if the input xx_err_tol is too small, the process will get halted since the Airsim has its inherent errors!!!
    dist_err_tol= max(0.5, dist_err_tol)
    
    # Update UAV status (single UAV)
    AirsimIO.updateUAVWorldPose(client, uav)
    # Calculate the command time difference
    curr_time = datetime.now()
    time_diff = (curr_time-uav.getCurrentCommandStartTime()).total_seconds()
    
    # cmd: empty (initial, before takeoff)
    if uav.getCurrentCommand() == "":
        return False
    # cmd: takeoff
    elif uav.getCurrentCommand() == "takeoff":
        return False
    # cmd: land
    elif uav.getCurrentCommand() == "land":
        return False
    # cmd: goHome
    elif uav.getCurrentCommand() == "goHome":
        return False
    
    # cmd: hover
    elif uav.getCurrentCommand() == "hover":
        # curr_time = datetime.now()
        # time_diff = (curr_time-uav.getCurrentCommandStartTime()).total_seconds()
        # Taskpoint hover for a certain duration. Only hover when all these conditions are met
        if taskpoint_hover_time > 0 and uav.getWaypointIndex() in uav.getTaskPointsIndices() and time_diff < taskpoint_hover_time:
            # Hover not completed
            return False
        else:
            # Final waypoint?
            if uav.getWaypointIndex() >= len(uav.getWaypoints())-1:
                is_completed = True
                return is_completed
            else:
                # Calculate target yaw
                target_yaw = uav.calculateTargetYaw()
                uav.setTargetYaw(target_yaw)
                # Rotate to target yaw
                AirsimIO.rotateUAVto(client, uav, target_yaw)
                print('{} starts to rotate to yaw angle {} deg'.format(uav.getName(), round(uav.getTargetYaw(),1)))
                return False
            
    # cmd: rotate
    elif uav.getCurrentCommand() == "rotateToYaw":
        # Check current cmd completed or not 
        # Check rotating by angle error. Change to check both angle and angular rate if needed.
        if abs(uav.getTargetYaw()-uav.getCurrWorldPose()[5]) < angle_err_tol:
            print('{} reached yaw angle {} deg'.format(uav.getName(), round(uav.getTargetYaw(),1)))
            # Move to the next waypoint with speed control (PID).
            next_waypoint = uav.getWaypoints()[uav.getWaypointIndex()+1]
            uav_curr_world_pos = uav.getCurrWorldPose()[:3]
            dist = math.dist(next_waypoint, uav_curr_world_pos)
            # PID control (P only)
            vel = min(Kp_vel*dist, max_vel) # limit max speed
            vel = max(vel, min_vel) # limit min
            AirsimIO.moveUAVto(client, uav, next_waypoint, vel)
            print('{} starts to move to waypoint {}'.format(uav.getName(), uav.getWaypointIndex()+1))
        # No completion under this cmd
        return False
            
    # cmd: moveToPosition
    elif uav.getCurrentCommand() == "moveToPosition":
        # Get distance between UAV current location and next waypoint.
        next_waypoint = uav.getWaypoints()[uav.getWaypointIndex()+1]
        uav_curr_world_pos = uav.getCurrWorldPose()[:3]
        dist = math.dist(next_waypoint, uav_curr_world_pos)
        # Check arrival
        if dist < dist_err_tol:
            print('{} starts to hover on waypoint {}'.format(uav.getName(), uav.getWaypointIndex()))
            # Arrived and update waypoint index (+1)
            uav.setWaypointIndex(uav.getWaypointIndex()+1)
            # Hover (No matter if the hover time is 0, UAV's next cmd will be updated in "hover" cmd)
            AirsimIO.hoverUAV(client, uav)
        # else:
        #     # Add PID control here! (PID not working well!)
        #     vel = min(Kp_vel*dist, max_vel) # limit max speed
        #     vel = max(vel, min_vel) # limit min
        #     AirsimIO.moveUAVto(client, uav, next_waypoint, vel)
        # No completion under this cmd
        return False



