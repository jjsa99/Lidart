# LiDART
(Light Detection And ranging using Triangulation)

This project was created within the academic space, thus it is considered as EXPERIMENTAL code.
This program intends to obtain a point-cloud of the surrounding using triangulation.

## Programs
The Project is divided in two main programs:
- LiDART (main)
- Point generator (branch coord_generator)

LiDART is capable of displaying in the GUI the point-cloud while the point-generator was the funtionality of solely outputing the point coordinates to a .txt file.

## Setup details

To run this setup, it was used:
- Linux 20.04 LTS
- ROS based system(noetic version)
- Cameras : IDS imaging UI-3260CP-M/C in stereo configuration
- Mirror: Optotune MR 15-30
- Laser : Thorlabs - HL6738MG
- Trigger: in-house developed system with a pulse with 100us
- Camera baseline: 0.5 meters

![image](https://user-images.githubusercontent.com/30303154/121823562-efcc2f80-cc9d-11eb-9024-7dd0c1fa2079.png)

### Setup explanation
In the GUI, the user inputs:
- Horizontal FoV
- Vertical FoV
- Horizontal step
- Vertical step
- Horizontal offset
- Vertical offset

(The last 2 can be set to 0)


The cameras and the laser are sincronzed by a trigger. When pressed, the laser emits a laser spot that is captured by the cameras. The mirror will redirect the laser spot to the different coordinates.
The photos will be collected and processed in the PPUnit.cpp that will output the an Z,Y,Z coordinate.

### Installation
Since the setup was run in ROS, I used ROS noetic.
It is necessary to install OpenCV https://opencv.org/ .

The cameras used come with proprietary software in order to connect them to the computer. I found a very usefull ROS package named ueye_cam from https://wiki.ros.org/ueye_cam . It creates the nodes for the cameras when connected.
```bash
git clone https://github.com/anqixu/ueye_cam.git
```
From there, we need to connect the mirror to the linux environment.
Originally, the software provived by the Optotune isn't compatible with LINUX.
With that, it was necessary to install the same libraries provided by the manufacture, but in LINUX, in this case:
- numpy 1.9.1
- pyserial 2.7

The simpler way to install the code on your computer is to setup a ROS environment using https://wiki.ros.org/ROS/Installation
Then, after that, create a package using
``` bash
catkin_create_pkg nameofthepackage std_msgs rospy roscpp sensor_msgs image_transport cv_bridge
```
Then import the folders inside the git /src to the src created in the ROS package.
Finally add to the CMakeList.txt
``` bash
add_executable (PPUnit src/PPUnit.cpp)
target_link_libaries(PPUnit ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})

add_executable (camera_subscriber src/camera_subscriber_test.cpp)
target_link_libaries(PPUnit ${catkin_LIBRARIES})

```

## How to run the setup


### Run the cameras
In order to run the cameras it is necessary to use the third party library created by anqixu(https://github.com/anqixu/).
When opening the repo, the path is :
``` bash
~/catkin_ws/src/ueye_cam/launch/
```
In order to trigger to cameras with the specs used in this project, it was created two launch files for this purpose:
- stereo_cameras_no_trigger.launch
- stereo_cameras_trigger.launch

Depending on which application the user wants to use the setup(having an external trigger to actuate both cameras at the same time(....trigger.launch) or other application where the trigger isn't important(...._no_trigger.launch)).

To launch either file:
``` bash
roslaunch ueye_cam stereo_cameras_trigger.launch
```

**Possible error and solutions:**
- It might be useful to have the ids manager application installed. Despite not being used, it is possible to quickly check whether a camera is being identified by the computer.
- These cameras require a higher voltage than normal USB devices. If your computer doesn't recognized the cameras it is possible that 2 things are happening:
    - The IDS driver isn't installed
    - The USB power the computer is supplying isn't enough
        - For this reason it is necessary to have a USB hub that can be powered externally.


