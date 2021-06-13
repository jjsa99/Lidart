# LiDART
(Light Detection And ranging using Triangulation)

This project was created within the academic space, thus it is considered as EXPERIMENTAL code.




## Setup details

To run this seltup, it was used:
- Linux 20.04 LTS
- ROS based system(noetic version)
- Cameras : IDS imaging UI-3260CP-M/C in stereo configuration
- Mirror: Optotune MR 15-30
- Laser : Thorlabs - HL6738MG
- Trigger: in-house developed system with a pulse with 100us
- Camera baseline: 0.5 meters
- 


### Installation
Since the setup was run in ROS, I used ROS noetic.
The cameras used come with proprietary software in order to connect them to the computer. I found a very usefull ROS package named ueye_cam from https://wiki.ros.org/ueye_cam . It creates two nodes for the cameras when connected.
```bash
git clone https://github.com/anqixu/ueye_cam.git
```

From there, we need to connect the mirror to the linux environment
