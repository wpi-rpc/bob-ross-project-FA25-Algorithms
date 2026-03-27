#ifndef PATH_VISUALIZER_HPP
#define PATH_VISUALIZER_HPP

#include <SFML/Graphics.hpp>
#include <vector>
#include <array>

class PathVisualizer {
public:
    PathVisualizer(int width, int height) 
        : window(sf::VideoMode({static_cast<unsigned int>(width), static_cast<unsigned int>(height)}), "Bob Ross Path Visualizer"),
          animationSpeed(0.05f),
          currentPathIndex(0),
          currentPointIndex(0),
          animationProgress(0.0f) {
        window.setFramerateLimit(60);
    }
    
    void drawPaths(const std::vector<std::vector<std::array<int, 2>>>& paths) {
        this->paths = paths;
        currentPathIndex = 0;
        currentPointIndex = 0;
        animationProgress = 0.0f;
    }
    
    void update() {
        window.clear(sf::Color::White);
        
        if (paths.empty()) {
            window.display();
            return;
        }
        
        sf::Color colors[] = {sf::Color::Red, sf::Color::Blue, sf::Color::Green, 
                             sf::Color::Yellow, sf::Color::Magenta, sf::Color::Cyan};
        
        // Draw completed paths
        for (size_t i = 0; i < currentPathIndex; i++) {
            const auto& path = paths[i];
            for (size_t j = 1; j < path.size(); j++) {
                sf::VertexArray line(sf::PrimitiveType::LineStrip, 2);
                line[0].position = sf::Vector2f(path[j-1][1], path[j-1][0]);
                line[0].color = colors[i % 6];
                line[1].position = sf::Vector2f(path[j][1], path[j][0]);
                line[1].color = colors[i % 6];
                window.draw(line);
            }
        }
        
        // Draw current path being animated
        if (currentPathIndex < paths.size()) {
            const auto& currentPath = paths[currentPathIndex];
            for (size_t j = 1; j < currentPointIndex; j++) {
                sf::VertexArray line(sf::PrimitiveType::LineStrip, 2);
                line[0].position = sf::Vector2f(currentPath[j-1][1], currentPath[j-1][0]);
                line[0].color = colors[currentPathIndex % 6];
                line[1].position = sf::Vector2f(currentPath[j][1], currentPath[j][0]);
                line[1].color = colors[currentPathIndex % 6];
                window.draw(line);
            }
            
            // Draw line to current point with interpolation
            if (currentPointIndex < currentPath.size()) {
                sf::VertexArray line(sf::PrimitiveType::LineStrip, 2);
                line[0].position = sf::Vector2f(currentPath[currentPointIndex-1][1], currentPath[currentPointIndex-1][0]);
                line[0].color = colors[currentPathIndex % 6];
                line[1].position = sf::Vector2f(currentPath[currentPointIndex][1], currentPath[currentPointIndex][0]);
                line[1].color = colors[currentPathIndex % 6];
                window.draw(line);
            }
            
            // Animate to next point
            animationProgress += animationSpeed;
            if (animationProgress >= 1.0f) {
                animationProgress = 0.0f;
                currentPointIndex++;
                
                if (currentPointIndex >= currentPath.size()) {
                    currentPointIndex = 0;
                    currentPathIndex++;
                }
            }
        }
        
        window.display();
    }
    
    bool isOpen() { return window.isOpen(); }
    
    void handleEvents() {
        while (auto event = window.pollEvent()) {
            if (event->is<sf::Event::Closed>()) {
                window.close();
            } else if (event->is<sf::Event::KeyPressed>()) {
                const auto& keyEvent = event->getIf<sf::Event::KeyPressed>();
                if (keyEvent && keyEvent->code == sf::Keyboard::Key::Space) {
                    // Reset animation
                    currentPathIndex = 0;
                    currentPointIndex = 0;
                    animationProgress = 0.0f;
                } else if (keyEvent && keyEvent->code == sf::Keyboard::Key::Up) {
                    animationSpeed = std::min(animationSpeed + 0.01f, 0.2f);
                } else if (keyEvent && keyEvent->code == sf::Keyboard::Key::Down) {
                    animationSpeed = std::max(animationSpeed - 0.01f, 0.01f);
                }
            }
        }
    }

private:
    sf::RenderWindow window;
    std::vector<std::vector<std::array<int, 2>>> paths;
    float animationSpeed;
    size_t currentPathIndex;
    size_t currentPointIndex;
    float animationProgress;
};

#endif
