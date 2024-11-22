import os
import time
import json
import pcapng
import datetime
import progressbar
import numpy as np
import multiprocessing
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket

from src.process.classes import Packet
from src.extract.extract_packet_data import *
from src.process.parallel_processing import parallel_processing

def read_capture_file(file):

    packet_array = []

    unprocessed_packet_list = []

    packet_hex_data_list = []

    timestamp_list = []
    
    file_name = os.path.basename(file.name)
    
    with open(file, 'rb') as file:
        scanner = FileScanner(file)
        
        for block in scanner:
            
            if isinstance(block, pcapng.blocks.EnhancedPacket):
                
                if hasattr(block, 'timestamp'):
                    data = block.packet_data.hex()
                    packet_hex_data_list.append(data)
                    timestamp_list.append(block.timestamp)

    packet_data_array = parallel_processing(packet_hex_data_list, assemble_packet_data, 16, None, None)

    i=0
    for packet in packet_data_array:
        setattr(packet, 'timestamp', timestamp_list[i])
        i+=1
    
    return packet_data_array, file_name