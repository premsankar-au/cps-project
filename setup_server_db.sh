#/bin/bashi
sqlite3 server.db "create table server_data(id INTEGER PRIMARY KEY AUTOINCREMENT, bouy_id INTEGER NOT NULL, time CHARACTER(32) NOT NULL, pressure INTEGER NOT NULL, ritcher FLOAT NOT NULL, alert TEXT NOT NULL);"
