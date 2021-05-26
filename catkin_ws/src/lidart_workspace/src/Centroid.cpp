#include "Centroid.h"

int findCentroid(uint8_t *data, double centroidCoord[]) {

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
