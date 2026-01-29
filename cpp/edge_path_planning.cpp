#include "edge_path_planning.hpp"

std::vector<std::vector<std::array<int, 2>>> edgePathCoordinates(cv::Mat &image) {
    std::vector<std::vector<std::array<int, 2>>> path;
    std::vector<std::array<int, 2>> streak = generateEdgeStreak(image);
    while (streak.size() > 0) {
        if (streak.size() > 2) {
            path.push_back(streak);
        }
        streak = generateEdgeStreak(image);
    }

    return interpolate(path);
}

std::vector<std::array<int, 2>> generateEdgeStreak(cv::Mat &image) {
    std::vector<std::array<int, 2>> streak;
    std::array<int, 2> current;
    for (int j = 0; j < image.rows; j++) {
        for (int i = 0; i < image.cols; i++) {
            if (image.at<unsigned char>(j, i) == 255) {
                current = {j, i};
                j = image.rows;
                break;
            }
        }
    }

    while (current != nullptr) {
        std::array<int, 2> current = queue.pop_front();
        if (image.at<unsigned char>(current[1], current[0]) == 255) {
            image.at<unsigned char>(current[1], current[0]) = 128;
            streak.push_back(current);

            std::vector<std::array<int, 2>> neighbors = getNeighbors(current, image);

            if (neighbors.size() > 0 && !containsArray(streak, neighbors[0])) {
                current = neighbors[0];
            } else if (neighbors.size() == 0) {
                break;
            }
        }
    }

    return streak;
}

// Returns all white pixel neighbors of a given pixel
std::vector<std::array<int, 2>> getNeighbors(std::array<int, 2>& pixel, cv::Mat &image) {
    std::vector<std::array<int, 2>> neighbors;
    int x = pixel[0]; int y = pixel[1];

    // Neighborws Below pixel 
    if (y > 0) {
        if (image.at<unsigned char>(y-1, x) == 255) {
            std::array<int, 2> newNeighbor = {x, y - 1};
            neighbors.push_back(newNeighbor);
        }
        if (x > 0 && image.at<unsigned char>(y-1, x-1) == 255) {
            std::array<int, 2> newNeighbor = {x - 1, y - 1};
            neighbors.push_back(newNeighbor);
        }
        if (x < image.cols - 1 && image.at<unsigned char>(y-1, x+1) == 255) {
            std::array<int, 2> newNeighbor = {x + 1, y - 1};
            neighbors.push_back(newNeighbor);
        }
    }
    // Neighbors above pixel
    if (y < image.rows - 1) {
        if (image.at<unsigned char>(y+1, x) == 255) {
            std::array<int, 2> newNeighbor = {x, y + 1};
            neighbors.push_back(newNeighbor);
        }
        if (x > 0 && image.at<unsigned char>(y+1, x-1) == 255) {
            std::array<int, 2> newNeighbor = {x - 1, y + 1};
            neighbors.push_back(newNeighbor);
        }
        if (x < image.cols - 1 && image.at<unsigned char>(y+1, x+1) == 255) {
            std::array<int, 2> newNeighbor = {x + 1, y + 1};
            neighbors.push_back(newNeighbor);
        }
    }
    // Neighbors to the sides of pixel
    if (x > 0 && image.at<unsigned char>(y, x-1) == 255) {
        std::array<int, 2> newNeighbor = {x - 1, y};
        neighbors.push_back(newNeighbor);
    }
    if (x < image.cols - 1 image.at<unsigned char>(y, x+1) == 255) {
        std::array<int, 2> newNeighbor = {x + 1, y};
        neighbors.push_back(newNeighbor);
    }

    return neighbors;
}

bool containsArray(const std::vector<std::array<int, 2>>& streak, const std::array<int, 2>& target) {
    auto it = std::find(streak.begin(), streak.end(), target);
    return it != queue.end();
}

std::vector<std::vector<std::array<int, 2>>> interpolate(std::vector<std::vector<std::array<int, 2>>> &path) {
    std::vector<std::vector<std::array<int, 2>>> new_path;
    for (int i = 0; i < path.size(); i++) {
        std::vector<std::array<int, 2>> new_streak;
        std::array<int, 2> previous_point = path[i][0];
        new_streak.push_back(previous_point);
        for (int j = 0; j < path[i].size(); j++) {
            std::array<int, 2> point = {path[i][j][0], path[i][j][1]};
            if ((((point[0] - previous_point[0]) * (point[0] - previous_point[0])) +
                ((point[1] - previous_point[1]) * (point[1] - previous_point[1]))) > 10) {
                new_streak.push_back(point);
                previous_point = point;
            }
        }
        new_path.push_back(new_streak);
    }
    return new_path;
} 