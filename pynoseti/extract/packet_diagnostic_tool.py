from scapy.all import rdpcap

from pynoseti.extract.extract_packet_data import *

def packet_diagnostic_tool(file_path):
    
    packet_number = int(input("\nEnter the packet number: "))
    packet = rdpcap(file_path)
    print(packet)
    print(packet[packet_number].show())
    print(packet[packet_number].summary())
    print(packet[packet_number].src)
    print(packet[packet_number].dst)
    print(packet[packet_number].len)
    print(packet[packet_number].proto)
    print(packet[packet_number].type)
    print(packet[packet_number].version)
    print(packet[packet_number].ihl)
    print(packet[packet_number].tos)
    print(packet[packet_number].len)
    print(packet[packet_number].id)
    print(packet[packet_number].flags)
    print(packet[packet_number].frag)
    print(packet[packet_number].ttl)
    print(packet[packet_number].chksum)
    print(packet[packet_number].options)
    print(packet[packet_number].payload)
    print('\nTime Received:')
    print(convert_unix_time(float(packet[packet_number].time/10e2)))