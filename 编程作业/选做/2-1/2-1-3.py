import socket
import sys

server_address = sys.argv[1]
server_port = int(sys.argv[2])
filename = sys.argv[3]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((server_address, server_port))

request = f"GET {filename} HTTP/1.1\r\nHost: {server_address}\r\n\r\n"
sock.sendall(request.encode())

# Receive and print server response
response = sock.recv(4096)
while response:
    print(response.decode(), end="")
    response = sock.recv(4096)

# Close the socket
sock.close()
