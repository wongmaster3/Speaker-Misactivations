import argparse
from scapy.all import *


parser = argparse.ArgumentParser(description='Convert pcap file to csv of times and packet size')
parser.add_argument('fromfile', help='pcap filename')
parser.add_argument('--ip', help='ip address of device')


def all_packets(config):
    output_filename = config.fromfile.rpartition('.')[0] + '.csv'
    output = open(output_filename, 'w', buffering=1)
    output.write('time,size\n')
    
    for packet in rdpcap(config.fromfile):
        if not IP in packet:
            continue
        if packet[IP].src != config.ip and packet[IP].dst != config.ip:
            continue
        output.write(f'{packet.time},{len(packet)}\n')
    
    output.close()


all_packets(parser.parse_args())
