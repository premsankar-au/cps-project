cps-project
===========

A simulation of Tsunami Warning System

## Requirements
The `server.py` requires applications like  `python-2.7`, `sqlite3` 
and  `libsqlite3-dev to be installed on your machine.
```bash
sudo apt-get install sqlite3 libsqlite3-dev
```

## How to setup DB
```bash
./setup_server_db.sh
```

## How to run the server program
```bash
python server.py
```

## How to connect to the server
I assume that you are running the `server.py` in your local machine.
The `server.py` runs on port no `8888`. You could use either `telnet`
or `netcat` to connect to the server
```bash
nc localhost 8888
```
or
```bash
telnet localhost 8888
```

## How to run the sensor bouy program
A bouy program is written in-order to generate sensor data and enables
automatic submission.
```bash
python bouy.py
```

## TODO
- [x] Server program basic structure
- [x] Server program error handling
- [x] Client program basic structure
- [x] Client program error handling
- [x] Server program DB connectivity
- [x] Client program automatic dataset generation
- [ ] Processing of sensor bouy data in server
- [ ] Comparing the sensor given data with the previous sets of data in DB
- [ ] Reaching a conclusion of error type
- [ ] Seding alert message

