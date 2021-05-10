import argparse
from scapy.all import *
import os
import simplejson as json

parser = argparse.ArgumentParser(description='Convert pcap file to csv of times and packet size')
parser.add_argument('directory', help='pcap filename')


def all_packets(oldfile, newfile, ip):
    output = open(newfile, 'w', buffering=1)
    output.write('time,size\n')
    
    for packet in rdpcap(oldfile):
        if not IP in packet:
            continue
        if packet[IP].src != ip and packet[IP].dst != ip:
            continue
        output.write(f'{packet.time},{len(packet)}\n')
    
    output.close()


def all_pcap_directory(config):
    root, dirs, _ = next(os.walk(config.directory))
    for exp_dir in dirs:
        _, _, files = next(os.walk(os.path.join(root, exp_dir)))
        for file in files:
            if file.endswith('.pcap'):
                oldfile = os.path.join(root, exp_dir, file)
                newfile = os.path.join(root, exp_dir, file.rpartition('.')[0] + '.csv')
                params_file = os.path.join(root, exp_dir, 'parameters.json')
                if not os.path.exists(params_file):
                    continue
                
                with open(params_file) as f:
                    ip = json.load(f)['ipaddress']
                all_packets(oldfile, newfile, ip)


if __name__ == '__main__':
    all_pcap_directory(parser.parse_args())

