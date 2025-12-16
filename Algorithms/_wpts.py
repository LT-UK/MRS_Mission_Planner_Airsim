# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #
import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)


class Get_Waypoints:
    def __init__(self, uavs):
        self.uavs = uavs
    
    def initWaypoints(self, waypoint_file=None):
        # hand code the waypoints
        point_1_0 = [0,0,0]
        point_1_1 = [0,0,-3]
        point_1_2 = [5,-5,-3]
        point_1_3 = [10,-5,-3]
        point_1_4 = [10,5,-3]
        point_1_5 = [0,0,-2]
        
        point_2_0 = [0,5,0]
        point_2_1 = [0,5,-3]
        point_2_2 = [10,20,-2]
        point_2_3 = [15,20,-3]
        point_2_4 = [20,15,-3]
        point_2_5 = [0,5,-4]

        self.points_1 = [point_1_0, point_1_1, point_1_2, point_1_3, point_1_4, point_1_5]
        self.points_2 = [point_2_0, point_2_1, point_2_2, point_2_3, point_2_4, point_2_5]
    

    
    def initPathForAllUavs(self):

        self.uavs[0].setWaypoints(self.points_1)
        self.uavs[1].setWaypoints(self.points_2)

        self.uavs[0].setTaskPointsIndices([1,3])
        self.uavs[1].setTaskPointsIndices([1,2,3])

        print('route for each uav is initiated.')


