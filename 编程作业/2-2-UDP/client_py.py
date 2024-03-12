import socket
import time
import struct
import sys

ping_time = 10


def ping(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((host, port))
    client_socket.settimeout(1.0)
    seq_num = 0
    rtt_list = []
    for i in range(ping_time):
        seq_num = seq_num+1
        send_time = time.time()
        ping_msg = f'Ping {i} {time.time()}'
        client_socket.sendall(ping_msg.encode())
        try:
            recv_msg, addr = client_socket.recvfrom(1024)
            rtt = (time.time() - send_time) * 1000
            rtt_list.append(rtt)
            print('Reply from', host, ':', ping_msg, 'RTT=', rtt, 'ms')
        except socket.timeout:
            print('request timed out')
    client_socket.close()
    packet_loss_rate = (ping_time - len(rtt_list))/ping_time * 100.0
    min_rtt = min(rtt_list)
    max_rtt = max(rtt_list)
    avg_rtt = sum(rtt_list)/len(rtt_list)
    print('Ping statistics for %s:' % host)
    print('    Packets: Sent = %d, Received = %d, Lost = %d (%.2f%% loss),' % (ping_time, len(rtt_list), ping_time - len(rtt_list), packet_loss_rate))
    print('Approximate round trip times in milli-seconds:')
    print('    Minimum = %.2fms, Maximum = %.2fms, Average = %.2fms' % (min_rtt, max_rtt, avg_rtt))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('The input is wrong')
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    ping(host, port)
