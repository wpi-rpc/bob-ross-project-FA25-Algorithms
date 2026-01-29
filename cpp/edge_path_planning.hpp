#ifndef EDGE_PATH_PLANNING
#define EDGE_PATH_PLANNING
#include <vector>
#include <array>
#include <algorithm>
#include <opencv2/opencv.hpp>

bool containsArray(const std::vector<std::array<int, 2>>& queue, const std::array<int, 2>& target);
std::vector<std::array<int, 2>> getNeighbors(std::array<int, 2>& pixel, cv::Mat &image);
std::vector<std::array<int, 2>> generateEdgeStreak(cv::Mat &image);
std::vector<std::vector<std::array<int, 2>>> edgePathCoordinates(cv::Mat &image);
std::vector<std::vector<std::array<int, 2>>> interpolate(std::vector<std::vector<std::array<int, 2>>> &path);

#endif