#include <iostream>
#include "utils.hpp"
#include <string>
#include <curl/curl.h>
#include <thread>


int main() {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    std::string api_key = read_api_key("config.ini", "API_KEY");
    if (api_key.empty()) {
        std::cerr << "API key not found!" << std::endl;
        return 1;
    }
    // std::cout << "API Key: " << api_key << std::endl;

    // Initialize CURL
    const std::string url = "https://api.the-odds-api.com/v4/sports?apiKey=" + api_key;

    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (!curl) {
        std::cerr << "Failed to initialize curl." << std::endl;
        curl_global_cleanup(); // Cleanup global resources if curl initialization fails
        return 1; // Exit if curl initialization fails
    }

    // Set the callback function to handle the response data, resused for all
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);

    readBuffer.clear(); // Clear the buffer for each new request
    // Set the URL for the request
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    // Set the buffer to write the response data into
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

    // Perform the request
    res = curl_easy_perform(curl);
    
    // Check for errors in the request
    if (res != CURLE_OK) {
        std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
    }
    else {
        // Print the response data
        std::cout << "Response data: " << readBuffer << std::endl;
    }

    // Cleanup
    curl_easy_cleanup(curl);
    curl_global_cleanup();

}