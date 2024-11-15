import os
import time
import json
import pcapng
import datetime
import progressbar
import numpy as np
import multiprocessing
from functions import *

from src.process.classes import Image
from src.process.compile_image import compile_image
from src.process.read_json_file import read_json_file

def generate_sequence(array_image_list):

    j=0

    telescope_list, quabo_address_list = read_json_file()
    
    for telescope in telescope_list:

        array_image_list.append([])
        
        for packet in packet_array:
            
            if packet.source_ip in telescope.quabo_addresses:
                telescope.data.append(packet)

        processed_packet_list = [[], [], [], []]

        for packet in telescope.data:
            
            if packet.length == 1140:
                
                if packet.source_ip == telescope.quabo_addresses[0]:
                    processed_packet_list[0].append(packet)
                
                elif packet.source_ip == telescope.quabo_addresses[1]:
                    processed_packet_list[1].append(packet)
                
                elif packet.source_ip == telescope.quabo_addresses[2]:
                    processed_packet_list[2].append(packet)
                
                elif packet.source_ip == telescope.quabo_addresses[3]:
                    processed_packet_list[3].append(packet)

        board_frame_count = [len(processed_packet_list[0]),
                            len(processed_packet_list[1]),
                            len(processed_packet_list[2]),
                            len(processed_packet_list[3])]
        
        i=0
    
        telescope_image_list = []

        for element in range(np.min(board_frame_count)):
            telescope_image_list.append(Image(compile_image(
                                                    processed_packet_list[0][i].data,
                                                    processed_packet_list[1][i].data,
                                                    processed_packet_list[2][i].data,
                                                    processed_packet_list[3][i].data),
                                                processed_packet_list[0][i].timestamp,
                                                i))
            i+=1


        j+=1

    print('\nComplete!\n')
    
    return array_image_list