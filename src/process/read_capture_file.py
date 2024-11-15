import os
import time
import json
import pcapng
import datetime
import progressbar
import numpy as np
import multiprocessing
from functions import *
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket

def read_capture_file(file):
    telescope_list, quabo_address_list = read_json_file(file)

    packet_list = []
    
    timestamp_list = []
    
    array_image_list = []
    
    file_name = os.path.basename(file.name)
    
    with open(file, 'rb') as file:
        scanner = FileScanner(file)
        
        for block in scanner:
            
            if isinstance(block, pcapng.blocks.EnhancedPacket):
                packet_list.append(block.packet_data.hex())
                
                if hasattr(block, 'timestamp'):
                    timestamp_list.append(block.timestamp)
    
    i=0
    
    packet_array = []
    
    for packet in packet_list:
        packet_array.append(Packet(get_image_source_ip(packet),
                                timestamp_list[i],
                                row_splitter(packet),
                                len(packet),
                                i))
        i+=1

    return(packet_array)