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

To run this seltup, it was used:
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
The cameras used come with proprietary software in order to connect them to the computer. I found a very usefull ROS package named ueye_cam from https://wiki.ros.org/ueye_cam . It creates the nodes for the cameras when connected.
```bash
git clone https://github.com/anqixu/ueye_cam.git
```

From there, we need to connect the mirror to the linux environment.
Originally, the software provived by the Optotune isn't compatible with LINUX.
With that, it was necessary to install the same libraries provided by the manufacture, but in LINUX, in this case:
- numpy 1.9.1
- pyserial 2.7
