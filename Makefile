# Compiler and flags
CXX := g++
CXXFLAGS := -Wall -Wextra -std=c++17 -Iinclude
LDFLAGS := -lcurl   # Link against libcurl

# Source files and target
SRC := src/main.cpp src/utils.cpp
OUT := live_bets 

# Build target
all: $(OUT)

$(OUT): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(OUT) $(LDFLAGS)

# Clean
clean:
	rm -f $(OUT)

