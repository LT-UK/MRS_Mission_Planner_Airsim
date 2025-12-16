# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

# ===== Class =====
class Sensor:
    
    # ===== Class variables =====
    
    # ===== Constructor =====
    def __init__(self, sensor_type, name, pose):
        self.sensor_type = sensor_type
        self.name = name
        self.pose = pose
        print("Sensor Instantiated")

    # ===== Getters and setters for instance variables =====
    # Sensor type
    def setSensorType(self, sensor_type):
        self.sensor_type = sensor_type

    def getSensorType(self):
        return self.sensor_type

    # Sensor name
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    # Sensor pose
    def setPose(self, pose):
        self.pose = pose

    def getPose(self):
        return self.pose

    # Sensor data
    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    # Sensor value
    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value


