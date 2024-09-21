import os
#import time
import json
import datetime
import progressbar
import numpy as np
from functions import *
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket

#path = input('Please specify the location of your Wireshark capture file: ')

# Declares the list that will hold the hexadecimal data for each packet.

###########################################################
#path = "//wsl.localhost/Ubuntu-20.04/home/brett/Data_for_pynoseti/Pause_onskyph0pe_ima0pe__20230426_041905.pcapng"
path = "/home/brett/Data_for_pynoseti/Pause_onskyph0pe_ima0pe__20230426_040905.pcapng"
# Specifies the path to the file to be used in processing.
# Don't forget to change when using a new file.
###########################################################

path = "/home/brett/Data_for_pynoseti"
os.mkdir(str(path)+'/pynoseti')
print('\nTarget directory created for selected files at '+str(path)+'/panoseti\n')

with os.scandir(path) as files:

    file_count = 0
    for file in files:
        if file.is_file():
            file_count += 1
    
with os.scandir(path) as files:

    file_number = 1
    for file in files:
        if file.is_file():

            file_name = os.path.basename(file.name)

            packet_list = []
            # Declares the list that will hold the hexadecimal data for each packet.

            timestamp_list = []
            # Declares the list that will be used to record the timestamps for each packet.

            print(f'Reading file {file_number} of {file_count}...')

            class Packet:
                def __init__(self, source_ip, timestamp, data):
                    self.source_ip = source_ip
                    self.timestamp = timestamp
                    self.data = data

            with open(file, 'rb') as file:
                scanner = FileScanner(file)
                for block in scanner:
                    if isinstance(block, pcapng.blocks.EnhancedPacket):
                        # Checks, while iterating over each block, if it is of the EnchancedPacket data type. If so,
                        # its hexadecimal packet data is stored in 'packet_array'.

                        packet_list.append(block.packet_data.hex())

                        if hasattr(block, 'timestamp'):
                            timestamp_list.append(block.timestamp)

            i=0
            packet_array = []
            bar = progressbar.ProgressBar(max_value=len(packet_list))
            for packet in packet_list:
                packet_array.append(Packet(get_image_source_ip(packet), timestamp_list[i], row_splitter(packet)))
                i+=1
                bar.update(i)

            packet_array = np.array(packet_array)

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

            #i=0
            #print("\nConverting hexidecimal data to photon intensity...\n")
            #print('Recognized telescopes:', '\n')
            #for telescope in telescope_list:
            #    print(str(i+1)+': '+telescope.name)
            #    i+=1
            
            #telescope_choice = input('\nWhich telescope would you like to playback data for?\n'
                                    #'Skip this prompt by pressing enter and process the entire file.\n'
                                    #'Enter the integer corresponding to one of the telescopes: ')

            #if telescope_choice != '':

            #telescope_choice = int(telescope_choice)-1

            array_image_list = []

            for telescope in telescope_list:

                for packet in packet_array:
                    if packet.source_ip in telescope.quabo_addresses:
                        telescope.data.append(packet)

                processed_packet_list = [[], [], [], []]
                for packet in telescope.data:
                    if packet.source_ip == telescope.quabo_addresses[0]:
                        processed_packet_list[0].append(packet)

                    elif packet.source_ip == telescope.quabo_addresses[1]:
                        processed_packet_list[1].append(packet)

                    elif packet.source_ip == telescope.quabo_addresses[2]:
                        processed_packet_list[2].append(packet)

                    elif packet.source_ip == telescope.quabo_addresses[3]:
                        processed_packet_list[3].append(packet)


                board_frame_count = [len(processed_packet_list[0]), len(processed_packet_list[1]), len(processed_packet_list[2]), len(processed_packet_list[3])]
                # Measures the length of the processed packet lists for each quabo so 
                # that it can be divided in half and a median be retrieved from the set.

                i=0
                telescope_image_list = []
                #image_median = np.median(quabo_image_compiler(processed_packet_list[0][int(np.min(board_frame_count)/2)].data,
                #                                            processed_packet_list[1][int(np.min(board_frame_count)/2)].data,
                #                                            processed_packet_list[2][int(np.min(board_frame_count)/2)].data,
                #                                            processed_packet_list[3][int(np.min(board_frame_count)/2)].data))
                
                for element in range(np.min(board_frame_count)):
                    telescope_image_list.append(Image(quabo_image_compiler(processed_packet_list[0][i].data,
                                                            processed_packet_list[1][i].data,
                                                            processed_packet_list[2][i].data,
                                                            processed_packet_list[3][i].data),#-image_median,
                                            processed_packet_list[0][i].timestamp,
                                            telescope.dome))
                    i+=1

                array_image_list.append(telescope_image_list)

            save_directory = os.path.join(str(path)+'/pynoseti', 'pynoseti_'+file_name)

            np.save(save_directory, np.array(array_image_list))

            file.close()
            file_number += 1
            print('\nComplete!')