"""
    Server program of TWS
"""

import socket
import sys, errno
import sqlite3
from datetime import datetime, timedelta
import struct

# This program should return these values
# 1: generic error
# 2: network error
# 3: Low Alert
# 4: Regular/Periodical 
# 5: Medium Alert
# 6: High Alert

MAX_CLIENT_CON = 10     # The max no of clients which could connect to the server at a  time
HOST = ''               # Symbolic name meaning the local host
PORT = 8888             # Arbitrary non-privileged port

def handle_recv_error(e):    
    err = e.args[0]
    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
        sleep(1)
        print 'No data available'

    elif err == ENOTCONN:
        print 'Client disconnected'
    else:
        print e
        sys.exit(1)

def get_alert_type(pressure, ritcher):
    """
    Returns the alert type of given data
    """
    if (pressure > 95 and pressure < 104.99) and  \
        (ritcher > 0 and ritcher < 2.99):
        return 'regular'

    elif (pressure > 105 and pressure < 114.99) and  \
        (ritcher > 3 and ritcher < 3.99):
        return 'low alert'

    elif (pressure > 115 and pressure < 129.99) and  \
        (ritcher > 4 and ritcher < 5.99):
        return 'medium alert'

    elif (pressure > 130 and pressure < 170) and  \
        (ritcher > 5 and ritcher < 20):
        return 'high alert'


def process_data(bouyid, pressure, ritcher):
    """
    A function to process the bouy input
    """
    """
    TODO: Check if the current bouy input is within the regular range
    If not, we should compare it with the previous values in the DB to conclude
    what kind of alert it is
    """

def close_client(client, addr):
    """
    Closes client in a safe way
    """
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    print '[+] ' + str(addr[0]) + ':' + str(addr[1]) + ' disconnected!'

def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

def client_thread(client, addr):
    """
    Handles all the client requests
    """

    client.send('Welcome to TWS server\nEnter Bouy id: ')

    try:
        # Recieves bouy id
        bouy_id = int(client.recv(4))
        # If client enters an invalid bouy_id range
        if not (bouy_id > 0 and bouy_id < 5): 
            client.send('Invalid id')
            raise ValueError("Invalid id")

        # Recieves pressure
        reply = 'Welcome Bouy - ' + str(bouy_id) + \
                '.\nEnter the measured pressure (in kPa): '
        client.send(reply)
        pressure = float(client.recv(10))
        
        # Recieves Ritcher scale value
        reply = 'Enter the Ritcher (in R): '
        client.send(reply)
        ritcher = float(client.recv(10))

    except ValueError:
        print 'Invalid value'
        close_client(client, addr)
        return False

    except IOError, e:
        # If client disconnects 
        if e.errno == errno.EPIPE:
            print 'Connection closed by client'
        else:
            print 'Other errors'
        close_client(client, addr)
        return False


    
    try :
        db = sqlite3.connect("server.db")
        c = db.cursor()

        # Generating a time to be stored along with bouy details
        time = datetime.now()
        alert = get_alert_type(pressure, ritcher) 
        print 'Received ' + str(alert) + ' from bouy: ' + str(bouy_id)

        # Insert a row of data
        db.execute('INSERT into server_data values (NULL, ?, ?, ?, ?, ?)', (bouy_id, time, \
            pressure, ritcher, alert))

        # Save (commit) the changes
        db.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        db.close()
        
    except sqlite3.DatabaseError, e:
        print 'SQLite error: ' + str(e)
        close_client(client, addr)
        sys.exit(1)

    except IOError, e:
        print 'Error in connecting to db'
        close_client(client, addr)
        sys.exit(1)

    try:
        client.send("Data successully received by server\n")
    except IOError, e:
        # If client disconnects 
        if e.errno == errno.EPIPE:
            print 'Connection closed by client'
        else:
            print 'Other errors'
        close_client(client, addr)
        return False

    return True
 
def main():
    """
    Main function
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Server binding 
    try:
        sock.bind((HOST, PORT))

    except socket.error, msg:
        print '[-] Bind failed. Error code: ' + str(msg[0]) + \
            '.\n[WARNING]: ' + msg[1]
        sys.exit(1)
    
    set_keepalive_linux(sock)

    # Listens to the client sockets
    try:
        sock.listen(MAX_CLIENT_CON) 
   
    except socket.error, msg:
        print '[-] Listening failed. Error code: ' + str(msg[0]) + \
            '.\n[WARNING]: ' + msg[1]
        sys.exit(1)
        
    while True:
        # Wait to accept a connection 
        try:
            client, addr  = sock.accept()

        except KeyboardInterrupt:
            break
        
        except socket.error, msg:
            print 'Socket Error: ' + str(msg)
        
        print '[+] Connected with ' + str(addr[0]) + ':' + str(addr[1])

        # Start new thread takes 1st argument as a function name to be run, second is
        # the tuple of arguments to the function.
        if client_thread(client,addr) == True:
            close_client(client, addr)
           
   
    # Close the server sock if done
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

if __name__ == '__main__':
    main()
