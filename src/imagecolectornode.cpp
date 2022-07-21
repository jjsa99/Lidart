/**
 * \file: main.c
 */

/**
 * \brief 
 * The objective of this file is to collect images from the stereo setup. It receives the trigger from the 
 */

// ROS
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
  
  flag_right = 0;

  // transforms msg back to image in mono8
  im_right = cv_bridge::toCvShare(msg, "mono8")->image;
  cv::waitKey(30);


  ROS_INFO("Initial Image: right_image received %d",counter2);
  std::string right_file = "/home/lidart/calibration_images/right/right_init.png";
  cv::imwrite(right_file,im_right);
  cv::waitKey(30);
    
  
}

void imageCallback_left(const sensor_msgs::ImageConstPtr& msg)
{

  flag_left = 0;

  im_left = cv_bridge::toCvShare(msg, "mono8")->image;
  cv::waitKey(30);

  ROS_INFO("Initial Image: left_image received %d",counter1);
  std::string left_file = "/home/lidart/calibration/left/left_init.png";
  cv::imwrite(left_file,im_left);
  cv::waitKey(30);


}


int main( int argc, char **argv)
{
    //initialize ROS
    ros::init(argc,argv,"Image collector Node");
    // Handler
    ros::NodeHandle nh;
    // initilize image transport
    image_transport::ImageTransport it(nh);
    // subscriber for right image
    image_transport::Subscriber sub_right = it.subscribe("/camera_right/image_raw_right", 1, imageCallback_right);
    // subscriber for left image
    image_transport::Subscriber sub_left  = it.subscribe("/camera_left/image_raw_left", 1, imageCallback_left);

    ros::spin()
}