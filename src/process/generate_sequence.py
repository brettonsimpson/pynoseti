import os
import time
import json
import pcapng
import datetime
import progressbar
import numpy as np
import multiprocessing

from src.process.classes import Image, Sequence
from src.process.compile_image import compile_image
from src.extract.extract_median_frame import extract_median_frame

def generate_sequence(packet_array, file_name, telescope_list):

    j=0

    array_image_list = []
    
    for telescope in telescope_list:

        telescope_image_list = []
        
        for packet in packet_array:
            
            if packet.source_ip in telescope.quabo_addresses:
                telescope.data.append(packet)

        processed_packet_list = [[], [], [], []]

        for packet in telescope.data:
            
            if packet.length == 570:
        
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
    
        for element in range(np.min(board_frame_count)):
            telescope_image_list.append(Image(compile_image(
                                                    processed_packet_list[0][i].data,
                                                    processed_packet_list[1][i].data,
                                                    processed_packet_list[2][i].data,
                                                    processed_packet_list[3][i].data),
                                                processed_packet_list[0][i].timestamp,
                                                i))
            i+=1

        if 'Ima_onsky' in file_name:

            median_subtracted_telescope_image_list = []
            median_frame = extract_median_frame(telescope_image_list)

            for frame in telescope_image_list:
            
                median_subtracted_telescope_image_list.append(Image(frame.data-median_frame,frame.timestamp,frame.number))

            sequence = Sequence(median_subtracted_telescope_image_list, median_frame, telescope.dome, file_name)

        else:
            median_frame = None
            sequence = Sequence(telescope_image_list, median_frame, telescope.dome, file_name)

        array_image_list.append(sequence)

        j+=1
    
    return array_image_list