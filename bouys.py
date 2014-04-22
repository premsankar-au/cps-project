import sys, errno
import socket
import sqlite3
import os 
import random
import time 

SERVER_PORT = 8888
HOST = ''

def gen_rand_type ():
    """
    Generates a type
    """
    list = ['regular', 'low alert', 'medium alert', 'high alert']
    i = random.randint(0, 3)
    return list[i]

def generate_data(type):
    """
    Generates a data
    """
    # Generates a regular data set
    if type.lower() == 'regular':
        pressure = random.uniform(95, 104.99)
        ritcher = random.uniform(0, 2.99)

    # Generates a low alert data set
    elif type.lower() == 'low alert':
        pressure = random.uniform(105, 114.99)
        ritcher = random.uniform(3, 3.99)
    
    # Generates a medium alert data set
    elif type.lower() == 'medium alert':
        pressure = random.uniform(115,129.99)
        ritcher = random.uniform(4, 5.99)

    # Generates a high alert data set
    elif type.lower() == 'high alert':
        pressure = random.uniform(130, 170)
        ritcher = random.uniform(6, 20)

    return ("{0:.2f}".format(pressure), "{0:.2f}".format(ritcher))
    
def send_info(sock, num):
    """
    Sends information to the server
    """
    try:
        sock.recv(37)
        print 'Bouy id: ' + str(num)
        sock.send(str(num) + '\n')

        type = gen_rand_type()
        pressure, ritcher = generate_data(type)

        sock.recv(56)
        print 'Pressure: ' + str(pressure)
        sock.send(str(pressure) + '\n')

        sock.recv(26)
        print 'Ritcher: ' + str(ritcher)
        sock.send(str(ritcher) + '\n')
        
        print sock.recv(36)
    except IOError, e:
        if e.errno == errno.EPIPE:
            print 'Server shutdown'
        else:
            print 'Socket error: ' + str(e)
        sock.close()

def main():
    """
    Main function
    """
    try:
        i=0
        j=0
        while i < 30:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((HOST, SERVER_PORT))
            send_info(sock, ((j % 4) + 1))
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            i = i + 1
            if j % 4 == 0:
                j = 1;
            else:
                j = j + 1
            time.sleep(2)
    except socket.error, msg:
        print '[-] Connection failed. Error code: ' + str(msg[0]) + '\n[WARNING]: ' + msg[1]
        sys.exit(1)

if __name__ == '__main__':
    main()
