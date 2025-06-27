#include "utils.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>

int dummy_task(int a) {
    std::cout << "Dummy Task, print args" << a << std::endl;
    return 0;
}

int add(int a, int b) {
    return a + b;
}

// Callback function to handle the response data, keep appending to the response string
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
    size_t totalSize = size * nmemb;
    response->append((char*)contents, totalSize);
    return totalSize;
}

// Function to read the API key from a configuration file
std::string read_api_key(const std::string& filename, const std::string& key) {
    std::ifstream file(filename);
    std::string line;
    while (getline(file, line)) {
        std::istringstream is_line(line);
        std::string k, v;
        if (getline(is_line, k, '=') && getline(is_line, v)) {
            if (k == key)
                return v;
        }
    }
    return ""; // Return empty if not found
}

void handle_response(const std::string& response, int call_number) {
    std::cout << "Call #" << call_number << " received response of size "
              << response.size() << " bytes.\n";
}