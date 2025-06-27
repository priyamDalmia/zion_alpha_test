# Zion Alpha Test 

## Python Analysis 

1. Fetch historical odds from *https://www.aussportsbetting.com/data/*. Data is stored in `data/`.

### Setup 

1. create virutal env, install requirements 
   - `python3 -m venv .venv && source ./.venv/bin/activate`
   - `pip install -r py/requirements.txt`

2. Run code in `analysis.ipynb` 

### Analysis 

- Getting AFL data from 
```txt
Data from 2009-06-19 00:00:00 to 2025-06-22 00:00:00
Total matches: 3264
```

## C++ Notificaiton System

- This is a small C++ app that makes an HTTP request using `libcurl`.
- For API - Connection Pooling, and Rate Limits to 5 requests per minute.
- For latency - Requests are handled in a thread. 

### Setup

1. Install `libcurl`:
   - macOS: `brew install curl`

2. Create a `config.ini` file:
   - add `api_key`

### Running 

```bash
# Clean project 
make clean 

# Build project 
make 

# Run live notification system 
./live_bets
```
### Design Considerations 

Designing a low latency notificaiton system. 

1. Rate limits for APIs. 
   1. Additionally I could have - separate CURL* handles per thread or wrap shared ones with std::mutex.

2. Send notifications on a separate thread or coroutine to avoid blocking main logic.
   1. Additionally I could have - Worker threads pull from the queue and send notifications.