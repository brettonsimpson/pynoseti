import os
import json
import pcapng
import pyshark
import datetime
import progressbar
import numpy as np
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket

with open('config.json', 'r') as file:
    config = json.load(file)
telescope_list = []
quabo_address_list = []
for setting in config['telescopes']:
    telescope = Telescope(name = setting['identifier'],
                        dome = setting['dome'], 
                        quabo_addresses = setting['quabo_addresses'],
                        data = []
                        )
    telescope_list.append(telescope)
    for address in telescope.quabo_addresses:
        if address not in quabo_address_list:
            quabo_address_list.append(address)

file_path = '/home/brett/Data_for_pynoseti/ph/Dual_onskyph12.5pe_ima2pe__20230428_042445.pcapng'
capture_file = pyshark.FileCapture(file_path, use_json=True, include_raw=True)

packet_number = int(input('\nEnter the integer corresponding to the packet you would like to open: '))

with open(file_path, 'rb') as file:
    scanner = FileScanner(file)
    i=0
    for block in scanner:
        if isinstance(block, pcapng.blocks.EnhancedPacket):
            if i == packet_number-1:
                packet_choice = block.packet_data.hex()
            else:
                i+=1

if 'IP' in capture_file[packet_number-1] and 'UDP' in capture_file[packet_number-1]:
    print(f'\nPacket Number: {packet_number}')
    print('\nIP Layer:')
    print(f'Source IP: {capture_file[packet_number-1].ip.src}')
    print(f'Destination IP: {capture_file[packet_number-1].ip.dst}')

    print('\nUDP Layer:')
    print(f'Source Port: {capture_file[packet_number-1].udp.srcport}')
    print(f'Destination Port: {capture_file[packet_number-1].udp.dstport}\n')

    print(f'Packet Length: {capture_file[packet_number-1].udp.length}')
    print(f'Packet Arrival Time: {capture_file[packet_number-1].sniff_time} PDT')

    print('\nRaw Hexadecimal Data:')
    print(capture_file[packet_number-1].get_raw_packet().hex(),'\n')

else:
    print('\nThis packet does not contain an IP and UDP layer and likely does not contain science data.\n')