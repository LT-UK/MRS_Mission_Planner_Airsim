# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

# ======== Airsim Installation ======== #
Installation instructions: https://microsoft.github.io/AirSim/


UE installation issue on macOS: “Can’t find Xcode install for Metal compiler. Please install Xcode and run Xcode.app to accept license or ensure active developer directory is set to current Xcode installation using xcode-select.”
Solution: https://forums.unrealengine.com/t/cant-find-xcode-install-for-metal-compiler/477836

Update/Install cmake: https://macappstore.org/cmake/

CSC: error CS2012:
Cannot open ‘/Users/Shared/Epic
Games/UE_4.27/Engine/Source/Programs/DotNETCommon/DotNETUtilities/obj/Development/DotNETUtilities.dll’
for writing – ‘Access to the path
“/Users/Shared/Epic
Games/UE_4.27/Engine/Source/Programs/DotNETCommon/DotNETUtilities/obj/Development/DotNETUtilities.dll”
is denied.’ 
Solution: https://forums.unrealengine.com/t/unable-to-compile-with-xcode-unreal-4-26-big-sur/475696
chmod -R u+w '/Users/Shared/Epic Games/UE_4.27/Engine/Source/Programs/DotNETCommon/DotNETUtilities/obj/Development'
chmod -R u+w '/Users/Shared/Epic Games/UE_4.27/Engine/Source/Programs/UnrealBuildTool/obj/Development'

# ======== Airsim APIs ======== #
ref: 
-Brief-
https://microsoft.github.io/AirSim/apis/

-Detailed-
https://microsoft.github.io/AirSim/api_docs/html/


# ======== Settings ======== #
ref: https://microsoft.github.io/AirSim/settings/

If settings.json is modified, Unreal Engine (UE) should be reloaded. 
Method: 
    during running: click Stop button then Play
    other: restart UE

ViewMode setting has default value "" which translates to "FlyWithMe" for drones and "SpringArmChase" for cars.

No camera yet. Cameras need special settings

UAV position has errors

".join()" command in thread should be avoided, because a thread with this command interferes with other threads.

If drones are not operating smoothly, please decrease the number of drones or restart the computer. Otherwise, the code running could raise an error related to looping problem in Python packages.


# ======== Loop Frequency ======== #
10 UAVs
Plot in Airsim max frequency 1hz (1s)
getUAVsStatus max frequency 20hz (0.05s)


# ======== Airsim Interface ======== #
What's the function of yaw_mode in moveToPosition()???