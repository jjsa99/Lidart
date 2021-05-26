/**
 * \brief Find Centroid function - It scans throught the images and finds where the max intensity of light is. It can detect if it's noise or part of the centroid.
 * @param [in] data: data pointer
 * @param [in] centroidCoord : array with the coordinates of the centroid.
 */

int findCentroid(uint8_t *data, double centroidCoord[]);