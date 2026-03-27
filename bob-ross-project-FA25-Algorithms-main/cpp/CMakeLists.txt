cmake_minimum_required(VERSION 3.10)
project(BobRoss)

find_package(OpenCV REQUIRED)
find_package(SFML 3 COMPONENTS Graphics Window System REQUIRED)

add_executable(BobRoss csv_write.cpp edge_path_planning.cpp)
target_link_libraries(BobRoss ${OpenCV_LIBS} SFML::Graphics SFML::Window SFML::System)