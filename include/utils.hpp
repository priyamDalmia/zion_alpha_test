#pragma once
#include <string>

// Callback function for libcurl to write response data
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response);
std::string read_api_key(const std::string& filename, const std::string& key);
void handle_response(const std::string& response, int call_number);
int dummy_task(int a);
int add(int a, int b);
