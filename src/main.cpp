#include <iostream>
#include "utils.hpp"
#include <string>
#include <curl/curl.h>
#include <thread>


int main() {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    // Set rate limit for the API requests
    int callsMade = 0;
    const int maxCallsPerMinute = 20;
    const int intervalMs = 60000 / maxCallsPerMinute; // Calculate interval in milliseconds

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

    while (true) {

        readBuffer.clear(); // Clear the buffer for each new request
        // Set the URL for the request
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        // Set the buffer to write the response data into
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

        // Perform the request
        res = curl_easy_perform(curl);
        // Increment the call count
        callsMade++;
        // Check for errors in the request
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }
        else {
            // Launch response thread; caller side exception handling
            std::thread responseThread([readBuffer, callsMade]() {
                try {
                    handle_response(readBuffer, callsMade);
                } catch (const std::exception& e) {
                    std::cerr << "Exception in handle_response thread: " << e.what() << std::endl;
                } catch (...) {
                    std::cerr << "Unknown exception in handle_response thread." << std::endl;
                }
            });
            responseThread.detach();
        }

        // Check if the rate limit has been reached
        if (callsMade >= maxCallsPerMinute) {
            std::cout << "Rate limit reached. Waiting for 1 minute..." << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(60000)); // Wait for 1 minute
            callsMade = 0; // Reset the call count after waiting
        } else {
            // Wait for the specified interval before making the next request
            std::this_thread::sleep_for(std::chrono::milliseconds(intervalMs));
        }
    }
    // Cleanup
    curl_easy_cleanup(curl);
    curl_global_cleanup();

}