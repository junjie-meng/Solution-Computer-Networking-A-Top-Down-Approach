from socket import *
import os
import sys
import getopt
import struct
import time
import select
import binascii  

ICMP_ECHO_REQUEST = 8


def checksum(string): 
    csum = 0
    countTo = (len(string) // 2) * 2  
    count = 0

    while count < countTo:
        thisVal = string[count] * 256 + string[count+1]
        csum = csum + thisVal 
        csum = csum & 0xffffffff  
        count = count + 2
        
    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff 
        
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum 
    answer = answer & 0xffff 
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer 


def receiveOnePong(mySocket, destAddr, ID, sequence, timeout):
    timeLeft = timeout
    
    while 1: 
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        #print("howLongInSelect:", howLongInSelect)
        if whatReady[0] == []: # Timeout
            return None
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        #print("receive!")
        #Fill in start
        ip_header = recPacket[:20]
        ip_TTL = struct.unpack("!B", ip_header[8:9])[0]
        header = recPacket[20:28]
        icmpType, icmpCode, icmpChecksum, icmpId, icmpSequence = struct.unpack("!BBHHH", header)
        # print("the icmp id in receive: ", icmpId)
        # print("the id in receive: ", ID)
        icmp_length = len(recPacket[20:])
        #print(icmpType, icmpId, ID, icmpSequence, sequence)
        if icmpType == 0 and icmpId == ID and icmpSequence == sequence:
            return timeReceived, ip_TTL, icmp_length
        else:
            print("Error: ICMP Type {}, Code {}".format(icmpType, icmpCode))
            if icmpType == 3 and icmpCode == 0:
                print("Desitination Network Unreachable")
            elif icmpType == 3 and icmpCode == 1:
                print("Destination Host Unreachable")
            elif icmpType == 3 and icmpCode == 3:
                print("Destination Port Unreachable")
            elif icmpType == 3 and icmpCode == 6:
                print("Destination Network Unknown")
            elif icmpType == 3 and icmpCode == 7:
                print("Destination Network Unknown")
            elif icmpType == 4 and icmpCode == 0:
                print("Source Quench")
            elif icmpType == 8 and icmpCode == 0:
                print("Echo Request")
            elif icmpType == 9 and icmpCode == 0:
                print(" Route Advertisement")
            elif icmpType == 10 and icmpCode == 0:
                print("Route Discovery")
            elif icmpType == 11 and icmpCode == 0:
                print("Time-To-Live Exceeded")
            elif icmpType == 12 and icmpCode == 0:
                print("IP Header Corruption")
            return None

        #Fill in end
        
        timeLeft = timeLeft - howLongInSelect
        #print("error!")
        if timeLeft <= 0:
            return None


def sendOnePing(mySocket, destAddr, ID, sequence):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    data = struct.pack("!d", time.time())

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff         
    else:
        myChecksum = htons(myChecksum)
        
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    # print("the id in send :", ID)
    packet = header + data
    
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def doOnePing(destAddr, ID, sequence, timeout): 
    icmp = getprotobyname("icmp")

    # SOCK_RAW is a powerful socket type. For more details: 
    #http://sock-raw.org/papers/sock_raw
    #Fill in start
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    #Fill in end
        
    sendOnePing(mySocket, destAddr, ID, sequence)
    # print("the id in do one ping:", ID)
    rtt = receiveOnePong(mySocket, destAddr, ID, sequence, timeout)
    
    mySocket.close()
    return rtt
    
def ping(dest, count):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    timeout = 1

    myID = os.getpid() & 0xFFFF  # Return the current process i
    # print("The id in ping:", myID)
    loss = 0
    rtt_time = []
    # Send ping requests to a server separated by approximately one second
    for i in range(count) :
        # Here is different from original code
        rec = time.time()
        result = doOnePing(dest, myID, i, timeout)

        #Fill in start
        if result is None:
            print("Request timed out.")
            loss += 1
        else:
            rtt = (result[0] - rec) * 1000
            rtt_time.append(rtt)
            print("Reply from {}: bytes={} time={:.1f} ms TTL={}".format(dest, result[2], rtt, result[1]))

        #Fill in end

        time.sleep(1)# one second

    #Fill in start
    print("\nPing statistics for {}".format(dest))
    print("     Packets: Send = {}, Received = {}, Lost = {}({}% loss)".format(count, count - loss, loss,
                                                                               (loss/count)*100))
    if loss == count:
        return
    rtt_time.sort()
    print("     Max RTT = {:.2f} ms, Min RTT = {:.2f} ms,  Ave RTT={:.2f} ms".format(rtt_time[-1], rtt_time[0], sum(rtt_time)/count))

    #Fill in end

    return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('IcmpPing.py dest_host [-n <count>]')
        sys.exit()
    host = sys.argv[1]
    try:
        dest = gethostbyname(host)
    except:
        print('Can not find the host "%s". Please check your input, then try again.'%(host))
        exit()
    
    count = 4
    try:
        opts, args = getopt.getopt(sys.argv[2:], "n:")
    except getopt.GetoptError:
        print('IcmpPing.py dest_host [-n <count>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-n':
            count = int(arg)

    print("Pinging " + host + " [" + dest + "] using Python:")
    print("")
    ping(dest, count)
