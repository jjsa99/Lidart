////////////////
// alteraçoes nas linhas 171, 172, 173 e 189, 190
////////////////


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

double cRightPh[2];                                 //Array for the centroid coordinates of the right photo
double cLeftPh[2];                                  //Array for the centroid coordinates of the left photo
cv::Mat im_right;
cv::Mat im_left;
int flag_right = 0;
int flag_left = 0;
int size_n = 0;                                    //inicialization of the variable for the size of the array

std::vector <geometry_msgs::Point> coord;
// geometry_msgs::Pose point;
geometry_msgs::Point point;

int findCentroid(uint8_t *data, double centroidCoord[]);

int findSpotCoordinates(double cRightPh[2],double cLeftPh[2]) {


    double pixel = 5.86*pow(10, -6);                    //Size of a pixel

    cLeftPh[0] = -(cLeftPh[0]-1936/2)*pixel;            //The coordinates of the centroid must be moved to a frame of reference where the origin is in the center of the photo
    cLeftPh[1] = (cLeftPh[1]-1216/2)*pixel;            //Then, each coordinate is multiplied by the pixel size, in order to obtain its real position on the sensor
    cRightPh[0] = -(cRightPh[0]-1936/2)*pixel;
    cRightPh[1] = (cRightPh[1]-1216/2)*pixel;


    double fl = 16*pow(10, -3);                         //Focal distance
    double d = 0.5;                                     //Distance between the cameras


    double Yph = (cLeftPh[1] + cRightPh[1])/2;          //Ideally, the y-coordinates of the centroids should be the same. However, this is not what happens. Thus, we calculated the average of the two y-coordinates of the centroids.

    double z = d*fl/(cRightPh[0]-cLeftPh[0]);           //Obtaining the laser spot coordinates by using the equations derived by the Dashboard team
    double x = -cLeftPh[0]*z/fl;
    double y = -Yph*z/fl;

     cout << "Z:" << z << endl;
     cout << "X:" << x << endl;
     cout << "Y:" << y << endl;

    // geometry_msgs::Pose point;



    // point.position.x = x;
    // point.position.y = y;
    // point.position.z = z;

    point.x = x;
    point.y = y;
    point.z = z;

    // // spotCoord.pose.push_back(point);
    // // spotCoord.position.x = x;
    // // spotCoord.position.y = y;
    // // spotCoord.position.z = z;

    coord.push_back(point);


	return 0;
}
//callback Size
void sizeCallBack(const std_msgs::Int8::ConstPtr& size)
// não será necessário declarar o size_n como global?
{

  size_n = size->data;
	printf("%d size :",size_n);

	return;
}
int counter2 =0;
void imageCallback_right(const sensor_msgs::ImageConstPtr& msg)
{

  flag_right = 0;
  try
  {
    im_right = cv_bridge::toCvShare(msg, "mono8")->image;
    cv::waitKey(30);
    ROS_INFO("right_image received %d",counter2);
    findCentroid(im_right.data, cRightPh);
    flag_right = 1;
    cout << flag_right << '\n';

  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
  }
  counter2++;
}

int counter1 =0;
void imageCallback_left(const sensor_msgs::ImageConstPtr& msg)
{

  flag_left = 0;
  try
  {
    im_left = cv_bridge::toCvShare(msg, "mono8")->image;
    cv::waitKey(30);
    ROS_INFO("left_image received %d",counter1);
    findCentroid(im_left.data, cLeftPh);
    //cout << "sent left" << '\n';
    flag_left = 1;
    cout << flag_left << '\n';

  }

  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
  }
  counter1++;

}

void call_Quit(const std_msgs::Int8::ConstPtr& msg_quit){
  ros::shutdown();
}

int volatile a = 0;

 int main(int argc, char **argv)
{
  int n = 6;
  int count = 0;
  ros::init(argc, argv, "subscriber_node");
  ros::NodeHandle nh;
  image_transport::ImageTransport it(nh);
  image_transport::Subscriber sub_right = it.subscribe("/camera_right/image_raw_right", 1, imageCallback_right);
  // ROS_INFO("Subscribed right topic");
  image_transport::Subscriber sub_left  = it.subscribe("/camera_left/image_raw_left", 1, imageCallback_left);
  // ROS_INFO("Subscribed left topic");
  ros::Subscriber subQuit = nh.subscribe("Quit", 10, call_Quit);
  // ROS_INFO("Subscribed the subQuit topic");
  // publishes the coordinates
  ros::Publisher pub = nh.advertise<geometry_msgs::Point>("Coordinates",10);
  // ROS_INFO("Publishing the coordinates");
  // subscribes the size of the array
  ros::Subscriber sub = nh.subscribe("size",100,sizeCallBack);
  // ROS_INFO("subscribed the size topic");

  ////////////////
  ros::Publisher pub_photoready1 = nh.advertise<std_msgs::Int8>("Photo_Ready1", 100);
  ros::Publisher pub_photoready2 = nh.advertise<std_msgs::Int8>("Photo_Ready2", 100);
  std_msgs::Int8 pub_flag;
  pub_flag.data = 1;
  ////////////////

  ros::Rate loop_rate(1);
  ros::spinOnce();

  double spotCoord[n][3];

  while(ros::ok())
  {
    ros::spinOnce();

    if(flag_right == 1 && flag_left == 1)
    {

      ////////////////
      ROS_INFO("FLAG");
      pub_photoready1.publish(pub_flag);
      printf("published the photoReady 1\n");
      pub_photoready2.publish(pub_flag);
      printf("published the photoReady 2\n");
      ////////////////

      findSpotCoordinates(cRightPh,cLeftPh);
      ROS_INFO("finding spot Coordinates");
      pub.publish(point);
      printf("published the point");

      flag_right = 0;
      flag_left = 0;
      ROS_INFO("%d",a);
      a = a+1;
    }


  loop_rate.sleep();
  }
  return 0;
}


int findCentroid(uint8_t *data, double centroidCoord[]) {

    ROS_INFO("find_centroid function()");
    int k = 0;                              //Variable to iterate over data

    int width = 1936;                       //width = 1936
    int height = 1216;                      //height = 1216

    int n = 50;                             //Auxiliary arrays to calculate the weigthed average of the centroid
    double lines[n] = {0};                  //Auxiliary array for lines
    double cols[n] = {0};                   //Auxiliary array for collums
    int l = 0;                              //Variable to iterate over lines[]
    int c = 0;                              //Variable to iterate over cols[]

    int count = 0;                          //Counting variable
    int count2 = 0;                         //Counting variable

    int begCol = width;                     //Index of left collum that delimits the centroid. This value is not its end value.
    int endCol = 0;                         //Index of right collum that delimits the centroid. This value is not its end value.
    int begLine;                            //Index of top line that delimits the centroid.
    int endLine;                            //Index of bottom line that delimits the centroid.

    int inSpot = 0;                         //Variable that indicates if one is inside the centroid
    int foundSpot = 0;                      //Variable that indicates if the centroid has been found
                                            //It is possible that centroid has been found but, in the current iteration, one is not inside of it.
                                            //These two variables were created out of the need of making this distinction.



    ////////////////////////////////////////////////////
    //Cycle to find the X-coordinate of the centroid
    ////////////////////////////////////////////////////

    for(int i = 0; i < height ; i++) {

        if(count2 > width) {                //This condition is verified after no iluminated pixel is found in a whole line, after the centroid has been found.
            endLine = i;                    //The bottom line of the centroid has been found and registered.
            break;                          //The for cycle can end, as all the relevant information about the centroid has been retrieved.
        }

        for (int j = 0; j < width; j++) {

            k = i * width + j; 

            if(data[k] == 255) {            //A pixel with the maximum intensity value has been found. It can be the centroid or just noise.

                if(~inSpot) {               //In case we are not inside the centroid (~inSpot)


                    inSpot = ((data[k+1] == 255) | (data[k+width] == 255) | (data[k-width] == 255));        //Checking if it's noise or we have found the centroid.

                    if(~foundSpot & inSpot) {           //In case one hadn't previosuly been inside the centroid (~foundSpot) and is now inside the centroid (inSpot)
                        begLine = i;                    //The current line is the top line that delimits the centroid.
                        foundSpot = 1;                  //The centroid has been found!
                    }
                }

                if(inSpot) {                            //If we are inside the centroid (inSpot)
                    lines[l] += j;                      //These values will later be used to calculate the value of the midpoint of the current line.
                    count++;

                    if(j < begCol)                      //If the current collum is the collum more to the left of the centroid that has been found
                        begCol = j;                     //she becomes the new potential collum that delimits the centroid from the left.
                }
            }

            else {                                      //If the current pixel isn't iluminated
                if(inSpot) {                            //If we were inside the spot (inSpot), this means that the previous pixel was the last pixel of the current line of the centroid

                    if(j > endCol)                      //If the current collum is the collum more to the right of the centroid that has been found
                        endCol = j;                     //she becomes the new potential collum that delimits the centroid from the right.

                    lines[l] = lines[l]/count;          //The value of the midpoint of this line
                    i++;                                //Because the centroid has ended in the current line, we can move on to the next line
                    j = -1;                             //Goes back to collum 0 (the j variable will be incremented in the next iteration due to the for cycle).
                    l++;                                //Move on the next element of lines[]
                    count = 0;                          //Reset this variable
                    inSpot = 0;                         //We are no longer inside the centroid
                    count2 = 0;                         //Reset this variable
                }

                else if(foundSpot)                      //This variable starts to be incremented after the spot has been found (foundSpot).
                    count2++;                           //If for a whole line no iluminated pixel is found (count2 > width), we have finished the centroid
            }
        }
    }

    double sum = 0;
    count = 0;

    for(l = 0; lines[l] != 0; l++) {                    //For each line of the centroid, a midpoint value was found
        sum += lines[l];                                //This cycle finds the average of the midpoints, thus obtaining the x-coordinate of the centroid.
        count++;
    }

    double x = sum/count;                               //X-coordinate of the centroid


    ////////////////////////////////////////////////////
    //Cycle to find the Y-coordinate of the centroid
    ////////////////////////////////////////////////////

    //Now that we have found the limits of the centroid
    //we only have to iterate inside those limits (begCol, endCol, begLine, endLine).

    count = 0;                                      //Reset of the variable count

    for(int j = begCol; j < endCol; j++) {
        for (int i = begLine; i < endLine; i++) {

            k = i * width + j;

            if(data[k] == 255) {                    //An iluminated pixel was found

                if(~inSpot)
                    inSpot = ((data[k+1] == 255) | (data[k+width] == 255) | (data[k-1] == 255));        //Check if it's noise

                if(inSpot) {
                    cols[c] += i;
                    count++;
                }
            }

            else {
                if(inSpot) {                        //In the current collum, there is no more centroid. We can move on to the next collum.
                    cols[c] = cols[c]/count;
                    j++;
                    i = begLine-1;
                    c++;
                    count = 0;
                    inSpot = 0;
                }
            }
        }
    }


    sum = 0;
    count = 0;

    for(c = 0; cols[c] != 0; c++) {                //For each collum of the centroid, a midpoint value was found
        sum += cols[c];                            //This cycle finds the average of the midpoints, thus obtaining the y-coordinate of the centroid.
        count++;
    }

    double y = sum/count;                           //Y-coordinate of the centroid


    //cout << "Coordenada x: " << x << endl;
    //cout << "Coordenada y: " << y << endl;

    centroidCoord[0] = x;
    centroidCoord[1] = y;

    return 0;

}
