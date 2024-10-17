import os
import json
import pcapng
import datetime
import progressbar
import numpy as np
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket
from functions import *

path = "/home/brett/Data_for_pynoseti"
#os.mkdir(str(path)+'/pynoseti')
#print('Target directory created for selected files at '+str(path)+'/panoseti\n')

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

            print(f'Processing file {file_number} of {file_count}...')

            class Packet:
                def __init__(self, source_ip, timestamp, data, number):
                    self.source_ip = source_ip
                    self.timestamp = timestamp
                    self.data = data
                    self.number = number
            
            '''
            with open(file, 'rb') as file:
                scanner = FileScanner(file)
                for block in scanner:
                    if isinstance(block, pcapng.blocks.EnhancedPacket):
                        #print(len(block.packet_data.hex()))
                        # Checks, while iterating over each block, if it is of the EnchancedPacket data type. If so,
                        # its hexadecimal packet data is stored in 'packet_array'.

                        #if len(block.packet_data.hex()) > 75:

                        packet_list.append(block.packet_data.hex())
                        #print(len(block.packet_data.hex()))

                        if hasattr(block, 'timestamp'):
                            timestamp_list.append(block.timestamp)
            



            i=0
            packet_array = []
            bar = progressbar.ProgressBar(max_value=len(packet_list))
            for packet in packet_list:
                packet_array.append(Packet(get_image_source_ip(packet), timestamp_list[i], row_splitter(packet), i))
                i+=1
                bar.update(i)

            '''

            packet_array = np.load(str(path)+'/pynoseti/pynoseti_Dual_onskyph12.5pe_ima2pe__20230426_041448.pcapng.npy', allow_pickle=True)

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

            count_list = []
            for i in range(12):
                count_list.append(0)


            for packet in packet_array:
                i=0
                for address in quabo_address_list:
                    if packet.source_ip == address:
                        count_list[i]+=1
                    else:
                        i+=1

            #print(count_list)
            
            
            array_image_list = []

            telescope = telescope_list[0]

           
            i=0
            j=0
            k=0
            l=0
                

            for packet in packet_array:
                if packet.source_ip in telescope.quabo_addresses:
                    telescope.data.append(packet)
                    #print(packet.number, packet.source_ip)


            #while i < 1000:
            #    print(packet_array[i].number, packet_array[i].source_ip)
            #    i+=1
            #i=0

            processed_packet_list = [[], [], [], []]
            for packet in telescope.data:
                if packet.source_ip == telescope.quabo_addresses[0]:
                    processed_packet_list[0].append(packet)
                    #print(packet.source_ip)
                    i+=1
                elif packet.source_ip == telescope.quabo_addresses[1]:
                    processed_packet_list[1].append(packet)
                    #print(packet.source_ip)
                    j+=1
                elif packet.source_ip == telescope.quabo_addresses[2]:
                    processed_packet_list[2].append(packet)
                    #print(packet.source_ip)
                    k+=1
                elif packet.source_ip == telescope.quabo_addresses[3]:
                    processed_packet_list[3].append(packet)
                    #print(packet.source_ip)
                    l+=1

            #print(len(telescope.data))

            #print(i, j, k ,l)


            board_frame_count = [len(processed_packet_list[0]), len(processed_packet_list[1]), len(processed_packet_list[2]), len(processed_packet_list[3])]
            #print(board_frame_count)
            # Measures the length of the processed packet lists for each quabo so 
            # that it can be divided in half and a median be retrieved from the set.

            i=0
            telescope_image_list = []
            #image_median = np.median(quabo_image_compiler(processed_packet_list[0][int(np.min(board_frame_count)/2)].data,
            #                                            processed_packet_list[1][int(np.min(board_frame_count)/2)].data,
            #                                            processed_packet_list[2][int(np.min(board_frame_count)/2)].data,
            #                                            processed_packet_list[3][int(np.min(board_frame_count)/2)].data))

            image_median = np.median(quabo_image_compiler(processed_packet_list[0][0].data,
                                                    processed_packet_list[1][0].data,
                                                    processed_packet_list[2][0].data,
                                                    processed_packet_list[3][0].data))


            for element in range(np.min(board_frame_count)):
                #print(processed_packet_list[0][i].source_ip, processed_packet_list[1][i].source_ip, processed_packet_list[2][i].source_ip, processed_packet_list[3][i].source_ip,)

                #print(len(processed_packet_list[0][i].data), len(processed_packet_list[1][i].data), len(processed_packet_list[2][i].data), len(processed_packet_list[3][i].data))
                
                #if [len(processed_packet_list[0][i].data), len(processed_packet_list[1][i].data), len(processed_packet_list[2][i].data), len(processed_packet_list[3][i].data)] == [16, 16, 16, 16]:
                #print(i)
                #print(telescope.dome)
                print(len(packet_array[i].data), packet_array[i].source_ip)
                #telescope_image_list.append(Image(quabo_image_compiler(processed_packet_list[0][i].data,
                #                                        processed_packet_list[1][i].data,
                #                                        processed_packet_list[2][i].data,
                #                                        processed_packet_list[3][i].data)/image_median,
                #                        processed_packet_list[0][i].timestamp,
                #                        telescope.dome))

                

                i+=1

                if i == 150:
                    break

            #normalized_list = []
            #median_frame = telescope_image_list[int(len(telescope_image_list)/2)].data
            #for frame in telescope_image_list:
            #    normalized_list.append(Image(frame.data-median_frame,))
            



            for frame in telescope_image_list:
                plt.imshow(telescope_image_list[0].data)
                plt.show()


            #save_directory = os.path.join(str(path)+'/pynoseti', 'pynoseti_'+file_name)
            #np.save(save_directory, np.array(packet_array))

            exit()
            #array_image_list.append(telescope_image_list)
            array_image_list.append(telescope_image_list)

            save_directory = os.path.join(str(path)+'/pynoseti', 'pynoseti_'+file_name)

            #np.save(save_directory, np.array(array_image_list))
            np.save(save_directory, packet_array)

            file.close()
            file_number += 1
            print('\nComplete!\n')