from functions import *

def reader_function(path):
    import os
    import json
    import pcapng
    import datetime
    import progressbar
    import numpy as np
    from pcapng import FileScanner
    from pcapng.blocks import EnhancedPacket
    
    os.mkdir(str(path)+'/pynoseti')
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
                    def __init__(self, source_ip, timestamp, data, length, number):
                        self.source_ip = source_ip
                        self.timestamp = timestamp
                        self.data = data
                        self.length = length
                        self.number = number

                with open(file, 'rb') as file:
                    scanner = FileScanner(file)
                    for block in scanner:
                        if isinstance(block, pcapng.blocks.EnhancedPacket):
                            packet_list.append(block.packet_data.hex())
                            if hasattr(block, 'timestamp'):
                                timestamp_list.append(block.timestamp)

                i=0
                packet_array = []
                bar = progressbar.ProgressBar(max_value=len(packet_list))
                for packet in packet_list:
                    packet_array.append(Packet(get_image_source_ip(packet),
                                               timestamp_list[i],
                                               row_splitter(packet),
                                               len(packet),
                                               i))
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

                array_image_list = []
                array_data_sequence_list = []
                for telescope in telescope_list:

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
                        frame_sequence = []
                        for frame in telescope_image_list:
                            frame_sequence.append(frame.data)
                        median_frame = np.median(np.stack(np.array(frame_sequence)), axis=0)
                        
                        
                        data_sequence = Sequence(telescope_image_list, median_frame, str(telescope.dome), str(file_name))
                        array_data_sequence_list.append(data_sequence)
                        array_image_list = array_data_sequence_list

                    else:
                        
                        data_sequence = Sequence(telescope_image_list, None, str(telescope.dome), str(file_name))
                        array_data_sequence_list.append(data_sequence)
                        array_image_list = array_data_sequence_list
                
                save_directory = os.path.join(str(path)+'/pynoseti', 'pynoseti_'+file_name+str(file_count))
                np.save(save_directory, np.array(array_image_list, dtype=object))

                file.close()
                file_number += 1
                print('\nComplete!\n')

    with os.scandir(str(path)+'/pynoseti') as files:
        file_number = 1
        combined_file_data = []

        for file in files:
            if file.is_file():
                if '.npy' in file.name:
                    combined_file_data.append([])
        print(len(combined_file_data))

        
        #print(len(combined_file_data))
        continuous_data_sequence = []

        for file in files:
            if file.is_file():
                if '.npy' in file.name:
                    #for entry in telescope_list:
                    #    continuous_data_sequence.append([])

                    i=0
                    file_data = np.load(file, allow_pickle=True)
                    for telescope in file_data:
                        combined_file_data[i].append(telescope)
                        print('test')
                        i+=1

                    #for telescope in combined_file_data:
                    #    np.stack(np.array(combined_file_data))

                    #file.close()
                    file_number += 1

        np.save(str(save_directory)+str('test'), np.array(combined_file_data, dtype=object))