#include <iostream>
#include "edge_path_planning.hpp"

int main() {
    cv::Mat img = cv::imread("../../images/circles.jpg", cv::IMREAD_GRAYSCALE);
    if (img.empty()) return -1;
    cv::Mat blur, edges;
 
    // Apply Gaussian blur
    cv::GaussianBlur(img, blur, cv::Size(5, 5), 1.4);
 
    // Apply Canny Edge Detector
    cv::Canny(blur, edges, 100, 200);
 
    // Display result
    cv::imshow("Canny Edge Detection", edges);
 
    cv::waitKey(0);
    return 0;
}