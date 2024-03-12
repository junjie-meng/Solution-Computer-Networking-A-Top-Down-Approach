from socket import *
import base64

# Mail content
subject = "I love computer networks!"
contenttype = "text/plain"
msg = "I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.qq.com'  #Fill-in-start  #Fill-in-end

# Sender and reciever
fromaddress = '2441353190@qq.com'
toaddress = '2021010915001@std.uestc.edu.cn' #Fill-in-start  #Fill-in-end

# Auth information (Encode with base64)
username = base64.b64encode(fromaddress.encode()).decode()   #Fill-in-start  #Fill-in-end
password = base64.b64encode('eviqziwrffmydjfi'.encode()).decode() #Fill-in-start  #Fill-in-end

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill-in-start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))
#Fill-in-end

recv = clientSocket.recv(1024) .decode()
print(recv)

# Send HELO command and print server response.
#Fill-in-start
clientSocket.sendall('HELO smtp.qq.com\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
#Fill-in-end

# Send AUTH LOGIN command and print server response.
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.sendall((username + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.sendall((password + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)


# Send MAIL FROM command and print server response.
#Fill-in-start
clientSocket.sendall(('MAIL FROM:<'+fromaddress+'>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
#Fill-in-end

# Send RCPT TO command and print server response.
#Fill-in-start
clientSocket.sendall(('RCPT TO:<'+toaddress+'>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
#Fill-in-end

# Send DATA command and print server response.
#Fill-in-start
clientSocket.sendall('DATA\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
#Fill-in-end

# Send message data.
#Fill-in-start
clientSocket.sendall(('Subject:'+subject+'\r\n').encode())
clientSocket.sendall(('Content-Type:'+contenttype+'\r\n').encode())
clientSocket.sendall(('From:<'+fromaddress+'>\r\n').encode())
clientSocket.sendall(('To:<'+toaddress+'>\r\n').encode())
clientSocket.sendall(('\r\n'+msg+'\r\n').encode())
#Fill-in-end

# Message ends with a single period and print server response.
#Fill-in-start
clientSocket.sendall(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
#Fill-in-end

# Send QUIT command and print server response.
#Fill-in-start
clientSocket.sendall('QUIT\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
#Fill-in-end

# Close connection
clientSocket.close()
