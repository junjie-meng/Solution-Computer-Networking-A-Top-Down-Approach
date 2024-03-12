import socket
import sys
import threading


class ClientThreading(threading.Thread):
    def __init__(self, connectionSocket, addr):
        threading.Thread.__init__(self)
        self.connectionSocket = connectionSocket
        self.addr = addr

    def run(self):
        try:
            message = self.connectionSocket.recv(4096)
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()
            header = header = 'HTTP/1.1 200 OK\nConnection: close\nConnect-Type: text/html\nConnect-Length: %d\n\n' %(len(outputdata))
            self.connectionSocket.send(header.encode())

            for i in range(0, len(outputdata)):
                self.connectionSocket.send(outputdata[i].encode())

            self.connectionSocket.close()

        except IOError:
            header = 'HTTP/1.1 404 Not Found'
            self.connectionSocket.send(header.encode())
            self.connectionSocket.close()


severSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
severSocket.bind(('localhost', 1234))
severSocket.listen(10)
count = 0

while True:
    print('The server is ready to receive')
    connection, addr = severSocket.accept()
    count = count + 1
    print('The receive time is ', count)
    newThread = ClientThreading(connection, addr)
    newThread.start()

severSocket.close()
sys.exit()
