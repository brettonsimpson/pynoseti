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

def packet_reader(file):
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
    packet_array = np.array(packet_array)

    j=0
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
            telescope_image_list.append(Image(quabo_image_compiler(
                                                    processed_packet_list[0][i].data,
                                                    processed_packet_list[1][i].data,
                                                    processed_packet_list[2][i].data,
                                                    processed_packet_list[3][i].data),
                                                processed_packet_list[0][i].timestamp,
                                                i))
            i+=1

        if 'Ima_onsky' in file_name:
            median_sequence = []
            for frame in telescope_image_list:
                median_sequence.append(frame.data)
            median_frame = np.median(np.stack(np.array(median_sequence)), axis=0)
            median_subtracted_telescope_image_list = []
            for frame in telescope_image_list:
                median_subtracted_telescope_image_list.append(Image(frame.data-median_frame,frame.timestamp,frame.number))
            
            array_image_list[j].append(Sequence(median_subtracted_telescope_image_list, median_frame, telescope.dome, file_name))

        else:
            array_image_list[j].append(Sequence(telescope_image_list, None, telescope.dome, file_name))

        j+=1

    file.close()
    file_number += 1
    print('\nComplete!\n')
    return array_image_list

def data_cube_assembler(path):
    telescope_list, quabo_address_list = read_json_file(file)

    for element
    
    processes = int(os.cpu_count()/2)
    
    os.mkdir(str(path)+'/pynoseti')
    with os.scandir(path) as files:
        file_count = 0
        for file in files:
            if file.is_file():
                file_count += 1

    array_data_sequence_list = []
    with os.scandir(path) as files:
        file_number = 1
        for file in files:
            if file.is_file():

        



                array_data_sequence_list = np.array(array_data_sequence_list)

                i=0
                final_sequence_array = []
                semifinal_telescope_data_array = []
                for telescope in range(len(telescope_list)):
                    semifinal_telescope_data_array.append([])
                    final_sequence_array.append([])
                    for file in array_data_sequence_list:
                        semifinal_telescope_data_array[i].append(file[i])
                    i+=1

                i=0
                for telescope in semifinal_telescope_data_array:
                    j=0
                    for file in telescope:
                        final_sequence_array[i].append(file[j])
                    i+=1

                i=0
                final_telescope_data_array = []
                for telescope in range(len(telescope_list)):
                    temp_complete_sequence = []
                    frame_number = 0
                    temp_median_list = []

                    for file in final_sequence_array[i]:

                        frame_selection = [frame_number]
                        for frame in file.sequence:
                            temp_complete_sequence.append(frame)
                            frame_number+=1

                        temp_complete_sequence = sorted(temp_complete_sequence, key=lambda obj: obj.timestamp)
                        frame_selection.append(frame_number)
                        temp_median_list.append(Median(file.median_data, frame_selection))
                        temp_telescope_identifier = file.telescope
                        temp_file_name = file.file_name
                        
                    final_telescope_data_array.append(Sequence(temp_complete_sequence,
                                                            temp_median_list,
                                                            temp_telescope_identifier,
                                                            temp_file_name))
                    
                    i+=1

        save_directory = os.path.join(str(path)+'/pynoseti', 'pynoseti_full_sequence_data_FINAL_DATA_Ima_onsky')
        np.save(save_directory, np.array(final_telescope_data_array, dtype='object'))

    #return(np.array(final_telescope_data_array))