e// ROS
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <sensor_msgs/image_encodings.h>
#include <sensor_msgs/Image.h>
#include <cv_bridge/cv_bridge.h>
#include "std_msgs/String.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <std_msgs/Int8.h>
// library for the publisher array -> float64 means double in C++
#include <iostream>
#include <cmath>
#include <vector>
#include <string>

#include "geometry_msgs/Point.h"
#include "geometry_msgs/PoseArray.h"
#include "geometry_msgs/Pose.h"

using namespace std;
using namespace cv;

void imageCallback_right(const sensor_msgs::ImageConstPtr& msg)
{
    ROS_INFO("subscribed left image");

}
void imageCallback_left(const sensor_msgs::ImageConstPtr& msg)
{

    
    ROS_INFO("subscribed left image");

}
int main(int argc, char **argv)
{
 
  ros::init(argc, argv, "camera_subscriber");
  ros::NodeHandle nh;
  image_transport::ImageTransport it(nh);
  image_transport::Subscriber sub_right = it.subscribe("/camera_right/image_raw_right", 1, imageCallback_right);
  image_transport::Subscriber sub_left  = it.subscribe("/camera_left/image_raw_left", 1, imageCallback_left);

  ros::Rate loop_rate(1); 
  
  while(ros::ok())
  {
    ros::spinOnce();
    image_transport::Subscriber sub_right = it.subscribe("/camera_right/image_raw_right", 1, imageCallback_right);
    image_transport::Subscriber sub_left  = it.subscribe("/camera_left/image_raw_left", 1, imageCallback_left);

    loop_rate.sleep();
    }
  return 0;

}
