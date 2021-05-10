from scapy.all import *
import math
import argparse
import pandas as pd

def collapse(time_list):
    result = []
    start_k = 0
    privious_k = 0
    privious_size = 0
    for k, v in time_list.items():
        if k == privious_k + 1 and v > 2000:
            privious_k = k
            privious_size += v
        else:
            if start_k == 0:
                start_k = k
                privious_k = k
            else:
                result.append((start_k, privious_k, privious_size))
                privious_size = v
                privious_k = k
                start_k = k

    return result



def main():
    parser = argparse.ArgumentParser(description="parse pcap file")


    #parsing arguments
    parser.add_argument("--ifname", "-if", required=True, help="input file name")
    parser.add_argument("--ip", "-ip", required=True, help="ip address of the device")
    parser.add_argument("--size", "-s", help="The size to determine if it is an activation or not")
    parser.add_argument("--time", "-t", help="The time to determine if it is an activation or not")
    parser.add_argument("--ofname", "-of", help="output file name")
    args = parser.parse_args()
    filename = args.ifname
    ip = args.ip
    threshold = 10000 if args.size == None else int(args.size)
    time_threshold = 3 if args.time == None else int(args.time)


    #read capture file
    packets = rdpcap(filename)
    result = {}
    
    df = pd.DataFrame(columns = ["start_time", "end_time", "packet_size"])
    df_sec = pd.DataFrame(columns = ["time", "packet_size"])
    
    for packet in packets:
        if not IP in packet:
            continue
        if packet[IP].src != ip and packet[IP].dst != ip:
            continue
        packet_time_sec = math.floor(packet.time)
        if packet_time_sec in result:
            result[packet_time_sec] = result[packet_time_sec] + len(packet)
        else:
            result[packet_time_sec] = len(packet)

    for k, v in result.items():
        if v > threshold:
            df_sec = df_sec.append({"time": k, "packet_size": v}, ignore_index=True)
            #print("{}: {}".format(k, v))
    
    collapsed_result = collapse(result)
    count = 0
    for (start, end, size) in collapsed_result:
        if size > threshold and (end - start) > time_threshold:
            count = count + 1
            #print("{} to {}, total size: {}".format(start, end, size))
            df = df.append({"start_time": start, "end_time": end,"packet_size": size}, ignore_index=True)

    print(df)
    print("Total activations: {}".format(count))
    if args.ofname != None:
        df.to_csv(args.ofname)
        df_sec.to_csv("sec_" + args.ofname)


if __name__ == "__main__":
    main()
