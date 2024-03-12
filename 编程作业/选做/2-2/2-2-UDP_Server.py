from socket import *
import random
import time

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('localhost', 1234))
time_rec = 0
serverSocket.settimeout(2)

while True:
    time_now = time.time()
    try:
        msg, add = serverSocket.recvfrom(1024)
        msg = msg.upper()
        serverSocket.sendto(msg, add)
        time_rec = time.time()
    except timeout:
        print("The app shuts down")
    print(time_now - time_rec)
