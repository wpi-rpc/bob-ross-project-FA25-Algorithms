#include <iostream>
#include "edge_path_planning.hpp"
#include "path_visualizer.hpp"

int main(int argc, char** argv) {
    cv::Mat img = cv::imread("../../images/circles.jpg", cv::IMREAD_GRAYSCALE);
    if (img.empty()) {
        std::cerr << "Could not load image" << std::endl;
        return -1;
    }

    std::cout << "Image loaded: " << img.cols << "x" << img.rows << std::endl;

    cv::Mat blur, edges;

    // Apply Gaussian blur
    cv::GaussianBlur(img, blur, cv::Size(5, 5), 1.4);

    // Apply Canny Edge Detector with lower thresholds
    cv::Canny(blur, edges, 50, 150);

    // Save edge detection result for inspection
    cv::imwrite("edges.png", edges);

    // Count white pixels (edges)
    int edgeCount = cv::countNonZero(edges);
    std::cout << "Detected edges: " << edgeCount << " pixels" << std::endl;

    // Generate paths from edges
    std::vector<std::vector<std::array<int, 2>>> paths = edgePathCoordinates(edges);

    std::cout << "Generated " << paths.size() << " paths" << std::endl;
    for (size_t i = 0; i < paths.size(); i++) {
        std::cout << "Path " << i << ": " << paths[i].size() << " points" << std::endl;
    }

    // If run with --headless, skip opening SFML window (useful for CI/inspection)
    bool headless = false;
    if (argc > 1 && std::string(argv[1]) == "--headless") headless = true;

    if (!headless) {
        // Visualize with SFML
        PathVisualizer visualizer(edges.cols, edges.rows);
        visualizer.drawPaths(paths);

        while (visualizer.isOpen()) {
            visualizer.update();
            visualizer.handleEvents();
        }
    }

    return 0;
}